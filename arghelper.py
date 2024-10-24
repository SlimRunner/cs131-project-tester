import textwrap
from argparse import ArgumentParser, RawTextHelpFormatter


# https://stackoverflow.com/a/29485128
class BlankLinesHelpFormatter(RawTextHelpFormatter):
    def _split_lines(self, text, width):
        return super()._split_lines(text, width) + [""]


class TestingOptions:
    UNIT_TEST = "testit"
    RUN_TEST = "timeit"
    OPTIONS = {UNIT_TEST, RUN_TEST}
    DEFAULT = UNIT_TEST

    def __init__(self, opt: str) -> None:
        if opt not in TestingOptions.OPTIONS:
            raise ValueError(f"'{opt}' is not a valid time type")
        self.__options = {o: o == opt for o in TestingOptions.OPTIONS}
        self.__selected = opt

    def __eq__(self, value: str) -> bool:
        return value == self.__selected

    def __repr__(self) -> str:
        return self.__selected

    def do_unit_test(self) -> bool:
        return self.__options[TestingOptions.UNIT_TEST]

    def do_run_test(self) -> bool:
        return self.__options[TestingOptions.RUN_TEST]


class ArgsWrapper:
    def __init__(self, args) -> None:
        self.__test_type = args.test_type

    @property
    def test_type(self) -> TestingOptions:
        return self.__test_type


def getArguments(*args: str) -> ArgsWrapper:
    arg_parser = ArgumentParser(
        prog="main",
        description="Runs Brewin programs from an markdown file.",
        formatter_class=BlankLinesHelpFormatter,
    )
    arg_parser.add_argument(
        "-t",
        "--test-type",
        nargs=1,
        default=[TestingOptions.DEFAULT],
        choices=TestingOptions.OPTIONS,
        help=textwrap.dedent(
            f"""\
            Allows different modes of running your test programs. The options are:
                - {TestingOptions.UNIT_TEST}: runs each program against the expected output and shows a diff.
                - {TestingOptions.RUN_TEST}: runs each program as-is and shows the output.
            """
        ),
    )

    if len(args) > 0:
        p_args = arg_parser.parse_args(list(args))
    else:
        p_args = arg_parser.parse_args()

    p_args.test_type = TestingOptions(p_args.test_type[0])

    return ArgsWrapper(p_args)
