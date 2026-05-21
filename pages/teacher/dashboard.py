from nicegui import ui, app
from sqlmodel import select
from data_access.db import Database
from domain.models import Quiz, Question, QuizAttempt


def teacher_dashboard(teacher_id: int):
    """Render the teacher dashboard page."""
    ui.query('body').style('background-color:#F8F7F4;margin:0')

    db = Database()
    session = db.get_session()
    username = app.storage.user.get('username', 'Teacher')

    # Load all quizzes for this teacher
    quizzes = session.exec(
        select(Quiz).where(Quiz.teacher_id == teacher_id)
    ).all()

    # Count total questions across all quizzes
    total_questions = 0
    for q in quizzes:
        total_questions += len(session.exec(
            select(Question).where(Question.quiz_id == q.id)
        ).all())

    # Count total student attempts across all quizzes
    total_attempts = 0
    for q in quizzes:
        total_attempts += len(session.exec(
            select(QuizAttempt).where(QuizAttempt.quiz_id == q.id)
        ).all())

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
                'Teacher</span>'
            ).style('font-size:18px;font-weight:500')
            ui.label(f'Welcome back, {username}').style(
                'font-size:12px;color:#666'
            )
        with ui.row().style('gap:8px'):
            ui.button('Profile',
                on_click=lambda: ui.navigate.to('/profile')
            ).style('font-size:12px')
            ui.button('Logout',
                on_click=lambda: ui.navigate.to('/')
            ).style('font-size:12px')

    with ui.column().style(
        'max-width:900px;margin:0 auto;padding:0 24px'
    ):
        # --- Stat cards (total quizzes, questions, attempts) ---
        with ui.row().style('gap:16px;margin-bottom:28px;width:100%'):
            for val, label, color in [
                (str(len(quizzes)), 'Total Quizzes', '#185FA5'),
                (str(total_questions), 'Total Questions', '#185FA5'),
                (str(total_attempts), 'Student Attempts', '#185FA5'),
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

        # --- Section header with "New Quiz" button ---
        with ui.row().style(
            'width:100%;align-items:center;'
            'justify-content:space-between;margin-bottom:16px'
        ):
            ui.label('My Quizzes').style('font-size:20px;font-weight:500')
            ui.button('+ New Quiz',
                on_click=lambda: ui.navigate.to('/teacher/create')
            ).style(
                'background:#111;color:white;border-radius:8px;font-size:13px'
            )

        # Empty state
        if not quizzes:
            with ui.card().style(
                'width:100%;padding:40px;text-align:center;border-radius:12px'
            ):
                ui.label('No quizzes created yet.').style('color:#666')
            return

        # --- Quiz cards ---
        with ui.row().style('gap:16px;flex-wrap:wrap'):
            for quiz in quizzes:
                questions = session.exec(
                    select(Question).where(Question.quiz_id == quiz.id)
                ).all()
                attempts = session.exec(
                    select(QuizAttempt).where(QuizAttempt.quiz_id == quiz.id)
                ).all()

                # Calculate average score percentage
                avg_pct = None
                if attempts:
                    avg_pct = round(
                        sum(
                            a.score / a.max_score * 100
                            for a in attempts if a.max_score > 0
                        ) / len(attempts)
                    )

                with ui.card().style(
                    'min-width:300px;flex:1;padding:20px;border-radius:12px;'
                    'box-shadow:0 1px 3px rgba(0,0,0,0.06)'
                ):
                    ui.label(quiz.title).style(
                        'font-size:15px;font-weight:500;color:#1A1A18'
                    )
                    ui.label(quiz.description).style(
                        'font-size:12px;color:#666;margin-top:2px;margin-bottom:10px'
                    )

                    # Question type badges derived from actual questions
                    types_used = set(q.question_type for q in questions)
                    type_map = {
                        'single': 'Single Choice',
                        'multiple': 'Multiple Choice',
                        'truefalse': 'True/False'
                    }
                    with ui.row().style(
                        'gap:4px;flex-wrap:wrap;margin-bottom:12px'
                    ):
                        for t in types_used:
                            ui.html(
                                f'<span style="background:#F0EDE6;color:#666;'
                                f'padding:3px 8px;border-radius:20px;font-size:10px">'
                                f'{type_map.get(t, t)}</span>'
                            )

                    # Stats row: questions / attempts / average
                    with ui.row().style(
                        'width:100%;justify-content:space-between;'
                        'padding:10px 0;border-top:0.5px solid #E5E5E5;'
                        'border-bottom:0.5px solid #E5E5E5;margin-bottom:12px'
                    ):
                        ui.label(f'{len(questions)} Questions').style(
                            'font-size:12px;color:#666'
                        )
                        ui.label(f'{len(attempts)} Attempts').style(
                            'font-size:12px;color:#666'
                        )
                        if avg_pct is not None:
                            ui.label(f'{avg_pct}% Ø').style(
                                'font-size:12px;font-weight:500;color:#3B6D11'
                            )
                        else:
                            ui.label('-').style('font-size:12px;color:#999')

                    # Action buttons: results + publish/status
                    with ui.row().style('gap:8px;align-items:center'):
                        ui.button('Results',
                            on_click=lambda q=quiz:
                                ui.navigate.to(f'/teacher/results/{q.id}')
                        ).style(
                            'flex:1;background:white;color:#1A1A18;'
                            'border:1.5px solid #E5E5E5;border-radius:6px;font-size:12px'
                        )

                        if quiz.is_published:
                            ui.html(
                                '<span style="background:#D4EDDA;color:#3B6D11;'
                                'padding:5px 12px;border-radius:20px;font-size:11px;'
                                'font-weight:500">Published</span>'
                            )
                        else:
                            def publish(q=quiz):
                                """Publish the quiz so students can see it."""
                                q.is_published = True
                                session.add(q)
                                session.commit()
                                ui.notify('Quiz published!', color='positive')
                                ui.navigate.to('/teacher/dashboard')

                            ui.button('Publish',
                                on_click=publish
                            ).style(
                                'background:white;color:#1A1A18;'
                                'border:1.5px solid #E5E5E5;border-radius:6px;font-size:12px'
                            )
                            ui.html(
                                '<span style="background:#F0EDE6;color:#666;'
                                'padding:5px 12px;border-radius:20px;font-size:11px">'
                                'Draft</span>'
                            )