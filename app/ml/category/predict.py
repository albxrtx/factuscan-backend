import joblib

MODEL_PATH = "app/ml/artifacts/model_category.pkl"

model = joblib.load(MODEL_PATH)


def predict_category(company_name: str, items_text: str):
    text = f"{company_name} {items_text}"
    return model.predict([text])[0]
