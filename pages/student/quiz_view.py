from nicegui import ui, app
from data_access.db import Database
from domain.models import Quiz
from services.quiz_service import QuizService
from services.attempt_service import AttemptService


def quiz_view(quiz_id: int, student_id: int):
    """Quiz taking page — handles Single, Multiple, and True/False correctly."""
    ui.query('body').style('background-color:#F5F5F7;margin:0')

    db = Database()
    session = db.get_session()
    quiz_service = QuizService()
    attempt_service = AttemptService()
    quiz = session.get(Quiz, quiz_id)
    questions = quiz_service.get_questions(session, quiz_id)

    if not quiz or not questions:
        ui.label('Quiz nicht gefunden.').style('padding:24px')
        return

    current_idx = {'v': 0}
    # For single/truefalse: question_id -> option_id
    # For multiple: question_id -> set of option_ids
    answers = {}

    # ── Header ───────────────────────────────────────────────────────────────
    with ui.row().style(
        'width:100%;background:white;padding:12px 40px;'
        'align-items:center;justify-content:space-between;'
        'box-shadow:0 1px 3px rgba(0,0,0,0.08)'
    ):
        with ui.button(on_click=lambda: ui.navigate.to('/student/dashboard')).style(
            'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:13px'
        ).props('no-caps flat'):
            ui.html('&#8592; Zurück')

        with ui.column().style('gap:0;align-items:center'):
            ui.label(quiz.title).style('font-size:16px;font-weight:700;color:#1A1A18')
            question_counter = ui.label('Frage 1 von ' + str(len(questions))).style('font-size:12px;color:#888')

        pct_label = ui.label('0%').style(
            'font-size:13px;color:#666;background:#F0F0F0;padding:4px 12px;border-radius:20px'
        )

    progress_bar = ui.linear_progress(value=0, show_value=False).style('height:4px;margin:0;border-radius:0')
    progress_bar.props('color=black instant-feedback')

    content = ui.column().style('max-width:700px;margin:32px auto;padding:0 40px;width:100%;box-sizing:border-box')

    def show_question(idx: int):
        current_idx['v'] = idx
        content.clear()

        q = questions[idx]
        pct = round(idx / len(questions) * 100)
        pct_label.set_text(f'{pct}%')
        progress_bar.set_value(idx / len(questions))
        question_counter.set_text(f'Frage {idx + 1} von {len(questions)}')

        options = quiz_service.get_answer_options(session, q.id)

        type_map = {'single': 'Single Choice', 'multiple': 'Multiple Choice', 'truefalse': 'True/False'}
        type_label = type_map.get(q.question_type, 'Single Choice')

        with content:
            ui.html(
                f'<span style="background:#F0EDE6;color:#666;'
                f'padding:4px 12px;border-radius:20px;font-size:11px;border:1px solid #E8E4DC">'
                f'{type_label}</span>'
            )

            with ui.card().style(
                'width:100%;padding:28px;border-radius:14px;'
                'background:white;box-shadow:0 1px 4px rgba(0,0,0,0.08);margin-top:16px'
            ):
                ui.label(q.text).style('font-size:20px;font-weight:700;margin-bottom:6px;color:#1A1A18')

                if q.question_type == 'multiple':
                    ui.label('Wähle alle richtigen Antworten').style('font-size:12px;color:#999;margin-bottom:20px')
                else:
                    ui.label('Wähle die richtige Antwort').style('font-size:12px;color:#999;margin-bottom:20px')

                if q.question_type == 'multiple':
                    # Multiple: checkbox-style, answers stored as set
                    selected_set = answers.get(q.id, set())

                    for opt in options:
                        is_selected = opt.id in selected_set
                        bg = 'background:#1A1A18;color:white' if is_selected else 'background:white;color:#1A1A18'
                        border = 'border:2px solid #1A1A18' if is_selected else 'border:1.5px solid #E5E5E5'
                        check = '☑' if is_selected else '☐'

                        with ui.row().style(
                            f'width:100%;align-items:center;gap:12px;'
                            f'padding:14px 18px;border-radius:10px;cursor:pointer;'
                            f'margin-bottom:8px;{bg};{border};box-sizing:border-box'
                        ) as row:
                            ui.label(check).style('font-size:18px')
                            ui.label(opt.text).style('font-size:15px;font-weight:500')

                            def on_click_multi(o=opt):
                                cur = answers.get(q.id, set())
                                if o.id in cur:
                                    cur.discard(o.id)
                                else:
                                    cur.add(o.id)
                                answers[q.id] = cur
                                show_question(idx)

                            row.on('click', on_click_multi)

                else:
                    # Single or True/False: radio-style
                    for opt in options:
                        is_selected = answers.get(q.id) == opt.id
                        bg = 'background:#1A1A18;color:white' if is_selected else 'background:white;color:#1A1A18'
                        border = 'border:2px solid #1A1A18' if is_selected else 'border:1.5px solid #E5E5E5'
                        radio = '●' if is_selected else '○'
                        icon_color = 'white' if is_selected else '#999'

                        with ui.row().style(
                            f'width:100%;align-items:center;gap:12px;'
                            f'padding:14px 18px;border-radius:10px;cursor:pointer;'
                            f'margin-bottom:8px;{bg};{border};box-sizing:border-box'
                        ) as row:
                            ui.label(radio).style(f'font-size:18px;color:{icon_color}')
                            ui.label(opt.text).style('font-size:15px;font-weight:500')

                            def on_click_single(o=opt):
                                answers[q.id] = o.id
                                show_question(idx)

                            row.on('click', on_click_single)

                # Navigation
                with ui.row().style('width:100%;justify-content:space-between;margin-top:24px;gap:8px'):
                    if idx > 0:
                        with ui.button(on_click=lambda: show_question(idx - 1)).style(
                            'flex:1;background:white;color:#1A1A18;border:1.5px solid #E5E5E5;border-radius:8px;font-size:14px;padding:12px'
                        ).props('no-caps flat'):
                            ui.html('&#8592; Zurück')
                    else:
                        ui.element('div').style('flex:1')

                    if idx < len(questions) - 1:
                        with ui.button(on_click=lambda: show_question(idx + 1)).style(
                            'flex:3;background:#1A1A18;color:white;border-radius:8px;font-size:14px;padding:12px'
                        ).props('no-caps flat'):
                            ui.html('Weiter &#8594;')
                    else:
                        def submit_quiz():
                            unanswered = [q for q in questions if q.id not in answers]
                            if unanswered:
                                ui.notify('Bitte alle Fragen beantworten!', color='negative')
                                return

                            attempt = attempt_service.submit_attempt(
                                session=session,
                                student_id=student_id,
                                quiz_id=quiz_id,
                                questions=questions,
                                answers=answers
                            )
                            ui.navigate.to(f'/student/results/{attempt.id}')

                        with ui.button(on_click=submit_quiz).style(
                            'flex:3;background:#3B6D11;color:white;border-radius:8px;font-size:14px;padding:12px'
                        ).props('no-caps flat'):
                            ui.html('&#10003; Quiz abgeben')

    show_question(0)
