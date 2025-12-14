import pytest
from datetime import date

from password_system.password_system import (
    Password,
    PasswordPolicy,
    PasswordGenerator,
    AbstractPasswordAnalyzer,
    BasicPasswordAnalyzer,
    AdvancedPasswordAnalyzer,
    run_analysis,
)


# ===============================
# PASSWORD CLASS TESTS
# ===============================

def test_password_creation_valid():
    pw = Password("Abc123!")
    assert pw.length == 7
    assert pw.contains_uppercase is True
    assert pw.contains_lowercase is True
    assert pw.contains_digit is True
    assert pw.contains_special is True


def test_password_empty_raises_error():
    with pytest.raises(ValueError):
        Password("")


def test_password_non_string_raises_error():
    with pytest.raises(TypeError):
        Password(12345)


# ===============================
# ABSTRACT BASE CLASS TEST
# ===============================

def test_abstract_analyzer_cannot_be_instantiated():
    pw = Password("Abc123!")
    with pytest.raises(TypeError):
        AbstractPasswordAnalyzer(pw)


# ===============================
# INHERITANCE + POLYMORPHISM TESTS
# ===============================

def test_basic_and_advanced_analyzers_have_different_outputs():
    pw = Password("Abc123!xyz")
    basic = BasicPasswordAnalyzer(pw)
    advanced = AdvancedPasswordAnalyzer(pw)

    basic_result = basic.analyze()
    advanced_result = advanced.analyze()

    assert "has_repeats" not in basic_result
    assert "has_repeats" in advanced_result


def test_polymorphism_via_base_class_reference():
    pw = Password("StrongPass123!")
    analyzers: list[AbstractPasswordAnalyzer] = [
        BasicPasswordAnalyzer(pw),
        AdvancedPasswordAnalyzer(pw),
    ]

    results = [run_analysis(analyzer)._analysis for analyzer in analyzers]

    assert results[0]["strength"] == "Strong"
    assert results[1]["strength"] == "Strong"
    assert "has_repeats" in results[1]


# ===============================
# COMPOSITION TESTS
# ===============================

def test_password_policy_validation():
    policy = PasswordPolicy(min_length=8)
    pw_valid = Password("Abc123!@")
    pw_invalid = Password("abc")

    assert policy.validate(pw_valid) is True
    assert policy.validate(pw_invalid) is False


def test_password_generator_respects_policy():
    policy = PasswordPolicy(min_length=12)
    generator = PasswordGenerator(policy)

    pw = generator.generate(length=12)

    assert isinstance(pw, Password)
    assert pw.length == 12
    assert policy.validate(pw) is True


# ===============================
# REPORT + ANALYSIS INTEGRATION
# ===============================

def test_run_analysis_returns_report():
    pw = Password("Abc123!@#")
    analyzer = AdvancedPasswordAnalyzer(pw)

    report = run_analysis(analyzer)

    assert hasattr(report, "__str__")
    report_str = str(report)

    assert "Password Analysis Report" in report_str
    assert "Strength" in report_str
    assert "Entropy" in report_str
