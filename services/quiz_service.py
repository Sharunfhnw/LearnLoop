from sqlmodel import select
from domain.models import (
    Quiz,
    Question,
    AnswerOption,
    QuizAttempt,
    StudentAnswer,
    StudentAnswerSelection,
)


class QuizService:
    """Business logic for quiz management."""

    def get_published(self, session) -> list:
        return session.exec(
            select(Quiz).where(Quiz.is_published == True)
        ).all()

    def get_by_teacher(self, session, teacher_id: int) -> list:
        return session.exec(
            select(Quiz).where(Quiz.teacher_id == teacher_id)
        ).all()

    def get_questions(self, session, quiz_id: int) -> list:
        return session.exec(
            select(Question).where(Question.quiz_id == quiz_id)
        ).all()

    def get_answer_options(self, session, question_id: int) -> list:
        return session.exec(
            select(AnswerOption).where(AnswerOption.question_id == question_id)
        ).all()

    def get_correct_answer_text(self, session, question_id: int) -> str:
        options = self.get_answer_options(session, question_id)
        return ", ".join(option.text for option in options if option.is_correct)

    def search_published(self, session, query: str) -> list:
        quizzes = self.get_published(session)
        query = (query or "").lower().strip()
        if not query:
            return quizzes
        return [
            quiz for quiz in quizzes
            if query in quiz.title.lower()
            or query in quiz.description.lower()
        ]

    def search_by_teacher(self, session, teacher_id: int, query: str) -> list:
        quizzes = self.get_by_teacher(session, teacher_id)
        query = (query or "").lower().strip()
        if not query:
            return quizzes
        return [
            quiz for quiz in quizzes
            if query in quiz.title.lower()
            or query in quiz.description.lower()
        ]

    def publish(self, session, quiz: Quiz) -> Quiz:
        quiz.publish()
        session.add(quiz)
        session.commit()
        return quiz

    def unpublish(self, session, quiz: Quiz) -> Quiz:
        quiz.is_published = False
        session.add(quiz)
        session.commit()
        return quiz

    def update_info(self, session, quiz: Quiz, title: str, description: str) -> Quiz:
        quiz.title = title.strip()
        quiz.description = description.strip()
        session.add(quiz)
        session.commit()
        return quiz

    def create(self, session, title: str, description: str, teacher_id: int) -> Quiz:
        quiz = Quiz(
            title=title,
            description=description,
            teacher_id=teacher_id,
            is_published=False
        )
        session.add(quiz)
        session.commit()
        session.refresh(quiz)
        return quiz

    def add_question(self, session, text: str, quiz_id: int, question_type: str) -> Question:
        question = Question(
            text=text,
            quiz_id=quiz_id,
            question_type=question_type
        )
        session.add(question)
        session.commit()
        session.refresh(question)
        return question

    def add_answer_option(self, session, text: str, is_correct: bool, question_id: int) -> AnswerOption:
        option = AnswerOption(
            text=text,
            is_correct=is_correct,
            question_id=question_id
        )
        session.add(option)
        session.commit()
        session.refresh(option)
        return option

    def delete_question(self, session, question: Question) -> None:
        options = self.get_answer_options(session, question.id)
        for option in options:
            session.delete(option)
        session.delete(question)
        session.commit()

    def delete(self, session, quiz: Quiz) -> None:
        """Delete quiz and related attempts, answers, selections, questions and options."""
        attempts = session.exec(
            select(QuizAttempt).where(QuizAttempt.quiz_id == quiz.id)
        ).all()
        for attempt in attempts:
            student_answers = session.exec(
                select(StudentAnswer).where(StudentAnswer.attempt_id == attempt.id)
            ).all()
            for student_answer in student_answers:
                selections = session.exec(
                    select(StudentAnswerSelection).where(
                        StudentAnswerSelection.student_answer_id == student_answer.id
                    )
                ).all()
                for selection in selections:
                    session.delete(selection)
                session.delete(student_answer)
            session.delete(attempt)

        questions = self.get_questions(session, quiz.id)
        for question in questions:
            options = self.get_answer_options(session, question.id)
            for option in options:
                session.delete(option)
            session.delete(question)

        session.delete(quiz)
        session.commit()
