## Container Mode

In Container Mode, LLM API Container acts as a bridge between Ollama container and the Extension enabling fine grained customizations and advanced features like Document Q&A, Chat History(caching), Resource Configuration etc.

### Pre-requisites

- Install [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

- **[Optional]** GPU (NVIDIA) -
  Download and install [NVIDIA® GPU drivers](https://www.nvidia.com/download/index.aspx?lang=en-us)

  Checkout [Useful links](#useful-links) for more information on configuring GPU for ollama.

### Quick Start

#### 1. Start containers using docker compose

#### CPU

Download [docker-compose-cpu.yml](https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-cpu.yml) and start

```sh
curl \
https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-cpu.yml \
-o docker-compose-cpu.yaml

docker compose -f docker-compose-cpu.yml up
```

#### NVIDIA® GPU

Download [docker-compose-gpu.yml](https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-gpu.yml) and start.

```sh
curl  \
https://raw.githubusercontent.com/nagaraj-real/localaipilot-api/main/recipes/docker-compose-gpu.yml \
-o docker-compose-gpu.yaml

docker compose -f docker-compose-gpu.yml up
```

This will start Ollama and LLM API containers. The Cache(Redis) container is plug and play which can be turned
on for cahing/searching chat history.

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

## Standalone mode

In standalone mode, the extension connects directly with a running Ollama instance.
Supported features: Code chat, Code completion, Explain/Review/Fix Code

### Pre-requisites

Ollama instance up and running.

Refer [Ollama Documentation](https://github.com/ollama/ollama) for detailed steps.

### Quick Start

#### Update extension setting

- Set the extension mode (_mode_) as "Standalone"
- Configure the port (_ollamaPort_) and host (_ollamaHost_) of running ollama instance.
- Configure model used for chat (_ollamaModel_)
- Configure model used for code completion (_ollamaCodeModel_)

### Useful links

#### GPU support help

- https://hub.docker.com/r/ollama/ollama
- https://docs.docker.com/compose/gpu-support/
- https://docs.docker.com/desktop/gpu/
