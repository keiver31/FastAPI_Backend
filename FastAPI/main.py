from fastapi import FastAPI
from routers import products, users, jwt_auth_users_router, basic_auth_users_router

app = FastAPI()

#Siempre que llamamos a un servidor la función tiene que ser asincrona

#El protocolo estandar es http

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users_router.router)
app.include_router(basic_auth_users_router.router)

#Para montar mis  archivos estaticos
from fastapi.staticfiles import StaticFiles

#Exponer recuersos estaticos como imagenes
#Función mount para montar los recursos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static") #app.mount("donde lo expongo",tipo de directorio)


@app.get("/")
async def root():
    return {"message": "Hello World"}

#Estoy creando rutas
@app.get("/url")
async def url():
    messagePru="Hemos avanzado"
    return {messagePru}

#Inicia el server: uvicorn main:app --reload
#Detener el server: CTRL+C

#Documentación con Swagger: http://127.0.0.1:8000/docs
#Documentación con Redocly: http://127.0.0.1:8000/redoc

