import pandas as pd
import joblib
import os

from app.ml.category.pipeline import build_pipeline

DATASET_PATH = "app/ml/data/dataset_category.csv"
MODEL_PATH = "app/ml/artifacts/model_category.pkl"


def train():
    df = pd.read_csv(DATASET_PATH)

    textos = df["text"]
    labels = df["label"]

    pipeline = build_pipeline()

    pipeline.fit(textos, labels)

    os.makedirs("app/ml/artifacts", exist_ok=True)

    joblib.dump(pipeline, MODEL_PATH)

    print("Modelo entrenado y guardado")


if __name__ == "__main__":
    train()
