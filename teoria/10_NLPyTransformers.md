Este es el desarrollo extenso del **Bloque 1**. Está diseñado para cubrir aproximadamente entre 3 y 5 horas de lectura, debate y explicación teórica profunda, sentando las bases científicas y técnicas antes de tocar el código.

---

# Bloque 1: Fundamentos de NLP Moderno y la Arquitectura Transformer

## 1.1. La Evolución del NLP: De las Reglas a la Probabilidad
El Procesamiento del Lenguaje Natural (NLP) ha pasado por tres grandes eras:

1.  **Era Simbólica (Reglas):** Basada en gramáticas hechas a mano y diccionarios. Era rígida y no escalaba ante la ambigüedad del lenguaje humano.
2.  **Era Estadística (Machine Learning Clásico):** Modelos como Naive Bayes, SVM o TF-IDF. El éxito dependía del *Feature Engineering* (extraer manualmente características del texto).
3.  **Era de las Redes Neuronales (Deep Learning):**
    *   **RNN (Redes Neuronales Recurrentes) y LSTM:** Procesaban el texto palabra a palabra, de izquierda a derecha. Tenían el problema del "gradiente desvaneciente": olvidaban el principio de una frase larga cuando llegaban al final.
    *   **Transformers (2017 - Presente):** El cambio de paradigma total. Abandonan la secuencialidad por el **paralelismo masivo**.

## 1.2. La Revolución del Transformer: "Attention is All You Need"
La arquitectura Transformer introdujo el mecanismo de **Self-Attention (Auto-atención)**. A diferencia de las RNN, el Transformer "mira" todas las palabras de una secuencia simultáneamente.

### 1.2.1. El Mecanismo de Atención (Q, K, V)
Para entender una palabra, el modelo calcula su relación con todas las demás en la frase. Técnicamente, esto se hace mediante tres vectores:
*   **Query (Consulta):** ¿Qué estoy buscando?
*   **Key (Clave):** ¿Qué información ofrezco?
*   **Value (Valor):** ¿Qué contenido tengo?

La atención se calcula como el producto escalar de $Q$ y $K$, normalizado y pasado por una función *Softmax*, que luego multiplica a $V$. Esto permite que, en la frase *"El banco estaba cerrado porque el río se desbordó"*, la palabra *"banco"* preste atención a *"río"* para entender que se refiere a un accidente geográfico y no a una entidad financiera.

### 1.2.2. Arquitecturas: Encoder vs. Decoder
*   **Encoder-only (ej. BERT):** Lee en ambas direcciones. Ideal para clasificación y extracción de entidades.
*   **Decoder-only (ej. GPT, Llama, Gemma):** Predice el siguiente token. Es la arquitectura reina de la IA Generativa actual.
*   **Encoder-Decoder (ej. T5, Whisper):** El estándar para traducción y transcripción.

## 1.3. Tokenización: El Puente entre Palabras y Números
Los modelos no leen letras ni palabras, leen **Tokens**.

*   **Subword Tokenization:** Técnicas como BPE (Byte Pair Encoding) dividen palabras raras en fragmentos comunes (ej: *"Inconstitucionalmente"* → `["In", "constitucional", "mente"]`).
*   **Vocabulario:** Un modelo suele tener entre 32.000 y 128.000 tokens únicos.
*   **El problema de los idiomas:** Si el tokenizador no ha visto suficiente español, usará más tokens para decir lo mismo que en inglés, lo que hace que el modelo sea más lento y caro en nuestro idioma.

## 1.4. Embeddings: El Espacio Semántico
Una vez tokenizado, cada token se convierte en un **Embedding**: un vector numérico de alta dimensión (ej. 4096 dimensiones en modelos medianos).
*   En este espacio vectorial, las palabras con significados similares están geométricamente cerca.
*   **Aritmética de vectores:** El famoso ejemplo `Rey - Hombre + Mujer = Reina` ocurre realmente en estos espacios latentes.

## 1.5. El Problema Crítico: La Alucinación
La alucinación es el mayor obstáculo para el uso profesional de LLMs.

### 1.5.1. ¿Por qué ocurre?
1.  **Naturaleza Probabilística:** El modelo está entrenado para maximizar la probabilidad del siguiente token (*Next Token Prediction*), no para verificar la veracidad de los hechos.
2.  **Sobreconfianza:** Debido al entrenamiento, el modelo tiende a ser asertivo incluso cuando no sabe la respuesta (un efecto del *RLHF*).
3.  **Falta de Grounding:** El modelo no tiene acceso a una base de datos de hechos; solo tiene su "memoria paramétrica", que es una compresión borrosa de internet.

### 1.5.2. Tipos de Alucinación
*   **Confabulación:** Inventar una biografía o un dato histórico.
*   **Alucinación de Seguimiento de Instrucciones:** El modelo entiende la pregunta pero ignora las restricciones (ej. *"Responde en 3 palabras"* y responde en 10).
*   **Falla de Razonamiento:** Errores en lógica matemática o silogismos simples.

## 1.6. Capacidades Emergentes y Scaling Laws
Se ha descubierto que al aumentar tres variables, el modelo desarrolla capacidades que no tenía antes (como programar o razonar):
1.  **Número de Parámetros:** El tamaño del cerebro (pesos de la red).
2.  **Dataset de Entrenamiento:** La cantidad de "libros" leídos.
3.  **Cómputo (FLOPs):** El tiempo y potencia de GPU invertidos.

Esto dio lugar a los **LLMs (Large Language Models)**. Sin embargo, el curso se centra en cómo usar modelos "pequeños" (7B-9B parámetros) de forma eficiente mediante técnicas avanzadas.

## 1.7. El Stack Tecnológico del Curso
Para trabajar en NLP moderno, necesitamos un ecosistema específico:

*   **Hugging Face:** El "GitHub" de la IA. Provee `transformers` (librería para cargar modelos), `datasets` y el `Hub` (donde están los modelos).
*   **PyTorch:** El motor de cálculo tensorial más usado en investigación.
*   **Accelerate:** Librería para gestionar la memoria de la GPU y el entrenamiento distribuido.
*   **LangChain / LlamaIndex:** Orquestadores para conectar el modelo con datos externos (RAG) y herramientas.
*   **Vector Databases (FAISS/Chroma):** Bases de datos optimizadas para buscar por significado semántico en lugar de por palabras clave.

---

### Dinámica de grupo sugerida para este bloque:
1.  **Debate:** ¿Es la alucinación un error de software o una característica intrínseca de la creatividad del modelo?
2.  **Visualización:** Usar herramientas como *Embedding Projector* para ver cómo se agrupan las palabras en el espacio.
3.  **Análisis de Tokenización:** Probar diferentes frases en el tokenizador de Hugging Face para ver cómo se fragmentan palabras técnicas o legales.

---

### Notas para el instructor:
Este bloque es fundamental para que el alumno entienda que el LLM **no piensa**, sino que **calcula probabilidades**. Sin esta base, no entenderán por qué necesitamos RAG (Bloque 3) o Tools (Bloque 4) para corregir el comportamiento del modelo.