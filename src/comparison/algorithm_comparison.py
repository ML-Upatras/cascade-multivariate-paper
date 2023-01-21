from collections import Counter

import pandas as pd


def algorithm_comparison(datasets, friedman_tables, save_dir):
    print("Creating comparison tables for each algorithm combination...")

    # load the friedman tables
    counter = Counter()
    for table in friedman_tables.glob("*.csv"):
        ft = pd.read_csv(table)
        ft = ft.reset_index(drop=True)
        ft = ft.drop(columns=["Unnamed: 0"])

        # evaluate cascade vs every other model
        ft["cascade_model"] = ft["cascade"] < ft["model"]
        ft["cascade_2nd"] = ft["cascade"] < ft["2nd_model"]
        ft["cascade_voting"] = ft["cascade"] < ft["voting"]
        ft["cascade_wins"] = (
            ft["cascade_model"] & ft["cascade_2nd"] & ft["cascade_voting"]
        )

        # create a row that has the sum of the cascade_better column
        ft.loc["sum"] = ft.sum()

        # update counter
        counter["cascade_model"] += ft["cascade_model"].loc["sum"]
        counter["cascade_2nd"] += ft["cascade_2nd"].loc["sum"]
        counter["cascade_voting"] += ft["cascade_voting"].loc["sum"]
        counter["cascade_wins"] += ft["cascade_wins"].loc["sum"]
        counter["total"] = counter["total"] + len(ft) - 1

        # reset index and replace each value except the last one with the dataset names
        ft = ft.reset_index()
        for i, dataset in enumerate(datasets):
            ft.loc[i, "index"] = dataset

        # save the comparison table
        ft.to_csv(save_dir / table.name)

    # save counter results to a csv
    counter = pd.DataFrame.from_dict(counter, orient="index")
    counter.to_csv(save_dir / "summary.csv")

    print("Done!\n")
