from nicegui import ui
from sqlmodel import select

from data_access.db import Database
from domain.models import QuizAttempt, Quiz, StudentAnswer, Question, AnswerOption


def results_page(attempt_id: int) -> None:
    ui.query('body').style('background-color: #F5F5F3')

    db = Database()
    session = db.get_session()

    attempt = session.get(QuizAttempt, attempt_id)
    if not attempt:
        ui.notify('Ergebnis nicht gefunden', color='negative')
        ui.navigate.to('/student/dashboard')
        return

    quiz = session.get(Quiz, attempt.quiz_id)
    quiz_title = quiz.title if quiz else 'Quiz'

    max_score = attempt.max_score or 0
    score = attempt.score or 0
    pct = round((score / max_score) * 100) if max_score > 0 else 0

    correct_count = score
    wrong_count = max_score - score if max_score >= score else 0

    if pct >= 80:
        pct_color = '#3E7B12'
        feedback = 'Sehr gut!'
    elif pct >= 60:
        pct_color = '#3E7B12'
        feedback = 'Gut gemacht!'
    else:
        pct_color = '#B53939'
        feedback = 'Weiter üben!'

    student_answers = session.exec(
        select(StudentAnswer).where(StudentAnswer.attempt_id == attempt_id)
    ).all()

    ui.add_head_html("""
    <style>
        .results-shell {
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 18px 36px 18px;
        }

        .results-page-card {
            background: #ffffff;
            border: 1px solid #dfdfdb;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: none;
        }

        .results-header {
            display: flex;
            align-items: center;
            gap: 18px;
            padding: 26px 38px;
            border-bottom: 1px solid #e8e8e3;
            background: #ffffff;
        }

        .results-content-bg {
            background: #f3f3f1;
            padding: 38px;
        }

        .back-btn {
            border: 1px solid #d7d7d1 !important;
            border-radius: 16px !important;
            background: #ffffff !important;
            color: #171717 !important;
            font-size: 20px !important;
            font-weight: 500 !important;
            padding: 14px 28px !important;
            box-shadow: none !important;
        }

        .result-main-card {
            width: 100%;
            max-width: 920px;
            margin: 0 auto 28px auto;
            padding: 42px 34px 30px 34px;
            background: #ffffff;
            border: 1px solid #dfdfdb;
            border-radius: 22px;
            box-shadow: none;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
            margin-top: 28px;
            margin-bottom: 24px;
        }

        .mini-stat-card {
            border: 1px solid #dfdfdb;
            border-radius: 18px;
            background: #ffffff;
            padding: 24px 20px;
            text-align: center;
        }

        .action-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 10px;
        }

        .secondary-btn {
            width: 100%;
            border: 1px solid #d7d7d1 !important;
            border-radius: 16px !important;
            background: #ffffff !important;
            color: #171717 !important;
            font-size: 20px !important;
            font-weight: 500 !important;
            padding: 16px 22px !important;
            box-shadow: none !important;
        }

        .detail-card {
            width: 100%;
            border: 1px solid #dfdfdb;
            border-radius: 22px;
            background: #ffffff;
            padding: 28px 30px;
            box-shadow: none;
        }

        .detail-row {
            display: flex;
            align-items: flex-start;
            gap: 18px;
            padding: 18px 0;
        }

        .detail-divider {
            border-top: 1px solid #ecece7;
        }

        .detail-icon-circle {
            width: 32px;
            height: 32px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 700;
            flex-shrink: 0;
            margin-top: 2px;
        }

        @media (max-width: 900px) {
            .stats-grid,
            .action-grid {
                grid-template-columns: 1fr;
            }

            .results-header {
                flex-direction: column;
                align-items: flex-start;
            }

            .results-content-bg {
                padding: 18px;
            }

            .result-main-card {
                padding: 26px 18px 22px 18px;
            }
        }
    </style>
    """)

    with ui.column().classes('results-shell'):
        with ui.card().classes('results-page-card'):

            with ui.row().classes('results-header'):
                ui.button('← Zurück', on_click=lambda: ui.navigate.to('/student/dashboard')).classes('back-btn')
                ui.label('Ergebnis').style('font-size: 28px; font-weight: 700; color: #111;')

            with ui.column().classes('results-content-bg'):

                with ui.card().classes('result-main-card'):
                    ui.label(f'{pct}%').style(
                        f'font-size: 96px; line-height: 1; font-weight: 700; text-align: center; color: {pct_color}; width: 100%;'
                    )
                    ui.label(quiz_title).style(
                        'font-size: 28px; font-weight: 700; text-align: center; color: #111; margin-top: 8px; width: 100%;'
                    )
                    ui.label(feedback).style(
                        'font-size: 20px; color: #6b6b6b; text-align: center; width: 100%; margin-top: 4px;'
                    )

                    with ui.element('div').classes('stats-grid'):
                        with ui.element('div').classes('mini-stat-card'):
                            ui.label('Richtig').style(
                                'font-size: 18px; color: #2c2c2c; text-align: center; width: 100%;'
                            )
                            ui.label(str(correct_count)).style(
                                'font-size: 40px; font-weight: 700; color: #3E7B12; text-align: center; width: 100%; margin-top: 8px;'
                            )

                        with ui.element('div').classes('mini-stat-card'):
                            ui.label('Falsch').style(
                                'font-size: 18px; color: #2c2c2c; text-align: center; width: 100%;'
                            )
                            ui.label(str(wrong_count)).style(
                                'font-size: 40px; font-weight: 700; color: #B53939; text-align: center; width: 100%; margin-top: 8px;'
                            )

                        with ui.element('div').classes('mini-stat-card'):
                            ui.label('Gesamt').style(
                                'font-size: 18px; color: #2c2c2c; text-align: center; width: 100%;'
                            )
                            ui.label(str(max_score)).style(
                                'font-size: 40px; font-weight: 700; color: #111; text-align: center; width: 100%; margin-top: 8px;'
                            )

                    with ui.element('div').classes('action-grid'):
                        ui.button('⌂ Dashboard', on_click=lambda: ui.navigate.to('/student/dashboard')).classes('secondary-btn')
                        ui.button('↺ Nochmal', on_click=lambda: ui.navigate.to(f'/student/quiz/{attempt.quiz_id}')).classes('secondary-btn')

                with ui.card().classes('detail-card'):
                    ui.label('Detailauswertung').style(
                        'font-size: 22px; font-weight: 700; color: #111; margin-bottom: 8px;'
                    )

                    for index, sa in enumerate(student_answers):
                        question = session.get(Question, sa.question_id)
                        selected_option = session.get(AnswerOption, sa.selected_answer_option_id)

                        correct_option = session.exec(
                            select(AnswerOption).where(
                                AnswerOption.question_id == sa.question_id,
                                AnswerOption.is_correct == True,
                            )
                        ).first()

                        is_correct = bool(sa.is_correct)
                        icon_symbol = '✓' if is_correct else '✕'
                        icon_color = '#3E7B12' if is_correct else '#B53939'
                        icon_bg = '#EDF6E5' if is_correct else '#FBEAEA'
                        answer_color = '#3E7B12' if is_correct else '#B53939'

                        if index > 0:
                            ui.separator().classes('detail-divider')

                        with ui.element('div').classes('detail-row'):
                            with ui.element('div').classes('detail-icon-circle').style(
                                f'color: {icon_color}; background: {icon_bg}; border: 2px solid {icon_color};'
                            ):
                                ui.label(icon_symbol).style(
                                    f'font-size: 18px; font-weight: 700; color: {icon_color}; margin: 0;'
                                )

                            with ui.column().style('gap: 2px; width: 100%;'):
                                ui.label(question.text if question else 'Frage').style(
                                    'font-size: 18px; font-weight: 700; color: #111;'
                                )
                                ui.label(
                                    f'Deine Antwort: {selected_option.text if selected_option else "-"}'
                                ).style(
                                    f'font-size: 16px; color: {answer_color};'
                                )

                                if not is_correct and correct_option:
                                    ui.label(f'Richtig: {correct_option.text}').style(
                                        'font-size: 16px; color: #5f5f5f;'
                                    )

    session.close()