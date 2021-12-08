import hashlib
from models import User
import pytest
from flask import Flask
from exts import db
import os


class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///qa.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    return app


@pytest.fixture()
def test_client():
    app = create_app()
    app.app_context().push()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["WTF_CSRF_ENABLED"] = False
    db.create_all()
    yield app.test_client()
    db.drop_all()


def login(test_client, telephone, password):
    test_client.post(
        "/login",
        data={"telephone": telephone, "password": password},
        follow_redirects=True,
    )


class Test:
    def test_get_register(self, test_client):
        response = test_client.get('/register')

        assert response is not None
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_post_register(self, test_client):
        response = test_client.post(
            "/register",
            data={
                "telephone": "15872383701",
                "username": "Jack",
                "password": "qwedf",
                "confirm_password": "qwedf",
            },
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully registered." in response.data

    def test_get_login(self, test_client):
        response = test_client.get("/login")

        assert response is not None
        assert response.status_code == 200
        assert b"Log In" in response.data

    def test_post_login(self, test_client):
        hashed_password = hashlib.md5("qwedf".encode('utf-8')).hexdigest()
        app_user = User(telephone="15872383701", username="Jack", password=hashed_password)
        db.session.add(app_user)
        db.session.commit()

        response = test_client.post(
            "/login",
            data={"telephone": app_user.telephone, "password": "qwedf"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully logged in" in response.data

    def test_post_logout(self, test_client):
        hashed_password = hashlib.md5("qwedf".encode('utf-8')).hexdigest()
        app_user = User(telephone="15872383701", username="Jack", password=hashed_password)
        db.session.add(app_user)
        db.session.commit()
        login(test_client, app_user.telephone, "qwedf")

        response = test_client.post("/logout", follow_redirects=True)

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully logged out" in response.data
