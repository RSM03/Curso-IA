### PRÁCTICA BLOQUE 2

1. Objetivo del bloque 2

Ajustar el modelo base para que cumpla mejor el prompt estricto.

Reducir alucinaciones y mejorar consistencia.

Mantener entrenamiento ligero usando LoRA o QLoRA.

Documentar cada decisión para que el grupo comprenda por qué ciertos ajustes funcionan.

2. Preparación del dataset

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

**Crear codigos bloque2.1.py y bloque2.2.py**

Entregable del bloque 2

Modelo ajustado (./lora_model)

Notebook reproducible con entrenamiento

Comparativa de respuestas pre y post SFT

Documento técnico breve justificando decisiones:
* Dataset y balance
* Hiperparámetros de LoRA
* Resultados observados y errores residuales