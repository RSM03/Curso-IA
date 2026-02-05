Este es el desarrollo extenso del **Bloque 6: Evaluación Avanzada y Auditable de Sistemas NLP**. Este bloque es, posiblemente, el más crítico para la transferencia al mundo real, ya que responde a la pregunta: *¿Cómo puedo garantizar que mi sistema es seguro y fiable antes de que lo use un cliente?*

---

# Bloque 6: Evaluación Avanzada y Auditable de Sistemas NLP

## 6.1. La Crisis de la Evaluación en la Era de los LLMs

Tradicionalmente, en el NLP clásico, evaluábamos modelos con métricas exactas como **F1-Score**, **Precision** o **Recall** (para clasificación) y **BLEU** o **ROUGE** (para traducción o resumen). 

### 6.1.1. Por qué las métricas clásicas ya no sirven
Las métricas basadas en el solape de palabras (como BLEU) fallan estrepitosamente con los LLMs porque:
*   **No miden la veracidad:** Una respuesta puede tener todas las palabras del texto original pero decir exactamente lo contrario (ej. añadir un "no").
*   **No miden la semántica:** "El salario es de mil euros" y "La remuneración asciende a 1.000€" tienen un solape bajo de palabras pero son semánticamente idénticas.
*   **No evalúan el razonamiento:** No pueden medir si un agente tomó la decisión correcta al elegir una herramienta.

Por tanto, necesitamos un nuevo paradigma: la **Evaluación Basada en Modelos y Criterios Técnicos**.

## 6.2. Dimensiones de Evaluación en Sistemas RAG y Agentes

Para evaluar el asistente académico que estamos construyendo, no podemos mirar solo la respuesta final. Debemos evaluar los componentes del sistema:

### 6.2.1. Fidelidad (Faithfulness)
Mide si la respuesta se deriva **exclusivamente** del contexto recuperado. Es la métrica principal para detectar alucinaciones. Si el modelo dice algo que no está en los chunks del BOE, la fidelidad es baja.

### 6.2.2. Relevancia de la Respuesta
Mide si la respuesta realmente aborda la pregunta del usuario. Un modelo puede ser muy fiel al texto pero responder algo que el usuario no preguntó.

### 6.2.3. Precisión de la Recuperación (Context Precision)
Evalúa si los chunks recuperados por el sistema RAG son realmente los que contienen la respuesta. Si el sistema recupera 5 chunks y solo el 5º es útil, la precisión es baja, lo que aumenta el ruido para el modelo.

## 6.3. LLM-as-a-Judge: El Modelo como Evaluador

Una de las técnicas más espectaculares y efectivas hoy en día es usar un modelo de lenguaje superior (el "Juez") para evaluar las respuestas de nuestro modelo (el "Estudiante").

### 6.3.1. ¿Cómo funciona un Juez LLM?
No se trata de pedirle al modelo "Dime si esta respuesta es buena". Eso genera respuestas subjetivas. El proceso técnico requiere:
1.  **Rúbricas Claras:** Proporcionar al juez criterios de puntuación del 0 al 10 con definiciones de qué significa cada número.
2.  **Justificación Obligatoria:** Forzar al juez a explicar su razonamiento antes de dar la nota (Chain of Thought).
3.  **Formato Estructurado:** Exigir la salida en JSON para poder procesar las métricas automáticamente.

### 6.3.2. Sesgos del Juez (y cómo mitigarlos)
Los jueces LLM no son perfectos. Tienen sesgos conocidos:
*   **Sesgo de Posición:** Tienden a puntuar mejor la primera respuesta que leen.
*   **Sesgo de Longitud:** Tienden a pensar que las respuestas más largas son mejores.
*   **Sesgo de Auto-preferencia:** Los modelos de una familia (ej. Gemma) suelen puntuar mejor a otros modelos de su misma familia.
*   **Mitigación:** Usar prompts de "pocos ejemplos" (few-shot) y modelos de juez muy capaces (como Gemma-3-12B o superiores).

## 6.4. El Contrato de Salida: Etiquetas de Control

En sistemas de producción, la evaluación automática depende de la **limpieza de los datos**. Si el modelo genera texto "basura" antes o después de la respuesta, el evaluador fallará.

### 6.4.1. El uso de `<ASSISTANT>` y `</ASSISTANT>`
Implementamos un "contrato formal". El sistema solo considera como respuesta válida lo que esté encerrado entre estas etiquetas. 
*   Esto permite separar el razonamiento interno del agente (que puede ser sucio y largo) de la respuesta final que recibe el usuario.
*   Si el modelo no respeta el formato, la evaluación lo marca como **"Error de Formato"**, lo cual es un fallo de ingeniería tan grave como una alucinación.

## 6.5. Construcción de un Benchmark (Conjunto de Pruebas)

Un benchmark es un conjunto de preguntas "doradas" (Ground Truth) que representan los casos de uso reales del sistema.

### 6.5.1. Tipos de casos en el Benchmark
Para que la evaluación sea auditable, el benchmark debe incluir:
1.  **Casos Factuales:** Preguntas con respuesta clara en los documentos.
2.  **Casos de Abstención:** Preguntas sobre temas que sabemos que NO están en los documentos. Aquí el éxito es que el modelo diga "No lo sé".
3.  **Casos Multi-fuente:** Preguntas que obligan al agente a consultar dos o más PDFs.
4.  **Casos de Trampa:** Preguntas con premisas falsas (ej. "¿Cuál es el salario en Marte según el convenio del metal?").

## 6.6. Métricas de Agente: Evaluando el Comportamiento

A diferencia de un chatbot simple, un agente toma decisiones. Debemos medir:
*   **Tool Selection Accuracy:** ¿Eligió el PDF correcto el 100% de las veces?
*   **Abstention Rate:** ¿Se abstiene demasiado (es muy cobarde) o demasiado poco (es muy arriesgado)?
*   **Efficiency:** ¿Cuántos pasos necesita para llegar a la respuesta?

## 6.7. Trazabilidad y Auditoría

La evaluación avanzada no termina con un número (ej. "Mi modelo tiene un 8.5"). Termina con un **informe de errores clasificables**.
*   **Análisis de Errores:** Debemos ser capaces de decir: "El 20% de los fallos se deben a una mala recuperación de FAISS y el 10% a que el modelo ignora el contexto".
*   **Logs de Evaluación:** Guardar cada juicio del LLM-as-a-judge para que un humano pueda revisar si el juez está siendo demasiado estricto o demasiado permisivo.

---

### Dinámica de grupo sugerida:
1.  **Ser el Juez:** Entregar a los alumnos 3 respuestas de un LLM y una rúbrica. Pedirles que las puntúen. Luego, comparar sus notas con las que da el script `bloque6.py`. Discutir por qué hay discrepancias.
2.  **Diseño de Preguntas Trampa:** Cada grupo debe crear 5 preguntas diseñadas específicamente para hacer que el agente alucine. Probarlas y ver si el sistema de evaluación detecta la alucinación.
3.  **Refinado de Rúbricas:** Modificar el prompt del juez en el código para que sea "extremadamente crítico" con el lenguaje académico y ver cómo cambian los resultados.

---

### Notas para el instructor:
Este bloque transforma el curso de "experimento" a "ingeniería". Es fundamental que los alumnos entiendan que **sin evaluación, no hay progreso**. Se debe enfatizar que el dataset de evaluación (`eval_dataset_b6.json`) es el activo más valioso de la empresa, ya que permite iterar el modelo y el RAG con la seguridad de que no estamos rompiendo lo que ya funcionaba (evitar la regresión).