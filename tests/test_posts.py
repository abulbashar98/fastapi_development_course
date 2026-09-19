from app import schemas

from app import schemas


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

    assert res.status_code == 200


