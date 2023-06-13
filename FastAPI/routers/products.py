from fastapi import APIRouter

router=APIRouter(prefix="/products",
                 tags=["products"], 
                 responses={404: {"message": "No encontrado"}}) #Puedo señalar un prefix que me sirve para mi endpoint
                #tags en la documentación de swagger crea su propio grupo


products_list = ["Producto 1","Producto 2","Producto 3","Producto 4","Producto 5","Producto 6"]


@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]