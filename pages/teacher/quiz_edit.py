from nicegui import ui
from data_access.db import Database
from domain.models import Quiz
from services.quiz_service import QuizService


def quiz_edit(quiz_id: int, teacher_id: int):
    """Edit an existing quiz — change title, description, manage questions."""
    ui.query('body').style('background-color:#F5F5F7;margin:0')

    db = Database()
    session = db.get_session()
    quiz_service = QuizService()
    quiz = session.get(Quiz, quiz_id)

    if not quiz or quiz.teacher_id != teacher_id:
        ui.label('Quiz nicht gefunden oder kein Zugriff.').style('padding:24px')
        return

    # ── Header ───────────────────────────────────────────────────────────────
    with ui.row().style(
        'width:100%;background:white;padding:14px 40px;'
        'align-items:center;gap:16px;'
        'border-bottom:1px solid #E8E8E8;box-sizing:border-box'
    ):
        with ui.button(on_click=lambda: ui.navigate.to('/teacher/dashboard')).style(
            'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px'
        ).props('no-caps flat'):
            ui.html('&#8592; Zurück')
        ui.label(f'Quiz bearbeiten: {quiz.title}').style('font-size:20px;font-weight:700;color:#1A1A18')

    with ui.column().style('max-width:800px;margin:32px auto;padding:0 40px;width:100%;box-sizing:border-box;gap:24px'):

        # Quiz info edit card
        with ui.card().style('width:100%;padding:28px;border-radius:16px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.08)'):
            ui.label('Quiz Informationen').style('font-size:16px;font-weight:700;margin-bottom:20px')

            ui.label('Titel').style('font-size:13px;font-weight:600;margin-bottom:6px')
            title_input = ui.input(value=quiz.title).style('width:100%;font-size:14px;margin-bottom:16px')
            title_input.props('outlined dense')

            ui.label('Beschreibung').style('font-size:13px;font-weight:600;margin-bottom:6px')
            desc_input = ui.textarea(value=quiz.description).style('width:100%;font-size:14px')
            desc_input.props('outlined rows=3')

            def save_info():
                if not title_input.value.strip():
                    ui.notify('Titel ist erforderlich!', color='negative')
                    return
                quiz_service.update_info(
                    session,
                    quiz,
                    title_input.value,
                    desc_input.value
                )
                ui.notify('Gespeichert!', color='positive')

            ui.button('Informationen speichern', on_click=save_info).style(
                'margin-top:16px;background:#1A1A18;color:white;border-radius:8px;font-size:13px'
            ).props('no-caps flat')

        # Existing questions
        questions = quiz_service.get_questions(session, quiz_id)

        with ui.card().style('width:100%;padding:28px;border-radius:16px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.08)'):
            ui.label(f'Vorhandene Fragen ({len(questions)})').style('font-size:16px;font-weight:700;margin-bottom:16px')

            type_map = {'single': 'Single Choice', 'multiple': 'Multiple Choice', 'truefalse': 'True/False'}

            if not questions:
                ui.label('Noch keine Fragen vorhanden.').style('color:#999;font-size:13px')
            else:
                for i, q in enumerate(questions):
                    opts = quiz_service.get_answer_options(session, q.id)
                    correct_opts = [o for o in opts if o.is_correct]
                    correct_text = ', '.join(o.text for o in correct_opts)

                    with ui.row().style(
                        'width:100%;padding:14px 16px;background:#F5F5F7;border-radius:10px;'
                        'align-items:flex-start;gap:12px;margin-bottom:8px;box-sizing:border-box'
                    ):
                        ui.label(f'{i+1}.').style('font-size:13px;color:#888;min-width:24px;margin-top:2px')
                        with ui.column().style('flex:1;gap:2px'):
                            ui.label(q.text).style('font-size:14px;font-weight:600;color:#1A1A18')
                            ui.label(type_map.get(q.question_type, q.question_type)).style('font-size:11px;color:#888')
                            ui.label(f'Richtig: {correct_text}').style('font-size:11px;color:#3B6D11')

                        def del_question(q=q):
                            quiz_service.delete_question(session, q)
                            ui.notify('Frage gelöscht.', color='info')
                            ui.navigate.to(f'/teacher/edit/{quiz_id}')

                        with ui.button(on_click=del_question).style(
                            'background:white;color:#A32D2D;border:1.5px solid #A32D2D;border-radius:6px;font-size:11px'
                        ).props('no-caps flat'):
                            ui.html('&#128465; Löschen')

        # Add new question card (same as create)
        with ui.card().style('width:100%;padding:28px;border-radius:16px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.08)'):
            ui.label('Neue Frage hinzufügen').style('font-size:16px;font-weight:700;margin-bottom:16px')

            q_type = ui.select(
                options={'single': 'Single Choice', 'multiple': 'Multiple Choice', 'truefalse': 'True/False'},
                value='single'
            ).style('width:100%;font-size:14px;margin-bottom:16px')
            q_type.props('outlined dense')

            q_text = ui.input(placeholder='Deine Frage hier...').style('width:100%;font-size:14px;margin-bottom:16px')
            q_text.props('outlined dense')

            opts_container = ui.column().style('width:100%;gap:10px')
            with opts_container:
                with ui.row().style('gap:10px;width:100%'):
                    opt1 = ui.input(placeholder='Option 1').style('flex:1;font-size:14px')
                    opt1.props('outlined dense')
                    opt2 = ui.input(placeholder='Option 2').style('flex:1;font-size:14px')
                    opt2.props('outlined dense')
                with ui.row().style('gap:10px;width:100%'):
                    opt3 = ui.input(placeholder='Option 3').style('flex:1;font-size:14px')
                    opt3.props('outlined dense')
                    opt4 = ui.input(placeholder='Option 4').style('flex:1;font-size:14px')
                    opt4.props('outlined dense')

            single_area = ui.column().style('width:100%;margin-top:8px')
            with single_area:
                ui.label('Richtige Antwort').style('font-size:13px;font-weight:600;margin-bottom:6px')
                correct_single = ui.select(
                    options=['Option 1', 'Option 2', 'Option 3', 'Option 4'], value='Option 1'
                ).style('width:100%;font-size:14px')
                correct_single.props('outlined dense')

            multi_area = ui.column().style('width:100%;margin-top:8px;display:none')
            with multi_area:
                ui.label('Richtige Antworten').style('font-size:13px;font-weight:600;margin-bottom:8px')
                cb1 = ui.checkbox('Option 1 ist korrekt')
                cb2 = ui.checkbox('Option 2 ist korrekt')
                cb3 = ui.checkbox('Option 3 ist korrekt')
                cb4 = ui.checkbox('Option 4 ist korrekt')

            tf_area = ui.column().style('width:100%;margin-top:8px;display:none')
            with tf_area:
                ui.label('Richtige Antwort').style('font-size:13px;font-weight:600;margin-bottom:8px')
                tf_correct = ui.select(
                    options={'wahr': 'Wahr (True)', 'falsch': 'Falsch (False)'}, value='wahr'
                ).style('width:100%;font-size:14px')
                tf_correct.props('outlined dense')

            def on_type_change(val):
                if val == 'truefalse':
                    opts_container.style('display:none'); single_area.style('display:none')
                    multi_area.style('display:none'); tf_area.style('display:block')
                elif val == 'multiple':
                    opts_container.style('display:block'); single_area.style('display:none')
                    multi_area.style('display:block'); tf_area.style('display:none')
                else:
                    opts_container.style('display:block'); single_area.style('display:block')
                    multi_area.style('display:none'); tf_area.style('display:none')

            q_type.on_value_change(lambda e: on_type_change(e.value))

            def add_question():
                if not q_text.value.strip():
                    ui.notify('Bitte Frage eingeben!', color='negative')
                    return
                question = quiz_service.add_question(session, q_text.value.strip(), quiz_id, q_type.value)
                if q_type.value == 'truefalse':
                    wahr_correct = (tf_correct.value == 'wahr')
                    quiz_service.add_answer_option(session, 'Wahr', wahr_correct, question.id)
                    quiz_service.add_answer_option(session, 'Falsch', not wahr_correct, question.id)
                elif q_type.value == 'single':
                    mapping = {'Option 1': 0, 'Option 2': 1, 'Option 3': 2, 'Option 4': 3}
                    correct_idx = mapping.get(correct_single.value, 0)
                    for i, opt in enumerate([opt1.value, opt2.value, opt3.value, opt4.value]):
                        if opt.strip():
                            quiz_service.add_answer_option(session, opt.strip(), i == correct_idx, question.id)
                else:
                    correct_list = [i for i, cb in enumerate([cb1, cb2, cb3, cb4]) if cb.value]
                    for i, opt in enumerate([opt1.value, opt2.value, opt3.value, opt4.value]):
                        if opt.strip():
                            quiz_service.add_answer_option(session, opt.strip(), i in correct_list, question.id)
                ui.notify('Frage hinzugefügt!', color='positive')
                ui.navigate.to(f'/teacher/edit/{quiz_id}')

            ui.button('+ Frage hinzufügen', on_click=add_question).style(
                'width:100%;background:#1A1A18;color:white;border-radius:10px;font-size:14px;padding:14px;margin-top:16px'
            ).props('no-caps flat')
