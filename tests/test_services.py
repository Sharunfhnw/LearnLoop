"""Service layer tests for LearnLoop.
Tests TC_013 to TC_018 covering AuthService and QuizService.
All tests use an in-memory SQLite database so no file is created.
"""
import pytest
from sqlmodel import SQLModel, create_engine, Session
from services.auth_service import AuthService
from services.quiz_service import QuizService


@pytest.fixture(name='session')
def session_fixture():
    """Create a fresh in-memory database for each test."""
    from domain.models import (
        User, Quiz, Question, AnswerOption,
        QuizAttempt, StudentAnswer, StudentAnswerSelection
    )
    engine = create_engine('sqlite:///:memory:')
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_hash_password_returns_bcrypt():
    """TC_013: hash_password() should return a valid bcrypt hash."""
    auth = AuthService()
    password = 'lehrer123'
    result = auth.hash_password(password)

    assert result != password
    assert result.startswith('$2')
    assert len(result) == 60
    assert auth.check_password(password, result) is True
    assert auth.check_password('wrong-password', result) is False


def test_check_password_correct():
    """TC_014: check_password() should return True for correct password."""
    auth = AuthService()
    password = 'meinPasswort123'
    stored_hash = auth.hash_password(password)
    result = auth.check_password(password, stored_hash)
    assert result is True


def test_check_password_wrong():
    """TC_015: check_password() should return False for wrong password."""
    auth = AuthService()
    stored_hash = auth.hash_password('richtigesPasswort')
    result = auth.check_password('falschesPasswort', stored_hash)
    assert result is False


def test_login_finds_user(session):
    """TC_016: login() should return the correct User object."""
    from domain.models import User
    auth = AuthService()
    user = User(
        username='testlehrer',
        email='test@learnloop.ch',
        password_hash=auth.hash_password('passwort123'),
        role='teacher'
    )
    session.add(user)
    session.commit()

    result = auth.login(session, 'testlehrer', 'passwort123')
    assert result is not None
    assert result.username == 'testlehrer'
    assert result.role == 'teacher'


def test_get_published_only_returns_published(session):
    """TC_017: get_published() returns only published quizzes."""
    from domain.models import User, Quiz
    quiz_service = QuizService()
    teacher = User(
        username='l', email='l@t.ch',
        password_hash='hash', role='teacher'
    )
    session.add(teacher)
    session.commit()

    q1 = Quiz(
        title='Veroeffentlicht', description='Test',
        is_published=True, teacher_id=teacher.id
    )
    q2 = Quiz(
        title='Entwurf', description='Test',
        is_published=False, teacher_id=teacher.id
    )
    session.add(q1)
    session.add(q2)
    session.commit()

    result = quiz_service.get_published(session)
    assert len(result) == 1
    assert result[0].title == 'Veroeffentlicht'


def test_publish_sets_is_published(session):
    """TC_018: publish() should set is_published to True."""
    from domain.models import User, Quiz
    quiz_service = QuizService()
    teacher = User(
        username='l2', email='l2@t.ch',
        password_hash='hash', role='teacher'
    )
    session.add(teacher)
    session.commit()
    quiz = Quiz(
        title='Test Quiz', description='Test',
        is_published=False, teacher_id=teacher.id
    )
    session.add(quiz)
    session.commit()

    quiz_service.publish(session, quiz)
    result = session.get(Quiz, quiz.id)
    assert result.is_published is True
