# Local AI Pilot

VS code extension which supports code chat, code completion using local running ollama models. Allows fine grained customization using docker containers.

## Standalone mode

In standalone (non-container) mode, the extension connects directly to running Ollama instance.

Supported features: Code chat, Code completion, Explain/Review/Fix Code

### Pre-requisites

- Running Ollama Instance

### Quick Start

#### Update extension settings under standalone section

- Configure the port (_ollamaPort_) and host (_ollamaHost_) of running ollama instance.
- Configure model used for chat (_ollamaModel_)
- Configure model used for code completion (_ollamaCodeModel_)

## Container mode (Recommended)

In container mode, the extension connects to a local API layer for fine grained customizations.
Also comes in built with ollama container which can be turned off if you already have a local instance running.

Supported features - Code chat, Code completion,Explain/Review/Fix Code,
Document Q&A, Chat History(caching), Resource Configuration.

### Pre-requisites

- Install [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

- [Optional] GPU (NVIDIA) -
  Download and install [NVIDIA® GPU drivers](https://www.nvidia.com/download/index.aspx?lang=en-us)

  Checkout [Useful links](#useful-links) for more information on configuring GPU for ollama.

### Quick Start

#### 1. Start containers using docker compose

- Download docker compose file and start

  #### Nvidia GPU

  Download [docker-compose-gpu.yml](https://github.com/nagaraj-real/localaipilot-api/blob/b8e7583e689d4e1715b386437a01a427f88ee605/recipes/docker-compose-gpu.yml)

  ```bash

  wget https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-gpu.yml -o docker-compose-gpu.yaml

  docker compose -f docker-compose-gpu.yml up
  ```

  #### CPU

  Download [docker-compose-cpu.yml](https://github.com/nagaraj-real/localaipilot-api/blob/b8e7583e689d4e1715b386437a01a427f88ee605/recipes/docker-compose-cpu.yml)

  ```bash
  wget https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-cpu.yml -o docker-compose-cpu.yaml

  docker compose -f docker-compose-cpu.yml up
  ```

  This will start ollama, LLM API and Redis containers.

#### 2. Pull ollama models

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

### Advanced Configuration

#### Using a different model

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

#### Using Remote models

Remote models require API keys which can be configured in your docker compose file.

Supported remote models - gemini, cohere

Create your API keys

Cohere - https://dashboard.cohere.com/api-keys

Gemini - https://aistudio.google.com/app/apikey

- Update model name and model key in docker compose environment variables.

  ```env
   MODEL_NAME: gemini/cohere
   EMBED_MODEL_NAME: gemini/cohere
   API_KEY: <API_KEY>
  ```

#### Chat History

Chat history is cached in Redis which can be configured using the docker compose file.
Caching allows searching previous chats using keyword or chat-id.
By default the chat history is cached for 1 hour.

#### Document Q&A (RAG Chat)

Use docker compose volume (_ragdir_) to bind the folder containing documents for Q&A.
The embeddings are stored in volume (_ragstorage_)

### Useful links

#### GPU support help

- https://hub.docker.com/r/ollama/ollama
- https://docs.docker.com/compose/gpu-support/
- https://docs.docker.com/desktop/gpu/
