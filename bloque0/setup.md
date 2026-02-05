## SETUP ENTORNO

Requisitos previos del sistema

Sistema base recomendado:
* Linux (Ubuntu 20.04 o superior ideal)
* Python 3.10 o 3.11
* GPU opcional pero recomendable (si no, se ajustan modelos pequeños)

Comprobaciones iniciales:

```bash

python3 --version

nvidia-smi

```

Si no hay GPU, no pasa nada, pero usaremos modelos más pequeños o inferencia CPU lenta.

Creación del entorno de trabajo

Creamos un entorno aislado y limpio. Esto es importante porque luego se añadirá entrenamiento y librerías pesadas.

Token hugging face

1. Ve a Hugging Face

2. Entra en tu cuenta → Settings → Access Tokens → New token.

3. Copia el token (tipo “Write” si quieres subir modelos, “Read” basta para descargar).

hf_login.py

```python

from huggingface_hub import login

# Pega tu token aquí

token = "hf_XXXXXXXXXXXXXXXXXXXX"

login(token=token)

```

```bash

sudo apt install python3-venv

mkdir nlp-curso

cd nlp-curso

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip setuptools wheel

pip install torch transformers accelerate datasets

pip install jupyter matplotlib pandas python-dotenv

# SFT y LoRA
pip install peft datasets evaluate

# QLoRA y 4-bit
pip install bitsandbytes

# PDF y embeddings
pip install pypdf sentence-transformers faiss-cpu

# Deploy API
pip install fastapi python-multipart uvicorn


```

Si hay GPU con CUDA compatible, torch suele detectarla solo. Para comprobarlo:

```bash

python - << EOF

import torch

print(torch.cuda.is_available())

EOF

```

PARA BORRAR UN MODELO, localizacion:

```bash
~/.cache/huggingface/hub/
```