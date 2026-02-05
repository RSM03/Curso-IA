import requests

URL = "http://localhost:8000/v1/ask"
HEADERS = {
    "X-API-KEY": "curso-nlp-2026-secret",
    "Content-Type": "application/json"
}

def test_query(question):
    payload = {"question": question}
    try:
        response = requests.post(URL, json=payload, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            print(f"\nPREGUNTA: {data['question']}")
            print(f"RESPUESTA: {data['answer']}")
            print(f"FUENTES: {', '.join(data['sources'])}")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    print("--- TEST DE PRODUCCIÓN ---")
    test_query("¿Cuál es la jornada laboral en el convenio del metal?")