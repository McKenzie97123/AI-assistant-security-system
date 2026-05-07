import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

MODEL_PATH = os.getenv("MODEL_PATH", "/app/model.pkl")

_BOT_AGENTS = {"python-requests", "curl", "wget", "scrapy", "go-http", "java/", "libwww", "aiohttp"}


class BotClassifier:
    def __init__(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
        else:
            self.model = self._train_default()
            joblib.dump(self.model, MODEL_PATH)

    def _featurize(self, f: dict) -> np.ndarray:
        ua = f.get("user_agent", "").lower()
        return np.array([[
            min(f.get("requests_per_minute", 0) / 60.0, 5.0),
            float(any(b in ua for b in _BOT_AGENTS)),
            float(not f.get("has_accept_header", True)),
            float(not f.get("has_accept_language", True)),
            min(f.get("body_size", 0) / 1000.0, 10.0),
        ]])

    def _train_default(self) -> RandomForestClassifier:
        rng = np.random.default_rng(42)

        bots = np.column_stack([
            rng.uniform(1.0, 5.0, 500),
            rng.choice([0, 1], 500, p=[0.1, 0.9]),
            rng.choice([0, 1], 500, p=[0.1, 0.9]),
            rng.choice([0, 1], 500, p=[0.1, 0.9]),
            rng.uniform(0.1, 2.0, 500),
        ])
        humans = np.column_stack([
            rng.uniform(0.0, 0.3, 500),
            rng.choice([0, 1], 500, p=[0.95, 0.05]),
            rng.choice([0, 1], 500, p=[0.95, 0.05]),
            rng.choice([0, 1], 500, p=[0.90, 0.10]),
            rng.uniform(0.1, 5.0, 500),
        ])

        X = np.vstack([bots, humans])
        y = np.array([1] * 500 + [0] * 500)

        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X, y)
        return clf

    def predict_proba(self, features: dict) -> float:
        return float(self.model.predict_proba(self._featurize(features))[0][1])
