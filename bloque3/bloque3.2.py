import json
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

STORE_DIR = "rag_store"

# Cargar chunks y metadatos
with open(f"{STORE_DIR}/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]
metas = [c["meta"] for c in chunks]

# Embeddings
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index(f"{STORE_DIR}/index.faiss")

# Modelo generativo
base_model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2-9b-it",
    device_map="auto",
    torch_dtype=torch.float16
)
model = PeftModel.from_pretrained(base_model, "./lora_model")
tokenizer = AutoTokenizer.from_pretrained("./lora_model")

system_prompt = """
Eres un asistente académico riguroso especializado en normativa laboral.
Solo puedes responder utilizando el CONTEXTO proporcionado.
Si el contexto no contiene la información necesaria, debes decir explícitamente que no lo sabes.
No debes inferir, completar ni inventar información.
"""

def retrieve_context(query, k=3):
    q_emb = embedder.encode([query])
    _, idxs = index.search(q_emb, k)
    results = []
    for i in idxs[0]:
        results.append(chunks[i])
    return results

def ask_rag(question):
    retrieved = retrieve_context(question)

    if not retrieved:
        return "No se ha recuperado ningún contexto relevante."

    context_text = "\n\n".join(
        f"[Fuente: {r['meta']['source']} | Página {r['meta']['page']}]\n{r['text']}"
        for r in retrieved
    )

    prompt = f"""
<SYSTEM>
{system_prompt}
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

# Preguntas de prueba
questions = [
    "¿Cuál es la duración máxima del contrato según el convenio del metal?",
    "¿Qué dice el BOE sobre teletrabajo en estos convenios?",
    "Resume el artículo 15 del convenio de hostelería."
]


results = ""
for q in questions:
    text = f"QUESTION:\n{q}\nANSWER:\n{ask_rag(q)}\n{'-'*15}\n\n"
    print(text)
    results += text
with open("results/results_b3.txt","w") as file:
    file.write(results)
