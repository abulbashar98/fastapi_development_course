from app import schemas
import pytest


def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    print(res.json())

    def validate(post):
        post = schemas.PostResponse_with_left_outer_join(**post)
        return post

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    print(posts_list)

    def find_post_with_matching_id(post_id):
        for post in posts_list:
            if post.post.id == post_id:
                return post

    for test_post in test_posts:
        found_post = find_post_with_matching_id(test_post.id)

        assert found_post is not None
        assert found_post.post.id == test_post.id


    def find_post_with_matching_title(post_title):
        for post in posts_list:
            if post.post.title == post_title:
                return post

    for test_post in test_posts:
        found_post = find_post_with_matching_title(test_post.title)

        assert found_post is not None
        assert found_post.post.title == test_post.title

    assert res.status_code == 200

def test_unauthorized_client_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401

def test_unauthorized_client_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_post_does_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/8888")
    assert res.status_code == 404

def test_get_one_post_successfully(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[1].id}")
    post = schemas.PostResponse_with_left_outer_join(**res.json())


    def find_matching_post_id_in_test_posts(post_id):
        for test_post in test_posts:
            if test_post.id == post_id:
                return test_post

        found_post_with_matching_id = find_matching_post_id_in_test_posts(post.post.id)

        assert post.post.id == found_post_with_matching_id.id

    def find_matching_post_title_in_test_posts(post_title):
            for test_post in test_posts:
                if test_post.title == post_title:
                    return test_post
    
            found_post_with_matching_title = find_matching_post_title_in_test_posts(post.post.title)
    
            assert post.post.title == found_post_with_matching_title.title

    def find_matching_post_content_in_test_posts(post_content):
            for test_post in test_posts:
                if test_post.content == post_content:
                    return test_post
    
            found_post_with_matching_content = find_matching_post_content_in_test_posts(post.post.content)
    
            assert post.post.content == found_post_with_matching_content.content


@pytest.mark.parametrize("title, content, published, phone_number, address",[
    ("awesome 1st post title", "content for 1st awesome post", True, "0745565666", "edsevo_finland"),
    ("My favorite pizza", "I love kebab pizza and shrimp",  False, "4588888758", "madrid spain"),
    ("Highest Skyscraper in the world", "welcome to burj al khalifa", True, "39358552145", "rome italy")

])
def test_create_post(authorized_client, test_user, title, content, published, phone_number, address):
    res = authorized_client.post("/posts", json={"title": title, "content": content, "published": published, "phone_number": phone_number, "address": address})

    created_post = schemas.PostResponse(**res.json())

    assert created_post.owner_id == test_user['id']
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published

def test_create_post_default_published_true     (authorized_client, test_user):
    res = authorized_client.post("/posts", json={"title": "arbitrary title", "content": "arbitrary content", "phone_number": "arbitrary phone number", "address": "arbitrary address"})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id'] 

def test_unauthorized_client_create_post(client, test_user):
    res = client.post("/posts", json={"title": "arbitrary title", "content": "arbitrary content", "phone_number": "arbitrary phone number", "address": "arbitrary address"})

    assert res.status_code == 401

def test_unauthorized_client_delete_post(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_does_not_exist(authorized_client,test_posts,test_user):
    res = authorized_client.delete(f"/posts/8888")
    assert res.status_code == 404

def test_delete_other_users_post(authorized_client, test_posts, test_user, test_user2):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.owner_id == test_posts[0].owner_id
    assert updated_post.address == test_posts[0].address
    assert updated_post.phone_number == test_posts[0].phone_number

def test_update_other_user_post(authorized_client, test_posts, test_user, test_user2):
    data = {
            "title": "updated title",
            "content": "updated content",
            "id": test_posts[3].id
        }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_posts, test_user):
    data = {
                "title": "updated title",
                "content": "updated content",
                "id": test_posts[3].id
            }

    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_update_post_does_not_exist(authorized_client, test_posts, test_user):
    data = {
                    "title": "updated title",
                    "content": "updated content",
                    "id": test_posts[3].id
                }

    res = authorized_client.put("/posts/55555", json=data)
    assert res.status_code == 404




