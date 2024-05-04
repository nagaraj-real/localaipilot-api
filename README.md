## Standalone Mode

In standalone (non-container) mode, the extension connects directly with an Ollama instance.

### 🚀 Quick Start

#### 1. Install Ollama on your machine from [Ollama Website](https://ollama.com/download)

#### 2. Pull local models

- Chat Model

  ```sh
  ollama pull gemma:2b
  ```

- Code Model

  ```sh
  ollama pull codegemma:2b
  ```

#### 3. Update the **mode** as "Standalone" in extension (**Settings > Local AI Pilot > Mode**)

#### Use a different model for chat or code model **[Optional]**

- Configure model used for chat in extension (**Settings > Local AI Pilot > ollamaModel**)
- Configure model used for code completion in extension (**Settings > Local AI Pilot > ollamaCodeModel**)

---

## Container Mode

In Container Mode, LLM API Container acts as a bridge between Ollama and the Extension enabling fine grained customizations and advanced features like Document Q&A, Chat History(caching), Remote models.

### Pre-requisites

- Install [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

- **[Optional]** GPU (NVIDIA) -
  Download and install [NVIDIA® GPU drivers](https://www.nvidia.com/download/index.aspx?lang=en-us)

  Checkout [Useful links](#useful-information-and-links) for more information on configuring GPU for ollama.

### 🚀 Quick Start

#### 1. Start containers using docker compose

#### Download docker compose and start the services on demand.

[docker-compose-cpu.yml](https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-cpu.yml) | [docker-compose-gpu.yml](https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-gpu.yml)

```sh
docker compose -f docker-compose-cpu|gpu.yml up llmapi [ollama] [cache]
```
**Container Services**

- **llmapi** : LLM API container service that connectes the Extension with Ollama. All configurations available through ENV variables.
- **ollama [Optional]** : Turn on this service for running [Ollama as container](https://github.com/nagaraj-real/localaipilot-api#running-ollama-as-container).
- **cache [Optional]** : Turn on this service for caching and searching [chat history](https://github.com/nagaraj-real/localaipilot-api?tab=readme-ov-file#1-chat-history)

> [!TIP]
> Start with llmapi service. Add other services based on your needs.

Configurating docker compose to connect with ollama running on localhost (via [ollama app](https://github.com/nagaraj-real/localaipilot-api?tab=readme-ov-file#1-install-ollama-on-your-machine-from-ollama-website))

```sh
docker compose -f docker-compose-cpu|gpu.yml up llmapi

# update OLLAMA_HOST env variable to point localhost(host.docker.internal)
```

#### 2. Update the **mode** as "Container" in extension. (**Settings > Local AI Pilot > Mode**)

---

### 📘 Advanced Configuration (Container Mode)

#### 1. Chat History

Chat History can be saved in Redis by turning on cache service.
By default, the chats are cached for 1 hour which is configurable in docker compose.
This also enables searching previous chats via Extension by keyword or chat Id.

```sh
docker compose -f docker-compose-cpu|gpu.yml up cache
```

#### 2. Document Q&A (RAG Chat)

Start Q&A chat using Retrieval-Augmented Generation (RAG) and embeddings.
Pull a local model to generate and query embeddings.

- Embed Model

  ```sh
  ollama pull nomic-embed-text
  ```

Use docker compose volume (_ragdir_) to bind the folder containing documents for Q&A.
The embeddings are stored in volume (_ragstorage_)

#### 3. Using a different Ollama model

- Pull your preferred model from [ollama model library](https://ollama.com/library)

  ```bash
  ollama pull <model-name>
  ollama pull <code-model-name>
  ollama pull <embed-model-name>
  ```

- Update model name in docker compose environment variable.

  Note: Local models are prefixed by the word "local/"

  ```env
  MODEL_NAME: local/<model-name>
  CODE_MODEL_NAME: local/<code-model-name>
  EMBED_MODEL_NAME: local/<embed-model-name>
  ```

---

#### 🌐 Remote models (Container Mode)

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


### Useful information and links

#### Running Ollama as container

```sh
docker compose -f docker-compose-cpu|gpu.yml up ollama

# update OLLAMA_HOST env variable to "ollama"
```

ollama commands are now available via docker.

```sh
docker exec -it ollama-container ollama ls
```

#### GPU support help

- https://hub.docker.com/r/ollama/ollama
- https://docs.docker.com/compose/gpu-support/
- https://docs.docker.com/desktop/gpu/
