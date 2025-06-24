# Debugging Submissions Locally

To debug your submission code and dependencies, you can reproduce all the steps locally. You will need access to a linux environment that's setup to run Docker (or podman) with NVIDIA GPU support.

See example [run_debug.sh](run_debug.sh) example:

```bash
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
```

Make sure to have a valid token and change `MODEL_REPO` to point to your model repo. This command will simulate the same steps that happeen during the online evaluation.

1. Setup eval environment by installing `requirements.txt` if it exists in the top level of `MODEL_REPO`, otherwise default [`requirments.txt`](requirements.txt) is used instead. 
2. Download dataset (here we use a dummy debug dataset consisting of a handful of misc. videos)
3. Download model from `MODEL_REPO`
4. Run `script.py` in the eval environment
5. Compute metrics from `submission.csv` and `solution.csv` using `metrics.py`


The [sample_practice_submission.csv](sample_practice_submission.csv) should look like this:
```csv
id,pred,score,time
9712245a-548d-584c-a82d-a543f1ea21ac,generated,0.8955863118171692,18.962587118148804
07bd0843-74a6-53ec-a3f0-00dfc31d6e2a,real,-0.4735659658908844,0.03756999969482422
06704fa4-5a0c-540c-86e6-c98af1528478,generated,0.4556829333305359,0.027454853057861328
c3e008aa-e4ba-5d2a-b37e-dd6d0ae640cb,real,-0.05135703459382057,0.03614068031311035
12dae22b-3251-5204-ad61-bdf55ccfff51,generated,0.752806544303894,0.03131747245788574
b681b921-7842-5942-b378-c491372dff93,real,-2.2116477489471436,0.03128170967102051
b2373bde-1e59-56cd-877b-c38dbce7e1d2,real,-1.3747910261154175,0.03574991226196289
6beaf7e5-2049-5640-bcad-2b77e31a3956,generated,0.5170786380767822,0.0328369140625
d346af27-f9f2-597d-b848-8e9d57a00847,real,-0.7394500374794006,0.031241655349731445
4cc52c06-b8d4-5b83-9069-a602bd2d71ef,real,-0.3091548681259155,0.03464174270629883
a7d079be-525a-547e-bc4a-984f1d61aa6f,real,-0.304933100938797,0.02721118927001953
a657caf4-4b97-5797-8c57-775fbd78aedd,generated,1.1447159051895142,0.025275468826293945
ec9778de-9c5c-5e20-b242-847ce24a10e1,real,-0.9481428265571594,0.03555035591125488
55117a10-2d11-5b76-adc5-39070c4987ca,real,-1.9522984027862549,0.02613973617553711
e08e97ff-ec7e-531f-afda-1749b550d4bf,generated,0.5286235809326172,0.03823685646057129
```



