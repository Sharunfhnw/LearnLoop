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
        html, body {
            margin: 0 !important;
            padding: 0 !important;
            background-color: #F5F5F3 !important;
        }

        .nicegui-container {
            background-color: #F5F5F3 !important;
            padding: 0 !important;
            width: 100%;
        }

        .results-shell {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 48px;
            background-color: #F5F5F3;
        }

        .results-card {
            background: #ffffff;
            border: 1px solid #dfdfdb;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: none !important;
        }

        .results-header {
            display: flex;
            align-items: center;
            gap: 20px;
            padding: 32px 48px;
            border-bottom: 1px solid #e8e8e3;
            background: #ffffff;
        }

        .back-btn {
            border: 1px solid #d0d0cb !important;
            border-radius: 12px !important;
            background: #ffffff !important;
            color: #000000 !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            padding: 10px 18px !important;
            box-shadow: none !important;
            white-space: nowrap;
            cursor: pointer;
            flex-shrink: 0;
        }

        .header-title {
            font-size: 28px !important;
            font-weight: 700 !important;
            color: #000000 !important;
            margin: 0 !important;
        }

        .results-content {
            background: #fafaf8;
            padding: 48px;
        }

        .main-result-card {
            background: #ffffff;
            border: 1px solid #dfdfdb;
            border-radius: 22px;
            padding: 48px 40px;
            margin-bottom: 32px;
            box-shadow: none !important;
        }

        .percentage {
            font-size: 120px !important;
            font-weight: 700 !important;
            text-align: center;
            line-height: 1;
            margin: 0 0 16px 0 !important;
        }

        .quiz-name {
            font-size: 28px !important;
            font-weight: 700 !important;
            text-align: center;
            color: #000000 !important;
            margin: 0 0 8px 0 !important;
        }

        .feedback-msg {
            font-size: 18px !important;
            color: #777777 !important;
            text-align: center;
            margin: 0 0 32px 0 !important;
        }

        .stats-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 32px;
        }

        .stat-box {
            background: #ffffff;
            border: 1px solid #dfdfdb;
            border-radius: 16px;
            padding: 28px 20px;
            text-align: center;
            box-shadow: none !important;
        }

        .stat-box-label {
            font-size: 16px !important;
            color: #555555 !important;
            margin: 0 0 12px 0 !important;
            font-weight: 500;
        }

        .stat-box-value {
            font-size: 48px !important;
            font-weight: 700 !important;
            margin: 0 !important;
        }

        .action-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .action-btn {
            border: 1px solid #d0d0cb !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            color: #000000 !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            padding: 14px 20px !important;
            box-shadow: none !important;
            cursor: pointer;
            width: 100%;
        }

        .detail-card {
            background: #ffffff;
            border: 1px solid #dfdfdb;
            border-radius: 22px;
            padding: 32px 40px;
            box-shadow: none !important;
        }

        .detail-title {
            font-size: 24px !important;
            font-weight: 700 !important;
            color: #000000 !important;
            margin: 0 0 28px 0 !important;
        }

        .question-item {
            display: flex;
            gap: 20px;
            padding: 24px 0;
            align-items: flex-start;
        }

        .question-item:not(:last-child) {
            border-bottom: 1px solid #f0f0ed;
        }

        .icon-circle {
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

        .question-details {
            flex: 1;
        }

        .question-text {
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #000000 !important;
            margin: 0 0 8px 0 !important;
            line-height: 1.4;
        }

        .student-answer {
            font-size: 16px !important;
            margin: 0 0 4px 0 !important;
            line-height: 1.4;
        }

        .correct-answer {
            font-size: 16px !important;
            color: #777777 !important;
            margin: 0 !important;
            line-height: 1.4;
        }

        @media (max-width: 900px) {
            .results-shell {
                padding: 20px 20px;
            }

            .results-header {
                flex-direction: column;
                align-items: flex-start;
                padding: 20px;
            }

            .results-content {
                padding: 20px;
            }

            .main-result-card {
                padding: 28px 20px;
            }

            .percentage {
                font-size: 80px !important;
            }

            .stats-container {
                grid-template-columns: 1fr;
                gap: 12px;
            }

            .action-buttons {
                grid-template-columns: 1fr;
            }

            .detail-card {
                padding: 20px;
            }
        }
    </style>
    """)

    # Main container
    main_container = ui.column().style('width: 100%; background-color: #F5F5F3; padding: 0; margin: 0')

    with main_container:
        with ui.column().classes('results-shell'):
            # Card wrapper
            with ui.card().classes('results-card').style('box-shadow: none'):
                # Header
                with ui.row().classes('results-header'):
                    ui.button('← Zurück', on_click=lambda: ui.navigate.to('/student/dashboard')).classes('back-btn')
                    ui.label('Ergebnis').classes('header-title')

                # Content area
                with ui.column().classes('results-content'):
                    # Main result card
                    with ui.card().classes('main-result-card').style('box-shadow: none'):
                        ui.label(f'{pct}%').classes('percentage').style(f'color: {pct_color}')
                        ui.label(quiz_title).classes('quiz-name')
                        ui.label(feedback).classes('feedback-msg')

                        # Stats grid
                        with ui.element('div').classes('stats-container'):
                            with ui.element('div').classes('stat-box').style('box-shadow: none'):
                                ui.label('Richtig').classes('stat-box-label')
                                ui.label(str(correct_count)).classes('stat-box-value').style('color: #3E7B12')

                            with ui.element('div').classes('stat-box').style('box-shadow: none'):
                                ui.label('Falsch').classes('stat-box-label')
                                ui.label(str(wrong_count)).classes('stat-box-value').style('color: #B53939')

                            with ui.element('div').classes('stat-box').style('box-shadow: none'):
                                ui.label('Gesamt').classes('stat-box-label')
                                ui.label(str(max_score)).classes('stat-box-value').style('color: #000000')

                        # Action buttons
                        with ui.element('div').classes('action-buttons'):
                            ui.button('⌂ Dashboard', on_click=lambda: ui.navigate.to('/student/dashboard')).classes('action-btn')
                            ui.button('↺ Nochmal', on_click=lambda: ui.navigate.to(f'/student/quiz/{attempt.quiz_id}')).classes('action-btn')

                    # Detail card
                    with ui.card().classes('detail-card').style('box-shadow: none'):
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

                            with ui.element('div').classes('question-item'):
                                with ui.element('div').classes('icon-circle').style(
                                    f'background-color: {icon_bg}; border-color: {icon_color}; color: {icon_color}'
                                ):
                                    ui.label(icon_symbol).style('margin: 0; padding: 0')

                                with ui.column().classes('question-details').style('gap: 2px'):
                                    ui.label(question.text if question else 'Frage').classes('question-text')
                                    ui.label(
                                        f'Deine Antwort: {selected_option.text if selected_option else "-"}'
                                    ).classes('student-answer').style(f'color: {answer_color}')

                                    if not is_correct and correct_option:
                                        ui.label(f'Richtig: {correct_option.text}').classes('correct-answer')

    session.close()