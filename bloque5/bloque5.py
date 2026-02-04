import json
import faiss
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import re
from datetime import datetime

# =============================
# CONFIG
# =============================
STORE_DIR = "rag_store"
DESC_FILE = "bloque4/description.json"
TOP_K = 3
LOG_FILE = "results/agent_log_b5.txt"

# =============================
# LOAD DATA
# =============================
with open(f"{STORE_DIR}/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

with open(DESC_FILE, "r", encoding="utf-8") as f:
    convenio_descriptions = json.load(f)

index = faiss.read_index(f"{STORE_DIR}/index.faiss")
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Modelo generativo
base_model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2-9b-it",
    device_map="auto",
    dtype=torch.float16
)
model = PeftModel.from_pretrained(base_model, "./lora_model")
tokenizer = AutoTokenizer.from_pretrained("./lora_model")

# =============================
# TOOL 1 · SELECT CONVENIOS (multi)
# =============================
system_prompt_router = """
Eres un clasificador experto en convenios colectivos.
Tu tarea: decidir qué convenios son relevantes para una pregunta.
Puedes devolver uno o varios PDFs separados por comas.
Si no hay ningún PDF aplicable, responde NONE.
"""

router_context = "\nConvenios disponibles:\n"
for k, v in convenio_descriptions.items():
    router_context += f"- {k}: {v}\n"

def select_convenios(question):
    prompt = f"""
<SYSTEM>
{system_prompt_router}
{router_context}
</SYSTEM>

<USER>
Pregunta: {question}

Responde únicamente con los nombres exactos de los PDFs separados por coma o NONE.
</USER>

<ASSISTANT>
"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=50, do_sample=False)
    raw_answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Regex original adaptado para multi-PDFs
    match = re.search(r'<ASSISTANT>\s*([a-zA-Z0-9_.,\s]+|NONE)\s*</ASSISTANT>', raw_answer)
    if match:
        raw_list = match.group(1).strip()
        if raw_list == "NONE":
            return []
        pdfs = [x.strip() for x in raw_list.split(",") if x.strip() in convenio_descriptions]
        return pdfs
    else:
        print(f"Regex fallido, salida cruda:\n{raw_answer}")
        return []

# =============================
# TOOL 2 · RETRIEVE CONTEXT MULTI-PDF
# =============================
def retrieve_context(question, pdf_list, k=3):
    all_chunks = []
    q_emb = embedder.encode([question])
    # buscamos en todo el índice, pero separamos por PDF
    _, idxs = index.search(q_emb, 50)  # buscamos más para tener margen
    for pdf in pdf_list:
        count = 0
        for i in idxs[0]:
            if chunks[i]["meta"]["source"] == pdf:
                all_chunks.append(chunks[i])
                count += 1
                if count == k:  # máximo k por cada PDF
                    break
    return all_chunks


# =============================
# TOOL 3 · CHECK CONTEXT SUFFICIENCY
# =============================
def check_context_sufficiency(chunks, threshold=50):
    total_length = sum(len(c["text"]) for c in chunks)
    return total_length >= threshold

# =============================
# TOOL 4 · SUMMARIZE CONTEXT
# =============================
def summarize_context(chunks):
    return "\n\n".join(f"[Fuente: {c['meta']['source']} | Página {c['meta']['page']}]\n{c['text']}" for c in chunks)

# =============================
# TOOL 5 · VALIDATE ANSWER
# =============================
def validate_answer(answer):
    prohibited_phrases = ["inventado", "no existe información", "no se sabe"]
    for p in prohibited_phrases:
        if p in answer.lower():
            return False
    return True

# =============================
# AGENT MULTI-CONVENIO
# =============================
class MultiAgent:
    def __init__(self):
        self.memory = []
        self.logs = []

    def log(self, action, detail):
        entry = f"{datetime.now().isoformat()} | {action} | {detail}"
        self.logs.append(entry)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")

    def act(self, question):
        self.log("QUESTION", question)
        pdfs = select_convenios(question)
        self.log("SELECT_CONVENIOS", pdfs)

        if not pdfs:
            # Fallback: usar todos los convenios disponibles
            pdfs = list(convenio_descriptions.keys())
            agent.log("FALLBACK_SELECT_CONVENIOS", pdfs)

        context_chunks = retrieve_context(question, pdfs)
        if not check_context_sufficiency(context_chunks):
            self.log("ABSTENERSE", f"Contexto insuficiente en {pdfs}")
            return f"No hay suficiente información en los convenios seleccionados."

        context_text = summarize_context(context_chunks)
        system_prompt_answer = """
Eres un asistente académico riguroso especializado en convenios colectivos.
Debes integrar información de todos los convenios relevantes.
Solo puedes usar el CONTEXTO recuperado.
Si no hay suficiente información, abstente de responder.
"""

        prompt = f"<SYSTEM>{system_prompt_answer}</SYSTEM>\n<CONTEXT>{context_text}</CONTEXT>\n<USER>{question}</USER>\n<ASSISTANT>"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=400, temperature=0.2, do_sample=False)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if not validate_answer(answer):
            self.log("ABSTENERSE", "Respuesta no válida")
            answer = "No puedo dar una respuesta fiable con la información disponible."

        self.memory.append({"question": question, "answer": answer, "pdfs": pdfs})
        self.log("ANSWER", answer)
        return answer

# =============================
# TEST
# =============================
agent = MultiAgent()
questions = [
    "¿Existe regulación de teletrabajo en estos convenios?",
    "Que diferencia hay en los salarios base entre medicina y hosteleria",
    "¿Cuál es la jornada laboral anual en el convenio del metal?",
    "¿Qué dice el convenio de hostelería sobre turnos partidos?",
    "¿Cuál es el salario base en el sector aeroespacial?"
]

results = ""
for q in questions:
    answer = agent.act(q)
    text = f"QUESTION:\n{q}\nANSWER:\n{answer}\n{'-'*15}\n\n"
    results += text

with open("results/results_b5.txt", "w") as f:
    f.write(results)