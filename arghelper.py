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


def strVersion(val: str):
    if not val.isnumeric():
        raise ValueError("Version should be numeric")
    return val


class ArgsWrapper:
    def __init__(self, args) -> None:
        self.__test_type = args.test_type
        self.__project = args.project
        self.__section = args.section
        self.__unit = args.unit
        self.__verbose = args.verbose

    @property
    def test_type(self) -> TestingOptions:
        return self.__test_type

    @property
    def project(self) -> str | None:
        return self.__project

    @property
    def verbose(self) -> str | None:
        return self.__verbose

    @property
    def filters(self) -> dict[str, dict]:
        return {"section_filter": self.__section, "unit_filter": self.__unit}


def getArguments(*args: str) -> ArgsWrapper:
    arg_parser = ArgumentParser(
        prog="main",
        description="Runs Brewin programs from a markdown file.",
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
    # Version is string because this allows to distinguish v1 from v01 and so on
    arg_parser.add_argument(
        "-p",
        "--project",
        nargs=1,
        type=strVersion,
        metavar="VERSION",
        help="Run a specific project VERSION. If ommited, newest is used.",
    )
    arg_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="If present testing mode will show the passed cases too.",
    )

    filter_group = arg_parser.add_mutually_exclusive_group()
    filter_group.add_argument(
        "-s", "--section", nargs="+", help="Filter by a specific set of sections."
    )
    filter_group.add_argument(
        "-u", "--unit", nargs="+", help="Filter by a specific set of units."
    )

    if len(args) > 0:
        p_args = arg_parser.parse_args(list(args))
    else:
        p_args = arg_parser.parse_args()

    p_args.test_type = TestingOptions(p_args.test_type[0])
    p_args.project = p_args.project[0] if p_args.project else p_args.project
    p_args.section = set(p_args.section) if p_args.section else set()
    p_args.unit = set(p_args.unit) if p_args.unit else set()

    return ArgsWrapper(p_args)
