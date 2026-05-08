import pandas as pd
import joblib
from app.ml.items.pipeline import build_pipeline

MODEL_PATH = "app/ml/artifacts/model_items.pkl"


def train():
    df = pd.read_csv("app/ml/data/dataset_items.csv")

    X = df["text"]
    y = df["label"]

    pipeline = build_pipeline()
    pipeline.fit(X, y)

    joblib.dump(pipeline, MODEL_PATH)
    print("Modelo de items entrenado y guardado")


if __name__ == "__main__":
    train()
