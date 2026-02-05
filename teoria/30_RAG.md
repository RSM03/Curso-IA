Este es el desarrollo extenso del **Bloque 3: Sistemas RAG (Retrieval-Augmented Generation)**. Este bloque representa el cambio de un modelo que "especula" a un modelo que "consulta". Es vital para aplicaciones profesionales donde la veracidad es innegociable.

---

# Bloque 3: Sistemas RAG bien diseñados

## 3.1. El concepto de RAG: Superando la Memoria Paramétrica

Los LLMs tienen dos tipos de "memoria":
1.  **Memoria Paramétrica:** Todo el conocimiento adquirido durante el pre-entrenamiento (los pesos del modelo). Es estática y tiene una fecha de corte (*knowledge cutoff*).
2.  **Memoria No Paramétrica:** Información externa que se le proporciona al modelo en el momento de la consulta.

**RAG (Generación Aumentada por Recuperación)** es la arquitectura que permite al modelo consultar una biblioteca externa de documentos antes de generar una respuesta. En lugar de confiar en lo que "recuerda", el modelo lee los documentos relevantes y sintetiza una respuesta basada exclusivamente en ellos.

### ¿Por qué RAG es superior al Fine-tuning para datos factuales?
*   **Actualización inmediata:** Si un Real Decreto cambia hoy, solo hay que actualizar el documento en la base de datos, no reentrenar el modelo.
*   **Trazabilidad:** RAG permite citar la fuente exacta (ej. "Según el Art. 14 del PDF X...").
*   **Reducción de Alucinaciones:** Al forzar al modelo a usar un contexto dado, se minimiza la invención de datos.

## 3.2. El Pipeline de Ingesta: Preparando el Conocimiento

La calidad de un sistema RAG depende en un 80% de cómo se preparan los datos.

### 3.2.1. Extracción de Texto
No todos los documentos son iguales. Los PDFs (como los del BOE) son especialmente complejos debido a:
*   Columnas múltiples.
*   Tablas.
*   Encabezados y pies de página que ensucian el contexto.
*   Metadatos ocultos.

### 3.2.2. Estrategias de Chunking (Fragmentación)
Un modelo tiene una "ventana de contexto" limitada. No podemos pasarle un PDF de 200 páginas de golpe. Debemos dividirlo en trozos o **chunks**.

*   **Fixed-size Chunking:** Dividir cada X caracteres o palabras. Es simple pero puede cortar una frase por la mitad.
*   **Recursive Character Chunking:** Intenta dividir por párrafos, luego por frases y finalmente por palabras para mantener la unidad semántica.
*   **Overlap (Solape):** Es fundamental mantener un pequeño porcentaje del fragmento anterior en el siguiente (ej. 10-20%) para que el contexto no se pierda en los cortes.

### 3.2.3. Embeddings: La Representación Semántica
Cada chunk se convierte en un vector numérico usando un modelo de **Embeddings** (como `all-MiniLM-L6-v2`). 
*   Estos modelos están entrenados para que frases con significados similares (ej. "vacaciones retribuidas" y "descanso pagado") resulten en vectores que están cerca en el espacio matemático, aunque no compartan palabras exactas.

## 3.3. El Pipeline de Recuperación (Retrieval)

Cuando el usuario hace una pregunta, el sistema realiza los siguientes pasos:

1.  **Vectorización de la consulta:** La pregunta del usuario se convierte en un vector usando el mismo modelo de embeddings.
2.  **Búsqueda de Similitud (Vector Search):** Se comparan el vector de la pregunta con todos los vectores de la base de datos.
3.  **Métricas de Distancia:** 
    *   **Distancia Euclídea (L2):** Mide la distancia física entre puntos.
    *   **Similitud de Coseno:** Mide el ángulo entre vectores (muy efectiva para texto).
4.  **Top-K:** Se seleccionan los $K$ fragmentos más cercanos (generalmente entre 3 y 5).

### Bases de Datos Vectoriales e Índices
Para que la búsqueda sea instantánea entre millones de documentos, usamos librerías como **FAISS** (Facebook AI Similarity Search). FAISS utiliza estructuras de datos como **IVF** (Inverted File Index) o **HNSW** (Hierarchical Navigable Small World) para agrupar vectores y no tener que comparar la pregunta con cada uno de los chunks existentes.

## 3.4. El Pipeline de Generación: Grounding y Prompting

Una vez tenemos los fragmentos relevantes, el último paso es la **Generación**. Aquí es donde el LLM (Gemma-2-9B en nuestro caso) entra en juego.

### 3.4.1. Construcción del Prompt con Contexto
El prompt se estructura de forma que el modelo entienda que tiene una "fuente de verdad".
Ejemplo:
> "Eres un asistente legal. Basándote exclusivamente en el siguiente CONTEXTO, responde a la PREGUNTA. Si la respuesta no está en el contexto, di que no lo sabes.
> CONTEXTO: {chunks_recuperados}
> PREGUNTA: {pregunta_usuario}"

### 3.4.2. Grounding (Anclaje)
El grounding es la técnica de asegurar que el modelo no se desvíe del contexto. Un modelo bien "anclado" rechazará responder preguntas sobre cultura general si su contexto solo habla de convenios laborales.

## 3.5. Problemas Comunes y RAG Avanzado

Incluso un RAG bien diseñado puede fallar. Los problemas típicos son:

1.  **Fallo en la Recuperación:** El sistema recupera chunks que no contienen la respuesta porque la pregunta era ambigua.
2.  **Fallo en la Generación:** El sistema tiene la información correcta en el contexto pero el modelo alucina o la ignora.
3.  **Lost in the Middle:** Los LLMs tienden a prestar más atención al principio y al final del contexto proporcionado, olvidando detalles que están en los chunks centrales.

### Técnicas de Mejora (RAG de 2ª Generación)
*   **Query Expansion:** El modelo reescribe la pregunta del usuario para que sea más fácil de buscar.
*   **Re-ranking:** Se recuperan 20 chunks con un modelo rápido y luego un segundo modelo más inteligente (Cross-Encoder) los ordena para seleccionar los 3 mejores.
*   **Hybrid Search:** Combinar búsqueda vectorial (semántica) con búsqueda tradicional por palabras clave (BM25), muy útil para encontrar códigos de artículos exactos o nombres propios.

---

### Dinámica de grupo sugerida:
1.  **Visualización de Chunks:** Mostrar cómo un mismo texto cambia radicalmente su significado si el chunking corta una frase clave.
2.  **Simulación de Búsqueda:** Pedir a los alumnos que busquen manualmente en un PDF y comparen su velocidad y precisión con el sistema RAG.
3.  **Análisis de "No sé":** Forzar al sistema RAG a responder preguntas sobre temas que no están en los documentos y ajustar el prompt hasta que el modelo admita su ignorancia de forma consistente.

---

### Notas para el instructor:
Este bloque es donde los alumnos verán la mayor mejora en la utilidad real del asistente. Es fundamental enfatizar que **un RAG es tan bueno como sus datos**. Si la extracción del PDF del BOE es mala, la respuesta será mala, por muy potente que sea el modelo Gemma. Se debe dedicar tiempo a explicar la importancia de los **metadatos** (saber de qué PDF y qué página viene cada chunk) para la auditoría posterior.