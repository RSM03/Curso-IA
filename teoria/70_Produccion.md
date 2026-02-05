Este es el desarrollo extenso del **Bloque 7: Puesta en Producción y Serving de Modelos**. Este bloque representa el paso final: transformar un experimento de inteligencia artificial en un **producto de software robusto, escalable y seguro**.

---

# Bloque 7: Puesta en Producción y Serving de Modelos (MLOps)

## 7.1. El Abismo entre el Notebook y la Producción

Muchos proyectos de IA mueren en la fase de prototipo porque no se tiene en cuenta que el entorno de producción es radicalmente distinto al de desarrollo. En un script local, controlamos todo; en producción, nos enfrentamos a:
*   **Concurrencia:** Múltiples usuarios preguntando al mismo tiempo.
*   **Latencia:** El usuario no puede esperar 30 segundos por una respuesta.
*   **Disponibilidad:** El sistema debe estar levantado 24/7.
*   **Seguridad:** No podemos permitir que cualquiera acceda a nuestro modelo o que nos inyecten código malicioso.

## 7.2. Arquitectura de una API de Deep Learning

Para exponer nuestro agente, utilizamos **FastAPI**, el estándar de la industria para servicios de ML en Python.

### 7.2.1. Por qué FastAPI
*   **Asincronía (async/await):** Permite manejar múltiples peticiones sin bloquear el servidor mientras el modelo está "pensando".
*   **Validación con Pydantic:** Obliga a que los datos de entrada y salida cumplan un contrato estricto, evitando errores de tipo.
*   **Documentación Automática:** Genera una interfaz (Swagger UI) para probar la API sin escribir una sola línea de código de cliente.

### 7.2.2. Gestión del Ciclo de Vida (Lifespan)
Cargar un modelo de 9B de parámetros y un índice FAISS tarda varios segundos y consume gigabytes de VRAM. 
*   **Singleton Pattern:** El modelo debe cargarse **una sola vez** al iniciar el servidor.
*   **Warm-up:** A veces es necesario realizar una inferencia "de prueba" al arrancar para inicializar los pesos en la GPU y evitar que el primer usuario sufra una latencia extra.

## 7.3. Gestión de Recursos y VRAM

El mayor cuello de botella en la producción de LLMs es la **Memoria de Video (VRAM)**.

### 7.3.1. Cuantización para Producción
Aunque hemos entrenado con QLoRA, en producción podemos usar formatos aún más optimizados:
*   **GGUF / AWQ / GPTQ:** Técnicas que permiten ejecutar modelos con una pérdida de precisión mínima pero reduciendo el uso de memoria a la mitad o menos.
*   **KV Caching:** Técnica que almacena las claves y valores de la atención de tokens anteriores para acelerar la generación de los siguientes.

### 7.3.2. Batching y Concurrencia
Si dos personas preguntan a la vez, ¿qué hacemos?
*   **Sequential Processing:** Una petición espera a que termine la otra (lento).
*   **Continuous Batching:** Los motores de inferencia modernos (como vLLM o TGI) agrupan peticiones dinámicamente para procesarlas en un solo paso de la GPU, multiplicando el rendimiento.

## 7.4. Contenerización con Docker

"En mi máquina funciona" no es una respuesta válida en producción. **Docker** nos permite empaquetar el código, las librerías (PyTorch, Transformers), los drivers de NVIDIA y el modelo en una imagen ligera y portable.

### 7.4.1. El reto de la GPU en Docker
Para que Docker use la tarjeta gráfica, necesitamos el **NVIDIA Container Toolkit**. La imagen base debe ser compatible con la versión de CUDA instalada en el servidor físico.

### 7.4.2. Capas de la imagen
Una buena imagen de Docker para NLP debe estar optimizada:
1.  Base con Python y CUDA.
2.  Instalación de dependencias (requirements.txt).
3.  Copia del código del agente y los adaptadores LoRA.
4.  Exposición del puerto (ej. 8000).

## 7.5. Seguridad y Control de Acceso

Un modelo de IA es un activo costoso. Debemos protegerlo:
*   **API Keys:** Un sistema sencillo pero eficaz para que solo aplicaciones autorizadas consuman el modelo.
*   **Rate Limiting:** Limitar cuántas preguntas puede hacer un usuario por minuto para evitar costes excesivos o ataques de denegación de servicio (DoS).
*   **CORS (Cross-Origin Resource Sharing):** Configurar qué dominios web pueden llamar a nuestra API.

## 7.6. Monitorización y Observabilidad

Una vez el modelo está fuera, necesitamos saber qué está pasando.

### 7.6.1. Logs Estructurados
No basta con imprimir texto. Necesitamos logs en formato JSON que registren:
*   Tiempo de respuesta (latencia).
*   Tokens generados por segundo.
*   Uso de VRAM.
*   **Feedback del usuario:** Si el usuario marca la respuesta como "mala", debemos guardar esa interacción para el re-entrenamiento futuro.

### 7.6.2. Health Checks
Endpoints como `/health` permiten que sistemas como Kubernetes sepan si el modelo sigue vivo o si se ha quedado sin memoria (OOM - Out of Memory) y necesita ser reiniciado.

## 7.7. El Ciclo de Mejora Continua (Flywheel)

La producción no es el final, es el principio de un ciclo:
1.  **Producción:** El modelo responde a usuarios reales.
2.  **Monitorización:** Detectamos casos donde el modelo duda o falla.
3.  **Curación:** Etiquetamos esos fallos manualmente.
4.  **Fine-tuning:** Re-entrenamos el modelo (Bloque 2) con esos nuevos datos.
5.  **Evaluación:** Pasamos el benchmark (Bloque 6) para asegurar que no hay regresiones.
6.  **Despliegue:** Actualizamos la API.

---

### Dinámica de grupo sugerida:
1.  **Simulacro de Carga:** Usar una herramienta sencilla (como `ab` o `locust`) para lanzar 10 peticiones simultáneas a la API y observar cómo sufre la latencia y la VRAM.
2.  **Swagger Exploration:** Navegar por la documentación automática de FastAPI y realizar pruebas de "preguntas prohibidas" para ver si los guardrails de seguridad funcionan.
3.  **Docker Debugging:** Intentar construir una imagen de Docker pequeña y discutir por qué las imágenes de IA suelen pesar varios Gigabytes (y cómo gestionarlo).

---

### Notas para el instructor:
Este bloque cierra el círculo. Es fundamental que los alumnos vean que todo el esfuerzo de los bloques anteriores (el entrenamiento preciso, el RAG complejo, el agente inteligente) solo tiene valor si llega al usuario de forma estable. Se debe enfatizar la importancia de las **variables de entorno** (`.env`) para no subir nunca tokens de Hugging Face o API Keys al repositorio de código (GitHub). Al finalizar, el alumno no solo sabrá de IA, sino que tendrá nociones sólidas de **Arquitectura de Software** aplicada a modelos de lenguaje.