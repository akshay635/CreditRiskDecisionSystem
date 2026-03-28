import joblib
import importlib
import training.config as config
importlib.reload(config)

def load_model():
    return joblib.load(config.MODEL_PATH)

def predict_pd(model, df):
    return model.predict_proba(df)[0][1]