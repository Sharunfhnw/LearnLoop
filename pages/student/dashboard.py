from nicegui import ui, app
from sqlmodel import select
from data_access.db import Database
from domain.models import Question
from services.quiz_service import QuizService
from services.attempt_service import AttemptService


def student_dashboard():
    """Student dashboard — Desktop layout, German UI, with search."""
    ui.query('body').style('background-color:#F5F5F7;margin:0;padding:0')

    quiz_service = QuizService()
    attempt_service = AttemptService()

    db = Database()
    session = db.get_session()
    student_id = app.storage.user.get('user_id', 1)
    username = app.storage.user.get('username', '')

    quizzes = quiz_service.get_published(session)
    attempts = attempt_service.get_attempts_by_student(session, student_id)
    avg = attempt_service.get_average(attempts)

    # ── Header ───────────────────────────────────────────────────────────────
    with ui.row().style(
        'width:100%;background:white;padding:14px 40px;'
        'align-items:center;justify-content:space-between;'
        'box-shadow:0 1px 3px rgba(0,0,0,0.08);box-sizing:border-box'
    ):
        with ui.column().style('gap:1px'):
            ui.html(
                'Learn<span style="color:#185FA5">Loop</span>'
                '<span style="font-size:13px;color:#888;font-weight:400;margin-left:8px">Schüler</span>'
            ).style('font-size:20px;font-weight:700;color:#1A1A18')
            ui.label(f'Willkommen, {username}').style('font-size:12px;color:#888')
        with ui.row().style('gap:10px;align-items:center'):
            with ui.button(on_click=lambda: ui.navigate.to('/student/statistics')).style(
                'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px'
            ).props('no-caps flat'):
                ui.html('&#9783; Statistik')
            with ui.button(on_click=lambda: ui.navigate.to('/profile')).style(
                'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px'
            ).props('no-caps flat'):
                ui.html('&#128100; Profil')
            with ui.button(on_click=lambda: ui.navigate.to('/')).style(
                'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px'
            ).props('no-caps flat'):
                ui.html('&#8594;&#xFE0E; Abmelden')

    with ui.column().style('max-width:1100px;margin:32px auto;padding:0 40px;width:100%;box-sizing:border-box'):

        # Stat cards
        with ui.row().style('gap:16px;margin-bottom:32px;width:100%'):
            for icon, val, label in [
                ('&#128216;', str(len(quizzes)), 'Verfügbare Quizze'),
                ('&#127942;', str(len(attempts)), 'Abgeschlossen'),
                ('&#37;', f'{avg}%', 'Durchschnitt'),
            ]:
                with ui.card().style(
                    'flex:1;padding:24px 28px;border-radius:12px;'
                    'background:#EAF3DE;box-shadow:none'
                ):
                    ui.html(f'{icon} <span style="font-size:13px;color:#3B6D11;font-weight:500">{label}</span>').style('margin-bottom:8px')
                    ui.label(val).style('font-size:40px;font-weight:700;color:#3B6D11')

        # Section header + search
        with ui.row().style('width:100%;align-items:center;justify-content:space-between;margin-bottom:20px'):
            ui.label('Verfügbare Quizze').style('font-size:22px;font-weight:700;color:#1A1A18')
            search_input = ui.input(placeholder='🔍  Quiz suchen...').style(
                'width:260px;font-size:13px;background:white;border-radius:8px'
            ).props('outlined dense')

        cards_container = ui.column().style('width:100%;gap:0')

        def render_cards():
            cards_container.clear()
            sq = search_input.value.lower().strip()
            filtered = [q for q in quizzes if sq in q.title.lower() or sq in q.description.lower()] if sq else quizzes

            if not filtered:
                with cards_container:
                    with ui.card().style('width:100%;padding:48px;text-align:center;border-radius:12px;background:white'):
                        ui.html('&#128216;').style('font-size:40px;color:#ccc')
                        ui.label('Keine Quizze gefunden.' if sq else 'Keine Quizze verfügbar.').style('color:#999;margin-top:8px')
                return

            with cards_container:
                with ui.row().style('gap:20px;flex-wrap:wrap;width:100%'):
                    for quiz in filtered:
                        questions = session.exec(select(Question).where(Question.quiz_id == quiz.id)).all()
                        types_used = list(dict.fromkeys(q.question_type for q in questions))
                        type_map = {'single': 'Single Choice', 'multiple': 'Multiple Choice', 'truefalse': 'True/False'}

                        with ui.card().style(
                            'min-width:320px;flex:1;max-width:500px;padding:24px;border-radius:14px;'
                            'background:white;box-shadow:0 1px 4px rgba(0,0,0,0.07)'
                        ):
                            ui.label(quiz.title).style('font-size:17px;font-weight:700;color:#1A1A18;margin-bottom:4px')
                            ui.label(quiz.description).style('font-size:12px;color:#888;margin-bottom:12px')

                            with ui.row().style('gap:6px;flex-wrap:wrap;margin-bottom:14px'):
                                for t in types_used:
                                    ui.html(
                                        f'<span style="background:#F0EDE6;color:#666;'
                                        f'padding:3px 10px;border-radius:20px;font-size:11px;border:1px solid #E8E4DC">'
                                        f'{type_map.get(t, t)}</span>'
                                    )

                            ui.label(f'{len(questions)} Fragen').style(
                                'font-size:12px;color:#999;'
                                'padding-top:10px;border-top:1px solid #F0F0F0;margin-bottom:14px'
                            )

                            with ui.button(
                                on_click=lambda q=quiz: ui.navigate.to(f'/student/quiz/{q.id}')
                            ).style(
                                'width:100%;background:#1A1A18;color:white;'
                                'border-radius:10px;font-size:14px;padding:14px'
                            ).props('no-caps flat'):
                                ui.html('&#9654; Quiz starten')

        render_cards()
        search_input.on_value_change(lambda _: render_cards())
