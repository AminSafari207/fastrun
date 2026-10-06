import unittest

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


class GroupedTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_class = None

    def startTest(self, test):
        test_class = test.__class__

        if test_class is not self.current_class:
            if self.current_class is not None:
                self.stream.writeln()

            self.current_class = test_class

            self.stream.writeln(test_class.__name__)
            self.stream.writeln("-" * len(test_class.__name__))

        self.stream.write(f"  {test._testMethodName} ... ")

        super().startTest(test)

    def addSuccess(self, test):
        self.stream.writeln(f"{GREEN}ok{RESET}")

    def addError(self, test, err):
        self.stream.writeln(f"{RED}ERROR{RESET}")

        super().addError(test, err)

    def addFailure(self, test, err):
        self.stream.writeln(f"{RED}FAIL{RESET}")

        super().addFailure(test, err)

    def printErrors(self):
        self.stream.writeln()
        self.stream.writeln()

        super().printErrors()


class GroupedTestRunner(unittest.TextTestRunner):
    resultclass = GroupedTestResult


if __name__ == "__main__":
    print()

    suite = unittest.defaultTestLoader.discover(
        "tests",
    )

    runner = GroupedTestRunner(
        verbosity=0,
    )

    result = runner.run(suite)

    raise SystemExit(not result.wasSuccessful())
