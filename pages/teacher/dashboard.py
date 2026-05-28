from nicegui import ui, app
from sqlmodel import select
from data_access.db import Database
from domain.models import Quiz, Question, QuizAttempt


def teacher_dashboard(teacher_id: int):
    """Teacher dashboard — Desktop layout, German UI."""
    ui.query('body').style('background-color:#F5F5F7;margin:0;padding:0')

    db = Database()
    session = db.get_session()
    username = app.storage.user.get('username', 'Lehrer')

    search_query = {'v': ''}

    def load_quizzes():
        return session.exec(
            select(Quiz).where(Quiz.teacher_id == teacher_id)
        ).all()

    def count_questions(quiz_id):
        return len(session.exec(
            select(Question).where(Question.quiz_id == quiz_id)
        ).all())

    def get_attempts(quiz_id):
        return session.exec(
            select(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id)
        ).all()

    # ── Header ───────────────────────────────────────────────────────────────
    with ui.row().style(
        'width:100%;background:white;padding:14px 40px;'
        'align-items:center;justify-content:space-between;'
        'box-shadow:0 1px 3px rgba(0,0,0,0.08);box-sizing:border-box'
    ):
        with ui.column().style('gap:1px'):
            ui.html(
                'Learn<span style="color:#185FA5">Loop</span>'
                '<span style="font-size:13px;color:#888;font-weight:400;margin-left:8px">Lehrer</span>'
            ).style('font-size:20px;font-weight:700;color:#1A1A18')
            ui.label(f'Willkommen zurück, {username}').style('font-size:12px;color:#888')
        with ui.row().style('gap:10px;align-items:center'):
            with ui.button(on_click=lambda: ui.navigate.to('/profile')).style(
                'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;'
                'border-radius:8px;font-size:13px'
            ).props('no-caps flat'):
                ui.html('&#128100; Profil')
            with ui.button(on_click=lambda: ui.navigate.to('/')).style(
                'background:white;color:#1A1A18;border:1.5px solid #E5E5E5;'
                'border-radius:8px;font-size:13px'
            ).props('no-caps flat'):
                ui.html('&#8594;&#xFE0E; Abmelden')

    # ── Main content ─────────────────────────────────────────────────────────
    with ui.column().style('max-width:1100px;margin:32px auto;padding:0 40px;width:100%;box-sizing:border-box'):

        # Stat cards
        quizzes = load_quizzes()
        total_q = sum(count_questions(q.id) for q in quizzes)
        total_a = sum(len(get_attempts(q.id)) for q in quizzes)

        with ui.row().style('gap:16px;margin-bottom:32px;width:100%'):
            for icon, val, label in [
                ('&#9783;', str(len(quizzes)), 'Gesamt Quizze'),
                ('&#9776;', str(total_q), 'Gesamt Fragen'),
                ('&#128101;', str(total_a), 'Schüler Versuche'),
            ]:
                with ui.card().style(
                    'flex:1;padding:24px 28px;border-radius:12px;'
                    'background:#EBF3FB;border:none;'
                    'box-shadow:none'
                ):
                    ui.html(f'{icon} <span style="font-size:13px;color:#185FA5;font-weight:500">{label}</span>').style('margin-bottom:8px')
                    ui.label(val).style('font-size:40px;font-weight:700;color:#185FA5')

        # Section header + search + new quiz
        with ui.row().style('width:100%;align-items:center;justify-content:space-between;margin-bottom:20px'):
            ui.label('Meine Quizze').style('font-size:22px;font-weight:700;color:#1A1A18')
            with ui.row().style('gap:12px;align-items:center'):
                search_input = ui.input(placeholder='🔍  Quiz suchen...').style(
                    'width:260px;font-size:13px'
                ).props('outlined dense')
                search_input.style(
                    'background:white;border-radius:8px'
                )
                ui.button(
                    on_click=lambda: ui.navigate.to('/teacher/create')
                ).style(
                    'background:#1A1A18;color:white;border-radius:8px;font-size:13px;padding:8px 18px'
                ).props('no-caps flat').set_text('+ Neues Quiz')

        # Quiz cards container
        cards_container = ui.column().style('width:100%;gap:0')

        def render_cards():
            cards_container.clear()
            q_list = load_quizzes()
            sq = search_input.value.lower().strip()
            filtered = [q for q in q_list if sq in q.title.lower() or sq in q.description.lower()] if sq else q_list

            if not filtered:
                with cards_container:
                    with ui.card().style('width:100%;padding:48px;text-align:center;border-radius:12px;background:white'):
                        ui.html('&#128196;').style('font-size:40px;color:#ccc')
                        ui.label('Keine Quizze gefunden.' if sq else 'Noch keine Quizze erstellt.').style('color:#999;margin-top:8px')
                return

            with cards_container:
                with ui.row().style('gap:20px;flex-wrap:wrap;width:100%'):
                    for quiz in filtered:
                        questions = session.exec(select(Question).where(Question.quiz_id == quiz.id)).all()
                        attempts = get_attempts(quiz.id)
                        avg_pct = None
                        if attempts:
                            avg_pct = round(sum(a.score / a.max_score * 100 for a in attempts if a.max_score > 0) / len(attempts))

                        types_used = list(dict.fromkeys(q.question_type for q in questions))
                        type_map = {'single': 'Single Choice', 'multiple': 'Multiple Choice', 'truefalse': 'True/False'}

                        with ui.card().style(
                            'min-width:320px;flex:1;max-width:500px;padding:24px;border-radius:14px;'
                            'background:white;box-shadow:0 1px 4px rgba(0,0,0,0.07)'
                        ):
                            # Title + description
                            ui.label(quiz.title).style('font-size:17px;font-weight:700;color:#1A1A18;margin-bottom:4px')
                            ui.label(quiz.description).style('font-size:12px;color:#888;margin-bottom:12px')

                            # Type badges
                            with ui.row().style('gap:6px;flex-wrap:wrap;margin-bottom:14px'):
                                for t in types_used:
                                    ui.html(
                                        f'<span style="background:#F0EDE6;color:#666;'
                                        f'padding:3px 10px;border-radius:20px;font-size:11px;border:1px solid #E8E4DC">'
                                        f'{type_map.get(t, t)}</span>'
                                    )

                            # Stats row
                            with ui.row().style(
                                'width:100%;justify-content:space-between;'
                                'padding:10px 0;border-top:1px solid #F0F0F0;'
                                'border-bottom:1px solid #F0F0F0;margin-bottom:14px'
                            ):
                                ui.label(f'{len(questions)} Fragen').style('font-size:12px;color:#888')
                                ui.label(f'{len(attempts)} Versuche').style('font-size:12px;color:#888')
                                if avg_pct is not None:
                                    ui.label(f'{avg_pct}% Ø').style('font-size:13px;font-weight:600;color:#3B6D11')
                                else:
                                    ui.label('-').style('font-size:12px;color:#bbb')

                            # Action buttons
                            with ui.row().style('gap:8px;align-items:center;flex-wrap:wrap'):
                                # Auswertungen button
                                with ui.button(
                                    on_click=lambda q=quiz: ui.navigate.to(f'/teacher/results/{q.id}')
                                ).style(
                                    'flex:2;min-width:120px;background:white;color:#1A1A18;'
                                    'border:1.5px solid #E5E5E5;border-radius:8px;font-size:12px;padding:8px 12px'
                                ).props('no-caps flat'):
                                    ui.html('&#9783; Auswertungen')

                                # Edit button
                                with ui.button(
                                    on_click=lambda q=quiz: ui.navigate.to(f'/teacher/edit/{q.id}')
                                ).style(
                                    'background:white;color:#185FA5;'
                                    'border:1.5px solid #185FA5;border-radius:8px;font-size:12px;padding:8px 12px'
                                ).props('no-caps flat'):
                                    ui.html('&#9998; Bearbeiten')

                                # Delete button
                                def confirm_delete(q=quiz):
                                    with ui.dialog() as dlg, ui.card().style('padding:24px;border-radius:12px;min-width:320px'):
                                        ui.label('Quiz löschen?').style('font-size:16px;font-weight:600;margin-bottom:8px')
                                        ui.label(f'"{q.title}" wird unwiderruflich gelöscht.').style('font-size:13px;color:#666;margin-bottom:20px')
                                        with ui.row().style('gap:10px;justify-content:flex-end'):
                                            ui.button('Abbrechen', on_click=dlg.close).props('flat no-caps').style('color:#666')
                                            def do_delete(q=q, d=dlg):
                                                # delete attempts, answers, options, questions, quiz
                                                from domain.models import StudentAnswer, AnswerOption, QuizAttempt, StudentAnswerSelection
                                                atts = session.exec(select(QuizAttempt).where(QuizAttempt.quiz_id == q.id)).all()
                                                for att in atts:
                                                    for sa in session.exec(select(StudentAnswer).where(StudentAnswer.attempt_id == att.id)).all():
                                                        for selection in session.exec(
                                                            select(StudentAnswerSelection).where(StudentAnswerSelection.student_answer_id == sa.id)
                                                        ).all():
                                                            session.delete(selection)
                                                        session.delete(sa)
                                                    session.delete(att)
                                                qs = session.exec(select(Question).where(Question.quiz_id == q.id)).all()
                                                for question in qs:
                                                    for opt in session.exec(select(AnswerOption).where(AnswerOption.question_id == question.id)).all():
                                                        session.delete(opt)
                                                    session.delete(question)
                                                session.delete(q)
                                                session.commit()
                                                d.close()
                                                ui.notify('Quiz gelöscht.', color='positive')
                                                render_cards()
                                            ui.button('Löschen', on_click=do_delete).style(
                                                'background:#A32D2D;color:white;border-radius:8px;font-size:13px'
                                            ).props('no-caps flat')
                                    dlg.open()

                                with ui.button(on_click=confirm_delete).style(
                                    'background:white;color:#A32D2D;'
                                    'border:1.5px solid #A32D2D;border-radius:8px;font-size:12px;padding:8px 12px'
                                ).props('no-caps flat'):
                                    ui.html('&#128465; Löschen')

                            # Publish status row
                            with ui.row().style('gap:8px;align-items:center;margin-top:8px'):
                                if quiz.is_published:
                                    ui.html(
                                        '<span style="background:#D4EDDA;color:#3B6D11;'
                                        'padding:5px 14px;border-radius:20px;font-size:11px;font-weight:600">'
                                        'Veröffentlicht</span>'
                                    )
                                    def unpublish(q=quiz):
                                        q.is_published = False
                                        session.add(q)
                                        session.commit()
                                        ui.notify('Quiz als Entwurf gesetzt.', color='info')
                                        render_cards()
                                    with ui.button(on_click=unpublish).style(
                                        'background:white;color:#666;border:1.5px solid #E5E5E5;'
                                        'border-radius:8px;font-size:11px;padding:4px 12px'
                                    ).props('no-caps flat'):
                                        ui.label('Als Entwurf setzen')
                                else:
                                    ui.html(
                                        '<span style="background:#F0EDE6;color:#888;'
                                        'padding:5px 14px;border-radius:20px;font-size:11px">Entwurf</span>'
                                    )
                                    def publish(q=quiz):
                                        q.is_published = True
                                        session.add(q)
                                        session.commit()
                                        ui.notify('Quiz veröffentlicht!', color='positive')
                                        render_cards()
                                    with ui.button(on_click=publish).style(
                                        'background:white;color:#185FA5;border:1.5px solid #185FA5;'
                                        'border-radius:8px;font-size:11px;padding:4px 12px'
                                    ).props('no-caps flat'):
                                        ui.html('&#10148; Veröffentlichen')

        render_cards()

        # Wire up search
        search_input.on_value_change(lambda _: render_cards())
