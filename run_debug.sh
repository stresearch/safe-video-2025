export HF_TOKEN=$(cat ~/.cache/huggingface/token)
docker build -t safe-test .
docker run --gpus all \
  -e SAFE_DATASET_REPO=dsf-sandbox/video-challenge-debug \
  -e MODEL_REPO=safe-challenge/safe-example-submission \
  -e HF_TOKEN="$HF_TOKEN" \
  safe-test