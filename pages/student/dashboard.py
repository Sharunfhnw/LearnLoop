from nicegui import ui, app
from data_access.db import Database
from services.quiz_service import QuizService
from services.attempt_service import AttemptService


def student_dashboard():
    ui.query('body').style('background-color:#F5F5F7;margin:0')
    quiz_service = QuizService()
    attempt_service = AttemptService()

    with ui.row().style(
        'width:100%;background:white;padding:16px 24px;'
        'align-items:center;justify-content:space-between;'
        'border-bottom:0.5px solid #E5E5E5;margin-bottom:24px'
    ):
        with ui.column().style('gap:2px'):
            ui.html(
                'Learn<span style="color:#185FA5">Loop</span> '
                '<span style="font-size:13px;color:#666;font-weight:400">'
                'Schueler</span>'
            ).style('font-size:18px;font-weight:500')
            username = app.storage.user.get('username', '')
            ui.label(f'Willkommen, {username}').style(
                'font-size:12px;color:#666'
            )
        with ui.row().style('gap:8px'):
            ui.button('Statistik',
                on_click=lambda: ui.navigate.to('/student/statistics')
            ).style('font-size:12px')
            ui.button('Profil',
                on_click=lambda: ui.navigate.to('/profile')
            ).style('font-size:12px')
            ui.button('Abmelden',
                on_click=lambda: ui.navigate.to('/')
            ).style('font-size:12px')

    with ui.column().style('padding:0 24px 24px'):
        db = Database()
        session = db.get_session()
        student_id = app.storage.user.get('user_id', 1)

        # Services verwenden
        quizze = quiz_service.get_published(session)
        attempts = attempt_service.get_attempts_by_student(
            session, student_id
        )
        avg = attempt_service.get_average(attempts)

        # Statistik-Karten
        with ui.row().style(
            'gap:12px;margin-bottom:24px;width:100%'
        ):
            for val, label, color in [
                (str(len(quizze)), 'Verfuegbare Quizze', '#3B6D11'),
                (str(len(attempts)), 'Abgeschlossen', '#3B6D11'),
                (f'{avg:.0f}%', 'Durchschnitt', '#3B6D11')
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

        # Suchleiste
        ui.label('Verfuegbare Quizze').style(
            'font-size:16px;font-weight:500;margin-bottom:12px'
        )
        search = ui.input(
            placeholder='Quiz suchen...'
        ).style(
            'width:100%;margin-bottom:16px;'
            'border-radius:8px;font-size:13px'
        )

        if not quizze:
            ui.label('Keine Quizze verfuegbar').style('color:#666')
            return

        # Quiz-Karten erstellen
        quiz_refs = {}
        with ui.row().style('gap:12px;flex-wrap:wrap'):
            for quiz in quizze:
                with ui.column() as col:
                    with ui.card().style(
                        'min-width:280px;flex:1;'
                        'padding:20px;border-radius:12px'
                    ):
                        ui.label(quiz.title).style(
                            'font-size:15px;font-weight:500;margin-bottom:4px'
                        )
                        ui.label(quiz.description).style(
                            'font-size:12px;color:#666;margin-bottom:12px'
                        )
                        ui.html(
                            '<hr style="border:none;border-top:'
                            '0.5px solid #E5E5E5;margin:10px 0">'
                        )
                        ui.button(
                            'Quiz starten',
                            on_click=lambda q=quiz:
                                ui.navigate.to(
                                    f'/student/quiz/{q.id}'
                                )
                        ).style(
                            'width:100%;background:#111;color:white;'
                            'border-radius:8px;font-size:13px'
                        )
                quiz_refs[quiz.id] = {
                    'col': col,
                    'title': quiz.title
                }

        # Search function — case-insensitive thanks to .lower()
        def filter_quizze():
            term = search.value.lower()
            for qid, data in quiz_refs.items():
                if term in data['title'].lower():
                    data['col'].style('display:block')
                else:
                    data['col'].style('display:none')

        search.on('input', filter_quizze)