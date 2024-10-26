from tester import Tester, BatchRun
from arghelper import getArguments, TestingOptions, ArgsWrapper
from testersetup import find_interpreters, choose_project, choose_latest_project


def main(Interpreter: type, test_path: str, args: ArgsWrapper):
    match args.test_type:
        case TestingOptions.UNIT_TEST:
            interpreter = Interpreter()
            test_results = Tester(test_path, interpreter.run)
            test_results.result.print_report()
        case TestingOptions.RUN_TEST:
            interpreter = Interpreter()
            test_results = BatchRun(test_path, interpreter.run)
            test_results.result.print_report()
        case _:
            pass


if __name__ == "__main__":
    args = getArguments()
    interpreters = find_interpreters()
    TARGET_MODULE = "Interpreter"

    if args.project:
        Interpreter, test_path = choose_project(
            args.project, interpreters, TARGET_MODULE
        )
    else:
        Interpreter, test_path = choose_latest_project(interpreters, TARGET_MODULE)

    main(Interpreter, test_path, args)
