import pandas as pd


def calculate_best_models(datasets, results_dir, save_dir):
    print("Calculating the best model for each dataset...")

    # create a dict to save the best model for each dataset
    best_models = pd.DataFrame(
        columns=["dataset", "model", "2nd_model", "type", "mse", "rmse"]
    )
    for dataset in datasets:
        # load the metrics for each dataset
        try:
            results_path = results_dir / dataset.upper()
            metrics_csv = results_path / "metrics.csv"
            metrics = pd.read_csv(metrics_csv)
        except FileNotFoundError:
            print(f"File not found for {dataset}")
            continue

        # for each dataset, save the best model
        best_models = update_best_models(metrics, dataset, best_models)

    # save the best model for each dataset
    best_models.to_csv(save_dir / "best_models.csv", index=False)

    # save percentages of each best model type on a csv
    best_models["type"].value_counts(normalize=True).to_csv(
        save_dir / "best_models_percentages.csv"
    )
    print("Done calculating the best model for each dataset!\n")


def update_best_models(metrics, dataset, best_models):
    # sort the metrics by mse
    metrics = metrics.sort_values(by="mse")

    # get the best model
    best_model = metrics.iloc[0]
    best_models = best_models.append(best_model, ignore_index=True)

    # add dataset name
    best_models.loc[best_models.index[-1], "dataset"] = dataset

    return best_models
