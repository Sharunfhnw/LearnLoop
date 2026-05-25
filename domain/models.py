"""LearnLoop domain models.
Defines all database tables using SQLModel.
Each class represents one table in the SQLite database.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: str
    role: str  # 'teacher' or 'student'

    quizzes: list["Quiz"] = Relationship(back_populates="teacher")
    attempts: list["QuizAttempt"] = Relationship(back_populates="student")

    def check_password(self, password_hash: str) -> bool:
        """Compare a given password hash with the stored password hash."""
        return self.password_hash == password_hash

    def is_teacher(self) -> bool:
        """Return True if this user has the teacher role."""
        return self.role == "teacher"

    def is_student(self) -> bool:
        """Return True if this user has the student role."""
        return self.role == "student"


class Quiz(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    is_published: bool = False
    teacher_id: int = Field(foreign_key="user.id")

    teacher: Optional[User] = Relationship(back_populates="quizzes")
    questions: list["Question"] = Relationship(back_populates="quiz")
    attempts: list["QuizAttempt"] = Relationship(back_populates="quiz")

    def publish(self) -> None:
        """Make the quiz visible for students."""
        self.is_published = True

    def add_question(self, question: "Question") -> None:
        """Add a question object to this quiz in memory."""
        self.questions.append(question)

    def get_questions(self) -> list["Question"]:
        """Return all questions that belong to this quiz."""
        return self.questions


class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    quiz_id: int = Field(foreign_key="quiz.id")
    question_type: str = Field(default="single")
    # 'single' | 'multiple' | 'truefalse'

    quiz: Optional[Quiz] = Relationship(back_populates="questions")
    answer_options: list["AnswerOption"] = Relationship(back_populates="question")
    student_answers: list["StudentAnswer"] = Relationship(back_populates="question")

    def check_answer(self, selected_option_ids: list[int]) -> bool:
        """Check if the selected options exactly match the correct options."""
        correct_ids = {option.id for option in self.answer_options if option.is_correct}
        selected_ids = set(selected_option_ids)
        return selected_ids == correct_ids


class AnswerOption(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_correct: bool
    question_id: int = Field(foreign_key="question.id")

    question: Optional[Question] = Relationship(back_populates="answer_options")
    selections: list["StudentAnswerSelection"] = Relationship(back_populates="answer_option")

    def is_valid_option(self) -> bool:
        """Return True if this answer option contains visible text."""
        return bool(self.text and self.text.strip())


class QuizAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.id")
    quiz_id: int = Field(foreign_key="quiz.id")
    score: int = Field(default=0)
    max_score: int = Field(default=0)
    completed_at: datetime = Field(default_factory=datetime.now)

    student: Optional[User] = Relationship(back_populates="attempts")
    quiz: Optional[Quiz] = Relationship(back_populates="attempts")
    student_answers: list["StudentAnswer"] = Relationship(back_populates="attempt")

    def calculate_score(self) -> int:
        """Calculate the score from all correct student answers."""
        self.score = sum(1 for answer in self.student_answers if answer.is_correct)
        self.max_score = len(self.student_answers)
        return self.score

    def finish_attempt(self) -> None:
        """Mark the attempt as finished by setting the completion time."""
        self.completed_at = datetime.now()

    def get_percentage(self) -> int:
        """Return the achieved score as a whole percentage."""
        if self.max_score == 0:
            return 0
        return round(self.score / self.max_score * 100)


class StudentAnswer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: int = Field(foreign_key="quizattempt.id")
    question_id: int = Field(foreign_key="question.id")
    is_correct: bool = False

    attempt: Optional[QuizAttempt] = Relationship(back_populates="student_answers")
    question: Optional[Question] = Relationship(back_populates="student_answers")
    selections: list["StudentAnswerSelection"] = Relationship(back_populates="student_answer")

    def check_correctness(self) -> bool:
        """Check correctness by comparing selected options with correct options."""
        if not self.question:
            return self.is_correct
        selected_ids = [selection.answer_option_id for selection in self.selections]
        self.is_correct = self.question.check_answer(selected_ids)
        return self.is_correct

    def save_answer(self, selected_option_ids: list[int]) -> None:
        """Store selected option ids as StudentAnswerSelection objects in memory."""
        self.selections = [
            StudentAnswerSelection(answer_option_id=option_id)
            for option_id in selected_option_ids
        ]


class StudentAnswerSelection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_answer_id: int = Field(foreign_key="studentanswer.id")
    answer_option_id: int = Field(foreign_key="answeroption.id")

    student_answer: Optional[StudentAnswer] = Relationship(back_populates="selections")
    answer_option: Optional[AnswerOption] = Relationship(back_populates="selections")
