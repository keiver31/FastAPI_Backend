from fastapi import APIRouter, HTTPException
from pydantic import BaseModel 

router = APIRouter()

#Siempre que llamamos a un servidor la función tiene que ser asincrona

#Inicia el server: uvicorn users:app --reload

#Entidad user
class User(BaseModel):
    id: int
    name: str
    lastname: str
    age: int
    
users_list = [User(id=1, name="Keiver",lastname="Rincon", age=23),
         User(id=2, name="Ednna",lastname="Rincon", age=19),
         User(id=3, name="Slendy",lastname="Rincon", age=14)]

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Keiver", "lastname":"Rincon", "age": 23},
            {"name": "Ednna", "lastname":"Rincon", "age":19}]



#PATH
#FastAPI lo detecta como un BaseModel
@router.get("/users")
async def users():
    return users_list

#PATH
#http://127.0.0.1:8000/userquery/int
@router.get("/user/{ide}")
async def user(ide: int):
    return search_user(ide)
    
    
#Ir por el path significa que esta dentro del propio path de la url



#QUERY
#Llamar por query
@router.get("/user/")
#http://127.0.0.1:8000/userquery/?id=int
async def user(id: int, name: str):
    return search_user(id)
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list) #filter es una funcion de orden superior      
    try:    
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
    
    
#------------------------------------METODO POST--------------------------------------------#

@router.post("/user/", status_code=201) #En la FN .post() existen cientos de parametros que se pueden configurar
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe") #raise=se ha producido un error excepcional
        #Los errores se lanzan con raise
        #return {"error":"El usuario ya existe"}
    
    users_list.append(user)
    return user
    

#------------------------------------METODO POST--------------------------------------------#
@router.put("/user/")
async def user(user: User):
    
    found = False
    
    #Recorre la lista, si coincide el usuario lo actualiza
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error":"No se ha actualizado el usuario"}
    return user


#------------------------------------METODO DELETE--------------------------------------------#
#http://127.0.0.1:8000/user/int (Para este ejemplo)
#Busca en el path un parametro que va a interpretar de tipo entero
@router.delete("/user/{id}")
async def user(id: int):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] #del consiste en una funcion ya predefinida
            found = True
            
    if not found:
        return {"error":"No se ha eliminado el usuario"}
            

#-----------------------FUNCION SEARCH-----------------------------------#
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list) #filter es una funcion de orden superior      
    try:    
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}