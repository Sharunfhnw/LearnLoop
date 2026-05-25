from nicegui import ui
from data_access.db import Database
from services.quiz_service import QuizService


def quiz_create(teacher_id: int):
    """Quiz creation page — Desktop layout, German UI, True/False fix."""
    ui.query('body').style('background-color:#F5F5F7;margin:0')

    db = Database()
    session = db.get_session()
    quiz_service = QuizService()
    questions = []  # list of dicts

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
        ui.label('Neues Quiz erstellen').style('font-size:20px;font-weight:700;color:#1A1A18')

    # ── Two-column layout ─────────────────────────────────────────────────────
    with ui.row().style(
        'padding:32px 40px;gap:28px;align-items:flex-start;'
        'max-width:1200px;margin:0 auto;box-sizing:border-box;width:100%'
    ):

        # ===== LEFT COLUMN =====
        with ui.column().style('flex:1;gap:20px;min-width:0'):

            # Quiz info card
            with ui.card().style('width:100%;padding:28px;border-radius:16px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.08)'):
                ui.label('Quiz Informationen').style('font-size:16px;font-weight:700;margin-bottom:20px')

                ui.label('Titel').style('font-size:13px;font-weight:600;margin-bottom:6px')
                title = ui.input(placeholder='z.B. Mathematik Grundlagen').style('width:100%;font-size:14px;margin-bottom:16px')
                title.props('outlined dense')

                ui.label('Beschreibung').style('font-size:13px;font-weight:600;margin-bottom:6px')
                description = ui.textarea(placeholder='Worum geht es in diesem Quiz?').style('width:100%;font-size:14px')
                description.props('outlined rows=3')

            # Add question card
            with ui.card().style('width:100%;padding:28px;border-radius:16px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.08)'):
                ui.label('Frage hinzufügen').style('font-size:16px;font-weight:700;margin-bottom:4px')

                ui.label('Fragetyp').style('font-size:13px;font-weight:600;margin-bottom:6px;margin-top:16px')
                q_type = ui.select(
                    options={'single': 'Single Choice', 'multiple': 'Multiple Choice', 'truefalse': 'True/False'},
                    value='single'
                ).style('width:100%;font-size:14px;margin-bottom:16px')
                q_type.props('outlined dense')

                ui.label('Frage').style('font-size:13px;font-weight:600;margin-bottom:6px')
                q_text = ui.input(placeholder='Deine Frage hier...').style('width:100%;font-size:14px;margin-bottom:16px')
                q_text.props('outlined dense')

                # ── Options area (Single / Multiple) ─────────────────────────
                opts_container = ui.column().style('width:100%;gap:10px')
                with opts_container:
                    ui.label('Antwortoptionen').style('font-size:13px;font-weight:600;margin-bottom:4px')
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

                # ── Single Choice: correct answer dropdown ────────────────────
                single_area = ui.column().style('width:100%;margin-top:8px')
                with single_area:
                    ui.label('Richtige Antwort').style('font-size:13px;font-weight:600;margin-bottom:6px')
                    correct_single = ui.select(
                        options=['Option 1', 'Option 2', 'Option 3', 'Option 4'],
                        value='Option 1'
                    ).style('width:100%;font-size:14px')
                    correct_single.props('outlined dense')

                # ── Multiple Choice: checkboxes ───────────────────────────────
                multi_area = ui.column().style('width:100%;margin-top:8px;display:none')
                with multi_area:
                    ui.label('Richtige Antworten (mehrere möglich)').style('font-size:13px;font-weight:600;margin-bottom:8px')
                    cb1 = ui.checkbox('Option 1 ist korrekt')
                    cb2 = ui.checkbox('Option 2 ist korrekt')
                    cb3 = ui.checkbox('Option 3 ist korrekt')
                    cb4 = ui.checkbox('Option 4 ist korrekt')

                # ── True/False: which answer is correct ───────────────────────
                tf_area = ui.column().style('width:100%;margin-top:8px;display:none')
                with tf_area:
                    ui.label('Richtige Antwort').style('font-size:13px;font-weight:600;margin-bottom:8px')
                    tf_correct = ui.select(
                        options={'wahr': 'Wahr (True)', 'falsch': 'Falsch (False)'},
                        value='wahr'
                    ).style('width:100%;font-size:14px')
                    tf_correct.props('outlined dense')

                def on_type_change(val):
                    if val == 'truefalse':
                        opts_container.style('display:none')
                        single_area.style('display:none')
                        multi_area.style('display:none')
                        tf_area.style('display:block')
                    elif val == 'multiple':
                        opts_container.style('display:block')
                        single_area.style('display:none')
                        multi_area.style('display:block')
                        tf_area.style('display:none')
                    else:
                        opts_container.style('display:block')
                        single_area.style('display:block')
                        multi_area.style('display:none')
                        tf_area.style('display:none')

                q_type.on_value_change(lambda e: on_type_change(e.value))

                ui.html('<hr style="border:none;border-top:1px solid #EBEBEB;margin:20px 0">')

                def add_question():
                    if not q_text.value.strip():
                        ui.notify('Bitte Frage eingeben!', color='negative')
                        return

                    type_map = {'single': 'Single Choice', 'multiple': 'Multiple Choice', 'truefalse': 'True/False'}

                    if q_type.value == 'multiple':
                        correct_list = [i for i, cb in enumerate([cb1, cb2, cb3, cb4]) if cb.value]
                        if not correct_list:
                            ui.notify('Bitte mindestens eine korrekte Antwort wählen!', color='negative')
                            return
                        options = [opt1.value, opt2.value, opt3.value, opt4.value]
                        if not any(options):
                            ui.notify('Bitte Antwortoptionen eingeben!', color='negative')
                            return
                        questions.append({'text': q_text.value, 'type': 'multiple',
                                          'options': options, 'correct_list': correct_list, 'tf_correct': None})

                    elif q_type.value == 'single':
                        mapping = {'Option 1': 0, 'Option 2': 1, 'Option 3': 2, 'Option 4': 3}
                        correct_list = [mapping.get(correct_single.value, 0)]
                        options = [opt1.value, opt2.value, opt3.value, opt4.value]
                        if not any(options):
                            ui.notify('Bitte Antwortoptionen eingeben!', color='negative')
                            return
                        questions.append({'text': q_text.value, 'type': 'single',
                                          'options': options, 'correct_list': correct_list, 'tf_correct': None})

                    else:  # truefalse
                        questions.append({'text': q_text.value, 'type': 'truefalse',
                                          'options': [], 'correct_list': [], 'tf_correct': tf_correct.value})

                    refresh_question_list()
                    ui.notify('Frage hinzugefügt!', color='positive')

                    # Reset form
                    q_text.value = ''
                    opt1.value = opt2.value = opt3.value = opt4.value = ''
                    cb1.value = cb2.value = cb3.value = cb4.value = False
                    tf_correct.value = 'wahr'

                ui.button('+ Frage hinzufügen', on_click=add_question).style(
                    'width:100%;background:#1A1A18;color:white;'
                    'border-radius:10px;font-size:14px;padding:14px'
                ).props('no-caps flat')

        # ===== RIGHT COLUMN =====
        with ui.column().style('flex:1;gap:20px;min-width:0'):
            with ui.card().style('width:100%;padding:28px;border-radius:16px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.08)'):
                with ui.row().style('width:100%;align-items:baseline;gap:8px;margin-bottom:6px'):
                    ui.label('Fragen').style('font-size:16px;font-weight:700')
                    q_badge = ui.label('(0)').style('font-size:14px;color:#888')

                ui.label('Ihre hinzugefügten Fragen').style('font-size:13px;color:#999;margin-bottom:20px')

                q_display = ui.column().style('width:100%;gap:8px')

                with q_display:
                    ui.html('&#128196;').style('font-size:32px;color:#ddd;text-align:center;display:block;margin:16px 0 4px')
                    ui.label('Noch keine Fragen hinzugefügt').style('font-size:13px;color:#ccc;text-align:center;padding-bottom:16px')

                ui.html('<hr style="border:none;border-top:1px solid #EBEBEB;margin:20px 0">')

                type_map = {'single': 'Single Choice', 'multiple': 'Multiple Choice', 'truefalse': 'True/False'}

                def refresh_question_list():
                    q_display.clear()
                    q_badge.set_text(f'({len(questions)})')
                    with q_display:
                        if not questions:
                            ui.html('&#128196;').style('font-size:32px;color:#ddd;text-align:center;display:block;margin:16px 0 4px')
                            ui.label('Noch keine Fragen hinzugefügt').style('font-size:13px;color:#ccc;text-align:center;padding-bottom:16px')
                            return
                        for i, q in enumerate(questions):
                            with ui.row().style(
                                'width:100%;align-items:flex-start;gap:10px;'
                                'padding:12px 14px;background:#F5F5F7;border-radius:10px'
                            ):
                                ui.label(f'{i + 1}.').style('font-size:13px;color:#888;min-width:20px;margin-top:2px')
                                with ui.column().style('flex:1;gap:2px'):
                                    ui.label(q['text']).style('font-size:13px;font-weight:600;color:#1A1A18')
                                    extra = ''
                                    if q['type'] == 'truefalse':
                                        extra = f" → Richtig: {'Wahr' if q['tf_correct'] == 'wahr' else 'Falsch'}"
                                    ui.label(f"{type_map.get(q['type'], q['type'])}{extra}").style('font-size:11px;color:#888')

                def save_quiz():
                    if not title.value.strip():
                        ui.notify('Titel ist erforderlich!', color='negative')
                        return
                    if not questions:
                        ui.notify('Mindestens 1 Frage erforderlich!', color='negative')
                        return

                    quiz = quiz_service.create(session=session, title=title.value,
                                               description=description.value, teacher_id=teacher_id)

                    for q in questions:
                        question = quiz_service.add_question(session=session, text=q['text'],
                                                             quiz_id=quiz.id, question_type=q['type'])
                        if q['type'] == 'truefalse':
                            # Correct answer determined by teacher selection
                            wahr_correct = (q['tf_correct'] == 'wahr')
                            quiz_service.add_answer_option(session, 'Wahr', wahr_correct, question.id)
                            quiz_service.add_answer_option(session, 'Falsch', not wahr_correct, question.id)
                        else:
                            for i, opt_text in enumerate(q['options']):
                                if not opt_text.strip():
                                    continue
                                is_correct = i in q['correct_list']
                                quiz_service.add_answer_option(session, opt_text, is_correct, question.id)

                    ui.notify('Quiz gespeichert!', color='positive')
                    ui.navigate.to('/teacher/dashboard')

                with ui.button(on_click=save_quiz).style(
                    'width:100%;background:#1A1A18;color:white;'
                    'border-radius:10px;font-size:15px;font-weight:600;padding:16px'
                ).props('no-caps flat'):
                    ui.html('&#128190; Quiz speichern')
