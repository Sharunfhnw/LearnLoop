from sqlmodel import select
from domain.models import (
    QuizAttempt,
    StudentAnswer,
    StudentAnswerSelection,
    AnswerOption,
)


class AttemptService:
    """Business logic for quiz attempts and score calculation."""

    def calculate_percentage(self, score: int, max_score: int) -> int:
        if max_score == 0:
            return 0
        return round(score / max_score * 100)

    def get_attempts_by_student(self, session, student_id: int) -> list:
        return session.exec(
            select(QuizAttempt).where(QuizAttempt.student_id == student_id)
        ).all()

    def get_attempts_by_quiz(self, session, quiz_id: int) -> list:
        return session.exec(
            select(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id)
        ).all()

    def get_student_answers_by_attempt(self, session, attempt_id: int) -> list:
        return session.exec(
            select(StudentAnswer).where(StudentAnswer.attempt_id == attempt_id)
        ).all()

    def get_selections_by_student_answer(self, session, student_answer_id: int) -> list:
        return session.exec(
            select(StudentAnswerSelection).where(
                StudentAnswerSelection.student_answer_id == student_answer_id
            )
        ).all()

    def get_selected_options(self, session, student_answer_id: int) -> list:
        selections = self.get_selections_by_student_answer(session, student_answer_id)
        return [
            session.get(AnswerOption, selection.answer_option_id)
            for selection in selections
        ]

    def get_selected_answer_text(self, session, student_answer_id: int) -> str:
        options = self.get_selected_options(session, student_answer_id)
        return ", ".join(option.text for option in options if option) or "-"

    def get_average(self, attempts: list) -> int:
        if not attempts:
            return 0
        percentages = [
            self.calculate_percentage(a.score, a.max_score)
            for a in attempts
            if a.max_score > 0
        ]
        if not percentages:
            return 0
        return round(sum(percentages) / len(percentages))

    def get_best(self, attempts: list) -> int:
        if not attempts:
            return 0
        percentages = [
            self.calculate_percentage(a.score, a.max_score)
            for a in attempts
            if a.max_score > 0
        ]
        return max(percentages) if percentages else 0

    def submit_attempt(self, session, student_id: int, quiz_id: int, questions: list, answers: dict) -> QuizAttempt:
        attempt = QuizAttempt(
            student_id=student_id,
            quiz_id=quiz_id,
            score=0,
            max_score=len(questions)
        )
        session.add(attempt)
        session.commit()
        session.refresh(attempt)

        score = 0
        for question in questions:
            selected_value = answers.get(question.id)
            if isinstance(selected_value, set):
                selected_ids = set(selected_value)
            elif isinstance(selected_value, list):
                selected_ids = set(selected_value)
            elif selected_value is None:
                selected_ids = set()
            else:
                selected_ids = {selected_value}

            options = session.exec(
                select(AnswerOption).where(AnswerOption.question_id == question.id)
            ).all()
            correct_ids = {option.id for option in options if option.is_correct}
            is_correct = selected_ids == correct_ids

            student_answer = StudentAnswer(
                attempt_id=attempt.id,
                question_id=question.id,
                is_correct=is_correct
            )
            session.add(student_answer)
            session.commit()
            session.refresh(student_answer)

            for option_id in selected_ids:
                session.add(StudentAnswerSelection(
                    student_answer_id=student_answer.id,
                    answer_option_id=option_id
                ))

            if is_correct:
                score += 1

        attempt.score = score
        session.add(attempt)
        session.commit()
        session.refresh(attempt)
        return attempt
