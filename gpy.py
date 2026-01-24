import os
import json
import call_functions

# Backend selection: 'openai' or 'ollama'. If AI_BACKEND is not set, we prefer OpenAI when OPENAI_API_KEY is present; otherwise default to Ollama (local).
AI_BACKEND = os.getenv("AI_BACKEND", None)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-4o-mini")

if AI_BACKEND is None:
    if OPENAI_API_KEY:
        AI_BACKEND = "openai"
    else:
        AI_BACKEND = "ollama"

# Lazy imports depending on backend to avoid failing when optional packages are missing
openai = None
requests = None
if AI_BACKEND == "openai":
    try:
        import openai as _openai
        openai = _openai
    except Exception as e:
        raise RuntimeError("Backend set to OpenAI but 'openai' package is not installed. Install with 'pip install openai'.")

if AI_BACKEND == "ollama":
    try:
        import requests as _requests
        requests = _requests
    except Exception as e:
        raise RuntimeError("Backend set to Ollama but 'requests' package is not installed. Install with 'pip install requests'.")

# API key resolution for OpenAI: check file fallback like before
if AI_BACKEND == "openai":
    api_key = OPENAI_API_KEY
    if not api_key:
        if os.path.exists("./api_key.txt"):
            with open("./api_key.txt", 'r') as arq:
                api_key = arq.read().strip()
        elif os.path.exists("./api_key_config.txt"):
            with open("./api_key_config.txt", 'r') as arq:
                content = arq.read().strip()
                if not content.lower().startswith("renomear"):
                    api_key = content

    if not api_key:
        raise RuntimeError(
            "API key not found for OpenAI. Set OPENAI_API_KEY or create 'api_key.txt'."
        )


class gpt:
    def __init__(self) -> None:
        self.object = self
        self.backend = AI_BACKEND
        self.model = OLLAMA_MODEL if self.backend == "ollama" else "gpt-4o-mini"
        self.prompts = []

        # OpenAI client init when needed
        if self.backend == "openai":
            # Using the openai.Client interface used in this repo
            self.client = openai.Client(api_key=api_key)

        #CARREGAR AS PERSONAS
        with open('./PERSONAS/friendly.json', 'r') as arq:
            self.persona = arq.read()

        #Carregar as funções definidas em ./CALL FUNCTIONS/
        self.functions = []
        self.names_functions = []

        for filename in os.listdir('./CALL FUNCTIONS/'):
            print(filename)
            with open(f"./CALL FUNCTIONS/{filename}", 'r') as arq:
                self.names_functions.append(filename[:-5])
                self.functions.append(json.loads(arq.read()))

    def send_chat(self, prompt):
        # Mensagem de sistema concatenando persona e histórico
        system_content = f"{self.persona},{self.prompts}"

        if self.backend == "openai":
            # Mantemos compatibilidade com implementação OpenAI existente
            self.completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_content},
                    {'role': 'user', 'content': prompt}
                ],
                functions=self.functions if self.functions else None,
            )

            self.prompts.append(prompt)

            # Tratar chamada de função (OpenAI)
            if self.completion.choices[0].finish_reason == "function_call":
                function_call = self.completion.choices[0].message.function_call
                res_function = function_call.name
                try:
                    attr = getattr(call_functions, res_function)
                    b = attr(function_call, self.object)
                    text = "FUNÇÃO CHAMADA"
                except Exception:
                    print("FALHA NA CONTRUÇÃO DO OBJETO FUNCTION")
                    text = "FALHA NA CONTRUÇÃO DA CHAMADA DE OBJETO"
            else:
                res_function = self.completion.choices[0].finish_reason
                text = self.completion.choices[0].message.content

            print('nome da função retornada', res_function)
            try:
                print("TOKENS DE ENTRADA", self.completion.usage.prompt_tokens)
                print('TOKENS DE RESPOSTA', self.completion.usage.completion_tokens)
                print("TOKENS TOTAL", self.completion.usage.total_tokens)
            except Exception:
                pass

            return text

        else:
            # Ollama backend: usamos apenas /api/chat para conversar e /v1/models para listar modelos
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ]
            }

            def get_available_models():
                try:
                    resp = requests.get(f"{OLLAMA_URL.rstrip('/')}/v1/models", timeout=5)
                    if resp.status_code == 200:
                        j = resp.json()
                        data = j.get('data') if isinstance(j, dict) else None
                        if isinstance(data, list):
                            return [d.get('id') for d in data if isinstance(d, dict) and 'id' in d]
                except Exception:
                    pass
                return []

            # Se o modelo configurado não estiver disponível, tentamos escolher um fallback
            available = get_available_models()
            if available and self.model not in available:
                # Preferências de fallback: gemma3:12b, qwen3:latest, default:latest, senão o primeiro disponível
                preferred = ["gemma3:12b", "qwen3:latest", "default:latest"]
                chosen = None
                for p in preferred:
                    if p in available:
                        chosen = p
                        break
                if not chosen:
                    chosen = available[0]
                # Atualizar o payload com modelo válido
                payload['model'] = chosen
                self.model = chosen

            try:
                resp = requests.post(f"{OLLAMA_URL.rstrip('/')}/api/chat", json=payload, timeout=30)
            except Exception as e:
                raise RuntimeError(f"Falha ao contatar Ollama em {OLLAMA_URL}: {e}")

            # Se o modelo não existe, Ollama costuma responder 404 com uma mensagem de erro especificando o model
            if resp.status_code == 404:
                # tente atualizar a lista de modelos e fazer fallback uma vez
                available = get_available_models()
                if available:
                    # escolher fallback conforme preferência
                    preferred = ["gemma3:12b", "qwen3:latest", "default:latest"]
                    chosen = None
                    for p in preferred:
                        if p in available:
                            chosen = p
                            break
                    if not chosen:
                        chosen = available[0]
                    payload['model'] = chosen
                    self.model = chosen
                    # re-tentar
                    resp = requests.post(f"{OLLAMA_URL.rstrip('/')}/api/chat", json=payload, timeout=30)

            if resp.status_code != 200:
                raise RuntimeError(f"Erro Ollama {resp.status_code}: {resp.text}")

            try:
                data = resp.json()
            except Exception:
                raise RuntimeError(f"Resposta inválida do Ollama: {resp.text}")

            # Extrair texto de formatos comuns do Ollama
            text = None
            try:
                # Estrutura semelhante a: choices -> 0 -> message -> content -> [{type:'output_text', 'text': '...'}]
                text = data['choices'][0]['message']['content'][0]['text']
            except Exception:
                try:
                    # Alternativa: choices -> 0 -> content
                    text = data['choices'][0].get('content')
                    if isinstance(text, list):
                        text = ''.join(text)
                except Exception:
                    text = None

            if text is None:
                # fallback para campos genéricos
                text = data.get('output') or data.get('text') or str(data)

            self.prompts.append(prompt)
            print('nome da função retornada', getattr(resp, 'model', 'ollama_response'))
            return text


class build_requiriment_functional:
    def __init__(self) -> None:
        pass
