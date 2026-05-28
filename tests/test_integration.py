import pytest

from sqlmodel import SQLModel, create_engine, Session, select
from services.auth_service import AuthService
from services.quiz_service import QuizService


@pytest.fixture(name='session')
def session_fixture():
    from domain.models import (
        User, Quiz, Question, AnswerOption,
        QuizAttempt, StudentAnswer, StudentAnswerSelection
    )
    engine = create_engine('sqlite:///:memory:')
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_quiz_veroeffentlichen(session):
    """TC_010: Quiz veroeffentlichen via QuizService."""
    from domain.models import User, Quiz
    auth = AuthService()
    quiz_service = QuizService()

    lehrer = User(
        username='l',
        email='l@t.ch',
        password_hash=auth.hash_password('p'),
        role='teacher'
    )
    session.add(lehrer)
    session.commit()
    quiz = Quiz(
        title='Test',
        description='Test',
        is_published=False,
        teacher_id=lehrer.id
    )
    session.add(quiz)
    session.commit()

    quiz_service.publish(session, quiz)
    result = session.get(Quiz, quiz.id)
    assert result.is_published is True


def test_quiz_loesen(session):
    """TC_011: Schueler loest Quiz, Attempt gespeichert."""
    from domain.models import User, Quiz, QuizAttempt
    auth = AuthService()

    lehrer = User(
        username='l2',
        email='l2@t.ch',
        password_hash=auth.hash_password('p'),
        role='teacher'
    )
    schueler = User(
        username='s1',
        email='s1@t.ch',
        password_hash=auth.hash_password('p'),
        role='student'
    )
    session.add(lehrer)
    session.add(schueler)
    session.commit()
    quiz = Quiz(
        title='Mathe',
        description='Test',
        is_published=True,
        teacher_id=lehrer.id
    )
    session.add(quiz)
    session.commit()
    attempt = QuizAttempt(
        student_id=schueler.id,
        quiz_id=quiz.id,
        score=1,
        max_score=1
    )
    session.add(attempt)
    session.commit()
    result = session.get(QuizAttempt, attempt.id)
    assert result.score == 1


def test_quiz_zweimal_loesen(session):
    """TC_012: Schueler loest Quiz zweimal."""
    from domain.models import User, Quiz, QuizAttempt
    auth = AuthService()

    lehrer = User(
        username='l3',
        email='l3@t.ch',
        password_hash=auth.hash_password('p'),
        role='teacher'
    )
    schueler = User(
        username='s2',
        email='s2@t.ch',
        password_hash=auth.hash_password('p'),
        role='student'
    )
    session.add(lehrer)
    session.add(schueler)
    session.commit()
    quiz = Quiz(
        title='Englisch',
        description='Test',
        is_published=True,
        teacher_id=lehrer.id
    )
    session.add(quiz)
    session.commit()
    session.add(QuizAttempt(
        student_id=schueler.id,
        quiz_id=quiz.id,
        score=2,
        max_score=5
    ))
    session.add(QuizAttempt(
        student_id=schueler.id,
        quiz_id=quiz.id,
        score=4,
        max_score=5
    ))
    session.commit()
    attempts = session.exec(select(QuizAttempt).where(
        QuizAttempt.student_id == schueler.id)).all()
    assert len(attempts) == 2
