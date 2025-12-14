# Project 3 – Advanced Password Security System

This project extends the Project 2 password system by applying advanced object-oriented programming principles, including **inheritance**, **polymorphism**, **abstract base classes**, and **composition**.  
The system analyzes password strength, enforces configurable password policies, and demonstrates scalable architecture through clean class design.

---

## Project Overview

The goal of this project is to transform an existing password evaluation system into a structured object-oriented system that supports:

- Code reuse through inheritance  
- Flexible behavior through polymorphism  
- Interface enforcement with abstract base classes  
- Clear "has-a" relationships using composition  

This design allows new password analyzers, policies, or reporting formats to be added with minimal changes to existing code.

---

## Repository Structure

Project_3_Abdullah_Khan/
├── password_system/
│ ├── password_system.py
│ └── demo.py
├── tests/
│ └── test_password_system.py
├── docs/
│ └── ARCHITECTURE.md
└── README.md


- **password_system.py** – Core system classes and logic  
- **demo.py** – Demonstrates inheritance and polymorphic behavior  
- **tests/** – Automated tests (pytest)  
- **docs/** – Architecture and design explanation  

---

## Class Hierarchy

AbstractPasswordAnalyzer (ABC)
└── BasicPasswordAnalyzer
└── AdvancedPasswordAnalyzer

- `AbstractPasswordAnalyzer` defines the required analysis interface  
- `BasicPasswordAnalyzer` implements standard strength and entropy checks  
- `AdvancedPasswordAnalyzer` extends analysis with repeated pattern detection  

---

## Key OOP Concepts Used

### Inheritance
The analyzer hierarchy uses inheritance to share behavior while allowing specialization.  
`AdvancedPasswordAnalyzer` inherits from `BasicPasswordAnalyzer` and overrides behavior using `super()`.

---

### Polymorphism
Polymorphism is demonstrated through a shared method interface:

```python
def run_analysis(analyzer: AbstractPasswordAnalyzer):
    return analyzer.analyze()



