from dotenv import load_dotenv
import os
import mlflow
import pandas as pd
import numpy as np

from fastapi import APIRouter, HTTPException
from app.api.schema import HouseInputSchema, HouseOutputSchema
from training.train_utils import HOUSE_PRICE_PREDICTION_FILE_PATH

 
# DagsHub / MLflow authentication


load_dotenv()

dagshub_token = os.getenv("DAGSHUB_PAT")


if not dagshub_token:
    raise EnvironmentError(
        "DAGSHUB_PAT environment variable is not set"
    )

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token


 
# MLflow / DagsHub configuration
 

dagshub_url = "https://dagshub.com"
repo_owner = "amitnegionway"
repo_name = "japan-property-price-prediction"

mlflow.set_tracking_uri(f"{dagshub_url}/{repo_owner}/{repo_name}.mlflow")


 
# Load Champion Model
 

def get_champion_model_version(model_name: str):

    client = mlflow.MlflowClient()

    champion_model = client.get_model_version_by_alias(model_name,"champion")

    return champion_model.version


model_name = "my_model"

model_version = get_champion_model_version(model_name)

model_uri = f"models:/{model_name}/{model_version}"

model = mlflow.pyfunc.load_model(model_uri)


 
# Categorical features
 

cat_features = [
    "Type",
    "Region",
    "DistrictName",
    "NearestStation",
    "LandShape",
    "Structure",
    "Use",
    "Purpose",
    "Direction",
    "Classification",
    "CityPlanning"
]


 
# Load training data
 
df=pd.read_csv(HOUSE_PRICE_PREDICTION_FILE_PATH)

 
# Remove columns not used by the model
 

drop_cols = [
    "Remarks",
    "Renovation",
    "No",
    "UnitPrice",
    "PricePerTsubo",
    "TotalFloorAreaIsGreaterFlag",
    "FloorPlan",
    "TimeToNearestStation",
    "MaxTimeToNearestStation",
    "AreaIsGreaterFlag",
    "Prefecture",
    "Municipality",
    "Period",
    "PrewarBuilding",
    "FrontageIsGreaterFlag",
    "TradePrice",
]

df = df.drop(columns=drop_cols)



# Create category map from training data


category_map = {}

for col in cat_features:

    df[col] = df[col].astype("category")

    category_map[col] = df[col].cat.categories.tolist()


# FastAPI Router


router = APIRouter()


@router.post("/House_Prediction",response_model=HouseOutputSchema)

def house_price_prediction(user_input: HouseInputSchema):

    try:

        # Convert Pydantic input to DataFrame
        data = pd.DataFrame([user_input.model_dump()])

        
        # Convert categorical columns using training categories
  

        for col in cat_features:

            data[col] = pd.Categorical(data[col],categories=category_map[col])


        # Model prediction


        log_prediction = model.predict(data)

        # Convert log prediction back to original price
        prediction = np.expm1(log_prediction)

        predicted_price = float(prediction[0])

        return {
            "Price": f"{int(predicted_price)} Yen"
        }
        

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )