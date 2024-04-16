from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from time import time
from fastapi.middleware.cors import CORSMiddleware

# Pydantic Class 



class BaseTodo(BaseModel):
    task:str
        
    
    

class Todo(BaseTodo):
    id:Optional[int] = None
    is_completed:bool = False
    # Type validation will happen automatically by pydantic
    
# What is the use of this class?
class ReturnTodo(BaseTodo):
    pass
# We will pass this class as response_model which has been inherited from BaseTodo 
# class. so when we make a post request it will only return task from BaseTodo
# but not id and is_completed






# uvicorn app:app --reload
        #app:instance of FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials= True,
    allow_methods  = ["*"],
    allow_headers = ["*"],
) 
# * -> wildcard operator, any one can access this
# if we want anyone to access out api then ["Yourwebsite.com"]
todos = [] # empty list to insert data into it



@app.post("/todos", response_model=ReturnTodo) 
async def add_todos(todo:Todo):
    todo.id= len(todos) + 1 # datatype of the Todo pydantic class
    todos.append(todo)
    return todo # returns id, task, is_complted of that id


# This will return whole to do list 
@app.get("/todos")
async def read_todos(completed:Optional[bool] = None):
    if completed is None:
        return todos
    else: 
        return [todo for todo in todos if todo.is_completed == completed]
    return todos

@app.get("/todos/{id}") #dynamic part. We can send any id that we want
# if the data is not present in todos list. It will return null. We can leave it like that, or
# we can HTTPException 
async def read_todo(id:int):
    for todo in todos:
        if todo.id == id:
            return todo
    raise HTTPException(status_code=404, detail = "Item not found")


@app.put("/todos/{id}")
async def update_todo(id:int, new_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == id:
            todos[index] = new_todo
            todos[index].id = id # to make sure the id is not garbage 
                                #after replacing with new todo
            return "Updated"
    raise HTTPException(status_code=404, detail="Item not present")

@app.delete("/todos/{id}")
async def delete_todo(id:int):
    for index, todo in enumerate(todos):
        if todo.id == id:
            del todos[index]
            return 
        return "Deleted"
    raise HTTPException(status_code=404, detail="Item not present")
    
    
@app.middleware("http")
async def log_middleware(request, call_next):
    start_time = time()
    response = await call_next(request)
    end_time = time()
    print("After route") 
    process_timee = end_time - start_time
    print(f"Request{request.url} processed in{process_timee} in sec")
    return response



