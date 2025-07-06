from src.util import get_db_connection,hash_password
from fastapi import FastAPI,HTTPException
from src.db_create import create_tables
from src.models import UserLogin,UserRegistration,UserResponse,TaskCreate,TaskResponse

app=FastAPI()
create_tables()

@app.get("/")
async def home():
    return {"mesage":"TaskManagement API app is runnning"}

@app.post("/TaskManagement/register",response_model=UserResponse)
async def register(user: UserRegistration):
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM users where email=?",(user.email,))
    existing_user=cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already exists")
    user_hashed_password=hash_password(user.password)
    cursor.execute("INSERT INTO users(name,email,password) OUTPUT INSERTED.id values (?,?,?)",(user.name,user.email,user_hashed_password))
    user_id=cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return UserResponse(id=user_id,name=user.name,email=user.email)

@app.post("/TaskManagement/login", response_model=UserResponse)
async def login(credentials :UserLogin):
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT id,name,email,password FROM users where email=?",(credentials.email,))
    user=cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email or password")
    id,name,email,hashed_pwd=user
    if hashed_pwd != hash_password(credentials.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    cursor.close()
    connection.close()

    return UserResponse(id=id,name=name,email=email)

@app.post("/TaskManagement/tasks/",response_model=TaskResponse)
async def createTask(task:TaskCreate):
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT id from users where id=? ",(task.user_id,))
    user=cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    cursor.execute("""INSERT INTO tasks(title,description,status,due_date,user_id) 
                   OUTPUT INSERTED.id VALUES(?,?,?,?,?)
                   """,(task.title,task.description,task.status,task.due_date,task.user_id)
                   )
    task_id=cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return TaskResponse(
        id=task_id,
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
        user_id=task.user_id
    )

@app.get("/TaskManagement/tasks/{user_id}",response_model=list[TaskResponse])
async def get_tasks(user_id:int):
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM users where id=?",(user_id,))
    user=cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!!")
    cursor.execute("""
                    SELECT id,title,description,status,due_date,user_id 
                            FROM tasks where user_id=?
                    """,(user_id,))
    tasks=[]
    rows=cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()

    for row in rows:
        tasks.append(TaskResponse(
            id=row.id,
            title=row.title,
            description=row.description,
            status=row.status,
            due_date=row.due_date,
            user_id=row.user_id
        ))

    return tasks

@app.put("/TaskManagement/tasks/{task_id}",response_model=TaskResponse)
async def put_task(task_id:int, task: TaskCreate):
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("select * from tasks where id=? and user_id=?",(task_id,task.user_id))
    existing_task=cursor.fetchone()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task belonging to user not found")
    cursor.execute("""
                        update tasks
                        set title=? , description=?, status=?,due_date=?
                        where id=? and user_id=?
                   """,(task.title,task.description,task.status,task.due_date,task_id,task.user_id))
    connection.commit()
    cursor.close()
    connection.close()
    return TaskResponse(
        id=task_id,
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
        user_id=task.user_id
    )

@app.delete("/TaskManagement/tasks/{task_id}")
async def delete_task(task_id:int,user_id:int):
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("select * from tasks where id=? and user_id=?",(task_id,user_id))
    existing_task=cursor.fetchone()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task belonging to user not found")
    cursor.execute("""
                        delete from tasks where id=? and user_id=?
                   """,(task_id,user_id))
    connection.commit()
    cursor.close()
    connection.close()

    return {"message":f"Task with ID '{task_id}' deleted successfully ."}