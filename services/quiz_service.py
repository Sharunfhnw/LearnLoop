from sqlmodel import select
from domain.models import Quiz, Question, AnswerOption
class QuizService:
    """Business logic for quiz management.
    Responsible for:
    - Create and save quizzes
    - Publish a quiz
    - View quizzes (all, by Teacher, published)
    - Save questions and answers
    """
    def get_published(self, session) -> list:
        """Return all published quizzes."""
        return session.exec(
            select(Quiz).where(Quiz.is_published == True)
        ).all()
    def get_by_teacher(
        self, session, teacher_id: int
    ) -> list:
        """Return all quizzes from a teacher."""
        return session.exec(
            select(Quiz).where(Quiz.teacher_id == teacher_id)
        ).all()
    def publish(self, session, quiz: Quiz) -> Quiz:
        """Publish a quiz."""
        quiz.publish()
        session.add(quiz)
        session.commit()
        return quiz
    def create(
        self,
        session,
        title: str,
        description: str,
        teacher_id: int
    ) -> Quiz:
        """Create a new quiz."""
        quiz = Quiz(
            title=title,
            description=description,
            teacher_id=teacher_id,
            is_published=False
        )
        session.add(quiz)
        session.commit()
        return quiz
    def add_question(
        self,
        session,
        text: str,
        quiz_id: int,
        question_type: str
    ) -> Question:
        """Add a question to a quiz."""
        question = Question(
            text=text,
            quiz_id=quiz_id,
            question_type=question_type
        )
        session.add(question)
        session.commit()
        return question
    def add_answer_option(
        self,
        session,
        text: str,
        is_correct: bool,
        question_id: int
    ) -> AnswerOption:
        """Add an answer option to a question."""
        option = AnswerOption(
            text=text,
            is_correct=is_correct,
            question_id=question_id
        )
        session.add(option)
        session.commit()
        return option