from jwt import jwt_manager
from fastapi.exceptions import HTTPException
from models import user
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter()

# NOTE: Testing
@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout bem-sucedido"}

@router.get("/protected-route")
async def protected_route(current_user: dict = Depends(jwt_manager.get_current_user)):
    return {"message": "Você está autenticado!", "user": current_user}


@router.post("/register")
async def register_user(name, email, password):
    usr = user.User(name, email, password)
    usr.save()
    return {"message": f"Usuario criado com sucesso: {usr.id}"}

@router.post("/login")
async def login_user(response: Response, form: OAuth2PasswordRequestForm = Depends()):

    #Pega o email
    usr = user.User.get_user_email(form.username)
    print(usr.id)

    if(usr is None):
        raise HTTPException(status_code=404, detail="Usuario não encontrado")

    if(usr.check_password(form.password)):
        jwt_token = jwt_manager.create_jwt(data={"sub": usr.email})
        
        if (jwt_token is None): return {"message": "Erro ao criar token"}

        response.set_cookie(key="access_token", value=jwt_token)
        return {"access_token": jwt_token, "token_type": "bearer"}
       # return {"message": "Login bem-sucedido"}

    raise HTTPException(status_code=401, detail="Senha Errada")

@router.delete("")
async def delete_user(id):
    usr = user.User.delete_user(id)
    if(usr):
        return {"message": f"Usuario deletado com sucesso: {usr[0]}"}
    return { "message": "Usuario não encontrado" }
