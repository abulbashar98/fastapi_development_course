from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

# request get Method url ("/")
@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    return {"message" : "These are your posts"}



# Note: Create post using body raw json from postman and use that post body as payload 
# @app.post("/createPosts")
# def create_post(payload: dict = Body(...)):
    # print(f"New post title: {payload["title"]} and New post content: {payload["content"]}")
    # return {"message" : "Your post was created"}


# Import basemodel from pydantic to use schema for post body structure and validation

class Posts(BaseModel):
    title: str
    content: str

@app.post("/createPosts")
def create_posts():
    return {"message": "Posts created with schema validation"}