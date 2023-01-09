import numpy as np
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
