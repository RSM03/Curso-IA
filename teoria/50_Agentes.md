Este es el desarrollo extenso del **Bloque 5: Agentes NLP y Orquestación**. En este punto del curso, los alumnos integran todo lo aprendido (SFT, RAG y Tools) para crear un sistema con capacidad de razonamiento autónomo y toma de decisiones multi-paso.

---

# Bloque 5: Agentes NLP y Orquestación

## 5.1. ¿Qué es realmente un Agente en el contexto de LLMs?

Hasta ahora, hemos construido sistemas **lineales** o **reactivos**: el usuario pregunta, el sistema busca y el sistema responde. Un **Agente** rompe esta linealidad. 

Un Agente es un sistema donde el LLM no solo genera texto, sino que actúa como un **motor de razonamiento** que utiliza un bucle de retroalimentación para resolver una tarea. El agente puede decidir que necesita ejecutar una herramienta, observar el resultado, y basándose en esa observación, decidir si necesita ejecutar otra herramienta o si ya tiene suficiente información para responder.

### 5.1.1. Diferencia entre Pipeline y Agente
*   **Pipeline (Flujo Rígido):** `Pregunta -> Clasificación -> RAG -> Respuesta`. Si la clasificación falla, todo el sistema falla.
*   **Agente (Flujo Dinámico):** `Pregunta -> ¿Qué herramientas necesito? -> [Ejecuta Tool A] -> ¿Es suficiente? -> No, necesito Tool B -> [Ejecuta Tool B] -> ¿Es suficiente? -> Sí -> Respuesta`.

## 5.2. Arquitecturas de Razonamiento

Para que un agente sea eficaz, debe seguir una metodología de "pensamiento". Las más importantes son:

### 5.2.1. Chain of Thought (CoT) - Cadena de Pensamiento
Consiste en forzar al modelo a generar pasos intermedios de razonamiento antes de dar la respuesta final. Se ha demostrado que esto reduce drásticamente los errores en tareas lógicas y matemáticas. En nuestro agente, el CoT se manifiesta cuando el modelo describe por qué elige ciertos convenios.

### 5.2.2. ReAct (Reasoning + Acting)
Es el estándar de oro para agentes. El modelo sigue un ciclo:
1.  **Thought (Pensamiento):** El modelo describe qué cree que está pasando y qué planea hacer.
2.  **Action (Acción):** El modelo elige una herramienta para ejecutar.
3.  **Observation (Observación):** El modelo recibe el resultado de la herramienta.
4.  **Repetición:** El modelo vuelve al paso 1 hasta que considera que la tarea está terminada.

### 5.2.3. Plan-and-Execute
En tareas muy complejas, el agente primero crea un plan completo de todos los pasos necesarios y luego los ejecuta uno a uno. Esto evita que el agente "se pierda" en mitad de un razonamiento largo.

## 5.3. Componentes Críticos del Agente del Curso

En nuestra práctica, el agente debe gestionar la complejidad de la normativa laboral. Para ello, implementamos varios componentes de orquestación:

### 5.3.1. Selección Multi-Fuente (Multi-PDF Routing)
A diferencia del Bloque 4, donde elegíamos un solo PDF, el agente ahora debe ser capaz de identificar si una pregunta requiere **comparar** varios documentos (ej. "¿Qué diferencia hay entre el salario del metal y el de hostelería?").
*   El agente debe generar una lista de herramientas a invocar.
*   Debe gestionar la agregación de esos resultados.

### 5.3.2. Evaluación de Suficiencia del Contexto
Un agente inteligente sabe cuándo **no tiene suficiente información**. 
*   Implementamos una lógica que mide la calidad y cantidad del contexto recuperado.
*   Si el contexto es pobre (ej. menos de 50 caracteres útiles o chunks irrelevantes), el agente debe abortar la generación para evitar la alucinación.

### 5.3.3. Memoria y Estado
El agente debe mantener un registro de lo que ha hecho.
*   **Memoria de corto plazo:** Los resultados de las herramientas ejecutadas en el turno actual.
*   **Trazabilidad:** Un log detallado que permita a un auditor humano entender por qué el agente tomó cada decisión.

## 5.4. El Bucle de Control y el Manejo de Errores

Un agente sin control es peligroso. En producción, debemos implementar salvaguardas:

1.  **Límite de Iteraciones (Max Iterations):** Evitar que el agente entre en un bucle infinito si no encuentra la respuesta (ej. intentar buscar una y otra vez en el mismo PDF infructuosamente).
2.  **Validación de Salida (Output Validation):** Antes de mostrar la respuesta al usuario, el agente (o un script de validación) comprueba si la respuesta contiene frases prohibidas o indica falta de conocimiento a pesar de haber generado un texto largo.
3.  **Fallback Estratégico:** Si el agente no logra determinar qué convenio usar, implementamos un "paso atrás" (fallback) donde el sistema intenta una búsqueda general en todos los documentos como último recurso.

## 5.5. Razonamiento Multi-fuente y Síntesis

El mayor reto de un agente NLP es la **síntesis**. Cuando el agente recupera información de tres convenios diferentes, no debe simplemente "pegar" los textos.
*   Debe identificar contradicciones.
*   Debe estructurar la respuesta de forma comparativa si el usuario lo pidió.
*   Debe mantener la atribución (citar qué parte viene de qué PDF) de forma clara y coherente.

## 5.6. Ética y Responsabilidad del Agente

Al dar "autonomía" a un modelo para decidir qué herramientas usar, entramos en el terreno de la responsabilidad técnica:
*   **Transparencia:** El usuario siempre debe saber que está interactuando con un agente que está tomando decisiones de búsqueda.
*   **Auditoría:** Los logs que generamos en la práctica no son solo para depurar; son el registro legal de cómo el sistema llegó a una conclusión normativa.
*   **Abstención:** En el ámbito académico y legal, **la abstención es una respuesta válida y a menudo la más correcta**. El agente debe estar orgulloso de decir "No puedo encontrar evidencia suficiente en los convenios proporcionados".

---

### Dinámica de grupo sugerida:
1.  **Simulación de "Agente Humano":** Un alumno hace de "LLM" y otro de "Sistema de Tools". El alumno LLM debe escribir en un papel qué herramienta quiere usar para responder a una pregunta compleja. El alumno Tool le da la información. Repetir hasta que el LLM tenga la respuesta. Esto ayuda a visualizar el ciclo ReAct.
2.  **Análisis de Logs de Errores:** Revisar un log donde el agente haya entrado en un bucle o haya elegido convenios incorrectos. ¿Fue un problema del prompt del sistema o de la descripción de los convenios?
3.  **Diseño de la "Métrica de Suficiencia":** Debatir qué hace que un contexto sea "suficiente". ¿Es el número de palabras? ¿Es la presencia de palabras clave? ¿Es la puntuación de similitud del vector?

---

### Notas para el instructor:
Este bloque es el clímax técnico del curso. Es fundamental que los alumnos entiendan que el código del agente (`MultiAgent` en la práctica) es el que orquesta a los modelos entrenados en el Bloque 2 y al RAG del Bloque 3. La clave aquí es la **robustez**: un buen agente no es el que siempre responde, sino el que siempre **razona correctamente** sobre si puede o no responder. Se debe hacer mucho hincapié en la lectura de los archivos de log generados (`agent_log_b5.txt`).