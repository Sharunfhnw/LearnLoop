from nicegui import ui
from data_access.db import Database
from ui.pages import Pages


class QuizApplication:
    """Composition Root app — gets everything started"""

    def __init__(self):
        self.database = Database()
        self.database.init_schema_and_seed()
        self.pages = Pages()

    def run(
        self,
        host: str = '0.0.0.0',
        port: int = 8080,
        reload: bool = False
    ) -> None:
        """Launch the NiceGUI app"""
        self.pages.register()
        ui.run(
            host=host,
            port=port,
            reload=reload,
            storage_secret='quiz_app_secret_key'
        )


if __name__ == '__main__':
    QuizApplication().run()