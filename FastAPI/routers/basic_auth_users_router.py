from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
                            #Libreria para la autenticación
                            #Gestiona la autenticación, la forma en como se va a enviar a la api para la validación


router = APIRouter()

#Instancia para el sistema de autenticación
#La url en la cual se debe realizar el proceso de autenticación
oauth2 = OAuth2PasswordBearer(tokenUrl="login")#Criterio de autenticación

class User(BaseModel):
    usermame: str
    full_name: str
    email: str
    disabled: bool
    

#Configuración del usuario de base de datos
#El usuario de BD tiene como extra el password
class UserDB(User):
    password: str



users_db ={
    "keiver":{
        "usermame": "keiver",
        "full_name": "keiver rincon",
        "email": "keiver@gmail.com",
        "disabled": False,
        "password": "123456"
        
    },
    "keiver2":{
        "usermame": "keiver2",
        "full_name": "keiver rincon 2",
        "email": "keiver2@gmail.com",
        "disabled": True,
        "password": "654321"
        
    },
    
}



#Buscar en base de datos el usuario
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #Se debe colocar el **
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])    
    
    

#Criterio de dependencia asincrono
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Credenciales de autenticación invalidad", 
            headers={"WWW-Authenticate": "Bearer"}) #raise=se ha producido un error excepcional
    
    if user.disabled:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo") 
        
    return user
        



    
#Operación para autenticarnos
@router.post("/login")
#Se captura el usuario y la contraseña
#Depends recibe datos pero no depende de nadie
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db =users_db.get(form.username)
    if not users_db: #Si el usuario no esta en la base de datos
        raise HTTPException(status_code=400, detail="El usuario no es correcto") #raise=se ha producido un error excepcional
    
    user = search_user_db(form.username)
    
    #Se comprueba la contraseña
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="La contraseña no es correcta") #raise=se ha producido un error excepcional
    
    #Lo que el sistema devolver es un access token
    return {"access_token": user.usermame, "token_type": "bearer"}         


#Operación que entrega los datos de usuario
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user 