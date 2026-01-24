# Listando modelos no Ollama

Este arquivo mostra como descobrir quais modelos estão disponíveis em uma instância Ollama via HTTP.

1) Use o script `scripts/list_ollama_models.py` (recomendado). Ele tenta vários endpoints comuns e exibe as respostas:

```bash
OLLAMA_URL=http://<HOST>:11434 python3 scripts/list_ollama_models.py
```

2) Se souber o modelo, teste diretamente com `--test`:

```bash
OLLAMA_URL=http://<HOST>:11434 python3 scripts/list_ollama_models.py --test qken3
OLLAMA_URL=http://<HOST>:11434 python3 scripts/list_ollama_models.py --test "gemma3:12b"
```

3) Exemplos de curl (substitua <HOST> e <MODEL>):

```bash
# Listar modelos (rota recomendada):
curl -s http://<HOST>:11434/v1/models | jq

# Testar um modelo via chat (rota correta):
curl -s -X POST "http://<HOST>:11434/api/chat" -H "Content-Type: application/json" \
  -d '{"model":"gemma3:12b","messages":[{"role":"user","content":"Teste: responda com OK"}]}' | jq
```

Observações:
- Nem toda instalação expõe `/api/models` ou `/models` — por isso o script tenta endpoints alternativos e mostra o conteúdo bruto quando não for JSON.
- No host de exemplo (http://192.168.156.225:11434) foram detectados os modelos: `default:latest`, `qwen3:latest`, `gemma3:12b`.

Exemplo de listagem com `jq` (quando o endpoint retorna JSON em `/v1/models`):

```bash
curl -s http://192.168.156.225:11434/v1/models | jq '.data[].id'
# -> "default:latest" "qwen3:latest" "gemma3:12b"
```

Exemplo rápido para testar `gemma3:12b`:

```bash
curl -s -X POST "http://192.168.156.225:11434/api/chat" -H "Content-Type: application/json" \
  -d '{"model":"gemma3:12b","messages":[{"role":"user","content":"Teste: responda com OK"}]}' | jq
```

Se quiser, eu posso ajustar `gpy.py` para automaticamente escolher um modelo disponível quando a configuração padrão falhar (ex.: usar `gemma3:12b` se `gpt-4o-mini` não existir).