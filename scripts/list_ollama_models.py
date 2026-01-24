#!/usr/bin/env python3
"""List models available on an Ollama HTTP server by probing common endpoints.
Usage: OLLAMA_URL=http://host:11434 python3 scripts/list_ollama_models.py [--test MODEL]
"""
import os
import requests
import json
import argparse

# Use only the authoritative endpoints: /v1/models for listing and /api/chat for chat
ENDPOINTS = [
    "/v1/models",
]

parser = argparse.ArgumentParser()
parser.add_argument('--test', '-t', help='Optional: test a model name (POST a simple chat to /api/chat)')
args = parser.parse_args()

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434')

print(f"Probing {OLLAMA_URL} for model listing endpoints...")
results = {}
for ep in ENDPOINTS:
    url = f"{OLLAMA_URL.rstrip('/')}{ep}"
    try:
        resp = requests.get(url, timeout=5)
        status = resp.status_code
        text = resp.text
        try:
            parsed = resp.json()
        except Exception:
            parsed = None
        results[ep] = {'url': url, 'status': status, 'json': parsed, 'text': text[:1000]}
        print(f"{ep} -> {status}")
    except Exception as e:
        results[ep] = {'url': url, 'error': str(e)}
        print(f"{ep} -> ERROR: {e}")

# Enhanced summary: print model ids when a V1-style response is found
print('\nSummary:')
for ep, info in results.items():
    if 'error' in info:
        print(f"{ep}: ERROR: {info['error']}")
    else:
        s = info['status']
        if info['json']:
            keys = list(info['json'].keys())
            print(f"{ep}: {s} (JSON) -> keys: {keys}")
            # If this looks like a v1 models list, print model ids
            data = info['json'].get('data')
            if isinstance(data, list):
                ids = [d.get('id') for d in data if isinstance(d, dict) and 'id' in d]
                if ids:
                    print(f"  -> models: {ids}")
        else:
            snippet = info['text'].strip().replace('\n',' ')[:200]
            print(f"{ep}: {s} -> snippet: {snippet}")

# If user asked to test a specific model, try sending a simple chat to /api/chat
if args.test:
    model = args.test
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': 'Teste: responda apenas com OK'}]
    }
    try:
        resp = requests.post(f"{OLLAMA_URL.rstrip('/')}/api/chat", json=payload, timeout=10)
        print('\nTest model POST to /api/chat')
        print('Status:', resp.status_code)
        try:
            j = resp.json()
            print('JSON keys:', list(j.keys()))
            # print a compact representation of likely text fields
            if 'choices' in j and j['choices']:
                print('choice snippet:', str(j['choices'][0])[:800])
            else:
                print('Body snippet:', str(j)[:1000])
        except Exception:
            print('Body:', resp.text[:2000])
    except Exception as e:
        print('Model test error:', e)

print('\nIf you know model names (e.g. qwen3, gemma3:12b), test them with:')
print('  OLLAMA_URL=http://host:11434 python3 scripts/list_ollama_models.py --test qwen3')
print('  OLLAMA_URL=http://host:11434 python3 scripts/list_ollama_models.py --test "gemma3:12b"')
