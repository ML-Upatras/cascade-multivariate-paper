from collections import Counter

import pandas as pd


def dataset_comparison(datasets, comparison_tables, save_dir):
    print("Calculating the best model for each dataset...")

    counter = Counter()
    for dataset in datasets:
        # create a dict to save the best model for each dataset
        df = pd.DataFrame(columns=["model", "2nd_model", "cascade", "voting"])
        for table in comparison_tables.glob("*.csv"):
            # if table is summary, skip
            if table.name == "summary.csv":
                continue

            # load table
            ct = pd.read_csv(table)

            # get the row that corresponds to the dataset
            dataset_row = ct[ct["index"] == dataset]

            # isolate the columns that we want
            dataset_row = dataset_row[["model", "2nd_model", "cascade", "voting"]]

            # make them int
            dataset_row = dataset_row.astype(float)

            # add to df
            df = df.append(dataset_row, ignore_index=True)

        # evaluate cascade vs every other model
        df["cascade_model"] = df["cascade"] < df["model"]
        df["cascade_2nd"] = df["cascade"] < df["2nd_model"]
        df["cascade_voting"] = df["cascade"] < df["voting"]
        df["cascade_wins"] = (
            df["cascade_model"] & df["cascade_2nd"] & df["cascade_voting"]
        )

        # create a row that has the sum of the cascade_better column
        df.loc["sum"] = df.sum()

        # update counter
        counter["cascade_model"] += df["cascade_model"].loc["sum"]
        counter["cascade_2nd"] += df["cascade_2nd"].loc["sum"]
        counter["cascade_voting"] += df["cascade_voting"].loc["sum"]
        counter["cascade_wins"] += df["cascade_wins"].loc["sum"]
        counter["total"] = counter["total"] + len(df) - 1

        # save the comparison table
        df.to_csv(save_dir / f"{dataset}.csv", index=False)

    # save counter results to a csv
    counter = pd.DataFrame.from_dict(counter, orient="index")
    counter.to_csv(save_dir / "summary.csv")

    print("Done calculating the best model for each dataset!\n")
