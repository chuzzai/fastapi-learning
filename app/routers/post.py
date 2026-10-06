from..import models, schema, util,oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)




@router.get("/", response_model=list[schema.postout])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0,search: str = ""):
    result = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .offset(skip)
        .limit(limit)
        .all())
    return [{"Post": post, "votes": votes} for post, votes in result]



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
async def create_post(posts: schema.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):


    #cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (posts.title, posts.content, posts.published))
   # new_post = cur.fetchone()
   # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@router.get("/{id}", response_model=schema.postout)
async def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    #cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cur.fetchone()  
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"Post": post[0], "votes": post[1]}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,)
async def delete_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cur.fetchone()
    #conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(deleted_post)
    db.commit()
    return {"message": "Post deleted successfully", "post": deleted_post}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Post)
async def update_post(id: int, updated_posts: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post=updated_post.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    updated_post.update(updated_posts.dict(), synchronize_session=False)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.commit()

    return updated_post.first()