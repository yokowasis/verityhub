#!/bin/sh
ollama serve &  # Start Ollama in the background
fastapi run main.py --port 3000 --proxy-headers --workers 4  # Start FastAPI
