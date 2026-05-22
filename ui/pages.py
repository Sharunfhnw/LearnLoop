from nicegui import ui, app


class Pages:
    def __init__(self):
        pass

    def register(self):
        """Register all URL routes."""

        @ui.page('/')
        def login():
            from pages.login import login_page
            login_page()

        @ui.page('/register')
        def register():
            from pages.register import register_page
            register_page()

        @ui.page('/profile')
        def profile():
            from pages.profile import profile_page
            profile_page()

        # Teacher Routen
        @ui.page('/teacher/dashboard')
        def teacher_dashboard():
            from pages.teacher.dashboard import teacher_dashboard
            teacher_id = app.storage.user.get('user_id', 1)
            teacher_dashboard(teacher_id=teacher_id)

        @ui.page('/teacher/create')
        def teacher_create():
            from pages.teacher.quiz_create import quiz_create
            teacher_id = app.storage.user.get('user_id', 1)
            quiz_create(teacher_id=teacher_id)

        @ui.page('/teacher/results/{quiz_id}')
        def teacher_results(quiz_id: int):
            from pages.teacher.quiz_results import quiz_results
            quiz_results(quiz_id=quiz_id)

        # Student Routen
        @ui.page('/student/dashboard')
        def student_dashboard():
            from pages.student.dashboard import student_dashboard
            student_dashboard()

        @ui.page('/student/statistics')
        def student_statistics():
            from pages.student.statistics import student_statistics
            student_statistics()

        @ui.page('/student/quiz/{quiz_id}')
        def student_quiz(quiz_id: int):
            from pages.student.quiz_view import quiz_view
            student_id = app.storage.user.get('user_id', 1)
            quiz_view(quiz_id=quiz_id, student_id=student_id)

        @ui.page('/student/results/{attempt_id}')
        def student_results(attempt_id: int):
            from pages.student.results import results_page
            results_page(attempt_id=attempt_id)