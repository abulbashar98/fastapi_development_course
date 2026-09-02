from fastapi import Response, status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .. import schemas,oAuth2,database,models

router = APIRouter(
    prefix = "/votes",
    tags = ['votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oAuth2.get_current_user)):


    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} was not found to vote")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User with {current_user.id} has already voted for the post with post id {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Your vote was casted successfully"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {current_user.id} did not vote for the post with id {vote.post_id}")
        vote_query.delete()
        db.commit()
        return {"message": "your vote was removed successfully"}
