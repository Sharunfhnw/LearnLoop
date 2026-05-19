from nicegui import ui
from data_access.db import Database
from services.auth_service import AuthService


def register_page():
    ui.query('body').style('background-color:#EEF2FF;margin:0')
    auth = AuthService()

    with ui.column().classes('absolute-center items-center'):
        ui.html(
            'Learn<span style="color:#185FA5">Loop</span>'
        ).style(
            'font-size:28px;font-weight:500;'
            'text-align:center;margin-bottom:4px'
        )
        ui.label('Konto erstellen').style(
            'font-size:14px;color:#666;'
            'text-align:center;margin-bottom:24px'
        )
        with ui.card().style(
            'width:400px;padding:28px;border-radius:16px'
        ):
            ui.label('Registrieren').style(
                'font-size:18px;font-weight:500;margin-bottom:20px'
            )
            username = ui.input('Benutzername').style(
                'width:100%;margin-bottom:12px'
            )
            email = ui.input('E-Mail').style(
                'width:100%;margin-bottom:12px'
            )
            password = ui.input(
                'Passwort (min. 6 Zeichen)', password=True
            ).style('width:100%;margin-bottom:16px')

            ui.label('Rolle waehlen').style(
                'font-size:13px;font-weight:500;margin-bottom:8px'
            )
            role_val = {'value': 'student'}

            with ui.row().style(
                'gap:10px;width:100%;margin-bottom:20px'
            ):
                t_card = ui.card().style(
                    'flex:1;padding:16px;text-align:center;'
                    'cursor:pointer;border:1.5px solid #185FA5;'
                    'background:#E6F1FB'
                )
                s_card = ui.card().style(
                    'flex:1;padding:16px;text-align:center;cursor:pointer'
                )
                with t_card:
                    ui.label('Lehrer').style(
                        'font-size:13px;font-weight:500'
                    )
                with s_card:
                    ui.label('Schueler').style(
                        'font-size:13px;font-weight:500'
                    )

            def do_register():
                if not username.value or not password.value:
                    ui.notify(
                        'Alle Felder ausfullen!', color='negative'
                    )
                    return
                if len(password.value) < 6:
                    ui.notify(
                        'Mind. 6 Zeichen!', color='negative'
                    )
                    return
                db = Database()
                session = db.get_session()
                # AuthService fuer Registrierung verwenden
                auth.register(
                    session=session,
                    username=username.value,
                    email=email.value,
                    password=password.value,
                    role=role_val['value']
                )
                ui.notify('Konto erstellt!', color='positive')
                ui.navigate.to('/')

            ui.button(
                'Konto erstellen', on_click=do_register
            ).style(
                'width:100%;background:#111;color:white;'
                'border-radius:8px;padding:12px'
            )
            ui.html(
                '<div style="text-align:center;margin-top:14px;'
                'font-size:13px;color:#666">'
                'Bereits ein Konto? '
                '<a href="/" style="color:#185FA5">'
                'Anmelden</a></div>'
            )