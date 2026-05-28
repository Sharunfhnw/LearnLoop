import pytest
from sqlmodel import SQLModel, create_engine, Session, select
from services.auth_service import AuthService


@pytest.fixture(name='session')
def session_fixture():
    from domain.models import (
        User, Quiz, Question, AnswerOption,
        QuizAttempt, StudentAnswer, StudentAnswerSelection
    )
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_user_speichern(session):
    """TC_007: User wird korrekt gespeichert."""
    from domain.models import User
    auth = AuthService()
    user = User(
        username='testlehrer',
        email='t@t.ch',
        password_hash=auth.hash_password('pass'),
        role='teacher'
    )
    session.add(user)
    session.commit()
    result = session.exec(select(User)).first()
    assert result is not None
    assert result.role == 'teacher'
    assert result.password_hash != 'pass'
    assert auth.check_password('pass', result.password_hash) is True


def test_quiz_speichern(session):
    """TC_008: Quiz wird korrekt gespeichert."""
    from domain.models import User, Quiz
    auth = AuthService()
    user = User(
        username='lehrer1',
        email='l@t.ch',
        password_hash=auth.hash_password('p'),
        role='teacher'
    )
    session.add(user)
    session.commit()
    quiz = Quiz(
        title='Mathe',
        description='Test',
        is_published=False,
        teacher_id=user.id
    )
    session.add(quiz)
    session.commit()
    result = session.exec(select(Quiz)).first()
    assert result is not None
    assert result.is_published is False


def test_leere_db(session):
    """TC_009: Leere Datenbank gibt keine Quizze zurueck."""
    from domain.models import Quiz
    result = session.exec(select(Quiz)).all()
    assert len(result) == 0
