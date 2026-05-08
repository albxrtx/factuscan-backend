import joblib

MODEL_PATH = "app/ml/artifacts/model_category.pkl"

model = joblib.load(MODEL_PATH)


def predict_category(text: str):
    prediction = model.predict([text])[0]
    return prediction
