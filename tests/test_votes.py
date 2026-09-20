import pytest
from app import models

@pytest.fixture
def test_vote(test_posts, test_user, session):
    new_vote = models.Vote(post_id = test_posts[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()





def test_vote_on_post(authorized_client, test_posts, test_user):
    res = authorized_client.post(f"/votes", json={"post_id": test_posts[0].id, "dir": 1})
    print(res.json())
    assert res.status_code == 201

def test_vote_on_a_post_already_voted(authorized_client, test_posts, test_user, test_vote):
    res = authorized_client.post("/votes", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409

def test_delete_vote_on_a_post(authorized_client, test_posts, test_user, test_vote):
    res = authorized_client.post("/votes", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201

def test_delete_vote_from_a_post_that_does_not_have_a_vote(authorized_client, test_posts, test_user):
    res = authorized_client.post("/votes/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404

def test_vote_on_a_post_does_not_exist(authorized_client, test_posts,test_user):
    res = authorized_client.post("/votes", json={"post_id": 80000, "dir": 1})
    assert res.status_code == 404

def test_unauthorized_client_vote_failed(client, test_posts, test_user):
    res = client.post("/votes", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401