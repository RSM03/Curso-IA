import os
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from dotenv import load_dotenv

# Importamos la lógica del agente del bloque 5
from bloque5.bloque5 import MultiAgent

load_dotenv()

# =============================
# CONFIGURACIÓN Y SEGURIDAD
# =============================
API_KEY_CREDENTIAL = os.getenv("APP_API_KEY", "curso-nlp-2026-secret")

app = FastAPI(
    title="Asistente Experto en Convenios Colectivos",
    description="API de producción para consulta de normativa laboral mediante Agentes y RAG",
    version="1.0.0"
)

# Instancia global del agente (se carga una sola vez al iniciar)
# Nota: En un entorno real, esto se gestionaría con un lifespan event de FastAPI
print("Cargando Agente y Modelos en memoria...")
agent = MultiAgent()
print("Sistema listo para recibir peticiones.")

# =============================
# MODELOS DE DATOS (Pydantic)
# =============================
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    timestamp: str

# =============================
# DEPENDENCIAS
# =============================
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY_CREDENTIAL:
        raise HTTPException(status_code=403, detail="API Key inválida o ausente")
    return x_api_key

# =============================
# ENDPOINTS
# =============================

@app.get("/health")
def health_check():
    """Verifica si el servicio y el modelo están vivos."""
    return {"status": "healthy", "model": "gemma-2-9b-it-lora"}

@app.post("/v1/ask", response_model=QueryResponse)
async def ask_agent(request: QueryRequest, api_key: str = Depends(verify_api_key)):
    """
    Punto de entrada principal para realizar consultas al agente.
    """
    try:
        # Ejecutar la lógica del agente
        answer = agent.act(request.question)
        
        # Recuperar metadatos de la memoria del agente para la respuesta
        last_interaction = agent.memory[-1] if agent.memory else {}
        
        return QueryResponse(
            question=request.question,
            answer=answer,
            sources=last_interaction.get("pdfs", []),
            timestamp=last_interaction.get("timestamp", "N/A") # Podrías añadirlo en el agente
        )
    except Exception as e:
        print(f"ERROR EN PRODUCCIÓN: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno procesando la consulta")

# =============================
# EJECUCIÓN
# =============================
if __name__ == "__main__":
    # Ejecutar con: python bloque7/app.py
    uvicorn.run(app, host="0.0.0.0", port=8000)