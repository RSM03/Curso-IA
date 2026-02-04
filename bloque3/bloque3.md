### PRÁCTICA BLOQUE 3 · RAG como corrección estructural del modelo

1. Objetivo del bloque 3

El objetivo no es que el modelo “tenga más información”, sino separar comportamiento y conocimiento.

Al finalizar el bloque, los alumnos deben poder demostrar con datos:

* Qué errores del bloque 1 y 2 no se pueden resolver con fine-tuning
* Cómo RAG reduce alucinaciones solo si está bien diseñado
* En qué casos RAG empeora la respuesta
* Qué decisiones de chunking, recuperación y prompt afectan directamente a la calidad

Este bloque introduce conocimiento externo sin reentrenar el modelo.

2. Diseño conceptual del RAG (antes de código)

Se fuerza a los alumnos a decidir explícitamente:

* Qué documentos son “fuente de verdad”
* Qué tamaño de chunk tiene sentido
* Qué ocurre cuando no hay evidencia recuperable
* Cómo se obliga al modelo a citar o abstenerse

Restricción clave: El modelo no puede responder usando conocimiento previo si no hay contexto recuperado.

3. Corpus documental del bloque

Se recomienda un corpus pequeño pero realista con PDFs o TXT. 

En este caso la carpeta "BOE" con diferentes convenios nacionales.

4. Ingesta de PDFs del BOE con chunking explícito

Objetivo técnico del punto 4

Transformar una carpeta BOE/ con múltiples PDFs en:

* Un conjunto de chunks textuales trazables
* Un índice vectorial reproducible
* Metadatos suficientes para auditar de dónde sale cada respuesta

Restricción clave del bloque: No se permite responder sin evidencia recuperada.

```pgsql
BOE/
 ├── convenio_metal_2022.pdf
 ├── convenio_hosteleria_2023.pdf
 ├── convenio_quimicas_2021.pdf

rag_store/
 ├── index.faiss
 ├── chunks.json
```

Decisiones de diseño previas al código:

* Extracción de texto por página (no todo el PDF de golpe)
* Chunking por tamaño fijo con solape
* Persistencia de metadatos: pdf, página, chunk_id
* Embeddings separados del modelo generativo

Esto permite luego analizar errores de recuperación, no solo de generación.

**Crear bloque3.1.py para ingesta**

5. **Crear bloque3.1.py para consulta RAG**

6. Análisis guiado obligatorio del bloque 3

Cada grupo debe documentar:

* ¿Recupera el chunk correcto pero responde mal?
* ¿Responde bien con chunk parcial?
* ¿Se apoya demasiado en frases genéricas del BOE?
* ¿Hay casos donde el modelo debería decir “no lo sé” y no lo hace?

Identificar explícitamente:

* Alucinaciones con contexto presente
* Alucinaciones con contexto insuficiente
* Falsos positivos por similitud semántica

7. Puente natural al bloque 4

Este punto queda sembrado de forma intencionada:

Problemas no resueltos todavía:

* El modelo no decide cuándo buscar más información
* No valida si el contexto es suficiente
* No puede ejecutar búsquedas dirigidas por artículo
* No razona sobre contradicciones entre convenios
* Eso justifica tools, function calling y agentes en el siguiente bloque, no como moda, sino como necesidad técnica.