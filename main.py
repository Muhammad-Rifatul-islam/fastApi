from fastapi import FastAPI


app =FastAPI()



student = {
    "name": "Rifat",
    "course": "FastAPI"
}
 
@app.get("/")
def greet():

   return student