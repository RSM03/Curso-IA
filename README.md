# NOTAS CURSO IA

## MAIN

**Enfoque general del curso**

Curso 100 % orientado a NLP moderno con LLMs. Se trabaja siempre sobre un mismo caso práctico, por ejemplo un asistente experto sobre documentación técnica o normativa, que irá incorporando fine-tuning, RAG, tools, agentes, evaluación y despliegue.

Formato recomendado: 30 horas divididas en 10 sesiones de 3 horas, combinando teoría corta y práctica guiada.

**Marco general de la práctica**

Caso base: construcción de un asistente experto académico que responde con rigor a partir de documentación especializada y es capaz de reconocer cuándo no sabe, buscar evidencia y justificar sus respuestas.

Restricciones intencionadas:
* Uso de un modelo open source mediano
* Recursos limitados para forzar entrenamiento eficiente
* Necesidad de trazabilidad y evaluación

Repositorio único que se va completando por bloques, con checkpoints claros y revisión técnica al final de cada uno.

**Bloque 1. Fundamentos y preparación del entorno (3 horas)**

Objetivo: que todos partan de una base común y tengan el entorno listo.

Contenidos:
* Repaso rápido de NLP clásico vs NLP con LLMs
* Arquitectura de los LLM modernos
* Tokens, contexto, embeddings, atención y limitaciones reales
* Alucinaciones y por qué ocurren
* Stack de trabajo: Python, Hugging Face, PyTorch, LangChain/LlamaIndex, vectores, APIs

**Práctica: Baseline controlado y diagnóstico**

Objetivo práctico: entender el comportamiento real del modelo antes de tocar nada.

Trabajo práctico:
* Cargar un modelo base y definir un prompt sistema estricto
* Diseñar un set de preguntas trampa y preguntas sin respuesta
* Medir alucinación, sobreconfianza y pérdida de contexto
* Documentar fallos observados y límites del modelo

Entrega del bloque:
* Notebook o script con pruebas reproducibles
* Informe breve de diagnóstico técnico

**Bloque 2. Fine-tuning y entrenamiento eficiente (6 horas)**

Objetivo: entender y aplicar SFT sin infraestructuras prohibitivas.

Contenidos:
* Qué es SFT y cuándo tiene sentido
* Preparación de datasets de entrenamiento NLP
* LoRA y QLoRA: conceptos y ventajas
* Ajuste de hiperparámetros clave
* Evaluación básica post-entrenamiento

**Práctica: Fine-tuning con SFT + LoRA**

Objetivo práctico: modificar el comportamiento del modelo, no su conocimiento.

Trabajo práctico:
* Diseño de un dataset de instrucciones de alta calidad
* Justificación del formato y balance del dataset
* Entrenamiento SFT con LoRA o QLoRA
* Comparación cuantitativa y cualitativa con el baseline
* Control de overfitting y degradación

Entrega del bloque:
* Modelo entrenado versionado
* Métricas comparativas
* Decisiones técnicas documentadas

**Bloque 3. Sistemas RAG bien diseñados (6 horas)**

Objetivo: reducir alucinaciones y ampliar conocimiento.

Contenidos:
* Arquitectura RAG de extremo a extremo
* Chunking, embeddings y bases vectoriales
* Recuperación semántica vs híbrida
* Prompting para RAG efectivo
* Errores comunes en RAG

**Práctica: RAG serio, no decorativo**

Objetivo práctico: añadir conocimiento externo fiable.

Trabajo práctico:
* Selección y preparación del corpus documental
* Decisiones de chunking y embeddings
* Construcción del índice vectorial
* Diseño del prompt RAG con citación
* Análisis de casos donde RAG empeora la respuesta

Entrega del bloque:
* Pipeline RAG completo
* Evaluación con y sin recuperación
* Registro de errores y ajustes

**Bloque 4. Tools, function calling y control del modelo (6 horas)**

Objetivo: que el modelo deje de “inventar” y sepa cuándo pedir ayuda.

Contenidos:
* Concepto de tools y function calling
* Detección de falta de conocimiento
* Diseño de herramientas seguras
* Integración con búsquedas, scripts y APIs
* Guardrails y validaciones de salida

**Práctica: Tools y detección de ignorancia**

Objetivo práctico: eliminar respuestas inventadas.

Trabajo práctico:
* Definir criterios explícitos de “no sé”
* Implementar function calling para búsquedas o scripts
* Forzar al modelo a elegir entre responder o usar una tool
* Validación estructurada de salidas

Entrega del bloque:
* Conjunto de tools funcionales
* Tests donde el modelo decide no responder
* Evidencia de reducción de alucinaciones

**Bloque 5. Agentes NLP y orquestación (4 horas)**

Objetivo: pasar de un chatbot a un sistema autónomo controlado.

Contenidos:
* Qué es un agente y cuándo usarlo
* Planificación, memoria y control
* Patrones de agentes
* Riesgos y límites de los agentes

**Práctica: Agente controlado**

Objetivo práctico: orquestar razonamiento sin perder control.

Trabajo práctico:
* Definir estados, memoria y límites del agente
* Separar planificación y ejecución
* Integrar RAG y tools en el loop del agente
* Manejo de errores y timeouts

Entrega del bloque:
* Agente funcional con logs
* Análisis de comportamiento paso a paso

**Bloque 6. Evaluación avanzada y métricas (3 horas)**

Objetivo: medir calidad y fiabilidad de forma objetiva.

Contenidos:
* Evaluación clásica vs evaluación con LLMs
* LLM-as-a-judge
* Métricas de RAG
* Detección de alucinaciones
* Logging y trazabilidad

**Práctica: Evaluación avanzada**

Objetivo práctico: medir calidad de forma defendible.

Trabajo práctico:
* Construcción de un benchmark propio
* Uso de LLM-as-a-judge con criterios explícitos
* Métricas específicas de RAG y tools
* Comparativa de versiones del sistema

Entrega del bloque:
* Pipeline de evaluación automatizado
* Resultados interpretados críticamente

**Bloque 7. Puesta en producción (2 horas)**

Objetivo: dejar el sistema listo para uso real.

Contenidos:
* Arquitectura de despliegue
* APIs y serving de modelos
* Gestión de versiones
* Seguridad y costes
* Monitorización en producción

**Práctica: Preparación para producción**

Objetivo práctico: cerrar el ciclo de vida.

Trabajo práctico:
* Exposición del sistema como API
* Gestión de configuración y versiones
* Logging, métricas y monitorización básica
* Análisis de costes y escalabilidad

Entrega final:
* Sistema desplegable
* Documento técnico completo del proyecto

Resultado final:
* Modelo entrenado con SFT + LoRA
* Sistema RAG funcional
* Uso de tools y function calling
* Agente controlado
* Evaluación automática
* Preparado para producción con métricas

### PRÁCTICA BLOQUE 1

Objetivo del bloque 1

El objetivo no es “usar un LLM”, sino entender cómo falla antes de modificarlo. Al finalizar el bloque, los alumnos deben ser capaces de explicar con evidencias:
* Qué sabe el modelo
* Qué no sabe
* Cuándo alucina
* Cómo responde ante incertidumbre
* Qué límites tiene sin fine-tuning ni RAG

Todo lo que se observe aquí se usará como referencia en los siguientes bloques.

Requisitos previos del sistema

Sistema base recomendado:
* Linux (Ubuntu 20.04 o superior ideal)
* Python 3.10 o 3.11
* GPU opcional pero recomendable (si no, se ajustan modelos pequeños)

Comprobaciones iniciales:

```bash

python3 --version

nvidia-smi

```

Si no hay GPU, no pasa nada, pero usaremos modelos más pequeños o inferencia CPU lenta.

Creación del entorno de trabajo

Creamos un entorno aislado y limpio. Esto es importante porque luego se añadirá entrenamiento y librerías pesadas.

Token hugging face

1. Ve a Hugging Face

2. Entra en tu cuenta → Settings → Access Tokens → New token.

3. Copia el token (tipo “Write” si quieres subir modelos, “Read” basta para descargar).

hf_login.py

```python

from huggingface_hub import login

# Pega tu token aquí

token = "hf_XXXXXXXXXXXXXXXXXXXX"

login(token=token)

```

```bash

sudo apt install python3-venv

mkdir nlp-curso

cd nlp-curso

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip setuptools wheel

pip install torch transformers accelerate datasets

pip install jupyter matplotlib pandas

```

Si hay GPU con CUDA compatible, torch suele detectarla solo. Para comprobarlo:

```bash

python - << EOF

import torch

print(torch.cuda.is_available())

EOF

```

bloque1.py:

```python

from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "google/gemma-2-9b-it"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(

    model_name,

    device_map="auto"

)

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

with open("results_b1.txt","w") as file:

    file.write(results)

```

Análisis guiado de resultados

Aquí es donde tú marcas el nivel del curso. Cada alumno o grupo debe analizar:
* ¿El modelo reconoce que no sabe?
* ¿Inventó detalles?
* ¿Usa lenguaje de certeza cuando no debería?
* ¿Ignora instrucciones del prompt sistema?

Se recomienda que documenten ejemplos claros de:
* Alucinación dura
* Alucinación suave
* Respuesta evasiva
* Respuesta correcta pero no justificada

Entregable del bloque 1

Cada grupo debe entregar:
* Código reproducible
* CSV con resultados
* Documento breve con diagnóstico técnico del modelo
* Lista priorizada de problemas a resolver en bloques posteriores


### PRÁCTICA BLOQUE 2

1. Objetivo del bloque 2

Ajustar el modelo base para que cumpla mejor el prompt estricto.

Reducir alucinaciones y mejorar consistencia.

Mantener entrenamiento ligero usando LoRA o QLoRA.

Documentar cada decisión para que el grupo comprenda por qué ciertos ajustes funcionan.

2. Preparación del entorno

Ya tenemos el entorno del bloque 1, solo necesitamos instalar librerías adicionales para SFT y LoRA.

```bash

source venv/bin/activate

# SFT y LoRA

pip install peft datasets evaluate

# QLoRA y 4-bit

pip install bitsandbytes

```

3. Preparación del dataset

Se recomienda crear un dataset de instrucciones personalizado, basado en las observaciones del bloque 1.

Incluir ejemplos de preguntas que el modelo respondió mal.

Añadir instrucciones claras de no inventar información.

Balancear tipos de preguntas: conocimiento seguro, dudas, premisas incorrectas, respuestas evasivas.

Formato simplificado para dataset.csv:

```csv

instruction|input|output

"Explica brevemente qué es el overfitting en ML"||"Overfitting es cuando un modelo se ajusta demasiado a los datos de entrenamiento y no generaliza bien a datos nuevos."

"Resume el contenido del Real Decreto 1234/2099"||"No tengo acceso a este documento, por lo que no puedo ofrecer un resumen."

"¿Cuál es el algoritmo exacto que usa el BOE para validar licitaciones?"||"No existe información pública sobre el algoritmo exacto utilizado por el BOE."

"¿Quién fue el primer presidente de Marte?"||"No existe información sobre presidentes de Marte."

"Describe cómo funciona un motor de combustión interna"||"Un motor de combustión interna convierte la energía química del combustible en energía mecánica mediante la combustión controlada en cilindros."

"Traduce al italiano: 'El aprendizaje automático es fascinante'"||"L'apprendimento automatico è affascinante."

"Explica el concepto de RAG en LLMs"||"RAG (Retrieval-Augmented Generation) combina un modelo generativo con un sistema de recuperación de información para mejorar las respuestas y reducir alucinaciones."

"Responde a esta pregunta imposible: ¿Cuál es la capital del océano Atlántico?"||"No hay una capital del océano Atlántico; la pregunta no tiene sentido geográfico."

"Da un ejemplo de una herramienta para procesar texto en Python"||"Un ejemplo es la librería `spaCy`, que permite tokenización, análisis gramatical y extracción de entidades."

"Resume brevemente qué son los embeddings en NLP"||"Los embeddings son representaciones vectoriales de palabras o frases que capturan su significado semántico en un espacio continuo."

```

```python

# -*- coding: utf-8 -*-

from datasets import load_dataset

from transformers import AutoTokenizer, AutoModelForCausalLM

from peft import LoraConfig, get_peft_model, PeftModel

from transformers import Trainer, TrainingArguments

import torch

# Carga dataset

dataset = load_dataset("csv", data_files="dataset_b2.csv", delimiter="|")

print(dataset)

# Modelo y tokenizer

model_name = "google/gemma-2-9b-it"

tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", dtype=torch.float16)

# Aplicar LoRA (si ya lo hiciste, conserva)

lora_config = LoraConfig(

    r=16,

    lora_alpha=32,

    target_modules=["q_proj","v_proj"],

    lora_dropout=0.05,

    bias="none",

    task_type="CAUSAL_LM"

)

model = get_peft_model(model, lora_config)

# Preprocess correcto: prompt separado de la respuesta y labels en -100 para prompt

def preprocess(example):

    instruction = example.get("instruction", "") or ""

    input_text = example.get("input", "") or ""

    output_text = example.get("output", "") or ""

    prompt = (

        "### Instrucción:\n"

        f"{instruction}\n\n"

        "### Entrada:\n"

        f"{input_text}\n\n"

        "### Respuesta:\n"

    )

    # Tokenizar prompt y output por separado

    prompt_ids = tokenizer(prompt, truncation=True, max_length=256, add_special_tokens=False)["input_ids"]

    output_ids = tokenizer(output_text, truncation=True, max_length=256, add_special_tokens=False)["input_ids"]

    input_ids = prompt_ids + output_ids

    attention_mask = [1] * len(input_ids)

    labels = [-100] * len(prompt_ids) + output_ids

    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}

# Mapear dataset (no batched para evitar problemas con la tokenización personalizada)

tokenized = dataset.map(preprocess, batched=False)

tokenized = tokenized["train"].train_test_split(test_size=0.2)

# Collate dinámico que usa tokenizer.pad y deja labels con -100

def collate_fn(features):

    # features: lista de dicts con input_ids, attention_mask, labels (listas de distinto length)

    batch = tokenizer.pad(

        features,

        padding=True,

        return_tensors="pt"

    )

    # Construir labels padded con -100

    labels = [f["labels"] for f in features]

    max_len = batch["input_ids"].shape[1]

    padded_labels = torch.full((len(labels), max_len), -100, dtype=torch.long)

    for i, lab in enumerate(labels):

        lab_t = torch.tensor(lab, dtype=torch.long)

        padded_labels[i, : lab_t.shape[0]] = lab_t

    batch["labels"] = padded_labels

    return batch

# Training args (ajusta a tu GPU/memoria)

training_args = TrainingArguments(

    output_dir="./lora_model",

    per_device_train_batch_size=1,

    gradient_accumulation_steps=4,

    num_train_epochs=8,

    learning_rate=2e-4,

    fp16=True,

    logging_steps=10,

    save_steps=200,

    save_total_limit=2,

    report_to="none"

)

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=tokenized["train"],

    eval_dataset=tokenized["test"],

    data_collator=collate_fn

)

trainer.train()

# Guardar adaptadores LoRA y tokenizer

model.save_pretrained("./lora_model")

tokenizer.save_pretrained("./lora_model")

```


```python

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

with open("results_b2.txt","w") as file:

    file.write(results)

```

Entregable del bloque 2

Modelo ajustado (./lora_model)

Notebook reproducible con entrenamiento

Comparativa de respuestas pre y post SFT

Documento técnico breve justificando decisiones:
* Dataset y balance
* Hiperparámetros de LoRA
* Resultados observados y errores residuales