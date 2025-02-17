docker build -t nagaraj23/local-llm-api:latest . | tee deploy.txt
docker tag nagaraj23/local-llm-api:latest ghcr.io/nagaraj-real/local-llm-api:latest
docker push ghcr.io/nagaraj-real/local-llm-api:latest | tee install_output.tx