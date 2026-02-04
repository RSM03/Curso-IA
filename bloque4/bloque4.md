**PRÁCTICA BLOQUE 4 · Tools, Function Calling y control explícito**

1. Objetivo del bloque 4

Transformar el sistema de “modelo que responde con contexto” en “modelo que decide qué información necesita y cómo obtenerla”.

Al finalizar el bloque, los alumnos deben demostrar:

* Que el modelo elige conscientemente qué PDF consultar
* Que reconoce cuándo no tiene información suficiente
* Que no inventa convenios ni artículos
* Que toda respuesta pasa por herramientas controladas
* Que las salidas son validables y seguras

Este bloque no mejora el modelo, mejora el sistema.

2. Concepto operativo de tools y function calling

Una tool es una función externa, determinista, auditable, que ejecuta acciones que el modelo no puede ni debe hacer por sí solo.

Principio clave: El LLM no ejecuta lógica, solo elige.

3. Tool 1 · Selección de convenio (PDF routing)

Se buscan resolver los siguientes problemas del modelo:

* No distingue bien entre convenios
* Recupera chunks semánticamente cercanos pero conceptualmente incorrectos
* Mezcla fuentes

Para ello haremos una tool decide qué PDF es el más adecuado

4. Preparación · Descripción controlada de convenios

Creamos **description.json**, un fichero determinista, auditable y cerrado, que el modelo solo puede leer, no modificar.

5. Definición conceptual de la tool

Nombre: select_convenio_pdf
Responsabilidad única:
Dada una pregunta, decidir qué PDF es relevante o declarar que ninguno aplica.

Principios de seguridad:

* Output estructurado
* Dominio cerrado
* Decisión explícita
* Posibilidad de “no sé”
