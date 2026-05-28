"""Demo data seeder for LearnLoop.
Creates multiple demo users, quizzes, and realistic results.

Demo accounts:
    Teachers: lehrer / lehrer123  |  frau_huber / huber123
    Students: schueler / schueler123  |  max / max123  |  lena / lena123
"""
import bcrypt
from datetime import datetime, timedelta
from sqlmodel import Session, select
from domain.models import User, Quiz, Question, AnswerOption, QuizAttempt, StudentAnswer, StudentAnswerSelection


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_data(session: Session) -> None:
    existing = session.exec(select(User)).first()
    if existing:
        return

    # ── Users ────────────────────────────────────────────────────────────────
    lehrer = User(username='lehrer', email='lehrer@learnloop.ch',
                  password_hash=hash_password('lehrer123'), role='teacher')
    huber = User(username='frau_huber', email='huber@learnloop.ch',
                 password_hash=hash_password('huber123'), role='teacher')
    schueler = User(username='schueler', email='schueler@learnloop.ch',
                    password_hash=hash_password('schueler123'), role='student')
    max_u = User(username='max', email='max@learnloop.ch',
                 password_hash=hash_password('max123'), role='student')
    lena = User(username='lena', email='lena@learnloop.ch',
                password_hash=hash_password('lena123'), role='student')

    for u in [lehrer, huber, schueler, max_u, lena]:
        session.add(u)
    session.commit()

    # ── Quiz 1: Basic Maths (published, teacher) ────────────────────
    q1 = Quiz(title='Mathematik Grundlagen',
              description='Teste dein Wissen in Mathematik',
              is_published=True, teacher_id=lehrer.id)
    session.add(q1)
    session.commit()

    # Single Choice
    f1 = Question(text='Was ist 2 + 2?', quiz_id=q1.id, question_type='single')
    session.add(f1); session.commit()
    session.add_all([
        AnswerOption(text='3', is_correct=False, question_id=f1.id),
        AnswerOption(text='4', is_correct=True,  question_id=f1.id),
        AnswerOption(text='5', is_correct=False, question_id=f1.id),
        AnswerOption(text='6', is_correct=False, question_id=f1.id),
    ]); session.commit()

    # True/False — correct answer is Wahr
    f2 = Question(text='10 ist eine gerade Zahl.', quiz_id=q1.id, question_type='truefalse')
    session.add(f2); session.commit()
    session.add_all([
        AnswerOption(text='Wahr',   is_correct=True,  question_id=f2.id),
        AnswerOption(text='Falsch', is_correct=False, question_id=f2.id),
    ]); session.commit()

    # Multiple Choice — whole point only if ALL correct selected
    f3 = Question(text='Welche Zahlen sind Primzahlen?', quiz_id=q1.id, question_type='multiple')
    session.add(f3); session.commit()
    session.add_all([
        AnswerOption(text='2', is_correct=True,  question_id=f3.id),
        AnswerOption(text='3', is_correct=True,  question_id=f3.id),
        AnswerOption(text='4', is_correct=False, question_id=f3.id),
        AnswerOption(text='7', is_correct=True,  question_id=f3.id),
    ]); session.commit()

    # Single Choice
    f4 = Question(text='Was ist die Quadratwurzel von 144?', quiz_id=q1.id, question_type='single')
    session.add(f4); session.commit()
    session.add_all([
        AnswerOption(text='10', is_correct=False, question_id=f4.id),
        AnswerOption(text='12', is_correct=True,  question_id=f4.id),
        AnswerOption(text='14', is_correct=False, question_id=f4.id),
        AnswerOption(text='16', is_correct=False, question_id=f4.id),
    ]); session.commit()

    # True/False — correct answer is Falsch
    f5 = Question(text='Die Zahl Pi ist genau 3.', quiz_id=q1.id, question_type='truefalse')
    session.add(f5); session.commit()
    session.add_all([
        AnswerOption(text='Wahr',   is_correct=False, question_id=f5.id),
        AnswerOption(text='Falsch', is_correct=True,  question_id=f5.id),
    ]); session.commit()

    # ── Quiz 2: English vocabulary (published, teacher) ────────────────────────
    q2 = Quiz(title='Englisch Vokabeln',
              description='Wichtige englische Vokabeln für den Alltag',
              is_published=True, teacher_id=lehrer.id)
    session.add(q2); session.commit()

    g1 = Question(text='Was bedeutet "apple"?', quiz_id=q2.id, question_type='single')
    session.add(g1); session.commit()
    session.add_all([
        AnswerOption(text='Birne',  is_correct=False, question_id=g1.id),
        AnswerOption(text='Apfel',  is_correct=True,  question_id=g1.id),
        AnswerOption(text='Orange', is_correct=False, question_id=g1.id),
        AnswerOption(text='Traube', is_correct=False, question_id=g1.id),
    ]); session.commit()

    g2 = Question(text='Was bedeutet "happy"?', quiz_id=q2.id, question_type='single')
    session.add(g2); session.commit()
    session.add_all([
        AnswerOption(text='Traurig',    is_correct=False, question_id=g2.id),
        AnswerOption(text='Wütend',     is_correct=False, question_id=g2.id),
        AnswerOption(text='Glücklich',  is_correct=True,  question_id=g2.id),
        AnswerOption(text='Müde',       is_correct=False, question_id=g2.id),
    ]); session.commit()

    g3 = Question(text='"School" ist ein deutsches Wort.', quiz_id=q2.id, question_type='truefalse')
    session.add(g3); session.commit()
    session.add_all([
        AnswerOption(text='Wahr',   is_correct=False, question_id=g3.id),
        AnswerOption(text='Falsch', is_correct=True,  question_id=g3.id),
    ]); session.commit()

    g4 = Question(text='Welche Wörter bedeuten "gross"?', quiz_id=q2.id, question_type='multiple')
    session.add(g4); session.commit()
    session.add_all([
        AnswerOption(text='big',    is_correct=True,  question_id=g4.id),
        AnswerOption(text='large',  is_correct=True,  question_id=g4.id),
        AnswerOption(text='small',  is_correct=False, question_id=g4.id),
        AnswerOption(text='tiny',   is_correct=False, question_id=g4.id),
    ]); session.commit()

    # ── Quiz 3: Geography (draft, for teachers) ────────────────────────────────────
    q3 = Quiz(title='Geografie Europa',
              description='Hauptstädte und Länder in Europa',
              is_published=False, teacher_id=lehrer.id)
    session.add(q3); session.commit()

    h1 = Question(text='Was ist die Hauptstadt von Frankreich?', quiz_id=q3.id, question_type='single')
    session.add(h1); session.commit()
    session.add_all([
        AnswerOption(text='Lyon',   is_correct=False, question_id=h1.id),
        AnswerOption(text='Paris',  is_correct=True,  question_id=h1.id),
        AnswerOption(text='Nizza',  is_correct=False, question_id=h1.id),
        AnswerOption(text='Bordeaux', is_correct=False, question_id=h1.id),
    ]); session.commit()

    h2 = Question(text='Die Schweiz ist Mitglied der EU.', quiz_id=q3.id, question_type='truefalse')
    session.add(h2); session.commit()
    session.add_all([
        AnswerOption(text='Wahr',   is_correct=False, question_id=h2.id),
        AnswerOption(text='Falsch', is_correct=True,  question_id=h2.id),
    ]); session.commit()

    # ── Quiz 4: Natural Sciences (published by frau_huber) ──────────────────
    q4 = Quiz(title='Naturwissenschaften',
              description='Physik, Chemie und Biologie Grundlagen',
              is_published=True, teacher_id=huber.id)
    session.add(q4); session.commit()

    n1 = Question(text='Welches Element hat das Symbol "O"?', quiz_id=q4.id, question_type='single')
    session.add(n1); session.commit()
    session.add_all([
        AnswerOption(text='Gold',       is_correct=False, question_id=n1.id),
        AnswerOption(text='Sauerstoff', is_correct=True,  question_id=n1.id),
        AnswerOption(text='Osmium',     is_correct=False, question_id=n1.id),
        AnswerOption(text='Silber',     is_correct=False, question_id=n1.id),
    ]); session.commit()

    n2 = Question(text='Wasser besteht aus Wasserstoff und Sauerstoff.', quiz_id=q4.id, question_type='truefalse')
    session.add(n2); session.commit()
    session.add_all([
        AnswerOption(text='Wahr',   is_correct=True,  question_id=n2.id),
        AnswerOption(text='Falsch', is_correct=False, question_id=n2.id),
    ]); session.commit()

    n3 = Question(text='Welche sind erneuerbare Energiequellen?', quiz_id=q4.id, question_type='multiple')
    session.add(n3); session.commit()
    session.add_all([
        AnswerOption(text='Solarenergie', is_correct=True,  question_id=n3.id),
        AnswerOption(text='Windenergie',  is_correct=True,  question_id=n3.id),
        AnswerOption(text='Kohle',        is_correct=False, question_id=n3.id),
        AnswerOption(text='Erdöl',        is_correct=False, question_id=n3.id),
    ]); session.commit()

    n4 = Question(text='Bei welcher Temperatur siedet Wasser (normal)?', quiz_id=q4.id, question_type='single')
    session.add(n4); session.commit()
    session.add_all([
        AnswerOption(text='80°C',  is_correct=False, question_id=n4.id),
        AnswerOption(text='90°C',  is_correct=False, question_id=n4.id),
        AnswerOption(text='100°C', is_correct=True,  question_id=n4.id),
        AnswerOption(text='110°C', is_correct=False, question_id=n4.id),
    ]); session.commit()

    # ── Demo Attempts ─────────────────────────────────────────────────────────
    # schueler: Quiz 1 — 4/5 correct
    def get_correct_option(session, question_id):
        opts = session.exec(
            select(AnswerOption).where(AnswerOption.question_id == question_id)
        ).all()
        return next((o for o in opts if o.is_correct), opts[0])

    def get_wrong_option(session, question_id):
        opts = session.exec(
            select(AnswerOption).where(AnswerOption.question_id == question_id)
        ).all()
        return next((o for o in opts if not o.is_correct), opts[0])

    def add_student_answer(session, attempt_id, question_id, option_id, is_correct):
        answer = StudentAnswer(
            attempt_id=attempt_id,
            question_id=question_id,
            is_correct=is_correct,
        )
        session.add(answer)
        session.commit()
        session.add(StudentAnswerSelection(
            student_answer_id=answer.id,
            answer_option_id=option_id,
        ))

    # schueler: Quiz 1 (Mathe), 4 of 5 correct
    a1 = QuizAttempt(student_id=schueler.id, quiz_id=q1.id, score=4, max_score=5,
                     completed_at=datetime.now() - timedelta(days=3))
    session.add(a1); session.commit()
    q1_questions = [f1, f2, f3, f4, f5]
    for i, frage in enumerate(q1_questions):
        correct = i < 4  # first 4 correct, last wrong
        opt = get_correct_option(session, frage.id) if correct else get_wrong_option(session, frage.id)
        add_student_answer(session, a1.id, frage.id, opt.id, correct)
    session.commit()

    # schueler: Quiz 2 (Englisch), 2 of 4 correct
    a2 = QuizAttempt(student_id=schueler.id, quiz_id=q2.id, score=2, max_score=4,
                     completed_at=datetime.now() - timedelta(days=1))
    session.add(a2); session.commit()
    q2_questions = [g1, g2, g3, g4]
    for i, frage in enumerate(q2_questions):
        correct = i < 2
        opt = get_correct_option(session, frage.id) if correct else get_wrong_option(session, frage.id)
        add_student_answer(session, a2.id, frage.id, opt.id, correct)
    session.commit()

    # max: Quiz 1 (Mathe), 5/5
    a3 = QuizAttempt(student_id=max_u.id, quiz_id=q1.id, score=5, max_score=5,
                     completed_at=datetime.now() - timedelta(days=2))
    session.add(a3); session.commit()
    for frage in q1_questions:
        opt = get_correct_option(session, frage.id)
        add_student_answer(session, a3.id, frage.id, opt.id, True)
    session.commit()

    # max: Quiz 4 (Natur), 3/4
    a4 = QuizAttempt(student_id=max_u.id, quiz_id=q4.id, score=3, max_score=4,
                     completed_at=datetime.now() - timedelta(hours=5))
    session.add(a4); session.commit()
    q4_questions = [n1, n2, n3, n4]
    for i, frage in enumerate(q4_questions):
        correct = i != 2  # n3 (multiple) wrong
        opt = get_correct_option(session, frage.id) if correct else get_wrong_option(session, frage.id)
        add_student_answer(session, a4.id, frage.id, opt.id, correct)
    session.commit()

    # lena: Quiz 2 (Englisch), 4/4
    a5 = QuizAttempt(student_id=lena.id, quiz_id=q2.id, score=4, max_score=4,
                     completed_at=datetime.now() - timedelta(days=1))
    session.add(a5); session.commit()
    for frage in q2_questions:
        opt = get_correct_option(session, frage.id)
        add_student_answer(session, a5.id, frage.id, opt.id, True)
    session.commit()

    # lena: Quiz 1 (Mathe), 3/5
    a6 = QuizAttempt(student_id=lena.id, quiz_id=q1.id, score=3, max_score=5,
                     completed_at=datetime.now() - timedelta(hours=2))
    session.add(a6); session.commit()
    for i, frage in enumerate(q1_questions):
        correct = i < 3
        opt = get_correct_option(session, frage.id) if correct else get_wrong_option(session, frage.id)
        add_student_answer(session, a6.id, frage.id, opt.id, correct)
    session.commit()

    print('LearnLoop demo data created!')
    print('  Teacher 1: lehrer / lehrer123')
    print('  Teacher 2: frau_huber / huber123')
    print('  Student 1: schueler / schueler123')
    print('  Student 2: max / max123')
    print('  Student 3: lena / lena123')
