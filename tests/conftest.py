import os
 
os.environ["TESTING"] = "1"
 
import pytest
 
from app import app, db
 
 
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        with app.test_client() as c:
            yield c
        db.session.remove()
        db.drop_all()
