import argparse
from typing import List

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_model", required=True, help="Input path of model.")
    parser.add_argument("--input_data", required=True, help="Input path of data.")
    args = parser.parse_args()
    return args


def main():
    
    args = parse_args()

    test_data = pd.read_csv(f"{args.input_data}/test.csv")
    model = joblib.load(f"{args.input_model}/model_pipeline.pkl")

    y_pred = model.predict(test_data["text_clean"])

    # Evaluate the model
    accuracy = accuracy_score(test_data["label"], y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Optional: Print detailed classification report
    print("\nClassification Report:")
    print(classification_report(test_data["label"], y_pred))

    return None


if __name__ == "__main__":
    main()