Este es el desarrollo extenso del **Bloque 2: Fine-tuning y Entrenamiento Eficiente**. Este bloque es el núcleo técnico del curso, donde pasamos de ser usuarios de modelos a "entrenadores". Está diseñado para cubrir entre 6 y 8 horas de contenido teórico-práctico.

---

# Bloque 2: Fine-tuning y Entrenamiento Eficiente (PEFT)

## 2.1. El Paradigma del Ajuste Fino (Fine-tuning)

El entrenamiento de un LLM no es un proceso único, sino una escalera de refinamiento. Para entender el **SFT (Supervised Fine-Tuning)**, primero debemos ubicarlo en el ciclo de vida del modelo:

1.  **Pre-training (Pre-entrenamiento):** El modelo aprende a predecir el siguiente token a partir de una cantidad masiva de datos (terabytes de texto). Aquí adquiere "conocimiento del mundo" y gramática, pero no sabe seguir instrucciones. Es un completador de frases.
2.  **SFT (Supervised Fine-Tuning):** Es el proceso de entrenar al modelo en un dataset más pequeño y curado de pares **Instrucción -> Respuesta**. Aquí es donde el modelo aprende el formato de chat y a obedecer órdenes.
3.  **Alignment (Alineación - RLHF/DPO):** Se ajusta el modelo para que sus respuestas sean seguras, útiles y honestas, basándose en preferencias humanas.

### ¿Cuándo hacer Fine-tuning y cuándo no?
Es un error común intentar usar Fine-tuning para inyectar conocimientos nuevos (ej. los detalles de un nuevo Real Decreto). Para eso es mejor el RAG (Bloque 3). El Fine-tuning se usa para:
*   **Dominio del lenguaje:** Aprender terminología técnica o legal muy específica que no estaba en el pre-entrenamiento.
*   **Formato y Estructura:** Forzar al modelo a responder siempre en un JSON específico, o con un tono académico extremadamente riguroso.
*   **Restricciones de comportamiento:** Enseñar al modelo a ser extremadamente precavido y a decir "No lo sé" con mayor frecuencia.

## 2.2. Ingeniería de Datos para Instrucciones

En el SFT, **la calidad es infinitamente más importante que la cantidad**. 1.000 ejemplos perfectos son mejores que 100.000 ejemplos mediocres.

### 2.2.1. Estructura de un Dataset de Instrucciones
Un dataset típico de SFT (como el que usaremos en la práctica) tiene tres campos:
*   **Instruction:** La tarea que debe realizar el modelo.
*   **Input:** Contexto adicional (opcional).
*   **Output:** La respuesta "dorada" o perfecta que el modelo debe imitar.

### 2.2.2. Formatos de Prompt (Templates)
Los modelos no ven el texto plano, lo ven dentro de una estructura. Los más comunes son:
*   **Alpaca:** `### Instruction: ... ### Response: ...`
*   **ChatML:** `<|im_start|>user ... <|im_end|> <|im_start|>assistant ...`
*   **Gemma/Llama 3:** Usan etiquetas especiales como `<start_of_turn>` o `<|begin_of_text|>`.

## 2.3. PEFT: Parameter-Efficient Fine-Tuning

Entrenar un modelo de 9.000 millones de parámetros (9B) requeriría actualizar 9B de números en cada paso. Esto necesita cientos de gigabytes de VRAM. PEFT surge como la solución para entrenar modelos potentes en hardware accesible.

### 2.3.1. LoRA (Low-Rank Adaptation)
LoRA es la técnica más popular de PEFT. Su funcionamiento se basa en una hipótesis matemática: los cambios que necesita un modelo durante el fine-tuning tienen un "rango intrínseco bajo".

**¿Cómo funciona?**
En lugar de modificar la matriz de pesos original $W$ (que es enorme), LoRA congela $W$ y añade dos matrices pequeñas, $A$ y $B$, al lado.
*   $W$ permanece intacta (no se entrena).
*   Solo se entrenan $A$ y $B$.
*   El resultado final es $W + (A \times B)$.

**Ventajas:**
*   Reducción del 99% de los parámetros entrenables.
*   Menor uso de memoria.
*   Los "adaptadores" resultantes pesan apenas unos megabytes, facilitando su distribución.

### 2.3.2. QLoRA: Cuantización + LoRA
QLoRA lleva la eficiencia al límite. Introduce tres innovaciones:
1.  **4-bit NormalFloat (NF4):** Comprime los pesos del modelo original a solo 4 bits sin perder apenas precisión.
2.  **Double Quantization:** Comprime incluso las constantes de cuantización.
3.  **Paged Optimizers:** Gestiona los picos de memoria usando la RAM del sistema si la VRAM de la GPU se llena, evitando errores de "Out of Memory".

**Resultado:** Podemos entrenar un modelo de 9B o incluso 13B en una sola GPU de consumo (como una RTX 3090 o 4090).

## 2.4. Hiperparámetros Críticos en el Entrenamiento

Para que el entrenamiento tenga éxito, debemos ajustar varios "pomos" técnicos:

*   **Rank (r):** El tamaño de las matrices $A$ y $B$ en LoRA. Valores comunes: 8, 16, 32. Un $r$ más alto permite aprender tareas más complejas pero usa más memoria.
*   **Lora Alpha ($\alpha$):** Un factor de escala para el aprendizaje. Normalmente se fija en el doble del Rank (si $r=16$, $\alpha=32$).
*   **Learning Rate (Tasa de aprendizaje):** En SFT suele ser mucho más baja que en el pre-entrenamiento (ej. $2 \times 10^{-4}$). Si es muy alta, el modelo "olvida" lo que sabía (Catastrophic Forgetting).
*   **Epochs (Épocas):** Cuántas veces el modelo ve el dataset completo. En SFT, entre 1 y 3 épocas suelen ser suficientes. Más de eso produce **Overfitting** (el modelo memoriza los ejemplos en lugar de aprender a razonar).

## 2.5. Evaluación del Entrenamiento

¿Cómo sabemos si el modelo ha mejorado?
1.  **Train/Eval Loss:** La curva de pérdida debe descender. Si la pérdida de validación empieza a subir mientras la de entrenamiento baja, hay overfitting.
2.  **Catastrophic Forgetting:** Debemos comprobar que el modelo no ha perdido habilidades básicas (ej. si después de entrenarlo en leyes, olvida cómo saludar o cómo sumar).
3.  **Benchmark Cualitativo:** Comparar las respuestas del modelo base vs. el modelo entrenado ante las mismas preguntas "trampa" diseñadas en el Bloque 1.

---

### Conceptos Avanzados para Discusión:
*   **Target Modules:** ¿A qué partes del Transformer aplicamos LoRA? (Normalmente a las capas de atención: `q_proj`, `v_proj`, `k_proj`, `o_proj`).
*   **Gradient Accumulation:** Técnica para simular batches grandes cuando tenemos poca memoria VRAM.
*   **FP16 vs BF16:** Formatos de precisión numérica. BF16 es preferible en GPUs modernas (Nvidia Ampere o superior) porque es más estable durante el entrenamiento.

---

### Notas para el instructor:
Este bloque debe dejar claro que el Fine-tuning es un **cambio de comportamiento**, no una **actualización de base de datos**. Al terminar la teoría, los alumnos deben entender que van a "congelar" el cerebro de Gemma-2-9B y solo van a entrenar unas pequeñas capas adicionales (LoRA) para que el modelo aprenda a ser un "Asistente Académico Riguroso" que no inventa nada.