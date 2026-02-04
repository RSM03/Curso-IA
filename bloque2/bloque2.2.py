from transformers import AutoTokenizer, AutoModelForCausalLM

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

model = AutoModelForCausalLM.from_pretrained("google/gemma-2-9b-it", device_map="auto")
model = PeftModel.from_pretrained(model, "./lora_model")  # Cargar pesos LoRA
tokenizer = AutoTokenizer.from_pretrained("./lora_model")

system_prompt = """
Eres un asistente académico riguroso.
Si no conoces la respuesta, debes decir explícitamente que no lo sabes.
No debes inventar información.
Responde de forma clara y concisa.
"""

def ask_llm(question):
    prompt = f"<s>[SYSTEM]\n{system_prompt}\n[/SYSTEM]\n[USER]\n{question}\n[/USER]\n[ASSISTANT]"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.7,
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

questions = [
    "Explica brevemente qué es el overfitting en machine learning.",
    "Resume el contenido del Real Decreto 1234/2099.",
    "¿Cuál es el algoritmo exacto que usa el BOE para validar licitaciones?",
    "¿Quién fue el primer presidente de Marte?",
]

results = ""
for q in questions:
    answer = ask_llm(q)
    text = f"QUESTION:\n{q}\nANSWER:\n{answer}\n{'-'*15}\n\n"
    print(text)
    results += text
with open("results/results_b2.txt","w") as file:
    file.write(results)

