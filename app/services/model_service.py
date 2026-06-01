import joblib
import pandas as pd 
import numpy as np
from app.core.config import setting
from app.cache.redis_cache import get_cached_prediction, set_cached_prediction
from training import train_utils   # only needed for file path constants if you don't want to duplicate
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
# Load models
model = joblib.load(setting.MODEL_PATH)
label_encoder = joblib.load(setting.MODEL_PATH_LABEL_ENCODER)

# Load data into DataFrames
# Option 1: Use train_utils paths (if they are defined as strings)
df = pd.read_csv(train_utils.DATA_FILE_PATH)                     # Training.csv with symptoms and disease
disease_diet_df = pd.read_csv(train_utils.DISEASES_DATA_FILE_PATH)  # df_disease_diet.csv
food_df = pd.read_csv(train_utils.FOOD_NUTRITION_DATA_FILE_PATH)    # konbiri_products.csv

# Option 2: Or directly use setting or hardcoded paths (adjust as needed)
# df = pd.read_csv("data/Training.csv")
# disease_diet_df = pd.read_csv("data/df_disease_diet.csv")
# food_df = pd.read_csv("data/konbiri_products.csv")

# Get feature columns (all except last two columns: prognosis and other?)
features = df.columns[:-2].tolist()   # assuming last two columns are not symptoms

class PremiumCustomer:
    def __init__(self, user_input):
        self.user_input = user_input
        self.symptoms_list = user_input.symptoms   # list of strings

    def predict_disease(self):
        cache_key = "disease_pred_" + "_".join(sorted(self.symptoms_list))
        cached = get_cached_prediction(cache_key)
        if cached:
            return cached

        symptoms_lower = [s.lower().strip() for s in self.symptoms_list]
        input_data = np.zeros(len(features))
        for symptom in symptoms_lower:
            if symptom in features:
                idx = features.index(symptom)
                input_data[idx] = 1
        result = model.predict([input_data])
        disease_name = label_encoder.inverse_transform(result)[0]

        set_cached_prediction(cache_key, disease_name)
        return disease_name

    def disease_nutrition(self):
        disease_name = self.predict_disease()
        row = disease_diet_df[disease_diet_df["disease"].str.lower() == disease_name.lower()]
        if row.empty:
            return {"disease": disease_name, "high": [], "low": []}
        high = row.iloc[0]["high"].split(", ") if pd.notna(row.iloc[0]["high"]) else []
        low = row.iloc[0]["low"].split(", ") if pd.notna(row.iloc[0]["low"]) else []
        return {"disease": disease_name, "high": high, "low": low}

    def top_foods_high(self, nutrient, top_n=5):
        if nutrient not in food_df.columns:
            return {}
        return (
            food_df.groupby("name")[nutrient]
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
            .to_dict()
        )

    def top_foods_low(self, nutrient, top_n=5):
        if nutrient not in food_df.columns:
            return {}
        return (
            food_df.groupby("name")[nutrient]
            .sum()
            .sort_values(ascending=True)
            .head(top_n)
            .to_dict()
        )

    def get_recommendations(self):
        nutr = self.disease_nutrition()
        disease = nutr["disease"]
        high_nutrients = nutr["high"]
        low_nutrients = nutr["low"]

        recommendations = {}

        for nutrient in high_nutrients:
            recommendations[f"eat_high_{nutrient}"] = self.top_foods_high(nutrient)
        for nutrient in low_nutrients:
            recommendations[f"eat_low_{nutrient}"] = self.top_foods_low(nutrient)

        nutrition_advice = f"Increase: {', '.join(high_nutrients)}. Decrease: {', '.join(low_nutrients)}."

        food_advice = ""
        for nutrient in high_nutrients[:3]:
            foods = self.top_foods_high(nutrient)
            if foods:
                food_advice += f"Eat {', '.join(list(foods.keys())[:3])} (rich in {nutrient}). "
        for nutrient in low_nutrients[:3]:
            foods = self.top_foods_low(nutrient)
            if foods:
                food_advice += f"Eat {', '.join(list(foods.keys())[:3])} (low in {nutrient}). "

        return {
            "disease": disease,
            "nutrition_advice": nutrition_advice,
            "food_advice": food_advice
        }