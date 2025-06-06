export HF_TOKEN=$(cat ~/.cache/huggingface/token)
export LOCAL_CACHE=/disk1/kirill/tmp
docker run -it --rm --gpus all \
  -e SAFE_DATASET_REPO=dsf-sandbox/video-challenge-debug \
  -e MODEL_REPO=dsf-sandbox/safe-video-example-submission \
  -e HF_TOKEN=$HF_TOKEN \
  -e PYTHONUNBUFFERED=1 \
  -w /app/debug \
  -v $LOCAL_CACHE:/tmp \
  ghcr.io/stresearch/competitions:latest \
  bash debug.sh