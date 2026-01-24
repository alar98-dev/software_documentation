#!/usr/bin/env python3
import os
import requests
import json

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434')
MODEL = os.getenv('OLLAMA_MODEL', 'gpt-4o-mini')

payload = {
    'model': MODEL,
    'messages': [
        {'role': 'user', 'content': 'Teste de integração: responda apenas OLLAMA_OK'}
    ]
}

print(f'Testando {OLLAMA_URL}/api/chat com modelo {MODEL}...')
try:
    resp = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=10)
    print('Status:', resp.status_code)
    print('Resposta (primeiros 1000 caracteres):')
    print(resp.text[:1000])
except Exception as e:
    print('Falha ao conectar:', e)
    print('\nDica: verifique se o Ollama está rodando localmente e se a variável OLLAMA_URL aponta para o endereço correto.')
