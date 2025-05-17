from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import Todo, get_db 
from typing import List
import schemas as sc

router = APIRouter()

@router.get("/todos", response_model=List[sc.Todo])
async def get_all_todos(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Todo))
    return res.scalars().all()

@router.get("/todos/{id}")
async def get_todos(id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Todo).where(Todo.id == id))
    data = res.scalars().first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
    return sc.TodoBase.model_validate(data)

@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: sc.TodoCreate, db: AsyncSession = Depends(get_db)):
    st = insert(Todo).values(todo.model_dump())
    try:
        await db.execute(st)
        await db.commit()
        return {"detail": f"{todo.title} added"}
    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"error")


@router.put("/todos/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_todo(id:int, todo: sc.TodoUpdate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Todo).where(Todo.id == id))
    data = res.scalars().first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
    try:
        st = update(Todo).where(Todo.id == id).values(todo.model_dump())
        await db.execute(st)
        await db.commit()
        return {"detail": f"id {id} updated"}
    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"error")
    
@router.delete("/todos/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_todo(id : int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Todo).where(Todo.id == id))
    data = res.scalars().first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
    try:
        st = delete(Todo).where(Todo.id==id)
        await db.execute(st)
        return {"detail": f"id {id} deleted"}
    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"server error")