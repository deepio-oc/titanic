import json

import click

import pandas as pd


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path(exists=True))
def eval(input_file, output_dir):
    """Eval script which compares prediction with ground truth."""
    predictions = pd.read_csv(input_file, index_col="PassengerId")
    ground_truth = pd.read_csv("ground_truth.csv", index_col="PassengerId")

    accurate = (predictions["Survived"] == ground_truth["Survived"]).cumsum().tolist()
    accuracy = accurate[-1] * 100 / len(predictions)

    metrics = {
        "sort": "accuracy-score",
        "metrics": [
            {
                "name": "accuracy-score",  # The name of the metric. Visualized as the column name in the runs table.
                "numberValue": accuracy,  # The value of the metric. Must be a numeric value.
                "format": "PERCENTAGE",  # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
            }
        ],
    }

    metrics = {"metrics": {"accuracy": accuracy}, "rank_metric": "accuracy"}
    with open(output_dir + "/metrics.json", "w") as f:
        json.dump(metrics, f)
    print(f"Accuracy: {round(accuracy,2)}")


if __name__ == "__main__":
    eval()
