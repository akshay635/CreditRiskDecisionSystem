import pandas as pd

def get_feature_importance(model):
    importances = model.named_steps.model.feature_importances_
    features = model.named_steps.preprocessing.get_feature_names_out()

    df = pd.DataFrame({
        "Features": features,
        "Importances": importances
    })

    df["Cleaned_Features"] = df["Features"].str.split("__").str[-1].str.split("_").str[0]

    return df.groupby("Cleaned_Features", as_index=False)["Importances"].sum().sort_values(by="Importances", ascending=False)