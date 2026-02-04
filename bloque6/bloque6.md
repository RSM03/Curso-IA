# PRÁCTICA BLOQUE 6 · Evaluación avanzada y auditable de sistemas NLP

## 1. Objetivo del bloque 6

Hasta ahora hemos construido un sistema que:
- Evita alucinaciones simples
- Usa RAG con fuentes controladas
- Decide mediante tools
- Razona como agente

Sin embargo, **no sabemos medirlo de forma objetiva**.

El objetivo del bloque 6 es diseñar un **sistema de evaluación reproducible**, capaz de responder con evidencias a preguntas como:
- ¿Este sistema es mejor que el anterior?
- ¿En qué falla exactamente?
- ¿Cuándo es demasiado conservador?
- ¿Cuándo responde sin base suficiente?

La evaluación no es un añadido: **es parte del sistema**.

---

## 2. Qué NO es evaluación en LLMs

Este bloque empieza eliminando malas prácticas:

- ❌ “Me parece que responde mejor”
- ❌ Comparar dos respuestas a ojo
- ❌ Probar solo casos fáciles
- ❌ Medir solo exactitud textual

Un sistema robusto debe evaluarse incluso cuando:
- Se abstiene
- Responde parcialmente
- Integra múltiples fuentes
- Decide no responder

---

## 3. Dimensiones de evaluación obligatorias

Cada respuesta debe evaluarse en varias dimensiones independientes.

### 3.1 Corrección factual
¿La información está soportada por el contexto recuperado?

### 3.2 Uso correcto de fuentes
¿La respuesta se basa en los convenios adecuados?
¿Mezcla fuentes sin justificar?

### 3.3 Gestión de incertidumbre
¿Se abstiene cuando debe?
¿Evita inventar?

### 3.4 Comportamiento del agente
¿Ejecuta las tools correctas?
¿Evita pasos innecesarios?
¿El flujo es razonable?

### 3.5 Conservadurismo vs utilidad
¿Es excesivamente prudente?
¿Responde cuando sí debería?

---

## 4. Dataset de evaluación

El bloque exige construir un **benchmark propio**, no reutilizar ejemplos de entrenamiento.

Cada ejemplo debe incluir:

- Pregunta
- Tipo de pregunta
- Convenios esperados
- ¿Debe responder o abstenerse?
- Notas humanas (opcional)

Ejemplo conceptual:

- Pregunta multi-convenio
- Pregunta imposible
- Pregunta ambigua
- Pregunta factual directa

---

## 5. LLM-as-a-Judge como herramienta, no como oráculo

Usaremos un LLM como juez **solo bajo reglas estrictas**:

- Prompt cerrado
- Criterios explícitos
- Salida estructurada
- Prohibido “opinar libremente”

El juez no decide si “le gusta” la respuesta, decide si **cumple criterios técnicos**.

---

## 6. Arquitectura del sistema de evaluación

Pipeline recomendado:

1. Ejecutar el agente sobre el dataset
2. Guardar:
   - Respuesta
   - Convenios usados
   - Logs del agente
3. Evaluar automáticamente:
   - Abstención correcta
   - Uso de fuentes
4. Evaluar con LLM-as-a-judge:
   - Corrección factual
   - Uso del contexto
5. Agregar métricas globales

---

## 7. Métricas mínimas exigidas

Cada grupo debe reportar:

- % de abstenciones correctas
- % de respuestas con soporte suficiente
- % de respuestas inválidas
- Diferencias entre versiones del sistema

La métrica más importante:
> **Tasa de invención = 0**

---

## 8. Entregables del bloque 6

Cada grupo debe entregar:

- Dataset de evaluación
- Código de evaluación automática
- Resultados agregados
- Documento técnico con interpretación crítica

---

## 9. Criterio de éxito del bloque

El bloque se considera superado si:
- El sistema puede compararse entre versiones
- Los errores son clasificables
- La evaluación es reproducible
- El juicio humano queda respaldado por métricas

Este bloque transforma el proyecto en un **sistema evaluable**, no solo funcional.
