from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import QuizAttempt, User, Quiz, StudentAnswer, Question, AnswerOption
 
 
def quiz_results(quiz_id: int):
    """Render teacher results page for a specific quiz."""
    ui.query('body').style('background-color:#F8F7F4;margin:0')
 
    db = Database()
    session = db.get_session()
    quiz = session.get(Quiz, quiz_id)
 
    attempts = session.exec(
        select(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id)
    ).all()
 
    # --- Header ---
    with ui.row().style(
        'width:100%;background:white;padding:16px 24px;'
        'align-items:center;gap:16px;'
        'border-bottom:1px solid #E5E5E5;margin-bottom:32px'
    ):
        ui.button('← Zurück',
            on_click=lambda: ui.navigate.to('/teacher/dashboard')
        ).style(
            'background:#111;color:white;border-radius:8px;'
            'font-size:13px;padding:8px 16px'
        ).props('no-caps')
        ui.label(f'Auswertungen: {quiz.title}').style(
            'font-size:20px;font-weight:600;color:#1A1A18'
        )
 
    with ui.column().style(
        'max-width:900px;margin:0 auto;padding:0 32px 32px;width:100%'
    ):
        if not attempts:
            with ui.card().style(
                'width:100%;padding:40px;text-align:center;border-radius:12px'
            ):
                ui.label('Noch keine Schüler-Versuche.').style('color:#666')
            return
 
        # Calculate average score
        avg = sum(
            a.score / a.max_score * 100 for a in attempts if a.max_score > 0
        ) / len(attempts)
 
        # --- Stat cards ---
        with ui.row().style('gap:16px;margin-bottom:28px;width:100%'):
            for val, label, color in [
                (str(len(attempts)), 'Versuche', '#185FA5'),
                (f'{avg:.0f}%', 'Durchschnitt', '#185FA5'),
            ]:
                with ui.card().style(
                    'flex:1;padding:20px;border-radius:10px;'
                    'box-shadow:0 1px 3px rgba(0,0,0,0.06)'
                ):
                    ui.label(label).style(
                        'font-size:12px;color:#666;margin-bottom:6px'
                    )
                    ui.label(val).style(
                        f'font-size:32px;font-weight:500;color:{color}'
                    )
 
        # --- Student attempts list ---
        with ui.card().style(
            'width:100%;padding:24px;border-radius:12px;'
            'box-shadow:0 1px 3px rgba(0,0,0,0.06)'
        ):
            # Table header
            ui.label('Alle Schüler').style(
                'font-size:16px;font-weight:600;margin-bottom:16px'
            )
            with ui.row().style(
                'width:100%;padding:8px 0;'
                'border-bottom:1px solid #E5E5E5;margin-bottom:8px'
            ):
                ui.label('Schüler').style(
                    'flex:2;font-size:12px;color:#666;font-weight:500'
                )
                ui.label('Punkte').style(
                    'flex:1;font-size:12px;color:#666;font-weight:500'
                )
                ui.label('%').style(
                    'flex:1;font-size:12px;color:#666;font-weight:500'
                )
                ui.label('Details').style(
                    'flex:1;font-size:12px;color:#666;font-weight:500'
                )
 
            for attempt in attempts:
                student = session.get(User, attempt.student_id)
                pct = round(
                    attempt.score / attempt.max_score * 100
                ) if attempt.max_score > 0 else 0
                color = '#3B6D11' if pct >= 60 else '#A32D2D'
 
                with ui.row().style(
                    'width:100%;align-items:center;'
                    'padding:12px 0;border-bottom:0.5px solid #F0F0F0'
                ):
                    ui.label(
                        student.username if student else '-'
                    ).style('flex:2;font-size:13px;font-weight:500')
                    ui.label(
                        f'{attempt.score}/{attempt.max_score}'
                    ).style('flex:1;font-size:13px;color:#666')
                    ui.label(f'{pct}%').style(
                        f'flex:1;font-size:13px;font-weight:500;color:{color}'
                    )
 
                    # Expand/collapse detail button
                    detail_container = ui.column().style(
                        'width:100%;display:none;margin-top:8px;gap:6px'
                    )
 
                    def toggle_detail(c=detail_container):
                        """Toggle the detail view for this attempt."""
                        current = c._props.get('style', '')
                        if 'display:none' in current:
                            c.style(current.replace('display:none', 'display:block'))
                        else:
                            c.style(current.replace('display:block', 'display:none'))
 
                    with ui.element('div').style('flex:1'):
                        ui.button('Details',
                            on_click=toggle_detail
                        ).style(
                            'background:white;color:#1A1A18;'
                            'border:1.5px solid #E5E5E5;border-radius:6px;'
                            'font-size:11px;padding:4px 10px'
                        ).props('no-caps')
 
                # Detail row: per-question breakdown
                answers = session.exec(
                    select(StudentAnswer).where(
                        StudentAnswer.attempt_id == attempt.id
                    )
                ).all()
 
                with detail_container:
                    with ui.card().style(
                        'width:100%;padding:14px;background:#F8F8F8;'
                        'border-radius:8px;margin-bottom:8px'
                    ):
                        for sa in answers:
                            q = session.get(Question, sa.question_id)
                            opt = session.get(
                                AnswerOption, sa.selected_answer_option_id
                            )
                            icon = '✓' if sa.is_correct else '✗'
                            c = '#3B6D11' if sa.is_correct else '#A32D2D'
                            bg = '#EAF3DE' if sa.is_correct else '#FCEBEB'
                            with ui.row().style(
                                f'width:100%;align-items:flex-start;gap:8px;'
                                f'padding:8px;border-radius:6px;'
                                f'background:{bg};margin-bottom:4px'
                            ):
                                ui.label(icon).style(
                                    f'color:{c};font-weight:600;font-size:14px'
                                )
                                with ui.column().style('gap:2px'):
                                    ui.label(
                                        q.text if q else '-'
                                    ).style('font-size:12px;font-weight:500')
                                    ui.label(
                                        f'Antwort: {opt.text if opt else "-"}'
                                    ).style(f'font-size:11px;color:{c}')