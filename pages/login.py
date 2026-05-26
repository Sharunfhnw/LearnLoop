from nicegui import ui, app
from data_access.db import Database
from services.auth_service import AuthService


def login_page():
    ui.query('body').style('background-color:#EEF2FF;margin:0')
    auth = AuthService()

    with ui.column().classes('absolute-center items-center').style('gap:0'):
        ui.html(
            'Learn<span style="color:#185FA5">Loop</span>'
        ).style(
            'font-size:28px;font-weight:500;'
            'text-align:center;margin-bottom:4px'
        )
        ui.label('Deine Lernplattform').style(
            'font-size:14px;color:#666;'
            'text-align:center;margin-bottom:24px'
        )
        with ui.card().style(
            'width:400px;padding:28px;border-radius:16px'
        ):
            ui.label('Anmelden').style(
                'font-size:18px;font-weight:500;margin-bottom:20px'
            )
            ui.label('Benutzername').style(
                'font-size:13px;font-weight:500;margin-bottom:6px'
            )
            username = ui.input(
                placeholder='Dein Benutzername'
            ).style('width:100%;margin-bottom:14px')
            ui.label('Passwort').style(
                'font-size:13px;font-weight:500;margin-bottom:6px'
            )
            password = ui.input(
                password=True, placeholder='••••••••'
            ).style('width:100%;margin-bottom:20px')

            def do_login():
                if not username.value or not password.value:
                    ui.notify(
                        'Alle Felder ausfüllen!',
                        color='negative'
                    )
                    return
                db = Database()
                session = db.get_session()
                # Use AuthService for login
                user = auth.login(
                    session=session,
                    username=username.value,
                    password=password.value
                )
                if user and user.role == 'teacher':
                    app.storage.user['user_id'] = user.id
                    app.storage.user['username'] = user.username
                    app.storage.user['role'] = user.role
                    ui.navigate.to('/teacher/dashboard')
                elif user and user.role == 'student':
                    app.storage.user['user_id'] = user.id
                    app.storage.user['username'] = user.username
                    app.storage.user['role'] = user.role
                    ui.navigate.to('/student/dashboard')
                else:
                    ui.notify(
                        'Login fehlgeschlagen!', color='negative'
                    )

            ui.button('Anmelden', on_click=do_login).style(
                'width:100%;background:#111;color:white;'
                'border-radius:8px;padding:12px;font-size:14px'
            )
            ui.html(
                '<div style="text-align:center;margin-top:14px;'
                'font-size:13px;color:#666">'
                'Noch kein Konto? '
                '<a href="/register" style="color:#185FA5">'
                'Registrieren</a></div>'
            )
            ui.html(
                '<hr style="border:none;'
                'border-top:0.5px solid #E5E5E5;margin:16px 0">'
            )
            ui.label('Demo-Zugänge').style(
                'font-size:12px;font-weight:500;'
                'color:#666;margin-bottom:8px'
            )
            with ui.row().style('gap:8px;width:100%'):
                with ui.element('div').style(
                    'flex:1;background:#E6F1FB;'
                    'border-radius:8px;padding:10px'
                ):
                    ui.label('Lehrer').style(
                        'font-size:12px;font-weight:500;color:#0C447C'
                    )
                    ui.label('lehrer / lehrer123').style(
                        'font-size:11px;color:#185FA5'
                    )
                with ui.element('div').style(
                    'flex:1;background:#EAF3DE;'
                    'border-radius:8px;padding:10px'
                ):
                    ui.label('Schueler').style(
                        'font-size:12px;font-weight:500;color:#27500A'
                    )
                    ui.label('schueler / schueler123').style(
                        'font-size:11px;color:#3B6D11'
                    )