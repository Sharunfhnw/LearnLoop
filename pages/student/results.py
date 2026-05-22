from nicegui import ui
from sqlmodel import select

from data_access.db import Database
from domain.models import QuizAttempt, Quiz, StudentAnswer, Question, AnswerOption


def results_page(attempt_id: int):
    ui.query('body').style('background-color: #F5F5F3')

    db = Database()
    session = db.get_session()

    attempt = session.get(QuizAttempt, attempt_id)
    if not attempt:
        ui.notify('Ergebnis nicht gefunden', color='negative')
        ui.navigate.to('/student/dashboard')
        session.close()
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
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
        }

        .results-container {
            width: 100%;
            min-height: 100vh;
            background-color: #F5F5F3;
            padding: 24px 48px;
        }

        .results-wrapper {
            width: 100%;
            max-width: 1000px;
            margin: 0 auto;
        }

        .results-page-card {
            background: #ffffff;
            border: 1px solid #e5e5e0;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: none;
        }

        .results-header {
            display: flex;
            align-items: center;
            gap: 24px;
            padding: 32px 40px;
            border-bottom: 1px solid #e8e8e3;
            background: #ffffff;
        }

        .back-btn {
            border: 1px solid #d0d0cb !important;
            border-radius: 12px !important;
            background: #ffffff !important;
            color: #171717 !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            padding: 10px 16px !important;
            box-shadow: none !important;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .back-btn:hover {
            background: #f5f5f5 !important;
        }

        .header-title {
            font-size: 28px;
            font-weight: 700;
            color: #171717;
            margin: 0;
        }

        .results-content-bg {
            background: #fafaf8;
            padding: 48px 40px;
        }

        .result-main-card {
            width: 100%;
            padding: 48px 40px;
            background: #ffffff;
            border: 1px solid #e5e5e0;
            border-radius: 20px;
            box-shadow: none;
            margin-bottom: 32px;
        }

        .percentage-display {
            font-size: 120px;
            line-height: 1;
            font-weight: 700;
            text-align: center;
            width: 100%;
            margin-bottom: 16px;
        }

        .quiz-title {
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            color: #171717;
            width: 100%;
            margin-bottom: 8px;
        }

        .feedback-text {
            font-size: 18px;
            color: #7a7a7a;
            text-align: center;
            width: 100%;
            margin-bottom: 32px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 32px;
        }

        .mini-stat-card {
            border: 1px solid #e5e5e0;
            border-radius: 16px;
            background: #ffffff;
            padding: 28px 20px;
            text-align: center;
        }

        .stat-label {
            font-size: 16px;
            color: #505050;
            text-align: center;
            width: 100%;
            margin-bottom: 12px;
            font-weight: 500;
        }

        .stat-value {
            font-size: 48px;
            font-weight: 700;
            text-align: center;
            width: 100%;
        }

        .action-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .secondary-btn {
            width: 100%;
            border: 1px solid #d0d0cb !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            color: #171717 !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            padding: 14px 20px !important;
            box-shadow: none !important;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .secondary-btn:hover {
            background: #f5f5f5 !important;
        }

        .detail-card {
            width: 100%;
            border: 1px solid #e5e5e0;
            border-radius: 20px;
            background: #ffffff;
            padding: 32px 40px;
            box-shadow: none;
        }

        .detail-title {
            font-size: 24px;
            font-weight: 700;
            color: #171717;
            margin-bottom: 28px;
        }

        .detail-row {
            display: flex;
            align-items: flex-start;
            gap: 20px;
            padding: 24px 0;
        }

        .detail-row:not(:last-child) {
            border-bottom: 1px solid #f0f0ed;
        }

        .detail-icon-circle {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 700;
            flex-shrink: 0;
            border: 2px solid;
        }

        .question-content {
            flex: 1;
            width: 100%;
        }

        .question-text {
            font-size: 18px;
            font-weight: 700;
            color: #171717;
            margin-bottom: 8px;
            line-height: 1.4;
        }

        .answer-text {
            font-size: 16px;
            margin-bottom: 4px;
            line-height: 1.4;
        }

        .correct-answer-text {
            font-size: 16px;
            color: #7a7a7a;
            line-height: 1.4;
        }

        @media (max-width: 768px) {
            .results-container {
                padding: 16px 20px;
            }

            .results-header {
                flex-direction: column;
                align-items: flex-start;
                padding: 20px;
                gap: 16px;
            }

            .results-content-bg {
                padding: 24px 20px;
            }

            .result-main-card {
                padding: 28px 20px;
                margin-bottom: 24px;
            }

            .percentage-display {
                font-size: 80px;
                margin-bottom: 12px;
            }

            .quiz-title {
                font-size: 22px;
            }

            .stats-grid {
                grid-template-columns: 1fr;
                gap: 12px;
                margin-bottom: 24px;
            }

            .action-grid {
                grid-template-columns: 1fr;
                gap: 12px;
            }

            .detail-card {
                padding: 20px;
                border-radius: 16px;
            }

            .detail-row {
                gap: 12px;
                padding: 16px 0;
            }

            .detail-icon-circle {
                width: 36px;
                height: 36px;
                font-size: 18px;
            }
        }
    </style>
    """)

    with ui.column().classes('results-container'):
        with ui.column().classes('results-wrapper'):
            with ui.card().classes('results-page-card'):

                with ui.row().classes('results-header'):
                    ui.button('← Zurück', on_click=lambda: ui.navigate.to('/student/dashboard')).classes('back-btn')
                    ui.label('Ergebnis').classes('header-title')

                with ui.column().classes('results-content-bg'):

                    with ui.card().classes('result-main-card'):
                        ui.label(f'{pct}%').classes('percentage-display').style(f'color: {pct_color}')
                        ui.label(quiz_title).classes('quiz-title')
                        ui.label(feedback).classes('feedback-text')

                        with ui.element('div').classes('stats-grid'):
                            with ui.element('div').classes('mini-stat-card'):
                                ui.label('Richtig').classes('stat-label')
                                ui.label(str(correct_count)).classes('stat-value').style('color: #3E7B12')

                            with ui.element('div').classes('mini-stat-card'):
                                ui.label('Falsch').classes('stat-label')
                                ui.label(str(wrong_count)).classes('stat-value').style('color: #B53939')

                            with ui.element('div').classes('mini-stat-card'):
                                ui.label('Gesamt').classes('stat-label')
                                ui.label(str(max_score)).classes('stat-value').style('color: #171717')

                        with ui.element('div').classes('action-grid'):
                            ui.button('⌂ Dashboard', on_click=lambda: ui.navigate.to('/student/dashboard')).classes('secondary-btn')
                            ui.button('↺ Nochmal', on_click=lambda: ui.navigate.to(f'/student/quiz/{attempt.quiz_id}')).classes('secondary-btn')

                    with ui.card().classes('detail-card'):
                        ui.label('Detailauswertung').classes('detail-title')

                        for sa in student_answers:
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

                            with ui.element('div').classes('detail-row'):
                                with ui.element('div').classes('detail-icon-circle').style(
                                    f'color: {icon_color}; background: {icon_bg}; border-color: {icon_color};'
                                ):
                                    ui.label(icon_symbol)

                                with ui.column().classes('question-content'):
                                    ui.label(question.text if question else 'Frage').classes('question-text')
                                    ui.label(
                                        f'Deine Antwort: {selected_option.text if selected_option else "-"}'
                                    ).classes('answer-text').style(f'color: {answer_color}')

                                    if not is_correct and correct_option:
                                        ui.label(f'Richtig: {correct_option.text}').classes('correct-answer-text')

    session.close()