import json
import faiss
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import re

# =============================
# CONFIG
# =============================

STORE_DIR = "rag_store"
DESC_FILE = "bloque4/description.json"
TOP_K = 3

# =============================
# LOAD DATA
# =============================

with open(f"{STORE_DIR}/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

with open(DESC_FILE, "r", encoding="utf-8") as f:
    convenio_descriptions = json.load(f)

texts = [c["text"] for c in chunks]
metas = [c["meta"] for c in chunks]

index = faiss.read_index(f"{STORE_DIR}/index.faiss")
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# =============================
# LOAD MODEL
# =============================

base_model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2-9b-it",
    device_map="auto",
    torch_dtype=torch.float16
)
model = PeftModel.from_pretrained(base_model, "./lora_model")
tokenizer = AutoTokenizer.from_pretrained("./lora_model")

# =============================
# TOOL 1 · ROUTER
# =============================

system_prompt_router = """
Eres un clasificador experto en convenios colectivos.

Tu única tarea es decidir qué convenio es relevante para una pregunta.

Reglas estrictas:
- Solo puedes elegir uno de los PDFs listados.
- Si la pregunta no se puede asociar claramente a un convenio, responde NONE.
- No inventes nombres de convenios.
- No mezcles sectores.
- No respondas a la pregunta.
"""

router_context = "\nConvenios disponibles:\n"
for k, v in convenio_descriptions.items():
    router_context += f"- {k}: {v}\n"

def select_convenio(question):
    prompt = f"""
<SYSTEM>
{system_prompt_router}
{router_context}
</SYSTEM>

<USER>
Pregunta: {question}

Responde únicamente con el nombre exacto del PDF o NONE.
</USER>

<ASSISTANT>
"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=30,
        do_sample=False
    )

    raw_answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Regex para extraer un PDF válido o NONE
    match = re.search(r'<ASSISTANT>\s*([a-zA-Z0-9_]+\.pdf|NONE)\s*</ASSISTANT>', raw_answer)

    if match:
        decision = match.group(1).strip()
        print("FUNCION SELECCIONADA:",decision)
    else:
        print(f"Ha fallado el regex {'-'*30}\n{raw_answer}\n{'-'*30}")
        decision = "INVALID"

    if decision == "INVALID":
        raise ValueError(f"PDF no permitido: {raw_answer}")

    return None if decision == "NONE" else decision

# =============================
# RAG RESTRICTED BY PDF
# =============================

def retrieve_context(question, pdf_name, k=TOP_K):
    q_emb = embedder.encode([question])
    _, idxs = index.search(q_emb, 20)  # búsqueda amplia

    filtered = []
    for i in idxs[0]:
        if chunks[i]["meta"]["source"] == pdf_name:
            filtered.append(chunks[i])
        if len(filtered) == k:
            break

    return filtered

# =============================
# FINAL ANSWER
# =============================

system_prompt_answer = """
Eres un asistente académico riguroso especializado en convenios colectivos.

Reglas obligatorias:
- Solo puedes usar la información del CONTEXTO.
- Si el contexto no contiene la respuesta, di explícitamente que no lo sabes.
- No completes ni infieras información.
- No mezcles convenios.
"""

def answer_question(question):
    pdf = select_convenio(question)

    if pdf is None:
        return "No puedo determinar el convenio aplicable con la información disponible."

    retrieved = retrieve_context(question, pdf)

    if not retrieved:
        return f"No se ha encontrado información relevante en el convenio {pdf}."

    context_text = "\n\n".join(
        f"[Fuente: {r['meta']['source']} | Página {r['meta']['page']}]\n{r['text']}"
        for r in retrieved
    )

    prompt = f"""
<SYSTEM>
{system_prompt_answer}
</SYSTEM>

<CONTEXT>
{context_text}
</CONTEXT>

<USER>
{question}
</USER>

<ASSISTANT>
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.2,
        do_sample=False
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# =============================
# TEST
# =============================

questions = [
    "¿Cuál es la jornada laboral anual en el convenio del metal?",
    "¿Qué dice el convenio de hostelería sobre turnos partidos?",
    "¿Existe regulación de teletrabajo en estos convenios?",
    "¿Cuál es el salario base en el sector aeroespacial?"
]

results = ""
for q in questions:
    text = f"QUESTION:\n{q}\nANSWER:\n{answer_question(q)}\n{'-'*15}\n\n"
    print(text)
    results += text
with open("results_b4.txt","w") as file:
    file.write(results)
