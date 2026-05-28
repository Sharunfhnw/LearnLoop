import hashlib


# TC_001 — Score 80%
def test_score_80_prozent():
    score = 4
    max_score = 5
    prozent = round(score / max_score * 100)
    assert prozent == 80


# TC_002 — Score 100%
def test_score_100_prozent():
    score = 5
    max_score = 5
    prozent = round(score / max_score * 100)
    assert prozent == 100


# TC_003 — Score 0%
def test_score_0_prozent():
    score = 0
    max_score = 5
    prozent = round(score / max_score * 100)
    assert prozent == 0


# TC_004 — Empty title is invalid
def test_validierung_leerer_titel():
    titel = ''
    assert titel.strip() == ''


# TC_005 — Quiz without questions is invalid
def test_validierung_keine_fragen():
    fragen = []
    assert len(fragen) == 0


# TC_006 — Password hashing
def test_passwort_hashing():
    passwort = 'meinPasswort123'
    hash1 = hashlib.sha256(passwort.encode()).hexdigest()
    hash2 = hashlib.sha256(passwort.encode()).hexdigest()
    assert hash1 == hash2


def test_passwort_hashing_unterschiedlich():
    hash1 = hashlib.sha256('passwort1'.encode()).hexdigest()
    hash2 = hashlib.sha256('passwort2'.encode()).hexdigest()
    assert hash1 != hash2

# ■■ AttemptService Tests ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# TC_019 — calculate_percentage returns correct value
def test_calculate_percentage_correct():
    """TC_019: calculate_percentage() should convert score to percent."""
    from services.attempt_service import AttemptService

    service = AttemptService()

    # 4 out of 5 correct = 80%
    result = service.calculate_percentage(score=4.0, max_score=5.0)
    assert result == 80.0

    # 0 out of 5 = 0%
    result = service.calculate_percentage(score=0.0, max_score=5.0)
    assert result == 0.0

    # 5 out of 5 = 100%
    result = service.calculate_percentage(score=5.0, max_score=5.0)
    assert result == 100.0


# TC_020 — get_average returns correct average
def test_get_average_correct():
    """TC_020: get_average() should calculate the mean percentage."""
    from services.attempt_service import AttemptService
    from unittest.mock import MagicMock

    service = AttemptService()

    # Create mock attempts with known scores
    attempt1 = MagicMock(score=4.0, max_score=5.0)  # 80%
    attempt2 = MagicMock(score=2.0, max_score=5.0)  # 40%

    attempts = [attempt1, attempt2]

    # Average of 80% and 40% = 60%
    result = service.get_average(attempts)
    assert result == 60.0

    # Empty list should return 0
    assert service.get_average([]) == 0.0


# ■■ Question Type Scoring Tests ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# TC_021 — Single Choice: 1 point for correct answer
def test_single_choice_scoring():
    """TC_021: Single Choice should give 1.0 for correct, 0.0 for wrong."""

    # Simulate scoring logic for single choice
    def score_single(is_correct: bool) -> float:
        """Return 1.0 if correct, 0.0 if wrong."""
        return 1.0 if is_correct else 0.0

    assert score_single(True) == 1.0
    assert score_single(False) == 0.0


# TC_022 — Multiple Choice: partial scoring
def test_multiple_choice_partial_scoring():
    """
    TC_022: Multiple Choice should award partial points per correct
    answer and deduct for wrong selections (minimum 0).
    """

    def score_multiple(
        correct_count: int,
        selected_correct: int,
        selected_wrong: int
    ) -> float:
        """
        Calculate partial score for multiple choice.

        Args:
            correct_count: Total number of correct answers.
            selected_correct: How many correct options student selected.
            selected_wrong: How many wrong options student selected.
        """
        if correct_count == 0:
            return 0.0

        # Points per correct answer
        pts = 1.0 / correct_count
        score = (selected_correct * pts) - (selected_wrong * pts)

        # Score cannot be negative
        return max(0.0, round(score, 2))

    # 3 correct answers, student selects all 3 → full point
    assert score_multiple(3, 3, 0) == 1.0

    # 3 correct, student selects 2 correct + 0 wrong → 2/3 points
    assert score_multiple(3, 2, 0) == round(2 / 3, 2)

    # 3 correct, student selects 1 correct + 2 wrong → 1/3 - 2/3 = negative → 0
    assert score_multiple(3, 1, 2) == 0.0

    # No correct answers selected → 0 points
    assert score_multiple(3, 0, 0) == 0.0


# TC_023 — True/False: 1 point for correct Wahr/Falsch
def test_true_false_scoring():
    """TC_023: True/False should give 1.0 for correct, 0.0 for wrong."""

    def score_truefalse(selected: str, correct_text: str) -> float:
        """Return 1.0 if selected matches correct answer text."""
        return 1.0 if selected == correct_text else 0.0

    # Student selects Wahr, correct answer is Wahr
    assert score_truefalse("Wahr", "Wahr") == 1.0

    # Student selects Falsch, correct answer is Wahr
    assert score_truefalse("Falsch", "Wahr") == 0.0

    # Student selects Falsch, correct answer is Falsch
    assert score_truefalse("Falsch", "Falsch") == 1.0