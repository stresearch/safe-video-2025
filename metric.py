import pandas as pd
from huggingface_hub import hf_hub_download
from sklearn.metrics import roc_auc_score


def compute_roc(solution_df):

    ## fix weird submissions
    if isinstance(solution_df.iloc[0]["score"], str):
        submission_df.loc[:, "score"] = submission_df.loc[:, "score"].apply(
            lambda a: float(
                # np.array(json.loads(re.sub(r"\b(\d+)\.(?!\d)", r"\1.0", a))).squeeze()
                np.array(json.loads(re.sub(r"\b(\d+)\.(?!\d)", r"\1.0", a))).squeeze()
                if isinstance(a, str)
                else float("nan")
            )
        )

    
    
    isna  = solution_df["score"].isna()
    
    if isna.all():
        ## if all nans
        return -1
        
    solution_df  = solution_df.loc[~isna]
    auc = roc_auc_score(solution_df["pred"] == "generated", solution_df["score"])
    return auc

def _metric(solution_df, submission_df, mode="top_level"):
    """
    This function calculates the accuracy of the generated predictions.

    Parameters
    ----------
    solution_df : pandas.DataFrame
        The dataframe containing the solution data.
    submission_df : pandas.DataFrame
        The dataframe containing the submission data.
    mode : str, optional
        The mode of evaluation. Can be "top_level" or "bottom_level". The default is "top_level".

    Returns
    -------
    None.
    """

    ## Ensure alignment of keys
    solution_df["submission_pred"] = solution_df.join(submission_df, lsuffix="_solution", rsuffix="_submission")[
        "pred_submission"
    ].values
    cols = ["split", "pred", "source"]

    solution_df["correct"] = solution_df["pred"] == solution_df["submission_pred"]
    accuracy = solution_df.groupby(cols)["correct"].mean().to_frame("accuracy").reset_index()
    accuracy["score_name"] = accuracy["pred"] + "_" + accuracy["source"]

    evaluation = {}

    for split, temp in accuracy.groupby("split"):
        scores_by_source = temp.set_index("score_name")["accuracy"].sort_index()
        scores_by_source["generated_accuracy"] = temp.query("pred=='generated'")["accuracy"].mean()
        scores_by_source["real_accuracy"] = temp.query("pred=='real'")["accuracy"].mean()
        scores_by_source["balanced_accuracy"] = (
            scores_by_source["generated_accuracy"] + scores_by_source["real_accuracy"]
        ) / 2.0
        if mode == "top_level":
            scores_to_save = ["generated_accuracy", "real_accuracy", "balanced_accuracy"]
            evaluation[f"{split}_score"] = scores_by_source.loc[scores_to_save].to_dict()
        else:
            evaluation[f"{split}_score"] = scores_by_source.to_dict()
        
        

    if "time" in submission_df.columns:
        solution_df["submission_time"] = submission_df["time"]
        for split, temp in solution_df.groupby("split"):
            evaluation[f"{split}_score"]["total_time"] = float(temp["submission_time"].sum())

    if "score" in submission_df.columns:
        solution_df["score"] = submission_df["score"]
        for split, temp in solution_df.groupby("split"):
            try:
                auc = compute_roc(temp)
            except Exception as e:
                print("failed auc")
                print(e)
                auc = -1
                
            evaluation[f"{split}_score"]["auc"] = float(auc)
            evaluation[f"{split}_score"]["fail_rate"] = float(temp["score"].isna().mean())
        

    # evaluation = {
    #     "public_score": {
    #         "metric1": public_score,
    #     },
    #     "private_score": {
    #         "metric1": private_score,
    #     }
    # }
    return evaluation


def compute(params):
    solution_file = hf_hub_download(
        repo_id=params.competition_id,
        filename="solution.csv",
        token=params.token,
        repo_type="dataset",
    )

    solution_df = pd.read_csv(solution_file).set_index(params.submission_id_col)

    submission_filename = f"submissions/{params.team_id}-{params.submission_id}.csv"
    submission_file = hf_hub_download(
        repo_id=params.competition_id,
        filename=submission_filename,
        token=params.token,
        repo_type="dataset",
    )

    submission_df = pd.read_csv(submission_file).set_index(params.submission_id_col)

    return _metric(solution_df, submission_df)
    