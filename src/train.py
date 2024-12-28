import argparse
from typing import List

import joblib
import pandas as pd
import mlflow
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data", required=True, help="Input path of data.")
    parser.add_argument("--output_model", required=True, help="Output path of data.")
    args = parser.parse_args()
    return args


def get_cv_results_string(grid_search: GridSearchCV):

    results = grid_search.cv_results_

    rows = zip(
        results["rank_test_score"],
        results["params"],
        results["mean_test_score"],
        results["std_test_score"],
    )

    sorted_rows = sorted(rows, key=lambda x: x[0])

    # initialize output string
    ouput = ""

    # add header and separator
    ouput += f"{'Rank':<6}{'Mean Test Score':<20}{'Std Test Score':<20}{'Parameters':<150}\n"
    ouput += "-" * 200 + "\n"

    # Add each row to the result string
    for _, (rank, params, mean_score, std_score) in enumerate(sorted_rows):
        ouput += f"{rank:<6}{mean_score:<20.3f}{std_score:<20.3f}{params}\n"
    
    return ouput


def main():
    
    args = parse_args()

    mlflow.start_run()

    train_data = pd.read_csv(f"{args.input_data}/train.csv")

    # initializing pipeline
    pipeline = Pipeline([
        ("vect", TfidfVectorizer()),
        ("clf", MultinomialNB())
    ])

    param_grid = {
        'vect__ngram_range': [(1, 1), (1, 2), (2, 2)],
        'clf__alpha': [0.01, 0.1, 1, 10],
    }

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=5,
        scoring="accuracy",
        verbose=2,
        n_jobs=-1
    )

    grid_search.fit(train_data["text_clean"], train_data["label"])

    joblib.dump(
        grid_search.best_estimator_, f"{args.output_model}/model_pipeline.pkl"
    )

    mlflow.sklearn.log_model(
        sk_model=grid_search.best_estimator_,
        artifact_path="model"
    )

    mlflow.end_run()

    return None


if __name__ == "__main__":
    main()