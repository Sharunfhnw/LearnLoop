from nicegui import ui, app
from data_access.db import Database
from services.attempt_service import AttemptService
from domain.models import Quiz


def student_statistics():
    """Student statistics page — German UI, desktop layout, whole numbers."""
    ui.query('body').style('background-color:#F5F5F7;margin:0')

    attempt_service = AttemptService()

    with ui.row().style(
        'width:100%;background:white;padding:14px 40px;'
        'align-items:center;gap:16px;'
        'border-bottom:1px solid #E5E5E5;box-sizing:border-box'
    ):
        with ui.button(on_click=lambda: ui.navigate.to('/student/dashboard')).style(
            'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px'
        ).props('no-caps flat'):
            ui.html('&#8592; Zurück')
        ui.label('Meine Statistik').style('font-size:18px;font-weight:700;color:#1A1A18')

    db = Database()
    session = db.get_session()
    student_id = app.storage.user.get('user_id', 1)
    attempts = attempt_service.get_attempts_by_student(session, student_id)

    with ui.column().style('max-width:900px;margin:32px auto;padding:0 40px;width:100%;box-sizing:border-box;gap:24px'):

        if not attempts:
            with ui.card().style('width:100%;padding:48px;text-align:center;border-radius:12px;background:white'):
                ui.html('&#127942;').style('font-size:40px;color:#ccc')
                ui.label('Noch keine Quizze gemacht.').style('color:#999;margin-top:8px')
            return

        avg = attempt_service.get_average(attempts)
        best = attempt_service.get_best(attempts)
        total = len(attempts)

        # Stat cards
        with ui.row().style('gap:16px;width:100%'):
            for val, label in [
                (str(total), 'Quizze gemacht'),
                (f'{avg}%', 'Durchschnitt'),
                (f'{best}%', 'Bestes Resultat'),
            ]:
                with ui.card().style(
                    'flex:1;padding:24px 28px;border-radius:12px;background:#EAF3DE;box-shadow:none'
                ):
                    ui.label(label).style('font-size:13px;color:#3B6D11;font-weight:500;margin-bottom:8px')
                    ui.label(val).style('font-size:40px;font-weight:700;color:#3B6D11')

        # All attempts table
        with ui.card().style('width:100%;padding:28px;border-radius:14px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.07)'):
            ui.label('Alle Versuche').style('font-size:16px;font-weight:700;margin-bottom:20px')

            # Table header
            with ui.row().style('width:100%;padding:0 8px 12px;border-bottom:1px solid #F0F0F0'):
                ui.label('Quiz').style('flex:3;font-size:12px;color:#999;font-weight:600')
                ui.label('Punkte').style('flex:1;font-size:12px;color:#999;font-weight:600')
                ui.label('%').style('flex:1;font-size:12px;color:#999;font-weight:600')
                ui.element('div').style('flex:1')

            for attempt in attempts:
                quiz = session.get(Quiz, attempt.quiz_id)
                pct = attempt_service.calculate_percentage(attempt.score, attempt.max_score)
                color = '#3B6D11' if pct >= 60 else '#A32D2D'

                with ui.row().style(
                    'width:100%;padding:14px 8px;border-bottom:0.5px solid #F5F5F5;align-items:center'
                ):
                    ui.label(quiz.title if quiz else '-').style('flex:3;font-size:14px;font-weight:500;color:#1A1A18')
                    ui.label(f'{attempt.score}/{attempt.max_score}').style('flex:1;font-size:13px;color:#888')
                    ui.label(f'{pct}%').style(f'flex:1;font-size:14px;font-weight:700;color:{color}')
                    with ui.button(
                        on_click=lambda a=attempt: ui.navigate.to(f'/student/results/{a.id}')
                    ).style(
                        'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:12px;padding:6px 14px'
                    ).props('no-caps flat'):
                        ui.label('Details')
