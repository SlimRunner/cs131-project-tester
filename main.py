from tester import Tester, BatchRun
from arghelper import getArguments, TestingOptions, ArgsWrapper
from testexporter import TestCaseExporter
from testersetup import (
    find_projects,
    choose_project,
    choose_latest_project,
    choose_suite,
    choose_latest_suite,
)


def main(Interpreter: type, proj_path: str, test_path: str, args: ArgsWrapper):
    interpreter = Interpreter()

    match args.test_type:
        case TestingOptions.UNIT_TEST:
            tester = Tester(proj_path, test_path, interpreter.run, args.arguments)
        case TestingOptions.RUN_TEST:
            tester = BatchRun(proj_path, test_path, interpreter.run, args.arguments)
        case _:
            raise SystemExit(f"Unexpected test type: {args.test_type}")

    tester.run_tests(
        **args.filters, verbose=args.verbose, raise_errors=args.raise_errors
    )
    tester.result.print_report()


def export(test_path: str, args: ArgsWrapper):
    cases = TestCaseExporter(test_path)
    cases.export_case_as_zip(args.export)


if __name__ == "__main__":
    args = getArguments()
    projects = find_projects()

    if args.export:
        if args.project:
            test_path = choose_suite(args.project, projects)
        else:
            test_path = choose_latest_suite(projects)
        export(test_path, args)
    else:
        TARGET_MODULE = "Interpreter"

        if args.project:
            Interpreter, proj_path, test_path = choose_project(
                args.project, projects, TARGET_MODULE
            )
        else:
            Interpreter, proj_path, test_path = choose_latest_project(
                projects, TARGET_MODULE
            )

        if Interpreter is None:
            raise SystemExit("Unexpected exit: Interpreter is None.")

        main(Interpreter, proj_path, test_path, args)
