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
model_name = "google/gemma-3-12b-it"

judge_tokenizer = AutoTokenizer.from_pretrained(model_name)
judge_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto"
)

# =============================
# JUDGE PROMPT
# =============================
JUDGE_SYSTEM = """
Eres un evaluador técnico de sistemas NLP.

Evalúa la respuesta del sistema teniendo en cuenta:
1. Corrección factual respecto al contexto
2. Uso adecuado y coherente de las fuentes
3. Presencia de invención o extrapolación no justificada
4. Acción tomada por el sistema:
   - ANSWERED: proporciona una respuesta sustantiva
   - ABSTAINED: decide no responder por falta de información suficiente

Devuelve exclusivamente un JSON con:
- factual_correct: entero de 0 a 10
- source_consistent: entero de 0 a 10
- hallucination: entero de 0 a 10
- system_action: "ANSWERED" o "ABSTAINED"
- justification: breve explicación técnica de la evaluación

Es de vital importancia que el formato del json sea correcto, con llave de apertura y cerrado, strings entre comillas, etc.

Ej.:
```json
{
 "factual_correct": 7,
 "source_consistent": 8,
 "hallucination": 2,
 "system_action": "ANSWERED",
 "justification": "He elegido poner un 7 en factual_correct porque..."
}
```
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
    with torch.no_grad():
        inputs = judge_tokenizer(prompt, return_tensors="pt").to(judge_model.device)
        outputs = judge_model.generate(**inputs, max_new_tokens=300, do_sample=False)
    raw = judge_tokenizer.decode(outputs[0], skip_special_tokens=True)
    del inputs
    del outputs
    torch.cuda.empty_cache()

    json_default = {
      "factual_correct": 7,
      "source_consistent": 8,
      "hallucination": 2,
      "system_action": "ANSWERED",
      "justification": "He elegido poner un 7 en factual_correct porque..."
    }

    
    default_answer = "No se ha podido evaluar"
    try:
        json_text = extract_last_json(raw)
        json_formated = json.loads(json_text)
        if json_formated==json_default:
            json_formated = default_answer
            print(raw)
        return json_formated
    except:
        print(raw)
        return default_answer

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

    judge_eval = judge_answer(question, answer, context)

    results.append({
        "question": question,
        "answer": answer,
        "judge_eval": judge_eval,
        "timestamp": datetime.now().isoformat()
    })

    del judge_eval
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()

# =============================
# SAVE RESULTS
# =============================
with open(RESULTS_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Evaluación completada.")