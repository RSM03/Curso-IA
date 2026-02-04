# PRÁCTICA BLOQUE 5 · Agentes NLP controlados y razonamiento multi-fuente

## 1. Objetivo del bloque 5

En los bloques anteriores hemos construido un sistema **correcto pero reactivo**:

- El modelo responde cuando se le pregunta  
- Usa RAG con fuentes controladas  
- Ejecuta tools de forma explícita  
- Evita alucinaciones simples  

Sin embargo, el sistema **no razona sobre el proceso completo**.

El objetivo del bloque 5 es transformar el pipeline en un **agente controlado**, capaz de:

- Decidir qué acciones ejecutar y en qué orden  
- Integrar información de múltiples convenios  
- Evaluar si el contexto es suficiente antes de responder  
- Abstenerse de responder cuando no hay base sólida  
- Dejar trazabilidad completa de cada decisión  

El resultado no es un chatbot, sino un **sistema deliberativo auditado**.

---

## 2. Qué problema técnico resuelve un agente (y cuál no)

Un agente **no sirve para “pensar mejor”**, sirve para:

- Orquestar decisiones explícitas
- Encadenar tools de forma controlada
- Separar planificación de ejecución
- Imponer límites al modelo

Errores que un agente **sí puede resolver**:
- Preguntas que requieren consultar varios convenios
- Comparaciones entre fuentes
- Necesidad de buscar más información antes de responder
- Detección de contexto insuficiente

Errores que **no resuelve**:
- PDFs mal ingestados
- Chunking deficiente
- Documentos incompletos
- Preguntas mal planteadas

---

## 3. Arquitectura conceptual del agente del bloque 5

El agente que vais a construir sigue este patrón:

1. Recepción de la pregunta
2. Decisión de qué convenios son relevantes
3. Recuperación de contexto por convenio
4. Evaluación de suficiencia del contexto
5. Generación de respuesta o abstención
6. Validación final
7. Registro completo del proceso

Principio clave del bloque:

> **El modelo no decide el resultado, decide los pasos.**

---

## 4. Diseño de tools obligatorias

Antes de escribir código, debéis definir explícitamente las herramientas del agente.

### Tool 1 · Selección de convenios múltiples

Problema:
- Algunas preguntas afectan a más de un convenio
- Otras son ambiguas
- Otras no aplican a ninguno

Requisitos:
- Dominio cerrado (solo PDFs existentes)
- Posibilidad de devolver varios convenios
- Posibilidad explícita de NONE
- Output estructurado y validable

Pregunta clave:
- ¿Cuándo tiene sentido devolver más de un convenio?

---

### Tool 2 · Recuperación de contexto multi-convenio

Problema:
- El RAG simple mezcla fuentes sin control
- Un convenio puede dominar la respuesta

Requisitos:
- Recuperar contexto por cada convenio seleccionado
- Limitar número de chunks por fuente
- Mantener trazabilidad (PDF + página)

Pregunta clave:
- ¿Cómo equilibrar cantidad de contexto vs ruido?

---

### Tool 3 · Evaluación de suficiencia del contexto

Problema:
- El modelo responde incluso con contexto mínimo
- No distingue entre evidencia débil y sólida

Requisitos:
- Métrica explícita (longitud, número de chunks, diversidad)
- Decisión binaria: suficiente / insuficiente
- Capacidad de abortar la respuesta

Pregunta clave:
- ¿Qué significa “suficiente” en vuestro dominio?

---

### Tool 4 · Síntesis controlada del contexto

Problema:
- El modelo recibe contexto desordenado
- Mezcla fuentes sin saberlo

Requisitos:
- Contexto estructurado
- Fuentes visibles
- Preparado para auditoría

---

### Tool 5 · Validación final de la respuesta

Problema:
- El modelo puede contradecir reglas previas
- Puede usar lenguaje inseguro o evasivo

Requisitos:
- Reglas deterministas
- Posibilidad de invalidar la respuesta
- Fallback seguro

---

## 5. Memoria y trazabilidad del agente

El agente debe mantener:

- Historial de preguntas
- Convenios seleccionados
- Decisiones de abstención
- Respuestas finales

Además, **cada paso debe quedar registrado**.

No es logging decorativo:
- Sirve para auditar
- Sirve para evaluar
- Sirve para depurar errores del agente

Pregunta clave:
- ¿Podría un tercero reconstruir el razonamiento del sistema?

---

## 6. Reglas estrictas del agente

El agente **no puede**:
- Responder sin contexto suficiente
- Mezclar convenios sin declararlo
- Inferir información no presente
- Ocultar incertidumbre

El agente **debe**:
- Abstenerse cuando corresponda
- Justificar implícitamente sus decisiones
- Ser reproducible
- Ser auditable

---

## 7. Casos de prueba obligatorios

Cada grupo debe probar al menos:

- Pregunta que afecta a varios convenios
- Pregunta ambigua que debería usar fallback
- Pregunta imposible
- Pregunta válida con respuesta clara
- Pregunta válida con contexto insuficiente

Para cada caso:
- ¿Qué tools se ejecutaron?
- ¿Dónde se podría haber equivocado?
- ¿El agente fue conservador o arriesgado?

---

## 8. Entregables del bloque 5

Cada grupo debe entregar:

- Código del agente
- Logs completos de ejecución
- Resultados de pruebas
- Documento técnico breve explicando:
  - Decisiones de diseño
  - Límites conocidos
  - Errores no resueltos

---

## 9. Criterio de éxito del bloque

El bloque 5 se considera superado si:

- El sistema **prefiere abstenerse antes que inventar**
- Las decisiones son trazables
- El agente actúa como orquestador, no como generador
- Los errores son explicables, no misteriosos

Este bloque no busca respuestas brillantes, sino **sistemas fiables**.
