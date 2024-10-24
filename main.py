import sys
import importlib.util
from tester import Tester, BatchRun
from arghelper import getArguments, TestingOptions


def main(Interpreter, args):
    match args.test_type:
        case TestingOptions.UNIT_TEST:
            interpreter = Interpreter()
            test_results = Tester("./testCases.md", interpreter.run)
            test_results.result.print_report()
        case TestingOptions.RUN_TEST:
            interpreter = Interpreter()
            test_results = BatchRun("./testCases.md", interpreter.run)
            test_results.result.print_report()
        case _:
            pass


def load_module(name, pckg):
    spec = importlib.util.find_spec(name)
    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module.Interpreter
    else:
        return None


if __name__ == "__main__":
    args = getArguments()
    for i in range(4, 0, -1):
        Interpreter = load_module(f"interpreterv{i}", "Interpreter")
        if Interpreter is not None:
            break

    if Interpreter is None:
        raise SystemExit("No projects were found.")

    main(Interpreter, args)
