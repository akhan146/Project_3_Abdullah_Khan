from password_system import (
    PasswordPolicy,
    PasswordGenerator,
    BasicPasswordAnalyzer,
    AdvancedPasswordAnalyzer,
    run_analysis,
)


def main():
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


if __name__ == "__main__":
    main()
