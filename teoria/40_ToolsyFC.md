Este es el desarrollo extenso del **Bloque 4: Tools, Function Calling y Control del Modelo**. En este punto del curso, los alumnos dejan de ver al LLM como una "enciclopedia" y empiezan a verlo como el **sistema operativo** de una aplicación compleja.

---

# Bloque 4: Tools, Function Calling y Control del Modelo

## 4.1. Más allá de la generación: El LLM como Orquestador

Hasta ahora, hemos tratado al modelo como un sistema que recibe texto y genera texto. Sin embargo, en un entorno profesional, esto no es suficiente. Necesitamos que el modelo interactúe con el mundo real o con bases de datos estructuradas de forma precisa. Aquí es donde entra el concepto de **Tools (Herramientas)** y **Function Calling (Llamada a funciones)**.

### 4.1.1. ¿Qué es una Tool?
Una herramienta es cualquier pieza de código externa (una búsqueda en Google, una consulta SQL, un script de Python o un router de archivos) que el modelo puede decidir invocar para obtener información que no tiene en su memoria paramétrica ni en su contexto inmediato.

### 4.1.2. El cambio de paradigma: De "Saber" a "Decidir"
El objetivo del Bloque 4 es que el modelo deje de intentar responder a todo. En su lugar, el modelo debe:
1.  **Analizar la intención** del usuario.
2.  **Evaluar si tiene la información** necesaria.
3.  **Seleccionar la herramienta** adecuada si le falta información.
4.  **Formatear la petición** para esa herramienta de forma técnica y exacta.

## 4.2. Mecánica del Function Calling

El *Function Calling* no significa que el modelo ejecute el código. El modelo es una red neuronal, no un intérprete de Python. 

**El proceso técnico es el siguiente:**
1.  **Definición:** Proporcionamos al modelo una descripción textual de las funciones disponibles (nombre, parámetros, qué hace).
2.  **Detección:** El modelo analiza el prompt y, si decide que necesita una función, genera un texto con un formato específico (generalmente JSON o etiquetas XML).
3.  **Intercepción:** Nuestro código (el "wrapper") detecta ese formato, detiene la generación del modelo, ejecuta la función real en el servidor y obtiene el resultado.
4.  **Inyección:** El resultado de la función se le devuelve al modelo como si fuera una nueva entrada de "sistema" o "contexto".
5.  **Respuesta Final:** El modelo lee el resultado de la herramienta y ahora sí, genera la respuesta para el usuario.

## 4.3. Diseño de Herramientas Seguras y Deterministas

Uno de los mayores riesgos de los LLMs es que "alucinen" parámetros para las funciones (ej. inventar un nombre de archivo que no existe). Por ello, el diseño de herramientas debe seguir principios de ingeniería de software:

### 4.3.1. El Router de Convenios (PDF Routing)
En nuestro caso práctico, hemos implementado un **Router**. En lugar de buscar en todos los PDFs a la vez (lo que genera ruido y mezcla conceptos de distintos sectores), obligamos al modelo a usar una herramienta que decide qué PDF es el correcto.

*   **Uso de `description.json`:** Es fundamental tener un archivo de metadatos que describa cada fuente. Esto actúa como un "ancla de realidad" para el modelo.
*   **Dominios Cerrados:** La herramienta no debe permitir cualquier entrada. Si el modelo pide un convenio que no está en nuestra lista, el sistema debe devolver un error o un valor `NONE`.

### 4.3.2. Salidas Estructuradas y Validación por Regex
Dado que los modelos a veces añaden texto innecesario ("Aquí tienes el JSON que me pediste..."), es vital implementar capas de validación:
*   **Regex (Expresiones Regulares):** Para extraer exactamente el nombre del archivo o el comando de la salida del modelo.
*   **Validación de Esquema:** Asegurarse de que si el modelo debe devolver un JSON, este sea válido y contenga los campos requeridos.

## 4.4. Detección de Ignorancia: El "No sé" como Victoria

En NLP académico y profesional, **una respuesta errónea es mucho peor que ninguna respuesta**. El control del modelo implica entrenarlo (vía SFT o Prompting) para reconocer sus límites.

### 4.4.1. Criterios de Abstención
Debemos definir reglas explícitas en el *System Prompt* para que el modelo elija la opción `NONE` o "No lo sé":
*   Cuando la pregunta es ambigua.
*   Cuando la pregunta trata sobre un sector no cubierto por los documentos.
*   Cuando hay una contradicción evidente en los datos.

### 4.4.2. Reducción de la Sobreconfianza
Los modelos modernos tienden a ser "complacientes" (intentan agradar al usuario). El uso de herramientas ayuda a mitigar esto porque separa el **razonamiento** de la **fuente de datos**. Si la herramienta de búsqueda no devuelve resultados, el modelo tiene una evidencia física de que no puede responder, lo que facilita que admita su ignorancia.

## 4.5. Guardrails y Seguridad del Sistema

Cuando permitimos que un modelo ejecute herramientas, abrimos la puerta a riesgos de seguridad, como la **Inyección de Prompts**.

*   **Validación de Argumentos:** Nunca debemos permitir que el modelo pase comandos directos al sistema operativo o a una base de datos sin una capa de limpieza intermedia.
*   **Principio de Mínimo Privilegio:** Las herramientas que el modelo puede "llamar" deben tener permisos de solo lectura y estar limitadas a un entorno controlado (sandbox).
*   **Human-in-the-loop:** En sistemas críticos, el modelo propone la llamada a la función, pero un humano (o un sistema de reglas rígidas) debe autorizarla antes de la ejecución.

## 4.6. Integración de Tools en el Pipeline RAG

El Bloque 4 mejora el RAG del Bloque 3 de la siguiente manera:
1.  **RAG Simple:** Pregunta -> Búsqueda Vectorial Global -> Respuesta.
2.  **RAG con Tools:** Pregunta -> **Tool de Clasificación** (¿A qué convenio se refiere?) -> Búsqueda Vectorial **Filtrada** (Solo en ese PDF) -> Respuesta.

Esta especialización reduce drásticamente las alucinaciones cruzadas (mezclar el salario de hostelería con las vacaciones del metal) y mejora la precisión de la recuperación semántica.

---

### Dinámica de grupo sugerida:
1.  **Análisis de Fallos de Tool Calling:** Mostrar ejemplos donde el modelo intenta llamar a una función que no existe o con parámetros mal formados. Discutir cómo mejorar el prompt de descripción de la herramienta.
2.  **El Juego del Router:** Dar a los alumnos una lista de 20 convenios y 5 preguntas ambiguas. Pedirles que escriban el "contrato" (la descripción) que le darían al modelo para que no se equivoque al elegir el PDF.
3.  **Implementación de un Guardrail:** Crear una función de validación que bloquee la respuesta del modelo si este intenta mencionar un convenio que no está en el `description.json`.

---

### Notas para el instructor:
Este bloque es el que separa a un "entusiasta de los prompts" de un "ingeniero de IA". Es crucial que los alumnos entiendan que **el modelo es propenso al error** y que nuestra labor es rodearlo de mecanismos de control (herramientas deterministas y validaciones de código) que actúen como "red de seguridad". La clave aquí es la **trazabilidad**: siempre debemos saber por qué el modelo eligió una herramienta y qué resultado obtuvo de ella.