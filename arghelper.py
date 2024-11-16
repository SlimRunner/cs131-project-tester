import textwrap
from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    Action as ArgAction,
)
from typing import Any, Sequence


# https://stackoverflow.com/a/29485128
class BlankLinesHelpFormatter(RawTextHelpFormatter):
    def _split_lines(self, text, width):
        return super()._split_lines(text, width) + [""]


class ArgumentPairsAction(ArgAction):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        if len(values) % 3 != 0:
            parser.error("Program arguments must come in name-type-value triples.")
        # a makeshift reducer to avoid importing reduce
        key = None
        vtype = None
        vtype_key = None

        Bool = lambda x: {"True": True, "False": False}[x]

        type_list = {
            "bool": Bool,
            "int": int,
            "float": float,
            "str": str,
        }

        out_map: dict[str] = dict()
        for item in values:
            if key is None:
                if not str.isidentifier(item):
                    parser.error(
                        f"Invalid key '{item}': arg names must be valid Python identifiers."
                    )
                key = item
            elif vtype is None:
                try:
                    vtype_key = item.lower()
                    vtype = type_list[vtype_key]
                except Exception as err:
                    parser.error(str(err) + "\nNot a valid type.")
            else:
                try:
                    out_map[key] = vtype(item)
                    key = None
                    vtype = None
                except Exception as err:
                    parser.error(str(err) + f"\nNot a valid `{vtype_key}' value.")

        setattr(namespace, self.dest, out_map)


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
        self.__arguments = args.args
        self.__unit = args.unit
        self.__verbose = args.verbose
        self.__raise_errors = args.raise_errors

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
    def raise_errors(self) -> str | None:
        return self.__raise_errors

    @property
    def arguments(self) -> str | None:
        return self.__arguments

    @property
    def filters(self) -> dict[str, set[str]]:
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
    arg_parser.add_argument(
        "-E",
        "--raise-errors",
        action="store_true",
        help="Do not waive exeptions, crash instead.",
    )
    arg_parser.add_argument(
        "--args",
        nargs="+",
        action=ArgumentPairsAction,
        help=textwrap.dedent(
            """\
            Pass extra arguments to your interpreter function. They must come in triples in
            the format name-type-value triples such as:
                --args <name1> <type1> <value1> [<name2> <type2> <value2> ...]
            Names must be valid Python identifiers, types can only be int,
            float, str, or bool, and values must parse correctly to their respective type.
            """
        ),
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
    p_args.args = p_args.args if p_args.args else dict()
    p_args.section = set(p_args.section) if p_args.section else set()
    p_args.unit = set(p_args.unit) if p_args.unit else set()

    return ArgsWrapper(p_args)
