from nicegui import ui, app
from data_access.db import Database
from services.auth_service import AuthService


def profile_page():
    ui.query('body').style('background-color:#F5F5F7;margin:0')
    auth = AuthService()

    with ui.row().style(
        'width:100%;background:white;padding:16px 24px;'
        'align-items:center;gap:12px;'
        'border-bottom:0.5px solid #E5E5E5;margin-bottom:24px'
    ):
        role = app.storage.user.get('role', 'student')
        back = '/teacher/dashboard' \
            if role == 'teacher' else '/student/dashboard'
        ui.button('← Zurück',
            on_click=lambda: ui.navigate.to(back)
        ).style('font-size:12px')
        ui.label('Mein Profil').style(
            'font-size:16px;font-weight:500'
        )

    with ui.column().style(
        'padding:0 24px 24px;max-width:480px;'
        'margin:0 auto;width:100%'
    ):
        # Profile card
        with ui.card().style(
            'width:100%;padding:20px;border-radius:12px;margin-bottom:16px'
        ):
            with ui.row().style('align-items:center;gap:16px'):
                username = app.storage.user.get('username', '')
                initials = username[:2].upper() if username else 'U'
                ui.html(
                    f'<div style="width:56px;height:56px;'
                    f'border-radius:50%;background:#E6F1FB;'
                    f'display:flex;align-items:center;'
                    f'justify-content:center;font-size:20px;'
                    f'font-weight:500;color:#185FA5">{initials}</div>'
                )
                with ui.column().style('gap:2px'):
                    ui.label(username).style(
                        'font-size:16px;font-weight:500'
                    )
                    role_label = 'Lehrer' \
                        if role == 'teacher' else 'Schüler'
                    role_color = '#185FA5' \
                        if role == 'teacher' else '#3B6D11'
                    role_bg = '#E6F1FB' \
                        if role == 'teacher' else '#EAF3DE'
                    ui.html(
                        f'<span style="background:{role_bg};'
                        f'color:{role_color};padding:3px 10px;'
                        f'border-radius:20px;font-size:11px;'
                        f'font-weight:500">{role_label}</span>'
                    )

        # Change password
        with ui.card().style(
            'width:100%;padding:20px;border-radius:12px'
        ):
            ui.label('Passwort ändern').style(
                'font-size:14px;font-weight:500;margin-bottom:16px'
            )
            old_pw = ui.input(
                'Altes Passwort', password=True
            ).style('width:100%;margin-bottom:12px')
            new_pw = ui.input(
                'Neues Passwort', password=True
            ).style('width:100%;margin-bottom:12px')
            confirm_pw = ui.input(
                'Passwort bestätigen', password=True
            ).style('width:100%;margin-bottom:20px')

            def change_password():
                if not old_pw.value or not new_pw.value:
                    ui.notify(
                        'Alle Felder ausfüllen!', color='negative'
                    )
                    return
                if len(new_pw.value) < 6:
                    ui.notify(
                        'Mind. 6 Zeichen!', color='negative'
                    )
                    return
                if new_pw.value != confirm_pw.value:
                    ui.notify(
                        'Passwörter stimmen nicht!', color='negative'
                    )
                    return
                db = Database()
                session = db.get_session()
                user_id = app.storage.user.get('user_id', 1)
                from domain.models import User
                user = session.get(User, user_id)
                # Use AuthService to change your password
                success = auth.change_password(
                    session=session,
                    user=user,
                    old_password=old_pw.value,
                    new_password=new_pw.value
                )
                if success:
                    ui.notify(
                        'Passwort geändert!', color='positive'
                    )
                    old_pw.value = new_pw.value = confirm_pw.value = ''
                else:
                    ui.notify(
                        'Altes Passwort falsch!', color='negative'
                    )

            ui.button(
                'Passwort ändern', on_click=change_password
            ).style(
                'width:100%;background:#111;color:white;'
                'border-radius:8px;font-size:13px'
            )
