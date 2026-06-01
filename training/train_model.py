import pandas as pd
import os 
from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestClassifier
import joblib
from .train_utils import DATA_FILE_PATH,MODEL_DIR,MODEL_PATH,LABEL_ENCODER_PATH
# Load training data
df = pd.read_csv(DATA_FILE_PATH)   # adjust path
# The last column with disease names – use 'prognosis' as shown in your column list
X = df.iloc[:, :-2]   # all symptom columns
y = df['prognosis'].str.lower()   # disease names as strings

# Encode labels to integers
le = LabelEncoder()
y_encoded = le.fit_transform(y)   # Now le.classes_ contains the disease names

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y_encoded)

# Save model and label encoder

os.makedirs(MODEL_DIR,exist_ok=True)
joblib.dump(model, MODEL_PATH)
joblib.dump(le, LABEL_ENCODER_PATH)
