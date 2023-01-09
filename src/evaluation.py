import logging

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error


def calculate_metrics(results, model_name, cmodel_name, label_test, preds, model_type):
    mse = mean_squared_error(label_test, preds)
    rmse = np.sqrt(mse)
    # save results
    result = {
        "model": model_name,
        "2nd_model": cmodel_name,
        "type": model_type,
        "mse": mse,
        "rmse": rmse,
    }
    results = results.append(result, ignore_index=True)

    return results


def calculate_importance(
    importance_df,
    model_name,
    cmodel_name,
    model_type,
    model,
    features_test,
    labels_test,
    metric,
    n_repeats,
):
    # calculate importance
    pis = {}
    pi = permutation_importance(
        estimator=model,
        X=features_test,
        y=labels_test,
        scoring=metric,
        n_repeats=n_repeats,
        random_state=42,
    )
    pis[model_name] = pi

    # unpack importance
    for i in pi.importances_mean.argsort()[::-1]:
        column_name = f"{features_test.columns[i]}"
        importance = f"{pi.importances_mean[i]:.3f}"
        std = f" +/- {pi.importances_std[i]:.3f}"

        importance_df = importance_df.append(
            {
                "model": model_name,
                "2nd_model": cmodel_name,
                "type": model_type,
                "column": column_name,
                "importance": importance,
                "std": std,
            },
            ignore_index=True,
        )

    return importance_df
