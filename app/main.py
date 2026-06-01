import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
# load the port info from env vars
port = os.environ["PORT"]

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import routes_auth,routes_predicts_diseases,routes_premium_product,router_manager,router_CV
from app.middleware.logging_middleware import LoggingMiddle
from app.core.exceptions import register_exception_handlers
from fastapi.middleware.gzip import GZipMiddleware


app=FastAPI(title="Konbini Fastapi")
app.add_middleware(GZipMiddleware, minimum_size=1000)

# link middle ware
app.add_middleware(LoggingMiddle)

# link endpoint

app.include_router(routes_auth.router,tags=['Auth'])
app.include_router(routes_predicts_diseases.router,tags=['Prediction'])
app.include_router(routes_premium_product.router,tags=['product details'])
app.include_router(router_manager.router,tags=['Manager Dashboard'])
app.include_router(router_CV.router,tags=['X-ray dieseases classification'])
# monitoring using promethues
#Instrumentator().instrument(app).expose(app)

# add exception handler
register_exception_handlers(app)