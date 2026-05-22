from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import QuizAttempt, Quiz, StudentAnswer, Question, AnswerOption


def results_page(attempt_id: int):
    """Render the quiz results page for students."""
    ui.query('body').style('background-color:#F8F7F4;margin:0')

    db = Database()
    session = db.get_session()
    attempt = session.get(QuizAttempt, attempt_id)
    quiz = session.get(Quiz, attempt.quiz_id)
    pct = round(
        attempt.score / attempt.max_score * 100
    ) if attempt.max_score > 0 else 0

    # --- Header ---
    with ui.row().style(
        'width:100%;background:white;padding:16px 24px;'
        'align-items:center;gap:16px;'
        'border-bottom:1px solid #E5E5E5;margin-bottom:32px'
    ):
        ui.button('← Zurück',
            on_click=lambda: ui.navigate.to('/student/dashboard')
        ).style(
            'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;'
            'border-radius:8px;font-size:13px;padding:8px 16px'
        ).props('no-caps')
        ui.label('Ergebnis').style(
            'font-size:20px;font-weight:600;color:#1A1A18'
        )

    with ui.column().style(
        'max-width:700px;margin:0 auto;padding:0 24px 32px;width:100%'
    ):

        # --- Score card ---
        score_color = '#3B6D11' if pct >= 60 else '#A32D2D'

        with ui.card().style(
            'width:100%;padding:32px;border-radius:12px;'
            'text-align:center;margin-bottom:16px;'
            'box-shadow:0 1px 3px rgba(0,0,0,0.06)'
        ):
            ui.label(f'{pct}%').style(
                f'font-size:56px;font-weight:600;color:{score_color}'
            )
            ui.label(quiz.title).style(
                'font-size:16px;font-weight:600;margin-top:8px'
            )

            # Motivational message based on score
            if pct >= 90:
                msg = 'Ausgezeichnet!'
            elif pct >= 75:
                msg = 'Sehr gut!'
            elif pct >= 60:
                msg = 'Gut gemacht!'
            else:
                msg = 'Weiter üben!'
            ui.label(msg).style('font-size:14px;color:#666;margin-top:4px')

            # Richtig / Falsch / Gesamt mini-cards
            with ui.row().style(
                'justify-content:center;gap:12px;margin-top:20px'
            ):
                for val, label, bg, c in [
                    (str(attempt.score), 'Richtig', '#F8F8F8', '#3B6D11'),
                    (
                        str(attempt.max_score - attempt.score),
                        'Falsch', '#F8F8F8', '#A32D2D'
                    ),
                    (str(attempt.max_score), 'Gesamt', '#F8F8F8', '#1A1A18'),
                ]:
                    with ui.card().style(
                        f'flex:1;padding:14px 20px;background:{bg};'
                        'border-radius:10px;text-align:center;'
                        'box-shadow:0 1px 2px rgba(0,0,0,0.04)'
                    ):
                        ui.label(label).style(
                            'font-size:12px;color:#666;margin-bottom:4px'
                        )
                        ui.label(val).style(
                            f'font-size:22px;font-weight:600;color:{c}'
                        )

            # Dashboard / Nochmal buttons
            with ui.row().style(
                'gap:8px;margin-top:20px;justify-content:center'
            ):
                ui.button('Dashboard',
                    on_click=lambda: ui.navigate.to('/student/dashboard')
                ).style(
                    'flex:1;background:white;color:#1A1A18;'
                    'border:1.5px solid #E5E5E5;border-radius:8px;'
                    'font-size:13px;padding:12px'
                ).props('no-caps')
                ui.button('Nochmal',
                    on_click=lambda: ui.navigate.to(
                        f'/student/quiz/{attempt.quiz_id}'
                    )
                ).style(
                    'flex:1;background:white;color:#1A1A18;'
                    'border:1.5px solid #E5E5E5;border-radius:8px;'
                    'font-size:13px;padding:12px'
                ).props('no-caps')

        # --- Detailauswertung ---
        with ui.card().style(
            'width:100%;padding:24px;border-radius:12px;'
            'box-shadow:0 1px 3px rgba(0,0,0,0.06)'
        ):
            ui.label('Detailauswertung').style(
                'font-size:16px;font-weight:600;margin-bottom:16px'
            )

            sa_list = session.exec(
                select(StudentAnswer).where(
                    StudentAnswer.attempt_id == attempt_id
                )
            ).all()

            for sa in sa_list:
                q = session.get(Question, sa.question_id)
                opt = session.get(AnswerOption, sa.selected_answer_option_id)
                icon = '✓' if sa.is_correct else '✗'
                c = '#3B6D11' if sa.is_correct else '#A32D2D'
                bg = '#EAF3DE' if sa.is_correct else '#FCEBEB'

                with ui.row().style(
                    f'width:100%;align-items:flex-start;gap:10px;'
                    f'padding:12px;margin-bottom:6px;'
                    f'background:{bg};border-radius:8px'
                ):
                    ui.label(icon).style(
                        f'color:{c};font-weight:600;font-size:16px;'
                        'margin-top:2px'
                    )
                    with ui.column().style('gap:3px'):
                        ui.label(
                            q.text if q else '-'
                        ).style(
                            'font-size:13px;font-weight:500;color:#1A1A18'
                        )
                        ui.label(
                            f'Deine Antwort: {opt.text if opt else "-"}'
                        ).style(f'font-size:12px;color:{c}')

                        # Show correct answer if wrong
                        if not sa.is_correct:
                            correct_opts = session.exec(
                                select(AnswerOption).where(
                                    AnswerOption.question_id == sa.question_id,
                                    AnswerOption.is_correct == True
                                )
                            ).all()
                            if correct_opts:
                                correct_text = ', '.join(
                                    o.text for o in correct_opts
                                )
                                ui.label(
                                    f'Richtig: {correct_text}'
                                ).style('font-size:12px;color:#666')