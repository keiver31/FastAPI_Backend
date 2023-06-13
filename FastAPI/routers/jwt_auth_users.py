from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
                            #Libreria para la autenticación
                            #Gestiona la autenticación, la forma en como se va a enviar a la api para la validación
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256" #Algoritmo de encriptación
ACCESS_TOKEN_DURATION = 1
SECRET = "AJALAASKSSSSSSAAAAAAAAADHDHGFELKWHEJSJAMMAWKKSAaddaa" #Al azar se genero
                            
app = FastAPI()

#Instancia para el sistema de autenticación
#La url en la cual se debe realizar el proceso de autenticación
oauth2 = OAuth2PasswordBearer(tokenUrl="login")#Criterio de autenticación

crypt = CryptContext(schemes=["bcrypt"]) #Algoritmo de criptografia

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    

#Configuración del usuario de base de datos
#El usuario de BD tiene como extra el password
class UserDB(User):
    password: str



users_db ={
    "keiver":{
        "username": "keiver",
        "full_name": "keiver rincon",
        "email": "keiver@gmail.com",
        "disabled": False,
        "password": "$2a$12$qxBpD7O6IyU9gHu12fXZpeTYxp1CFiT2R9K9uBNL4BczoU/svGNUm"
        
    },
    "keiver2":{
        "username": "keiver2",
        "full_name": "keiver rincon 2",
        "email": "keiver2@gmail.com",
        "disabled": True,
        "password": "$2a$12$w3oOjMF7LXFJSv6sTbHvh.U6/mMDn4zsxzp3KVzn9QCREDDi/xFXC"
        
    },
    
}

#Buscar en base de datos el usuario
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #Se debe colocar el **
    
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])  
    
async def auth_user(token: str = Depends(oauth2)):
    
    exception =  HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Credenciales de autenticación invalidas", 
        headers={"WWW-Authenticate": "Bearer"}) #raise=se ha producido un error excepcional
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None: #En caso de que el username viaje vacio
             raise exception
    
    except JWTError: #La idea es capturar el error
        raise exception
    
    return search_user(username)
                
        
    
    
#Criterio de dependencia asincrono
async def current_user(user: str = Depends(auth_user)):
    
    if user.disabled:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Usuario inactivo") 
        
    return user


#Operación para autenticarnos
@app.post("/login")
#Se captura el usuario y la contraseña
#Depends recibe datos pero no depende de nadie
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db =users_db.get(form.username)
    if not users_db: #Si el usuario no esta en la base de datos
        raise HTTPException(status_code=400, detail="El usuario no es correcto") #raise=se ha producido un error excepcional
    
    user = search_user_db(form.username)
    
    

    #Se comprueba la contraseña
    if not crypt.verify(form.password, user.password): #se compara la contraseña con la encriptada en base de datos
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta") #raise=se ha producido un error excepcional
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) #Un tiempo de duración de un minuto más del tiempo de generación del token
    
    #En el jwt se envian los siguientes datos: nombre del usuario
    
    #Se crea un objeto para el access token
    access_token = {"sub":user.username, "exp": expire}
    
    
    #Lo que el sistema devolver es un access token
    #Ahora se debe generar un access token de formasegura
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}    



#Ahora como se maneja el token?
#Operación que entrega los datos de usuario #Entrega el algoritmo de dependencia
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user 