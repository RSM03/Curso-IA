# PRÁCTICA BLOQUE 7 · Puesta en producción y Serving de Modelos

## 1. Objetivo del bloque 7

Hemos construido un sistema inteligente (Agente + RAG + LoRA), pero actualmente solo vive en scripts locales de ejecución única. El objetivo de este bloque es cerrar el ciclo de vida del software (MLOps) convirtiéndolo en un **servicio de producción**.

Al finalizar el bloque, los alumnos deben ser capaces de:
- Exponer el agente a través de una **API REST** profesional.
- Implementar **medidas de seguridad** básicas (API Keys).
- Gestionar la **configuración mediante variables de entorno**.
- **Contenerizar** la aplicación con Docker para asegurar la portabilidad.
- Establecer un sistema de **logs estructurados** para monitorización.

---

## 2. El stack de producción

Para este bloque utilizaremos:
- **FastAPI**: Framework moderno y de alto rendimiento para construir APIs con Python.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación.
- **Pydantic**: Para validación de datos y esquemas de entrada/salida.
- **Docker**: Para empaquetar el modelo, el código y las dependencias.

---

## 3. Diseño de la API (Contrato de Servicio)

Una API de producción no solo devuelve texto; debe ser predecible. Definiremos:
- `POST /v1/ask`: Punto de entrada principal para preguntas al agente.
- `GET /health`: Endpoint de control para sistemas de orquestación (Kubernetes/Docker).
- **Headers de Seguridad**: Uso de `X-API-KEY` para autorizar peticiones.

---

## 4. Gestión de Recursos y Concurrencia

En producción, cargar el modelo en cada petición es inviable. 
- El modelo y el índice FAISS se cargan **una sola vez** al arrancar el servidor (Singleton pattern).
- Se debe tener en cuenta la memoria VRAM disponible, ya que FastAPI puede recibir múltiples peticiones simultáneas.

---

## 5. Dockerización: "Funciona en mi máquina"

El mayor reto de los LLMs en producción son las dependencias de sistema (CUDA, drivers, librerías de C++ para FAISS). 
Crearemos un `Dockerfile` que:
1. Use una imagen base optimizada.
2. Instale las dependencias de Python.
3. Exponga el puerto del servidor.

---

## 6. Tareas de la práctica

### 6.1 Implementación del Servidor (`app.py`)
Crear un servidor que envuelva la clase `MultiAgent` del Bloque 5.

### 6.2 Configuración (`.env`)
Mover todas las rutas de archivos (`lora_model`, `rag_store`) y tokens a un archivo de configuración.

### 6.3 Cliente de Pruebas (`client_test.py`)
Simular un entorno real donde una aplicación externa consume nuestro servicio.

---

## 7. Entregables del bloque 7

Cada grupo debe entregar:
- Código de la API (`app.py`).
- `Dockerfile` funcional.
- Captura de pantalla de la documentación automática de la API (Swagger UI).
- Log de una sesión de producción donde se vea la trazabilidad de una consulta.

---

## 8. Criterio de éxito del bloque

El sistema se considera "listo para producción" si:
1. La API responde en menos de un tiempo razonable (dependiendo del hardware).
2. No se filtran errores internos de Python al cliente (manejo de excepciones).
3. El sistema es capaz de recuperarse o informar si el modelo no carga correctamente.
4. Existe una separación clara entre código, datos y configuración.