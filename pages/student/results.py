from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import QuizAttempt, Quiz, StudentAnswer, Question, AnswerOption, StudentAnswerSelection


def results_page(attempt_id: int):
    """Results page — whole numbers only, detailed breakdown."""
    ui.query('body').style('background-color:#F5F5F7;margin:0')

    db = Database()
    session = db.get_session()
    attempt = session.get(QuizAttempt, attempt_id)
    quiz = session.get(Quiz, attempt.quiz_id)
    pct = round(attempt.score / attempt.max_score * 100) if attempt.max_score > 0 else 0

    # ── Header ───────────────────────────────────────────────────────────────
    with ui.row().style(
        'width:100%;background:white;padding:14px 40px;'
        'align-items:center;gap:16px;'
        'box-shadow:0 1px 3px rgba(0,0,0,0.08);box-sizing:border-box'
    ):
        with ui.button(on_click=lambda: ui.navigate.to('/student/dashboard')).style(
            'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px'
        ).props('no-caps flat'):
            ui.html('&#8592; Zurück')
        ui.label('Ergebnis').style('font-size:18px;font-weight:700;color:#1A1A18')

    with ui.column().style('max-width:760px;margin:32px auto;padding:0 40px;width:100%;box-sizing:border-box;gap:20px'):

        # Score summary card
        with ui.card().style(
            'width:100%;padding:36px 28px;border-radius:14px;'
            'background:white;box-shadow:0 1px 4px rgba(0,0,0,0.07);text-align:center'
        ):
            color = '#3B6D11' if pct >= 60 else '#A32D2D'
            ui.label(f'{pct}%').style(f'font-size:56px;font-weight:700;color:{color};line-height:1')
            ui.label(quiz.title).style('font-size:18px;font-weight:700;margin-top:12px;color:#1A1A18')

            if pct >= 90:
                msg = 'Ausgezeichnet! 🌟'
            elif pct >= 75:
                msg = 'Sehr gut! 👏'
            elif pct >= 60:
                msg = 'Gut gemacht! 👍'
            else:
                msg = 'Weiter üben! 💪'
            ui.label(msg).style('font-size:14px;color:#888;margin-top:4px')

            # Richtig / Falsch / Gesamt cards
            wrong = attempt.max_score - attempt.score
            with ui.row().style('justify-content:center;gap:16px;margin-top:24px'):
                for val, label, bg, tc in [
                    (str(attempt.score), 'Richtig', '#EAF3DE', '#3B6D11'),
                    (str(wrong), 'Falsch', '#FCEBEB', '#A32D2D'),
                    (str(attempt.max_score), 'Gesamt', '#F1EFE8', '#1A1A18'),
                ]:
                    with ui.card().style(f'padding:16px 28px;background:{bg};border-radius:10px;border:none;box-shadow:none'):
                        ui.label(val).style(f'font-size:28px;font-weight:700;color:{tc};text-align:center')
                        ui.label(label).style('font-size:12px;color:#888;text-align:center;margin-top:4px')

            with ui.row().style('gap:12px;margin-top:24px;justify-content:center'):
                with ui.button(on_click=lambda: ui.navigate.to('/student/dashboard')).style(
                    'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px;padding:10px 24px'
                ).props('no-caps flat'):
                    ui.html('&#8962; Dashboard')
                with ui.button(on_click=lambda: ui.navigate.to(f'/student/quiz/{attempt.quiz_id}')).style(
                    'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px;padding:10px 24px'
                ).props('no-caps flat'):
                    ui.html('&#8635; Nochmal')

        # Detailed breakdown
        with ui.card().style('width:100%;padding:28px;border-radius:14px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.07)'):
            ui.label('Detailauswertung').style('font-size:16px;font-weight:700;margin-bottom:20px')

            questions = session.exec(select(Question).where(Question.quiz_id == attempt.quiz_id)).all()
            sa_list = session.exec(select(StudentAnswer).where(StudentAnswer.attempt_id == attempt_id)).all()

            for q in questions:
                # Find student answer(s) for this question
                sa_for_q = [sa for sa in sa_list if sa.question_id == q.id]
                if not sa_for_q:
                    continue

                sa = sa_for_q[0]  # representative
                is_correct = sa.is_correct

                icon = '✓' if is_correct else '✗'
                color = '#3B6D11' if is_correct else '#A32D2D'
                bg = '#F6FBF0' if is_correct else '#FDF5F5'

                # What was selected
                selections = session.exec(
                    select(StudentAnswerSelection).where(
                        StudentAnswerSelection.student_answer_id == sa.id
                    )
                ).all()
                sel_ids = [selection.answer_option_id for selection in selections]
                sel_opts = [session.get(AnswerOption, sid) for sid in sel_ids]
                sel_text = ', '.join(o.text for o in sel_opts if o) if sel_opts else '–'

                # Correct answer
                all_opts = session.exec(select(AnswerOption).where(AnswerOption.question_id == q.id)).all()
                correct_text = ', '.join(o.text for o in all_opts if o.is_correct)

                with ui.row().style(
                    f'width:100%;padding:14px 16px;border-radius:10px;'
                    f'background:{bg};align-items:flex-start;gap:12px;'
                    'margin-bottom:8px;box-sizing:border-box'
                ):
                    ui.html(
                        f'<span style="color:{color};font-size:18px;font-weight:700;'
                        f'width:24px;min-width:24px;margin-top:2px">{icon}</span>'
                    )
                    with ui.column().style('flex:1;gap:3px'):
                        ui.label(q.text).style('font-size:14px;font-weight:700;color:#1A1A18')
                        ui.label(f'Deine Antwort: {sel_text}').style(f'font-size:13px;color:{color}')
                        if not is_correct:
                            ui.label(f'Richtig: {correct_text}').style('font-size:12px;color:#888')
