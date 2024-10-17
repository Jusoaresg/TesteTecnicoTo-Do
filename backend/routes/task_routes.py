from pydantic import BaseModel
from models import task, user
from fastapi import APIRouter, Depends, HTTPException
from jwt import jwt_manager

router = APIRouter()

class TaskModel(BaseModel):
    name: str
    desc: str
    completed: bool

class EditTaskModel(BaseModel):
    id: str
    name: str
    desc: str
    completed: bool

@router.post("")
async def create_task(taskModel: TaskModel, current_user: dict = Depends(jwt_manager.get_current_user)):
    usr = user.User.get_user_email(current_user.get("email"))
    if(usr is None): return

    name = taskModel.name
    desc = taskModel.desc
    completed = taskModel.completed

    tsk = task.Task(name, desc, str(usr.id), completed)
    tsk.save()
    return tsk

@router.get("/all")
async def list_tasks(current_user: dict = Depends(jwt_manager.get_current_user)):
    usr = user.User.get_user_email(current_user.get("email"))
    if(usr is None): return
    tasks = await task.Task.get_user_tasks(str(usr.id))
    return tasks

@router.get("")
async def get_task(id):
    tsk = await task.Task.get_task(id)
    return tsk

#WARNING: Falta fazer verificação do usuario que esta deletando
@router.delete("")
async def delete_task(id, current_user: dict = Depends(jwt_manager.get_current_user)):
    tsk = task.Task.delete_task(id)
    if(tsk is None): 
        raise HTTPException(status_code=404, detail="Task not found")
    return {"Message": f"Task deleted: {tsk}"}

@router.put("")
async def edit_task(taskModel: EditTaskModel, current_user: dict = Depends(jwt_manager.get_current_user)):
    tsk = task.Task.get_task(taskModel.id)
    print(tsk)
    if(tsk is None): 
        raise HTTPException(status_code=404, detail="Task not found")

    task.Task.edit_task(taskModel)
    return {"Message": f"Task Edited: {tsk}"}
