# bloque6.py
import json
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from peft import PeftModel
from bloque5.bloque5 import MultiAgent
import re

# =============================
# CONFIG
# =============================
EVAL_FILE = "bloque6/eval_dataset_b6.json"
RESULTS_FILE = "results/eval_results_b6.json"

# =============================
# LOAD EVAL DATASET
# =============================
with open(EVAL_FILE, "r", encoding="utf-8") as f:
    eval_data = json.load(f)

# =============================
# LOAD JUDGE MODEL
# =============================
judge_base = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2-9b-it",
    device_map="auto",
    dtype=torch.float16
)
judge_model = PeftModel.from_pretrained(judge_base, "./lora_model")
judge_tokenizer = AutoTokenizer.from_pretrained("./lora_model")

# =============================
# JUDGE PROMPT
# =============================
JUDGE_SYSTEM = """
Eres un evaluador técnico de sistemas NLP.

Evalúa la respuesta según estos criterios:
1. Corrección factual respecto al contexto
2. Uso adecuado de fuentes
3. Ausencia de invención

Devuelve un JSON con:
- factual_correct 0-10
- source_consistent 0-10
- hallucination 0-10

Ej.:
```json
{
 "factual_correct": 7,
 "source_consistent": 8,
 "hallucination": 2
}
```

ES DE VITAL IMPORTANCIA QUE RESPONDAS SOLO CON EL JSON. Prohibido texto fuera del bloque JSON.
"""
def extract_last_json(text):
    matches = re.findall(r'```json\s*(.*?)\s*```', text, flags=re.DOTALL)
    if matches:
        return matches[-1]
    return None

def judge_answer(question, answer, context):
    prompt = f"""
<SYSTEM>
{JUDGE_SYSTEM}
</SYSTEM>

<PREGUNTA>
{question}
</PREGUNTA>

<CONTEXTO>
{context}
</CONTEXTO>

<RESPUESTA>
{answer}
</RESPUESTA>

<ASSISTANT>
"""
    inputs = judge_tokenizer(prompt, return_tensors="pt").to(judge_model.device)
    outputs = judge_model.generate(**inputs, max_new_tokens=200, do_sample=False)
    raw = judge_tokenizer.decode(outputs[0], skip_special_tokens=True)

    try:
        json_text = extract_last_json(raw)
        print(json_text)
        return json.loads(json_text)
    except:
        print(raw)
        return {
            "factual_correct": False,
            "source_consistent": False,
            "hallucination": True
        }

# =============================
# RUN EVALUATION
# =============================
agent = MultiAgent()
results = []

for sample in eval_data:
    question = sample["question"]
    should_answer = sample["should_answer"]

    answer = agent.act(question)
    context = str(agent.memory[-1])

    auto_abstained = "no puedo" in answer.lower()

    auto_eval = {
        "correct_abstention": (not should_answer and auto_abstained),
        "incorrect_abstention": (should_answer and auto_abstained)
    }

    judge_eval = judge_answer(question, answer, context)

    results.append({
        "question": question,
        "answer": answer,
        "auto_eval": auto_eval,
        "judge_eval": judge_eval,
        "timestamp": datetime.now().isoformat()
    })

# =============================
# SAVE RESULTS
# =============================
with open(RESULTS_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Evaluación completada.")