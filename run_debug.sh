export HF_TOKEN=$(cat ~/.cache/huggingface/token)
export LOCAL_CACHE=$(pwd)
docker run -it --rm --gpus all \
  -e SAFE_DATASET_REPO=safe-challenge/video-challenge-pilot-debug \
  -e MODEL_REPO=safe-challenge/video-challenge-pilot-debug \
  -e HF_TOKEN=$HF_TOKEN \
  -e PYTHONUNBUFFERED=1 \
  -w /app/debug \
  -v $LOCAL_CACHE:/tmp \
  ghcr.io/stresearch/competitions:latest \
  bash debug.sh