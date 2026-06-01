import io
import numpy as np
from PIL import Image
from fastapi import File, UploadFile
import tensorflow as tf
from training.train_utils import CV_DATA_FILE_NAME_PATH
from fastapi import HTTPException,APIRouter

router=APIRouter()

xray_model = tf.keras.models.load_model(CV_DATA_FILE_NAME_PATH, compile=False)

# Define your class names – adjust these to your model's actual output order
XRAY_CLASSES = ['COVID19', 'NORMAL', 'PNEUMONIA', 'TURBERCULOSIS']  # only 4 classes? check your model



from tensorflow.keras.applications.resnet50 import preprocess_input

def preprocess_xray_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img)          # range [0, 255]
    img_array = preprocess_input(img_array)   # now matches training
    return np.expand_dims(img_array, axis=0)

@router.post("/predict_xray")
async def predict_xray(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Empty file")
        input_tensor = preprocess_xray_image(contents)
        predictions = xray_model.predict(input_tensor)[0]
        predicted_idx = int(np.argmax(predictions))
        confidence = float(predictions[predicted_idx])
        disease = XRAY_CLASSES[predicted_idx]
        return {"disease": disease, "confidence": confidence}
    except Exception as e:
        print(f"X‑ray prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))