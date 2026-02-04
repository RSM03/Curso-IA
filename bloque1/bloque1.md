### PRÁCTICA BLOQUE 1

Objetivo del bloque 1

El objetivo no es “usar un LLM”, sino entender cómo falla antes de modificarlo. Al finalizar el bloque, los alumnos deben ser capaces de explicar con evidencias:
* Qué sabe el modelo
* Qué no sabe
* Cuándo alucina
* Cómo responde ante incertidumbre
* Qué límites tiene sin fine-tuning ni RAG

Todo lo que se observe aquí se usará como referencia en los siguientes bloques.

**Crear bloque1.py**

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