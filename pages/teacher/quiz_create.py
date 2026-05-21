from nicegui import ui
from data_access.db import Database
from services.quiz_service import QuizService


def quiz_create(teacher_id: int):
    """Render the quiz creation page for teachers."""
    ui.query('body').style('background-color:#F5F5F7;margin:0')

    db = Database()
    session = db.get_session()
    quiz_service = QuizService()

    # List of question dicts collected before saving
    questions = []

    # --- Header bar ---
    with ui.row().style(
        'width:100%;background:white;padding:16px 24px;'
        'align-items:center;gap:16px;'
        'border-bottom:1px solid #E5E5E5;margin-bottom:32px'
    ):
        ui.button('← Back',
            on_click=lambda: ui.navigate.to('/teacher/dashboard')
        ).style(
            'background:#111;color:white;border-radius:8px;'
            'font-size:13px;padding:8px 16px'
        )
        ui.label('Create New Quiz').style(
            'font-size:20px;font-weight:600;color:#1A1A18'
        )

    # --- Two-column layout (50% / 50%) ---
    with ui.row().style(
        'padding:0 32px 32px;gap:24px;align-items:flex-start;width:100%;'
        'box-sizing:border-box'
    ):

        # ===== LEFT COLUMN =====
        with ui.column().style('flex:1;gap:20px;min-width:0'):

            # Quiz information card
            with ui.card().style(
                'width:100%;padding:28px;border-radius:16px;'
                'box-shadow:0 1px 4px rgba(0,0,0,0.08)'
            ):
                ui.label('Quiz Information').style(
                    'font-size:16px;font-weight:600;margin-bottom:20px'
                )
                ui.label('Title').style(
                    'font-size:14px;font-weight:500;margin-bottom:8px'
                )
                title = ui.input(
                    placeholder='e.g. Math Basics'
                ).style('width:100%;font-size:14px;margin-bottom:16px')
                title.props('outlined dense')

                ui.label('Description').style(
                    'font-size:14px;font-weight:500;margin-bottom:8px'
                )
                description = ui.textarea(
                    placeholder='What is this quiz about?'
                ).style('width:100%;font-size:14px')
                description.props('outlined rows=3')

            # Add question card
            with ui.card().style(
                'width:100%;padding:28px;border-radius:16px;'
                'box-shadow:0 1px 4px rgba(0,0,0,0.08)'
            ):
                ui.label('Add Question').style(
                    'font-size:16px;font-weight:600;margin-bottom:4px'
                )
                ui.label('Add questions to your quiz').style(
                    'font-size:13px;color:#888;margin-bottom:20px'
                )

                # Question type dropdown
                ui.label('Question Type').style(
                    'font-size:14px;font-weight:500;margin-bottom:8px'
                )
                q_type = ui.select(
                    options={
                        'single': 'Single Choice',
                        'multiple': 'Multiple Choice',
                        'truefalse': 'True/False'
                    },
                    value='single'
                ).style('width:100%;font-size:14px;margin-bottom:16px')
                q_type.props('outlined dense')

                # Question text
                ui.label('Question').style(
                    'font-size:14px;font-weight:500;margin-bottom:8px'
                )
                q_text = ui.input(
                    placeholder='Your question here...'
                ).style('width:100%;font-size:14px;margin-bottom:16px')
                q_text.props('outlined dense')

                # Answer options container (hidden for True/False)
                opts_container = ui.column().style('width:100%;gap:10px')
                with opts_container:
                    ui.label('Answer Options').style(
                        'font-size:14px;font-weight:500;margin-bottom:4px'
                    )
                    opt1 = ui.input(placeholder='Option 1').style('width:100%;font-size:14px')
                    opt1.props('outlined dense')
                    opt2 = ui.input(placeholder='Option 2').style('width:100%;font-size:14px')
                    opt2.props('outlined dense')
                    opt3 = ui.input(placeholder='Option 3').style('width:100%;font-size:14px')
                    opt3.props('outlined dense')
                    opt4 = ui.input(placeholder='Option 4').style('width:100%;font-size:14px')
                    opt4.props('outlined dense')

                # Single choice: correct answer dropdown
                single_area = ui.column().style('width:100%;margin-top:8px')
                with single_area:
                    ui.label('Correct Answer').style(
                        'font-size:14px;font-weight:500;margin-bottom:8px'
                    )
                    correct_single = ui.select(
                        options=['Option 1', 'Option 2', 'Option 3', 'Option 4']
                    ).style('width:100%;font-size:14px')
                    correct_single.props('outlined dense')

                # Multiple choice: checkboxes for correct answers
                multi_area = ui.column().style(
                    'width:100%;margin-top:8px;display:none'
                )
                with multi_area:
                    ui.label('Correct Answers (multiple allowed)').style(
                        'font-size:14px;font-weight:500;margin-bottom:8px'
                    )
                    cb1 = ui.checkbox('Option 1 is correct')
                    cb2 = ui.checkbox('Option 2 is correct')
                    cb3 = ui.checkbox('Option 3 is correct')
                    cb4 = ui.checkbox('Option 4 is correct')

                def on_type_change(val):
                    """Show/hide answer sections based on question type."""
                    if val == 'truefalse':
                        opts_container.style('display:none')
                        single_area.style('display:none')
                        multi_area.style('display:none')
                    elif val == 'multiple':
                        opts_container.style('display:block')
                        single_area.style('display:none')
                        multi_area.style('display:block')
                    else:
                        opts_container.style('display:block')
                        single_area.style('display:block')
                        multi_area.style('display:none')

                q_type.on_value_change(lambda e: on_type_change(e.value))

        # ===== RIGHT COLUMN =====
        with ui.column().style('flex:1;gap:20px;min-width:0'):

            with ui.card().style(
                'width:100%;padding:28px;border-radius:16px;'
                'box-shadow:0 1px 4px rgba(0,0,0,0.08)'
            ):
                # Header with live question count
                with ui.row().style(
                    'width:100%;align-items:baseline;gap:8px;margin-bottom:6px'
                ):
                    ui.label('Questions').style(
                        'font-size:16px;font-weight:600'
                    )
                    q_badge = ui.label('(0)').style(
                        'font-size:14px;color:#888'
                    )

                ui.label('Your added questions').style(
                    'font-size:13px;color:#888;margin-bottom:20px'
                )

                # Live question list display
                q_display = ui.column().style('width:100%;gap:8px')
                with q_display:
                    no_q_label = ui.label('No questions added yet').style(
                        'font-size:13px;color:#BBB;text-align:center;'
                        'padding:24px 0'
                    )

                ui.html(
                    '<hr style="border:none;border-top:1px solid #EBEBEB;'
                    'margin:20px 0">'
                )

                def save_quiz():
                    """Validate and save the quiz with all its questions."""
                    if not title.value:
                        ui.notify('Title is required!', color='negative')
                        return
                    if not questions:
                        ui.notify(
                            'Add at least 1 question!', color='negative'
                        )
                        return

                    # Create quiz record
                    quiz = quiz_service.create(
                        session=session,
                        title=title.value,
                        description=description.value,
                        teacher_id=teacher_id
                    )

                    # Save each question and its answer options
                    for q in questions:
                        question = quiz_service.add_question(
                            session=session,
                            text=q['text'],
                            quiz_id=quiz.id,
                            question_type=q['type']
                        )
                        if q['type'] == 'truefalse':
                            quiz_service.add_answer_option(
                                session, 'True', True, question.id
                            )
                            quiz_service.add_answer_option(
                                session, 'False', False, question.id
                            )
                        else:
                            for i, opt_text in enumerate(q['options']):
                                if not opt_text:
                                    continue
                                is_correct = i in q['correct_list']
                                quiz_service.add_answer_option(
                                    session, opt_text, is_correct, question.id
                                )

                    ui.notify('Quiz saved!', color='positive')
                    ui.navigate.to('/teacher/dashboard')

                ui.button('💾 Save Quiz',
                    on_click=save_quiz
                ).style(
                    'width:100%;background:#111;color:white;'
                    'border-radius:10px;font-size:15px;'
                    'font-weight:500;padding:16px'
                )

    # --- Add question button (defined after q_display exists) ---
    def add_question():
        """Validate, add question to list and refresh right-side display."""
        if not q_text.value:
            ui.notify('Please enter a question!', color='negative')
            return

        type_map = {
            'single': 'Single Choice',
            'multiple': 'Multiple Choice',
            'truefalse': 'True/False'
        }

        # Collect correct answer indices per type
        if q_type.value == 'multiple':
            correct_list = [
                i for i, cb in enumerate([cb1, cb2, cb3, cb4]) if cb.value
            ]
            if not correct_list:
                ui.notify(
                    'Select at least one correct answer!', color='negative'
                )
                return
        elif q_type.value == 'single':
            mapping = {
                'Option 1': 0, 'Option 2': 1,
                'Option 3': 2, 'Option 4': 3
            }
            correct_list = [mapping.get(correct_single.value, -1)]
        else:
            correct_list = []

        questions.append({
            'text': q_text.value,
            'type': q_type.value,
            'options': [opt1.value, opt2.value, opt3.value, opt4.value],
            'correct_list': correct_list
        })

        # Refresh right-side question list
        q_display.clear()
        with q_display:
            for i, q in enumerate(questions):
                with ui.row().style(
                    'width:100%;align-items:flex-start;gap:10px;'
                    'padding:12px 14px;background:#F5F5F7;'
                    'border-radius:10px'
                ):
                    ui.label(f'{i + 1}.').style(
                        'font-size:13px;color:#888;min-width:20px;margin-top:2px'
                    )
                    with ui.column().style('flex:1;gap:2px'):
                        ui.label(q['text']).style(
                            'font-size:13px;font-weight:500;color:#1A1A18'
                        )
                        ui.label(type_map.get(q['type'], q['type'])).style(
                            'font-size:11px;color:#888'
                        )

        q_badge.set_text(f'({len(questions)})')
        ui.notify('Question added!', color='positive')

        # Reset form fields
        q_text.value = ''
        opt1.value = opt2.value = ''
        opt3.value = opt4.value = ''
        cb1.value = cb2.value = False
        cb3.value = cb4.value = False

    # Attach add_question to the button inside the left card
    # Re-render the button in the left column at the bottom
    with ui.row().style('padding:0 32px;margin-top:-12px'):
        ui.button('+ Add Question',
            on_click=add_question
        ).style(
            'flex:1;background:#111;color:white;'
            'border-radius:10px;font-size:14px;'
            'padding:14px;margin-bottom:32px'
        )