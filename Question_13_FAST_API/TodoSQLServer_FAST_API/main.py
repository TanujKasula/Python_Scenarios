from util import get_config,get_sql_con
from sqlalchemy import text
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()

class Todo(BaseModel):
    title: str
    description: str = None
    completed : bool | None=None

class TodoCompleted(BaseModel):
    completed:bool

@app.post("/todos/")
async def create_todo(todo: Todo):
    con=get_sql_con()
    cursor=con.cursor()
    completed_value=int(todo.completed) if todo.completed is not None else 0
    cursor.execute(
        "INSERT INTO todos (title,description,completed) values(?,?,?)",(todo.title,todo.description,completed_value)
    )
    con.commit()
    con.close()
    return {"message":"Todo created successfully. Now completed that task asap!!!"}

@app.get("/todos/")
async def get_todo():
    con=get_sql_con()
    cursor=con.cursor()
    cursor.execute("select id, title,description, completed from todos")
    rows=cursor.fetchall()
    result=[dict(zip([column[0] for column in cursor.description],row)) for row in rows]
    con.close()
    return result

@app.get("/todos/{todo_id}")
async def get_one_todo(todo_id:int):
    con=get_sql_con()
    cursor=con.cursor()
    cursor.execute("SELECT id,title,description,completed from todos where id= ?",todo_id)
    row=cursor.fetchone()
    con.close()
    if row:
        result=dict(zip([column[0] for column in cursor.description],row))
        return result
    raise HTTPException(status_code=404, detail="Todo not found")



@app.put("/todos/{todo_id}")
async def put_todo(todo_id:int,todo: Todo):
    con=get_sql_con()
    cursor=con.cursor()
    cursor.execute("UPDATE todos set title=?,description=?,completed=? where id=?",
                   (todo.title,todo.description,int(todo.completed),todo_id))
    if cursor.rowcount == 0:
        con.close()
        raise HTTPException(status_code=404, detail="Todo Not found")
    con.commit()
    con.close()
    return{"message":f"Todo '{todo_id}' updated successfully"}

@app.patch("/todos/{todo_id}")
async def update_todo(todo_id:int, todocompleted:TodoCompleted):
    con=get_sql_con()
    cursor=con.cursor()
    cursor.execute("update todos set completed=? where id=?",
                   (int(todocompleted.completed),todo_id))
    if cursor.rowcount ==0:
        con.close()
        raise HTTPException(status_code=404,detail="Todo Not found")
    con.commit()
    con.close()
    return{"message":f"Todo '{todo_id}' is updated using patch successfully"}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id:int):
    con=get_sql_con()
    cursor=con.cursor()
    cursor.execute("Delete from todos where id=?",todo_id)
    if cursor.rowcount ==0:
        con.close()
        raise HTTPException(status_code=404,detail="Todo Not found")
    con.commit()
    con.close()
    return {"message":f"Todo with todo id '{todo_id}' deleted successfully"}
    
