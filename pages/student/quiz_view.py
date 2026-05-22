from nicegui import ui, app
from sqlmodel import select
from data_access.db import Database
from domain.models import (
    Quiz, Question, AnswerOption, QuizAttempt, StudentAnswer
)


def quiz_view(quiz_id: int, student_id: int):
    """Render the quiz taking page (one question at a time)."""
    ui.query('body').style('background-color:#F8F7F4;margin:0')

    db = Database()
    session = db.get_session()
    quiz = session.get(Quiz, quiz_id)
    questions = session.exec(
        select(Question).where(Question.quiz_id == quiz_id)
    ).all()

    if not quiz or not questions:
        ui.label('Quiz not found.').style('padding:24px')
        return

    # Track the current question index and collected answers
    current_idx = {'v': 0}
    answers = {}  # question_id -> selected answer option id

    # --- Header bar ---
    with ui.row().style(
        'width:100%;background:white;padding:12px 24px;'
        'align-items:center;justify-content:space-between;'
        'box-shadow:0 1px 3px rgba(0,0,0,0.08)'
    ):
        ui.button('← Back',
            on_click=lambda: ui.navigate.to('/student/dashboard')
        ).style('background:transparent;color:#666;font-size:12px')

        ui.label(quiz.title).style(
            'font-size:16px;font-weight:500;color:#1A1A18'
        )

        # Progress percentage badge (updates per question)
        pct_label = ui.label('0%').style(
            'font-size:13px;color:#666;background:#F0F0F0;'
            'padding:4px 10px;border-radius:20px'
        )

    # Thin progress bar below header
    progress_bar = ui.linear_progress(
        value=0, show_value=False
    ).style('height:4px;margin:0;border-radius:0')
    progress_bar.props('color=black instant-feedback')

    # Main content container (cleared and re-rendered per question)
    content = ui.column().style(
        'max-width:600px;margin:32px auto;padding:0 20px;width:100%'
    )

    def show_question(idx: int):
        """Render the question at the given index."""
        current_idx['v'] = idx
        content.clear()

        q = questions[idx]

        # Update progress indicators
        pct = round(idx / len(questions) * 100)
        pct_label.set_text(f'{pct}%')
        progress_bar.set_value(idx / len(questions))

        # Load answer options for this question
        options = session.exec(
            select(AnswerOption).where(AnswerOption.question_id == q.id)
        ).all()

        with content:
            # Question type badge
            type_map = {
                'single': 'Single Choice',
                'multiple': 'Multiple Choice',
                'truefalse': 'True/False'
            }
            type_label = type_map.get(q.question_type, 'Single Choice')
            ui.html(
                f'<span style="background:#F0EDE6;color:#666;'
                f'padding:4px 10px;border-radius:20px;font-size:11px">'
                f'{type_label}</span>'
            )

            with ui.card().style(
                'width:100%;padding:24px;border-radius:12px;'
                'box-shadow:0 1px 3px rgba(0,0,0,0.08);margin-top:12px'
            ):
                ui.label(q.text).style(
                    'font-size:18px;font-weight:500;margin-bottom:6px'
                )
                ui.label('Choose the correct answer').style(
                    'font-size:12px;color:#999;margin-bottom:20px'
                )

                # Render each answer option as a clickable row
                for opt in options:
                    is_selected = answers.get(q.id) == opt.id

                    bg = 'background:#111;color:white' if is_selected \
                        else 'background:white;color:#1A1A18'
                    border = 'border:2px solid #111' if is_selected \
                        else 'border:1.5px solid #E5E5E5'
                    radio = '●' if is_selected else '○'
                    icon_color = 'white' if is_selected else '#999'
                    weight = '500' if is_selected else '400'

                    with ui.row().style(
                        f'width:100%;align-items:center;gap:12px;'
                        f'padding:14px 16px;border-radius:10px;cursor:pointer;'
                        f'margin-bottom:8px;{bg};{border}'
                    ) as row:
                        ui.label(radio).style(
                            f'font-size:16px;color:{icon_color}'
                        )
                        ui.label(opt.text).style(
                            f'font-size:14px;font-weight:{weight}'
                        )

                        def on_click(o=opt):
                            """Save the selected answer and re-render."""
                            answers[q.id] = o.id
                            show_question(idx)

                        row.on('click', on_click)

                # --- Navigation buttons ---
                with ui.row().style(
                    'width:100%;justify-content:space-between;'
                    'margin-top:24px;gap:8px'
                ):
                    # Back button (hidden on first question)
                    if idx > 0:
                        ui.button('← Back',
                            on_click=lambda: show_question(idx - 1)
                        ).style(
                            'flex:1;background:white;color:#1A1A18;'
                            'border:1.5px solid #E5E5E5;border-radius:8px;'
                            'font-size:13px;padding:12px'
                        )
                    else:
                        ui.element('div').style('flex:1')

                    # Next button or Submit on last question
                    if idx < len(questions) - 1:
                        ui.button('Next →',
                            on_click=lambda: show_question(idx + 1)
                        ).style(
                            'flex:3;background:#111;color:white;'
                            'border-radius:8px;font-size:13px;padding:12px'
                        )
                    else:
                        def submit_quiz():
                            """Validate all answered, save attempt and navigate to results."""
                            unanswered = [
                                q for q in questions if q.id not in answers
                            ]
                            if unanswered:
                                ui.notify(
                                    'Please answer all questions!',
                                    color='negative'
                                )
                                return

                            # Create the attempt record
                            attempt = QuizAttempt(
                                student_id=student_id,
                                quiz_id=quiz_id,
                                score=0,
                                max_score=len(questions)
                            )
                            session.add(attempt)
                            session.commit()

                            # Save each student answer and calculate score
                            score = 0
                            for question in questions:
                                sel_id = answers.get(question.id)
                                opt = session.get(AnswerOption, sel_id)
                                correct = opt.is_correct if opt else False
                                if correct:
                                    score += 1
                                session.add(StudentAnswer(
                                    attempt_id=attempt.id,
                                    question_id=question.id,
                                    selected_answer_option_id=sel_id,
                                    is_correct=correct
                                ))

                            attempt.score = score
                            session.add(attempt)
                            session.commit()

                            ui.navigate.to(
                                f'/student/results/{attempt.id}'
                            )

                        ui.button('Submit Quiz',
                            on_click=submit_quiz
                        ).style(
                            'flex:3;background:#111;color:white;'
                            'border-radius:8px;font-size:13px;padding:12px'
                        )

    # Show the first question on page load
    show_question(0)