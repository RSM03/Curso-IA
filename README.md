# NOTAS CURSO IA

## MAIN

**Enfoque general del curso**

Curso 100 % orientado a NLP moderno con LLMs. Se trabaja siempre sobre un mismo caso práctico, por ejemplo un asistente experto sobre documentación técnica o normativa, que irá incorporando fine-tuning, RAG, tools, agentes, evaluación y despliegue.

Formato recomendado: 30 horas divididas en 10 sesiones de 3 horas, combinando teoría corta y práctica guiada.

**Marco general de la práctica**

Caso base: construcción de un asistente experto académico que responde con rigor a partir de documentación especializada y es capaz de reconocer cuándo no sabe, buscar evidencia y justificar sus respuestas.

Restricciones intencionadas:
* Uso de un modelo open source mediano
* Recursos limitados para forzar entrenamiento eficiente
* Necesidad de trazabilidad y evaluación

Repositorio único que se va completando por bloques, con checkpoints claros y revisión técnica al final de cada uno.

**Bloque 1. Fundamentos y preparación del entorno (3 horas)**

Objetivo: que todos partan de una base común y tengan el entorno listo.

Contenidos:
* Repaso rápido de NLP clásico vs NLP con LLMs
* Arquitectura de los LLM modernos
* Tokens, contexto, embeddings, atención y limitaciones reales
* Alucinaciones y por qué ocurren
* Stack de trabajo: Python, Hugging Face, PyTorch, LangChain/LlamaIndex, vectores, APIs

**Práctica: Baseline controlado y diagnóstico**

Objetivo práctico: entender el comportamiento real del modelo antes de tocar nada.

Trabajo práctico:
* Cargar un modelo base y definir un prompt sistema estricto
* Diseñar un set de preguntas trampa y preguntas sin respuesta
* Medir alucinación, sobreconfianza y pérdida de contexto
* Documentar fallos observados y límites del modelo

Entrega del bloque:
* Notebook o script con pruebas reproducibles
* Informe breve de diagnóstico técnico

**Bloque 2. Fine-tuning y entrenamiento eficiente (6 horas)**

Objetivo: entender y aplicar SFT sin infraestructuras prohibitivas.

Contenidos:
* Qué es SFT y cuándo tiene sentido
* Preparación de datasets de entrenamiento NLP
* LoRA y QLoRA: conceptos y ventajas
* Ajuste de hiperparámetros clave
* Evaluación básica post-entrenamiento

**Práctica: Fine-tuning con SFT + LoRA**

Objetivo práctico: modificar el comportamiento del modelo, no su conocimiento.

Trabajo práctico:
* Diseño de un dataset de instrucciones de alta calidad
* Justificación del formato y balance del dataset
* Entrenamiento SFT con LoRA o QLoRA
* Comparación cuantitativa y cualitativa con el baseline
* Control de overfitting y degradación

Entrega del bloque:
* Modelo entrenado versionado
* Métricas comparativas
* Decisiones técnicas documentadas

**Bloque 3. Sistemas RAG bien diseñados (6 horas)**

Objetivo: reducir alucinaciones y ampliar conocimiento.

Contenidos:
* Arquitectura RAG de extremo a extremo
* Chunking, embeddings y bases vectoriales
* Recuperación semántica vs híbrida
* Prompting para RAG efectivo
* Errores comunes en RAG

**Práctica: RAG serio, no decorativo**

Objetivo práctico: añadir conocimiento externo fiable.

Trabajo práctico:
* Selección y preparación del corpus documental
* Decisiones de chunking y embeddings
* Construcción del índice vectorial
* Diseño del prompt RAG con citación
* Análisis de casos donde RAG empeora la respuesta

Entrega del bloque:
* Pipeline RAG completo
* Evaluación con y sin recuperación
* Registro de errores y ajustes

**Bloque 4. Tools, function calling y control del modelo (6 horas)**

Objetivo: que el modelo deje de “inventar” y sepa cuándo pedir ayuda.

Contenidos:
* Concepto de tools y function calling
* Detección de falta de conocimiento
* Diseño de herramientas seguras
* Integración con búsquedas, scripts y APIs
* Guardrails y validaciones de salida

**Práctica: Tools y detección de ignorancia**

Objetivo práctico: eliminar respuestas inventadas.

Trabajo práctico:
* Definir criterios explícitos de “no sé”
* Implementar function calling para búsquedas o scripts
* Forzar al modelo a elegir entre responder o usar una tool
* Validación estructurada de salidas

Entrega del bloque:
* Conjunto de tools funcionales
* Tests donde el modelo decide no responder
* Evidencia de reducción de alucinaciones

**Bloque 5. Agentes NLP y orquestación (4 horas)**

Objetivo: pasar de un chatbot a un sistema autónomo controlado.

Contenidos:
* Qué es un agente y cuándo usarlo
* Planificación, memoria y control
* Patrones de agentes
* Riesgos y límites de los agentes

**Práctica: Agente controlado**

Objetivo práctico: orquestar razonamiento sin perder control.

Trabajo práctico:
* Definir estados, memoria y límites del agente
* Separar planificación y ejecución
* Integrar RAG y tools en el loop del agente
* Manejo de errores y timeouts

Entrega del bloque:
* Agente funcional con logs
* Análisis de comportamiento paso a paso

**Bloque 6. Evaluación avanzada y métricas (3 horas)**

Objetivo: medir calidad y fiabilidad de forma objetiva.

Contenidos:
* Evaluación clásica vs evaluación con LLMs
* LLM-as-a-judge
* Métricas de RAG
* Detección de alucinaciones
* Logging y trazabilidad

**Práctica: Evaluación avanzada**

Objetivo práctico: medir calidad de forma defendible.

Trabajo práctico:
* Construcción de un benchmark propio
* Uso de LLM-as-a-judge con criterios explícitos
* Métricas específicas de RAG y tools
* Comparativa de versiones del sistema

Entrega del bloque:
* Pipeline de evaluación automatizado
* Resultados interpretados críticamente

**Bloque 7. Puesta en producción (2 horas)**

Objetivo: dejar el sistema listo para uso real.

Contenidos:
* Arquitectura de despliegue
* APIs y serving de modelos
* Gestión de versiones
* Seguridad y costes
* Monitorización en producción

**Práctica: Preparación para producción**

Objetivo práctico: cerrar el ciclo de vida.

Trabajo práctico:
* Exposición del sistema como API
* Gestión de configuración y versiones
* Logging, métricas y monitorización básica
* Análisis de costes y escalabilidad

Entrega final:
* Sistema desplegable
* Documento técnico completo del proyectos