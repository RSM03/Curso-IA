Esta sección se sitúa justo antes de la evolución del NLP, proporcionando el contexto técnico necesario sobre qué es el aprendizaje automático (Machine Learning) en su sentido más amplio. Es fundamental para que los alumnos entiendan que los LLMs no son entes aislados, sino la culminación de décadas de optimización matemática.

---

# Prolegómeno: Los Cimientos del Machine Learning

Antes de sumergirnos en el lenguaje, debemos entender la disciplina que lo hace posible. El Machine Learning (ML) es, en esencia, el arte de **encontrar patrones en los datos para predecir el futuro o clasificar el presente** sin ser programado explícitamente para ello.

La progresión desde una simple línea en un gráfico hasta las redes neuronales profundas es una historia de lucha contra la complejidad.

## 1. El Origen: Modelos Paramétricos y Lineales
Todo comenzó con la estadística. Los primeros modelos de ML buscaban una relación matemática directa entre variables.

### Regresión Lineal: La base de la predicción
Es el modelo más sencillo: intentar ajustar una línea recta a un conjunto de puntos. 
*   **Concepto:** $y = wx + b$. Aquí aprendimos los conceptos de **Pesos (Weights)** y **Sesgo (Bias)**. 
*   **Aprendizaje:** El modelo "aprende" ajustando esos pesos para minimizar el error (Función de Pérdida). Todo lo que vemos hoy en IA, incluidos los LLMs, sigue basándose en este principio de optimizar pesos.

### Regresión Logística: El salto a la clasificación
A pesar de su nombre, es un modelo de clasificación. Introdujo la **Función Sigmoide**, que comprime cualquier número en un rango entre 0 y 1 (probabilidad). Fue la primera vez que las máquinas pudieron decidir de forma probabilística: "¿Es este correo spam: Sí (1) o No (0)?".

---

## 2. La Era de los Árboles y el Aprendizaje No Lineal
El mundo real rara vez es una línea recta. Para manejar datos más complejos y relaciones no lineales, surgieron los modelos basados en decisiones.

### Árboles de Decisión
Modelos que dividen los datos en función de preguntas (ej. "¿Es el ingreso > 30.000€?"). Son muy interpretables pero tienden al **Overfitting** (memorizan los datos de entrenamiento pero fallan con datos nuevos).

### Bosques Aleatorios (Random Forest) y Gradient Boosting (XGBoost)
Aquí entramos en el concepto de **Ensemble Learning** (Aprendizaje por Conjunto). 
*   **Random Forest:** En lugar de un árbol, usamos cientos y promediamos su decisión ("La sabiduría de la multitud").
*   **Gradient Boosting:** Los árboles aprenden secuencialmente, donde cada nuevo árbol intenta corregir los errores del anterior. 
*   **Importancia:** Hasta el día de hoy, para datos tabulares (Excel, bases de datos estructuradas), estos modelos suelen superar a las redes neuronales.

---

## 3. El Renacimiento de las Redes Neuronales
Inspiradas vagamente en la biología, las redes neuronales intentan aproximar cualquier función matemática, por compleja que sea.

### El Perceptrón y el MLP (Multi-Layer Perceptron)
Una red neuronal es, simplificando mucho, una pila de regresiones logísticas. 
*   **Capas Ocultas:** Permiten al modelo encontrar "características" que los humanos no vemos a simple vista.
*   **Backpropagation (Retropropagación):** El algoritmo que permite a la red entender qué neuronas se equivocaron y ajustar sus pesos hacia atrás. Es el motor de toda la IA moderna.

---

## 4. Deep Learning: La Extracción Automática de Características
La gran diferencia entre el ML "clásico" y el Deep Learning (Aprendizaje Profundo) es quién diseña las características.
*   **En ML Clásico:** Un humano decide que para predecir el precio de una casa, lo importante es el número de habitaciones y el código postal.
*   **En Deep Learning:** Le damos al modelo los datos brutos (píxeles de una imagen, ondas de audio) y el modelo, a través de sus múltiples capas, descubre por sí solo qué es importante (bordes, texturas, formas, conceptos).

### Modelos Especializados:
*   **CNN (Redes Convolucionales):** Revolucionaron la visión artificial al imitar cómo el ojo procesa imágenes por regiones.
*   **RNN (Redes Recurrentes):** Diseñadas para secuencias (tiempo, audio, texto), introdujeron la noción de "estado" o memoria.

---

## 5. El Límite del ML Tradicional y el Salto al NLP Moderno
A pesar de su potencia, estos modelos tenían un problema: la **escalabilidad** y la **generalización**. Un modelo entrenado para detectar perros no servía para nada más. 

Los modelos de ML actuales han evolucionado hacia el **Aprendizaje Auto-supervisado**, donde el modelo no necesita que un humano le diga qué es cada cosa, sino que aprende la estructura del mundo (o del lenguaje) simplemente observando cantidades ingentes de datos.

Este es el puente que nos lleva a los LLMs: hemos pasado de modelos que resuelven una tarea específica a modelos que aprenden una **representación universal del conocimiento**.

---
*Con esta base técnica, ahora podemos entender por qué el lenguaje, al ser la forma más compleja de datos secuenciales, requirió una arquitectura totalmente nueva: el Transformer.*