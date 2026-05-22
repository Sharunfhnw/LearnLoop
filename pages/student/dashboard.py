from nicegui import ui, app
from sqlmodel import select
from data_access.db import Database
from domain.models import Question
from services.quiz_service import QuizService
from services.attempt_service import AttemptService


def student_dashboard():
    """Render the student dashboard page."""
    ui.query('body').style('background-color:#F8F7F4;margin:0')

    quiz_service = QuizService()
    attempt_service = AttemptService()

    db = Database()
    session = db.get_session()
    student_id = app.storage.user.get('user_id', 1)
    username = app.storage.user.get('username', '')

    # Load data for stat cards
    quizzes = quiz_service.get_published(session)
    attempts = attempt_service.get_attempts_by_student(session, student_id)
    avg = attempt_service.get_average(attempts)

    # --- Header bar ---
    with ui.row().style(
        'width:100%;background:white;padding:16px 24px;'
        'align-items:center;justify-content:space-between;'
        'box-shadow:0 1px 3px rgba(0,0,0,0.08);margin-bottom:24px'
    ):
        with ui.column().style('gap:2px'):
            ui.html(
                'Learn<span style="color:#185FA5">Loop</span> '
                '<span style="font-size:13px;color:#666;font-weight:400">'
                'Student</span>'
            ).style('font-size:18px;font-weight:500')
            ui.label(f'Welcome, {username}').style(
                'font-size:12px;color:#666'
            )
        with ui.row().style('gap:8px'):
            ui.button('Statistics',
                on_click=lambda: ui.navigate.to('/student/statistics')
            ).style('font-size:12px')
            ui.button('Profile',
                on_click=lambda: ui.navigate.to('/profile')
            ).style('font-size:12px')
            ui.button('Logout',
                on_click=lambda: ui.navigate.to('/')
            ).style('font-size:12px')

    with ui.column().style('max-width:900px;margin:0 auto;padding:0 24px'):

        # --- Stat cards (available quizzes, completed, average) ---
        with ui.row().style('gap:16px;margin-bottom:28px;width:100%'):
            for val, label, color in [
                (str(len(quizzes)), 'Available Quizzes', '#3B6D11'),
                (str(len(attempts)), 'Completed', '#3B6D11'),
                (f'{avg:.0f}%', 'Average', '#3B6D11'),
            ]:
                with ui.card().style(
                    'flex:1;padding:20px;border-radius:10px;'
                    'box-shadow:0 1px 3px rgba(0,0,0,0.06)'
                ):
                    ui.label(label).style(
                        'font-size:12px;color:#666;margin-bottom:6px'
                    )
                    ui.label(val).style(
                        f'font-size:32px;font-weight:500;color:{color}'
                    )

        # --- Available quizzes section ---
        ui.label('Available Quizzes').style(
            'font-size:20px;font-weight:500;margin-bottom:16px'
        )

        # Empty state
        if not quizzes:
            with ui.card().style(
                'width:100%;padding:40px;text-align:center;border-radius:12px'
            ):
                ui.label('No quizzes available.').style('color:#666')
            return

        # --- Quiz cards ---
        with ui.row().style('gap:16px;flex-wrap:wrap'):
            for quiz in quizzes:
                questions = session.exec(
                    select(Question).where(Question.quiz_id == quiz.id)
                ).all()

                # Collect question types for badge display
                types_used = set(q.question_type for q in questions)
                type_map = {
                    'single': 'Single Choice',
                    'multiple': 'Multiple Choice',
                    'truefalse': 'True/False'
                }

                with ui.card().style(
                    'min-width:280px;flex:1;padding:20px;border-radius:12px;'
                    'box-shadow:0 1px 3px rgba(0,0,0,0.06)'
                ):
                    ui.label(quiz.title).style(
                        'font-size:15px;font-weight:500;color:#1A1A18;margin-bottom:4px'
                    )
                    ui.label(quiz.description).style(
                        'font-size:12px;color:#666;margin-bottom:10px'
                    )

                    # Question type badges
                    with ui.row().style(
                        'gap:4px;flex-wrap:wrap;margin-bottom:12px'
                    ):
                        for t in types_used:
                            ui.html(
                                f'<span style="background:#F0EDE6;color:#666;'
                                f'padding:3px 8px;border-radius:20px;font-size:10px">'
                                f'{type_map.get(t, t)}</span>'
                            )

                    ui.label(f'{len(questions)} Questions').style(
                        'font-size:12px;color:#999;margin-bottom:12px'
                    )

                    ui.button(
                        '▷ Start Quiz',
                        on_click=lambda q=quiz:
                            ui.navigate.to(f'/student/quiz/{q.id}')
                    ).style(
                        'width:100%;background:#111;color:white;'
                        'border-radius:8px;font-size:13px;padding:12px'
                    )