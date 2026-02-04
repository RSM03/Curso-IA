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