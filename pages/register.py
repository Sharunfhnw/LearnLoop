from nicegui import ui
from data_access.db import Database
from services.auth_service import AuthService


def register_page():
    ui.query('body').style('background-color:#EEF2FF;margin:0')
    auth = AuthService()

    role_val = {'value': 'teacher'}  # default

    with ui.column().classes('absolute-center items-center'):
        ui.html(
            'Learn<span style="color:#185FA5">Loop</span>'
        ).style('font-size:28px;font-weight:500;text-align:center;margin-bottom:4px')
        ui.label('Konto erstellen').style(
            'font-size:14px;color:#666;text-align:center;margin-bottom:24px'
        )
        with ui.card().style('width:420px;padding:28px;border-radius:16px'):
            ui.label('Registrieren').style(
                'font-size:18px;font-weight:500;margin-bottom:20px'
            )

            username = ui.input('Benutzername', placeholder='Dein Benutzername').style(
                'width:100%;margin-bottom:12px'
            )
            username.props('outlined dense')

            email = ui.input('E-Mail', placeholder='deine@email.ch').style(
                'width:100%;margin-bottom:12px'
            )
            email.props('outlined dense')

            password = ui.input(
                'Passwort (min. 6 Zeichen)', placeholder='••••••••', password=True
            ).style('width:100%;margin-bottom:20px')
            password.props('outlined dense')

            ui.label('Rolle wählen').style(
                'font-size:13px;font-weight:600;margin-bottom:10px'
            )

            # Role cards — use ui.element so clicks register properly
            with ui.row().style('gap:12px;width:100%;margin-bottom:20px'):

                t_card = ui.card().style(
                    'flex:1;padding:20px;text-align:center;cursor:pointer;'
                    'border:2px solid #185FA5;background:#E6F1FB;border-radius:10px'
                )
                s_card = ui.card().style(
                    'flex:1;padding:20px;text-align:center;cursor:pointer;'
                    'border:1.5px solid #E5E5E5;background:white;border-radius:10px'
                )

                with t_card:
                    ui.html('&#127891;').style('font-size:24px')
                    ui.label('Lehrer').style('font-size:14px;font-weight:600;margin-top:6px')

                with s_card:
                    ui.html('&#128100;').style('font-size:24px')
                    ui.label('Schüler').style('font-size:14px;font-weight:600;margin-top:6px')

            def select_teacher():
                role_val['value'] = 'teacher'
                t_card.style(
                    'flex:1;padding:20px;text-align:center;cursor:pointer;'
                    'border:2px solid #185FA5;background:#E6F1FB;border-radius:10px'
                )
                s_card.style(
                    'flex:1;padding:20px;text-align:center;cursor:pointer;'
                    'border:1.5px solid #E5E5E5;background:white;border-radius:10px'
                )

            def select_student():
                role_val['value'] = 'student'
                s_card.style(
                    'flex:1;padding:20px;text-align:center;cursor:pointer;'
                    'border:2px solid #3B6D11;background:#EAF3DE;border-radius:10px'
                )
                t_card.style(
                    'flex:1;padding:20px;text-align:center;cursor:pointer;'
                    'border:1.5px solid #E5E5E5;background:white;border-radius:10px'
                )

            t_card.on('click', lambda _: select_teacher())
            s_card.on('click', lambda _: select_student())

            def do_register():
                if not username.value or not password.value or not email.value:
                    ui.notify('Bitte alle Felder ausfüllen!', color='negative')
                    return
                if len(password.value) < 6:
                    ui.notify('Passwort mind. 6 Zeichen!', color='negative')
                    return
                db = Database()
                session = db.get_session()
                auth.register(
                    session=session,
                    username=username.value,
                    email=email.value,
                    password=password.value,
                    role=role_val['value']
                )
                ui.notify('Konto erstellt!', color='positive')
                ui.navigate.to('/')

            ui.button('Konto erstellen', on_click=do_register).style(
                'width:100%;background:#111;color:white;'
                'border-radius:8px;padding:12px;font-size:14px'
            ).props('no-caps flat')

            ui.html(
                '<div style="text-align:center;margin-top:14px;font-size:13px;color:#666">'
                'Bereits ein Konto? '
                '<a href="/" style="color:#185FA5">Anmelden</a></div>'
            )
