from nicegui import ui
from data_access.db import Database
from domain.models import User, Quiz
from services.quiz_service import QuizService
from services.attempt_service import AttemptService


def quiz_results(quiz_id: int):
    """Detailed teacher view of student results for a quiz."""
    ui.query('body').style('background-color:#F5F5F7;margin:0')

    db = Database()
    session = db.get_session()
    quiz_service = QuizService()
    attempt_service = AttemptService()
    quiz = session.get(Quiz, quiz_id)
    attempts = attempt_service.get_attempts_by_quiz(session, quiz_id)
    questions = quiz_service.get_questions(session, quiz_id)

    # ── Header ───────────────────────────────────────────────────────────────
    with ui.row().style(
        'width:100%;background:white;padding:14px 40px;'
        'align-items:center;gap:16px;'
        'box-shadow:0 1px 3px rgba(0,0,0,0.08);box-sizing:border-box'
    ):
        with ui.button(on_click=lambda: ui.navigate.to('/teacher/dashboard')).style(
            'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px'
        ).props('no-caps flat'):
            ui.html('&#8592; Zurück')
        ui.label(f'Auswertungen: {quiz.title}').style('font-size:18px;font-weight:700;color:#1A1A18')

    with ui.column().style('max-width:1000px;margin:32px auto;padding:0 40px;width:100%;box-sizing:border-box'):

        if not attempts:
            with ui.card().style('width:100%;padding:48px;text-align:center;border-radius:12px;background:white'):
                ui.html('&#128202;').style('font-size:40px;color:#ccc')
                ui.label('Noch keine Schüler-Versuche vorhanden.').style('color:#999;margin-top:8px')
            return

        avg = attempt_service.get_average(attempts)

        # Summary cards
        with ui.row().style('gap:16px;margin-bottom:28px;width:100%'):
            for val, label, color in [
                (str(len(attempts)), 'Versuche gesamt', '#185FA5'),
                (f'{avg}%', 'Durchschnitt', '#3B6D11'),
                (str(len(questions)), 'Fragen im Quiz', '#185FA5'),
            ]:
                with ui.card().style(
                    'flex:1;padding:20px 24px;border-radius:12px;'
                    'background:#EBF3FB;box-shadow:none'
                ):
                    ui.label(label).style('font-size:12px;color:#185FA5;font-weight:500;margin-bottom:6px')
                    ui.label(val).style(f'font-size:36px;font-weight:700;color:{color}')

        # Per-student detail table
        with ui.card().style('width:100%;padding:24px;border-radius:14px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.07)'):
            ui.label('Alle Schüler – Detailansicht').style('font-size:16px;font-weight:700;margin-bottom:20px')

            for attempt in attempts:
                student = session.get(User, attempt.student_id)
                pct = attempt_service.calculate_percentage(attempt.score, attempt.max_score)
                color = '#3B6D11' if pct >= 60 else '#A32D2D'
                bg_header = '#EAF3DE' if pct >= 60 else '#FCEBEB'

                student_answers = attempt_service.get_student_answers_by_attempt(session, attempt.id)

                with ui.card().style(
                    'width:100%;border-radius:10px;margin-bottom:16px;'
                    'box-shadow:0 1px 3px rgba(0,0,0,0.06);overflow:hidden'
                ):
                    # Student header
                    with ui.row().style(
                        f'width:100%;padding:14px 20px;background:{bg_header};'
                        'align-items:center;justify-content:space-between;box-sizing:border-box'
                    ):
                        ui.label(student.username if student else '?').style(
                            'font-size:15px;font-weight:600;color:#1A1A18'
                        )
                        with ui.row().style('gap:16px;align-items:center'):
                            ui.label(f'{attempt.score}/{attempt.max_score} Punkte').style(
                                'font-size:13px;color:#666'
                            )
                            ui.label(f'{pct}%').style(
                                f'font-size:16px;font-weight:700;color:{color}'
                            )
                            ui.label(attempt.completed_at.strftime('%d.%m.%Y %H:%M')).style(
                                'font-size:11px;color:#999'
                            )

                    # Per-question breakdown
                    with ui.column().style('padding:12px 20px;gap:6px;width:100%;box-sizing:border-box'):
                        for q in questions:
                            sa = next((s for s in student_answers if s.question_id == q.id), None)
                            if sa is None:
                                continue
                            selected_text = attempt_service.get_selected_answer_text(session, sa.id)
                            correct_text = quiz_service.get_correct_answer_text(session, q.id)

                            icon = '✓' if sa.is_correct else '✗'
                            row_color = '#3B6D11' if sa.is_correct else '#A32D2D'
                            row_bg = '#F6FBF0' if sa.is_correct else '#FDF5F5'

                            with ui.row().style(
                                f'width:100%;padding:10px 14px;border-radius:8px;'
                                f'background:{row_bg};align-items:flex-start;gap:12px;'
                                'box-sizing:border-box'
                            ):
                                ui.label(icon).style(f'color:{row_color};font-size:16px;font-weight:700;min-width:18px')
                                with ui.column().style('flex:1;gap:2px'):
                                    ui.label(q.text).style('font-size:13px;font-weight:600;color:#1A1A18')
                                    ui.label(
                                        f'Antwort: {selected_text}'
                                    ).style(f'font-size:12px;color:{row_color}')
                                    if not sa.is_correct:
                                        ui.label(f'Richtig wäre: {correct_text}').style(
                                            'font-size:11px;color:#888'
                                        )
