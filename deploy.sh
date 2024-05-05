docker build -t nagaraj23/local-llm-api:latest . | tee deploy.txt

docker push nagaraj23/local-llm-api:latest | tee install_output.txt