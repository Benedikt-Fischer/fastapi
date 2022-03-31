from urllib import response
import pytest
from app import schemas
from jose import jwt
#from tests.database import client, session
from app.config import settings

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    #def validate(post):
    #    return schemas.PostResponse(**post)
    #posts_map = map(validate, res.json())
    #print(list(posts_map))
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    #print(res.json())
    post = schemas.PostVoteResponse(**res.json())
    #print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.json()['Post']['id'] == test_posts[0].id
    assert res.json()['Post']['title'] == test_posts[0].title
    assert res.json()['Post']['content'] == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("fav pizza", "quattro formaggi", False),
    ("tk", "wahoo", True)
])
def test_create_post(authorized_client, test_posts, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_posts, test_user):
    res = authorized_client.post("/posts/", json={"title": "arb", "content": "kp"})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arb"
    assert created_post.content == "kp"
    assert created_post.published is True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_posts, test_user):
    res = client.post("/posts/", json={"title": "arb", "content": "kp"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/567654754674567")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "owner_id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_posts, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "owner_id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "owner_id": test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "owner_id": test_posts[0].id
    }
    res = authorized_client.put("/posts/567654754674567", json=data)
    assert res.status_code == 404