## Standalone mode

In standalone (non-container) mode, the extension connects directly with Ollama instance running in your machine.

### 🚀 Quick Start

#### 1. Download and install Ollama in your machine from [Ollama Website](https://ollama.com/download)

#### 2. Pull local models

```sh
 ollama pull gemma:2b
```

```sh
 ollama pull codegemma:2b
```

#### 3. Update the **mode** as "Standalone" in extension settings.

**[Optional]** Use a different model for chat or code model

- Configure model used for chat using extension setting **ollamaModel**
- Configure model used for code completion using extension setting **ollamaCodeModel**

---

## Container Mode

In Container Mode, LLM API Container acts as a bridge between Ollama Container and the Extension enabling fine grained customizations and advanced features like Document Q&A, Chat History(caching), Remote models.


### Pre-requisites

- Install [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

- **[Optional]** GPU (NVIDIA) -
  Download and install [NVIDIA® GPU drivers](https://www.nvidia.com/download/index.aspx?lang=en-us)

  Checkout [Useful links](#useful-links) for more information on configuring GPU for ollama.

### 🚀 Quick Start

#### 1. Start containers using docker compose

#### CPU - [docker-compose-cpu.yml](https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-cpu.yml)

```sh
curl \
https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-cpu.yml \
-o docker-compose-cpu.yaml

docker compose -f docker-compose-cpu.yml up
```

#### NVIDIA® GPU - [docker-compose-gpu.yml](https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-gpu.yml)

```sh
curl  \
https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-gpu.yml \
-o docker-compose-gpu.yaml

docker compose -f docker-compose-gpu.yml up
```

This will start Ollama and LLM API containers. The Cache(Redis) container is plug and play which can be turned on for caching/searching chat history.

#### 2. Pull Ollama models

- Chat Model

  ```bash
  docker exec -it ollama-container ollama pull gemma:2b
  ```

- Code Model (code completion)

  ```bash
  docker exec -it ollama-container ollama pull codegemma:2b
  ```

- Embed Model (Optional) only if you are using document Q&A

  ```bash
  docker exec -it ollama-container ollama pull nomic-embed-text
  ```

- (Optional) List down local models downloaded
  ```bash
  docker exec -it ollama-container ollama list
  ```
#### 3. Update the **mode** as "Container" in extension settings.

---

### 📘 Advanced Configuration (Container Mode)

#### Using a different Ollama model

- Pull your preferred model from [ollama model library](https://ollama.com/library)

  ```bash
  docker exec -it ollama-container ollama pull <model-name>
  docker exec -it ollama-container ollama pull <code-model-name>
  docker exec -it ollama-container ollama pull <embed-model-name>
  ```

- Update model name in docker compose environment variable.

  Note: Local models are prefixed by the word "local/"

  ```env
  MODEL_NAME: local/<model-name>
  CODE_MODEL_NAME: local/<code-model-name>
  EMBED_MODEL_NAME: local/<embed-model-name>
  ```

#### Chat History

Chat history is cached in Redis which can be configured using the docker compose file.
Caching allows searching previous chats using keyword or chat-id.
By default the chat history is cached for 1 hour.

#### Document Q&A (RAG Chat)

Use docker compose volume (_ragdir_) to bind the folder containing documents for Q&A.
The embeddings are stored in volume (_ragstorage_)

---

### 🌐 Remote models (Container Mode)

Remote models require API keys which can be configured in the docker compose file.

Supports the models of gemini, cohere, openai LLM providers.

Update model name and model key in docker compose environment variables.

Turn down ollama service if it's running as it will not be used for remote inference.

```bash
docker compose down ollama
```

Supports _{Provider}/{ModelName}_ format

- Gemini

  Create API keys https://aistudio.google.com/app/apikey

  ```env
   MODEL_NAME: gemini/gemini-pro
   EMBED_MODEL_NAME: gemini/embedding-001
   API_KEY: <API_KEY>
   EMBED_API_KEY: <API_KEY>
  ```

- Cohere

  Create API keys https://dashboard.cohere.com/api-keys

  ```env
   MODEL_NAME: cohere/command
   EMBED_MODEL_NAME: cohere/embed-english-v3.0
   API_KEY: <API_KEY>
   EMBED_API_KEY: <API_KEY>
  ```

- Open AI

  Create API keys https://platform.openai.com/docs/quickstart/account-setup

  ```env
   MODEL_NAME: openai/gpt-3.5-turbo
   EMBED_MODEL_NAME: openai/text-embedding-3-large
   API_KEY: <API_KEY>
   EMBED_API_KEY: <API_KEY>
  ```
---

### Useful links

#### GPU support help

- https://hub.docker.com/r/ollama/ollama
- https://docs.docker.com/compose/gpu-support/
- https://docs.docker.com/desktop/gpu/
