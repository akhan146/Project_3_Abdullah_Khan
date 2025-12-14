
# Architecture Document – Advanced Password Security System

## Overview

This project extends the Project 2 password system into a fully object-oriented design that demonstrates **inheritance**, **polymorphism**, **abstract base classes**, and **composition**.  
The system is designed to be modular, scalable, and easy to extend without modifying existing components.

The domain remains focused on password security, analysis, and policy enforcement.

---

## Inheritance Hierarchy

### Analyzer Hierarchy
AbstractPasswordAnalyzer (ABC)
└── BasicPasswordAnalyzer
└── AdvancedPasswordAnalyzer


- **AbstractPasswordAnalyzer**
  - Defines the required interface for all password analyzers
  - Enforces implementation of the `analyze()` method
  - Cannot be instantiated directly

- **BasicPasswordAnalyzer**
  - Implements core password analysis features
  - Calculates entropy, strength, and common-password detection

- **AdvancedPasswordAnalyzer**
  - Extends `BasicPasswordAnalyzer`
  - Adds repeated pattern detection
  - Uses `super().analyze()` to reuse parent behavior

This hierarchy represents a true **“is-a” relationship**:
> An advanced password analyzer *is a* basic password analyzer, and both *are* password analyzers.

The hierarchy is intentionally shallow to maintain clarity and avoid unnecessary complexity.

---

## Polymorphism

Polymorphism is demonstrated through the shared `analyze()` method defined in the abstract base class.

```python
def run_analysis(analyzer: AbstractPasswordAnalyzer):
    return analyzer.analyze()

At runtime, different analyzer objects produce different results when the same method is called:

BasicPasswordAnalyzer.analyze() returns basic analysis results

AdvancedPasswordAnalyzer.analyze() returns extended results including pattern detection

This behavior occurs without conditional logic or type checking, demonstrating true dynamic dispatch.

Abstract Base Classes

The abstract base class ensures that all analyzer implementations conform to the same interface.
class AbstractPasswordAnalyzer(ABC):
    @abstractmethod
    def analyze(self) -> dict:
        pass
Benefits:

-Prevents incomplete analyzer implementations

-Guarantees consistent behavior across analyzer types

-Composition Relationships

-Composition is used throughout the system to model “has-a” relationships where inheritance would be inappropriate.

-Key Composition Examples

-PasswordAnalyzer has a Password

-An analyzer examines a password but is not a password

-PasswordPolicy has a Password

-A policy validates a password against defined rules

-PasswordGenerator has a PasswordPolicy

-A generator uses policy rules to create valid passwords

-A report formats analysis results for display

-Composition was chosen over inheritance because these objects collaborate rather than represent specialized forms of one another.

-Design Decisions

-Why Inheritance Was Used

-Analyzer types share common behavior

-Subclasses extend functionality without duplication

-Why Composition Was Used

-Prevents misuse of inheritance

-Improves modularity

-Allows components to change independently

-Additional password policies

-Alternative report formats

-Integration with external security services

-New features can be added by extending existing classes without modifying current implementations, following the Open/Closed Principle.

Conclusion

The system demonstrates a clean and intentional application of object-oriented design principles.
Inheritance, polymorphism, abstract base classes, and composition are each used where appropriate, resulting in a maintainable and scalable architecture that builds directly on the original Project 2 implementation.
