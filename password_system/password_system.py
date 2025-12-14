from __future__ import annotations
import string
import math
import random
from abc import ABC, abstractmethod


# Represents a user's password and exposes useful properties
class Password:
    """Represents a user's password with controlled access."""

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        if not value:
            raise ValueError("Password cannot be empty")

        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @property
    def masked(self) -> str:
        return "*" * len(self._value)

    @property
    def length(self) -> int:
        return len(self._value)

    @property
    def contains_uppercase(self) -> bool:
        return any(c.isupper() for c in self._value)

    @property
    def contains_lowercase(self) -> bool:
        return any(c.islower() for c in self._value)

    @property
    def contains_digit(self) -> bool:
        return any(c.isdigit() for c in self._value)

    @property
    def contains_special(self) -> bool:
        return any(c in string.punctuation for c in self._value)

    def __str__(self):
        return f"Password(masked='{self.masked}', length={self.length})"


# Abstract base class defining the analyzer interface
class AbstractPasswordAnalyzer(ABC):
    """Abstract base class enforcing password analysis interface."""

    def __init__(self, password: Password):
        self._password = password

    @abstractmethod
    def analyze(self) -> dict:
        """Analyze the password and return results."""
        raise NotImplementedError


# Performs basic password analysis
class BasicPasswordAnalyzer(AbstractPasswordAnalyzer):
    """Performs basic password strength analysis."""

    COMMON_PASSWORDS = {"password", "123456", "qwerty", "abc123"}

    def entropy(self) -> float:
        pool = 0
        if self._password.contains_lowercase:
            pool += 26
        if self._password.contains_uppercase:
            pool += 26
        if self._password.contains_digit:
            pool += 10
        if self._password.contains_special:
            pool += len(string.punctuation)

        if pool == 0:
            return 0.0

        return round(self._password.length * math.log2(pool), 2)

    def strength(self) -> str:
        score = sum([
            self._password.length >= 8,
            self._password.contains_lowercase,
            self._password.contains_uppercase,
            self._password.contains_digit,
            self._password.contains_special,
        ])

        if score <= 2:
            return "Weak"
        elif score <= 4:
            return "Medium"
        return "Strong"

    def analyze(self) -> dict:
        return {
            "password": self._password.masked,
            "length": self._password.length,
            "entropy": self.entropy(),
            "strength": self.strength(),
            "is_common": self._password.value.lower() in self.COMMON_PASSWORDS,
        }


# Extends the basic analyzer with additional checks
class AdvancedPasswordAnalyzer(BasicPasswordAnalyzer):
    """Extends analysis with repeated pattern detection."""

    def has_repeated_patterns(self) -> bool:
        pw = self._password.value
        n = len(pw)

        for size in range(1, n // 2 + 1):
            for start in range(n - 2 * size + 1):
                if pw[start:start + size] == pw[start + size:start + 2 * size]:
                    return True
        return False

    def analyze(self) -> dict:
        results = super().analyze()
        results["has_repeats"] = self.has_repeated_patterns()
        return results


# Defines password validation rules
class PasswordPolicy:
    """Defines password validation rules."""

    def __init__(
        self,
        min_length=8,
        require_upper=True,
        require_lower=True,
        require_digit=True,
        require_special=True,
    ):
        self.min_length = min_length
        self.require_upper = require_upper
        self.require_lower = require_lower
        self.require_digit = require_digit
        self.require_special = require_special

    def validate(self, password: Password) -> bool:
        return all([
            password.length >= self.min_length,
            not self.require_upper or password.contains_uppercase,
            not self.require_lower or password.contains_lowercase,
            not self.require_digit or password.contains_digit,
            not self.require_special or password.contains_special,
        ])


# Generates passwords that follow a policy
class PasswordGenerator:
    """Generates passwords based on a policy."""

    def __init__(self, policy: PasswordPolicy):
        self._policy = policy

    def generate(self, length=12) -> Password:
        if length < self._policy.min_length:
            raise ValueError("Length below policy minimum")

        while True:
            chars = [
                random.choice(string.ascii_uppercase),
                random.choice(string.ascii_lowercase),
                random.choice(string.digits),
                random.choice(string.punctuation),
            ]

            chars += random.choices(
                string.ascii_letters + string.digits + string.punctuation,
                k=length - 4,
            )

            random.shuffle(chars)
            password = Password("".join(chars))

            if self._policy.validate(password):
                return password


# Formats analysis results for display
class PasswordReport:
    """Formats analysis results for display."""

    def __init__(self, analysis: dict):
        self._analysis = analysis

    def __str__(self) -> str:
        lines = [
            "Password Analysis Report",
            "------------------------",
        ]
        for key, value in self._analysis.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
        return "\n".join(lines)


# Runs analysis using polymorphism
def run_analysis(analyzer: AbstractPasswordAnalyzer) -> PasswordReport:
    """Runs analysis using polymorphism."""
    return PasswordReport(analyzer.analyze())


# Demonstrates system usage
if __name__ == "__main__":
    policy = PasswordPolicy(min_length=10)
    generator = PasswordGenerator(policy)

    password = generator.generate()
    print(password)

    analyzers = [
        BasicPasswordAnalyzer(password),
        AdvancedPasswordAnalyzer(password),
    ]

    for analyzer in analyzers:
        report = run_analysis(analyzer)
        print()
        print(report)
