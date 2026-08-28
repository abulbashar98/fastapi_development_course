from fastapi import FastAPI, Response, status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..database import engine,get_db
from .. import models,schemas,utils
from typing import List

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)


@router.get("/" ,response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    # # print(posts)

    posts = db.query(models.Post).all()

    return posts



# Note: Create post using body raw json from postman and use that post body as payload 
# @app.post("/createPosts")
# def create_post(payload: dict = Body(...)):
#     print(f"New post title: {payload["title"]} and New post content: {payload["content"]}")
#     return {"message" : "Your post was created"}


# Import BaseModel from pydantic to use schema for post body structure and validation


  

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # print(post.published)
    # print(post.rating)
    # print(post.model_dump())
    # print(new_post.published)

    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""", (post.title,post.content,post.published))
    # created_post = cursor.fetchone()
    # conn.commit()

    # print(**post.model_dump())

    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    # return {"data": post_dict}
    return new_post

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

#Note: Notice the /posts/latest is before /posts/{id}. It is working top down. Because of that reason if we put latest after /{id} it will not be validated as int and will not work.



# @app.get("/posts/latest")
# def get_latest_post():
#     latest_post = my_posts[my_posts.__len__() - 1]
#     print(latest_post)
#     return {"latest_post_detail": latest_post}



@router.get("/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # print(type(id))
    # post = find_post(id)

    # if not post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #                     detail = f"Post with id {id} was not found")

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"The post with id {id} was not found"}

    return post



# def find_post_index(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)):
    # index = find_post_index(id)

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # print("post deleted successfully")

    post_query = db.query(models.Post).filter(models.Post.id == id)
    deletable_post = post_query.first()

    if deletable_post == None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": f"post with id {id} was not found"}

    post_query.delete(synchronize_session = False)
    db.commit()

    # my_posts.pop(index)
    return {status.HTTP_204_NO_CONTENT}


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int,post: schemas.PostCreate,response: Response, db: Session = Depends(get_db)):
    # index = find_post_index(id)

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,(str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updatable_post = post_query.first()

    if updatable_post == None:
        
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} was not found!")

    # post_dict = post.model_dump()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    # print(post_dict)
    
    # return {"post": post}

    post_query.update(post.model_dump(), synchronize_session = False)
    db.commit()

    return post_query.first()