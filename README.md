# 🏪 Konbini FastAPI

Backend API service for the **Konbini AI Assistant** – a Japanese convenience store (konbini) chatbot.  
This FastAPI application provides:

- 🍱 **Product nutrition** – price, calories, macros, vitamins (`/premium_product`)
- 🩺 **Disease prediction** – from symptoms + konbini food recommendations (`/predict_problems`)
- 🩻 **X‑ray classification** – Normal / Pneumonia / Tuberculosis / COVID‑19 (`/predict_xray`)
- 📊 **Manager analytics** – sales pie chart (`/manager/sales-pie`)
- 🔐 **Authentication** – OAuth2 with JWT, role‑based access (normal, premium, manager)
- 💾 **Caching** – Redis for frequent predictions
- 📈 **Monitoring** – Prometheus metrics endpoint

> 📌 The conversational LangGraph agent that calls these APIs lives in a separate repository.

---

## 🧱 Tech Stack

| Category | Technologies |
|----------|--------------|
| **API Framework** | FastAPI, Uvicorn |
| **ML & Data** | TensorFlow 2.17, scikit-learn, pandas, numpy, Pillow |
| **Authentication** | python-jose, passlib (bcrypt), OAuth2PasswordBearer |
| **Caching** | Redis |
| **Monitoring** | prometheus-fastapi-instrumentator |
| **Utilities** | python-dotenv, requests, pydantic |

---

## 📁 Project Structure

Konbini-Fastapi/
├── app/
│ ├── api/ # Routers (auth, diseases, premium, manager, xray)
│ ├── core/ # Security, config, dependencies, caching
│ ├── middleware/ # Logging middleware
│ ├── services/ # ML model loading & prediction logic
│ ├── training/ # Training scripts (optional)
│ └── main.py # FastAPI entrypoint
├── models/ # Saved models (.keras, .pkl)
├── data/ # CSV files (products, disease‑diet mapping)
├── logs/ # Application logs
├── .env # Environment variables
├── requirements.txt
└── README.md
