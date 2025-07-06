from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()

fake_db=[]

#Get method
@app.get("/")
async def read_root():
    return{"people":fake_db}

#Post method.....

#----Step 1---

class Person(BaseModel):
    name:str
    age:int

@app.post("/create-person")
async def create_person(person : Person):
    for p in fake_db:
        if p.name==person.name:
            raise HTTPException(status_code=400,detail="Person already exists")
    fake_db.append(person)
    return {
        "message":f"Person '{person.name}' of age {person.age} is addedd successfully!!",
        "data":person
    }

@app.put("/update-person/{person_name}")
async def update_person(person_name:str, updated_person:Person):
    for id,person in enumerate(fake_db):
        if person.name==person_name:
            fake_db[id]=updated_person
            return{
                "message":f"Person {person_name} updated successfully!!",
                "data":updated_person
            }
    raise HTTPException(status_code=400,detail="Person not found!!")


@app.delete("/delete-person/{person_name}")
async def delete_person(person_name:str):
    for idx,person in enumerate(fake_db):
        if person.name==person_name:
            removed=fake_db.pop(idx)
            return{
                "message":f"Person {person_name} deleted successfully!!",
                "data":removed
            } 
    raise HTTPException(status_code=404,detail="Person not found error")