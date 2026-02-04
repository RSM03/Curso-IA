from huggingface_hub import login
from dotenv import load_dotenv
import os

load_dotenv()

# Acceder a la variable
token = os.getenv("HF")

login(token=token)