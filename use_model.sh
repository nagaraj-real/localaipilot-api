#!/bin/sh

echo "installing dependencies"


model_name="$MODEL_NAME"
embed_model_name="$EMBED_MODEL_NAME"
code_model_name="$CODE_MODEL_NAME"


if [ "$model_name" = "cohere" ]; then
  pip install llama-index-llms-cohere | tee install_output.txt
elif [ "$model_name" = "gemini" ]; then
  pip install llama-index-llms-gemini | tee install_output.txt
  pip install google-generativeai | tee install_output.txt
fi

if [ "$embed_model_name" = "cohere" ]; then
  pip install llama-index-embeddings-cohere | tee install_output.txt
elif [ "$embed_model_name" = "gemini" ]; then
  pip install llama-index-embeddings-gemini | tee install_output.txt
fi

echo "model_name" "$model_name"
echo "code_model_name" "$code_model_name"
echo "embed_model_name" "$embed_model_name"

