from tester import Tester, BatchRun
from arghelper import getArguments, TestingOptions, ArgsWrapper
from testersetup import find_interpreters, choose_project, choose_latest_project


def main(Interpreter: type, proj_path: str, test_path: str, args: ArgsWrapper):
    interpreter = Interpreter()

    match args.test_type:
        case TestingOptions.UNIT_TEST:
            tester = Tester(proj_path, test_path, interpreter.run)
        case TestingOptions.RUN_TEST:
            tester = BatchRun(proj_path, test_path, interpreter.run)
        case _:
            pass

    tester.run_tests(**args.filters)
    tester.result.print_report()


if __name__ == "__main__":
    args = getArguments()
    interpreters = find_interpreters()
    TARGET_MODULE = "Interpreter"

    if args.project:
        Interpreter, proj_path, test_path = choose_project(
            args.project, interpreters, TARGET_MODULE
        )
    else:
        Interpreter, proj_path, test_path = choose_latest_project(
            interpreters, TARGET_MODULE
        )

    if Interpreter is None:
        raise SystemExit("Unexpected exit: Interpreter is None.")

    main(Interpreter, proj_path, test_path, args)
