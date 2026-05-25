from sqlmodel import select
from domain.models import QuizAttempt, StudentAnswer


class AttemptService:
    """Business logic for quiz attempts and score calculation."""

    def calculate_percentage(self, score: int, max_score: int) -> int:
        """Convert score to percentage (whole number)."""
        attempt = QuizAttempt(score=score, max_score=max_score, student_id=0, quiz_id=0)
        return attempt.get_percentage()

    def get_attempts_by_student(self, session, student_id: int) -> list:
        return session.exec(
            select(QuizAttempt).where(QuizAttempt.student_id == student_id)
        ).all()

    def get_attempts_by_quiz(self, session, quiz_id: int) -> list:
        return session.exec(
            select(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id)
        ).all()

    def get_average(self, attempts: list) -> int:
        """Calculate the average score as a whole percentage."""
        if not attempts:
            return 0
        return round(
            sum(a.score / a.max_score * 100 for a in attempts if a.max_score > 0)
            / len(attempts)
        )

    def get_best(self, attempts: list) -> int:
        """Best result as a whole percentage."""
        if not attempts:
            return 0
        return round(max(
            a.score / a.max_score * 100 for a in attempts if a.max_score > 0
        ))
