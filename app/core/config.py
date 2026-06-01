import os 
import dotenv
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME='knobini-chatbot-api'
    API_KEY=os.getenv('API_KEY')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHMS='HS256'
    REDIS_URL=os.getenv('REDIS_URL')
    MODEL_PATH='app/models/model.joblib'
    MODEL_PATH_LABEL_ENCODER='app/models/label_encoder.joblib'


setting= Settings()
