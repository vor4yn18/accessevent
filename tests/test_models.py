from datetime import datetime
 
import pytest
 
from models import db, User, Event, Registration, ChatMessage
 
 
def test_user_creation_valid(client):
    u = User(username="anna", email="anna@mail.ru",
             password_hash="x", role="user", is_deaf=True)
    db.session.add(u)
    db.session.commit()
    found = User.query.filter_by(email="anna@mail.ru").first()
    assert found is not None
    assert found.is_deaf is True
 
 
def test_user_duplicate_email_fails(client):
    db.session.add(User(username="a", email="dup@mail.ru", password_hash="x"))
    db.session.commit()
    db.session.add(User(username="b", email="dup@mail.ru", password_hash="x"))
    with pytest.raises(Exception):
        db.session.commit()
 
 
def test_event_requires_title(client):
    db.session.add(User(username="org", email="org@mail.ru",
                        password_hash="x", role="organizer"))
    db.session.commit()
    org = User.query.filter_by(email="org@mail.ru").first()
    ev = Event(organizer_id=org.id, event_date=datetime(2026, 12, 1, 12, 0))
    db.session.add(ev)
    with pytest.raises(Exception):
        db.session.commit()
 
 
def test_registration_unique_per_user_event(client):
    db.session.add(User(username="o", email="o@mail.ru",
                        password_hash="x", role="organizer"))
    db.session.add(User(username="p", email="p@mail.ru", password_hash="x"))
    db.session.commit()
    org = User.query.filter_by(email="o@mail.ru").first()
    part = User.query.filter_by(email="p@mail.ru").first()
    ev = Event(title="Кинопросмотр", organizer_id=org.id,
               event_date=datetime(2026, 12, 1, 12, 0), is_inclusive=True)
    db.session.add(ev)
    db.session.commit()
    db.session.add(Registration(user_id=part.id, event_id=ev.id,
                                status="pending"))
    db.session.commit()
    db.session.add(Registration(user_id=part.id, event_id=ev.id,
                                status="pending"))
    with pytest.raises(Exception):
        db.session.commit()
 
 
def test_event_organizer_relationship(client):
    u = User(username="org2", email="org2@mail.ru",
             password_hash="x", role="organizer")
    db.session.add(u)
    db.session.commit()
    ev = Event(title="Лекция", organizer_id=u.id,
               event_date=datetime(2026, 12, 2, 18, 0))
    db.session.add(ev)
    db.session.commit()
    assert ev.organizer.username == "org2"
 
 
def test_chat_message_belongs_to_event(client):
    u = User(username="o3", email="o3@mail.ru",
             password_hash="x", role="organizer")
    db.session.add(u)
    db.session.commit()
    ev = Event(title="Экскурсия", organizer_id=u.id,
               event_date=datetime(2026, 12, 3, 10, 0))
    db.session.add(ev)
    db.session.commit()
    m = ChatMessage(event_id=ev.id, user_id=u.id, message="Привет!")
    db.session.add(m)
    db.session.commit()
    assert ChatMessage.query.filter_by(event_id=ev.id).count() == 1
