from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def build_pipeline():
    return Pipeline(
        [
            (
                "tfid",
                TfidfVectorizer(lowercase=True),
            ),
            ("clf", MultinomialNB()),
        ]
    )
