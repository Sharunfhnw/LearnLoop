from nicegui import ui, app
from data_access.db import Database
from services.attempt_service import AttemptService
from domain.models import Quiz


def student_statistics():
    ui.query('body').style('background-color:#F5F5F7;margin:0')
    attempt_service = AttemptService()

    with ui.row().style(
        'width:100%;background:white;padding:16px 24px;'
        'align-items:center;gap:12px;'
        'border-bottom:0.5px solid #E5E5E5;margin-bottom:24px'
    ):
        ui.button('← Zurueck',
            on_click=lambda: ui.navigate.to('/student/dashboard')
        ).style('font-size:12px')
        ui.label('Meine Statistik').style(
            'font-size:16px;font-weight:500'
        )

    db = Database()
    session = db.get_session()
    student_id = app.storage.user.get('user_id', 1)

    # Use AttemptService
    attempts = attempt_service.get_attempts_by_student(
        session, student_id
    )

    with ui.column().style(
        'padding:0 24px 24px;max-width:700px'
    ):
        if not attempts:
            ui.label(
                'Noch keine Quizze gemacht'
            ).style('color:#666')
            return

        # Services for calculations
        avg = attempt_service.get_average(attempts)
        best = attempt_service.get_best(attempts)
        total = len(attempts)

        with ui.row().style(
            'gap:12px;margin-bottom:24px;width:100%'
        ):
            for val, label, color in [
                (str(total), 'Quizze gemacht', '#3B6D11'),
                (f'{avg:.0f}%', 'Durchschnitt', '#3B6D11'),
                (f'{best:.0f}%', 'Bestes Resultat', '#3B6D11')
            ]:
                with ui.card().style(
                    'flex:1;padding:16px;border-radius:8px'
                ):
                    ui.label(label).style(
                        'font-size:12px;color:#666;margin-bottom:6px'
                    )
                    ui.label(val).style(
                        f'font-size:28px;font-weight:500;color:{color}'
                    )

        with ui.card().style(
            'width:100%;padding:16px;border-radius:12px'
        ):
            ui.label('Alle Versuche').style(
                'font-size:14px;font-weight:500;margin-bottom:14px'
            )
            for attempt in attempts:
                quiz = session.get(Quiz, attempt.quiz_id)
                pct = attempt_service.calculate_percentage(
                    attempt.score, attempt.max_score
                )
                color = '#3B6D11' if pct >= 60 else '#A32D2D'
                with ui.row().style(
                    'width:100%;justify-content:space-between;'
                    'padding:10px 0;border-bottom:0.5px solid #E5E5E5;'
                    'align-items:center'
                ):
                    ui.label(
                        quiz.title if quiz else '-'
                    ).style('font-size:13px')
                    ui.label(
                        f'{attempt.score:.1f}/{attempt.max_score:.1f}'
                    ).style('font-size:12px;color:#666')
                    ui.label(f'{pct:.0f}%').style(
                        f'font-size:13px;font-weight:500;color:{color}'
                    )
                    ui.button('Details',
                        on_click=lambda a=attempt:
                            ui.navigate.to(
                                f'/student/results/{a.id}'
                            )
                    ).style('font-size:11px')