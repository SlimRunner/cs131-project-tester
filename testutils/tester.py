import io
import os
import re
import sys
import time
import difflib
from unittest.mock import patch


# I did not inherit from SyntaxError because for some reason
# super().__init__() does not support end_lineno or end_offset. So
# stupid that this is not mentioned in the documentation.
def ParseError(msg, file, lnum, lerr, mark):
    ms, ml = mark
    return SyntaxError(msg, (file, lnum, ms, lerr, lnum, ms + ml))


class PrintableReport:
    def __init__(self, proj_path: str, test_path: str) -> None:
        self.__test_path = test_path
        self.__proj_path = proj_path

    @property
    def suite_name(self) -> str:
        return f"./{os.path.relpath(self.__test_path)}"

    @property
    def module_name(self) -> str:
        return f"./{os.path.relpath(self.__proj_path)}"

    def print_report(self, report_lines: list[str]):
        print()
        print("-" * 40)
        print("\n".join(f"* {l}" for l in report_lines))


class TestResults(PrintableReport):
    def __init__(self, proj_path: str, test_path: str) -> None:
        super().__init__(proj_path, test_path)
        self.__entries = []

    def add_entry(self, passed: bool) -> None:
        self.__entries.append(passed)

    def count_success(self):
        return len([i for i in self.__entries if i])

    def give_score(self) -> tuple[int, int]:
        return (self.count_success(), len(self.__entries))

    def print_report(self):
        passed, total = self.give_score()
        COLSIZE = 8
        out_report = []
        out_report.append(f"{'module:':<{COLSIZE}}{self.module_name}")
        out_report.append(f"{'suite:':<{COLSIZE}}{self.suite_name}")
        out_report.append(f"{'score:':<{COLSIZE}}{passed}/{total}\n")
        super().print_report(out_report)


class ProfilerStats(PrintableReport):
    def __init__(self, proj_path: str, test_path: str) -> None:
        super().__init__(proj_path, test_path)
        self.__start = None
        self.__records: list[float] = []

    def start(self):
        self.__start = time.time()

    def record(self):
        if self.__start is None:
            raise RuntimeError("Cannot call end before start")
        self.__records.append(time.time() - self.__start)
        self.__start = None

    def total_time(self):
        return sum(self.__records)

    def average_time(self):
        if len(self.__records):
            return self.total_time() / len(self.__records)
        else:
            return float("NaN")

    def print_report(self):
        COLSIZE = 14
        out_report = []
        out_report.append(f"{'module:':<{COLSIZE}}{self.module_name}")
        out_report.append(f"{'suite:':<{COLSIZE}}{self.suite_name}")
        out_report.append(
            f"{'average time:':<{COLSIZE}}{1000 * self.average_time()} ms"
        )
        out_report.append(f"{'total time:':<{COLSIZE}}{1000 * self.total_time()} ms\n")
        super().print_report(out_report)


class TesterBase:
    CODE = "code"
    USER_INPUT = "stdin"
    PROG_OUTPUT = "stdout"
    ERROR_OUTPUT = "stderr"
    LINE_NUMBER = "linenum"
    TAB = "  "

    def __init__(self, test_path: str, callback, cb_kwargs: dict[str]):
        self.__callback = callback
        self.__kwargs = cb_kwargs
        self.__ttree: dict[str, dict[str, dict[str, dict[str, list[str]]]]] = dict()
        self.__test_path = test_path
        self.__key_map = []
        self.__curr_line = None

        state = None
        whitelist = re.compile(r"^$|\*[\w ]+\*|^>")

        with open(test_path) as file:
            for num, line in enumerate(file):
                self.__curr_line = num + 1
                lnw = line.rstrip("\n")
                lsp = line.rstrip()

                if self.update_sections(state, lnw):
                    continue

                if whitelist.match(lsp):
                    continue  # ignore line

                state = self.advance_fsm(state, lnw)

        self.__curr_line = None

    @property
    def test_path(self):
        return self.__test_path

    def set_kwarg(self, key, value):
        self.__kwargs[key] = value

    def get_kwarg(self, key):
        exists = key in self.__kwargs
        val = self.__kwargs[key] if exists else None
        return val, exists

    def callback(self, prog_arg: str):
        if len(self.__kwargs):
            return self.__callback(prog_arg, **self.__kwargs)
        else:
            return self.__callback(prog_arg)

    def validate_uniqueness(self, item: dict, key: str):
        if key in item:
            lnum = self.__curr_line
            full_path = os.path.abspath(self.test_path)
            raise ParseError(
                "duplicate entry in test suite", full_path, lnum, key, (5, len(key))
            )

    def add_level(self, active_item: dict, key: str, payload):
        self.validate_uniqueness(active_item, key)
        active_item[key] = payload
        self.__key_map.append(active_item[key])

    def add_item(self, active_item: dict, key: str, payload):
        self.validate_uniqueness(active_item, key)
        active_item[key] = payload

    def run_section(self, unit: dict[str, list[str]]) -> tuple[bool, list[str]]:
        raise NotImplementedError("run_section must be derived")

    def is_filtered(self, key: str, filter: set[str]):
        if len(filter) == 0:
            return False
        remove_hash = re.compile(r"^#+ ")
        key = remove_hash.sub("", key).lower()
        return key not in filter

    def run_tests(
        self,
        section_filter: set[str],
        unit_filter: set[str],
        verbose: bool,
        raise_errors: bool,
    ):
        print_buffer: list[str] = []
        section_filter = {i.lower() for i in section_filter}
        unit_filter = {i.lower() for i in unit_filter}

        for name, title in self.__ttree.items():
            print_buffer.append(name)
            for name, section in title.items():
                has_children = False
                print_buffer.append(name)

                if self.is_filtered(name, section_filter):
                    print_buffer.pop()
                    continue

                for name, unit in section.items():
                    if self.is_filtered(name, unit_filter):
                        continue

                    passed, msg = self.run_section(unit, raise_errors)

                    if passed and not verbose:
                        continue

                    print_buffer.append(name)
                    has_children = True
                    print_buffer.extend(msg)

                if not has_children:
                    print_buffer.pop()

        if print_buffer[-1] == "":
            print_buffer.pop()

        print("\n".join(print_buffer))

    def update_sections(self, state, line):
        if line == "```":
            return False

        match state:
            case "code" | "stdin" | "stdout" | "stderr":
                self.__key_map[-1][state].append(line)
                return True

            case _:
                return False

    def advance_fsm(self, state, line):
        lnum = self.__curr_line
        FSM = {
            None: [(r"^# ", "title")],
            "title": [(r"^## ", "section")],
            "section": [(r"^### ", "unit")],
            "unit": [(r"^```", "code")],
            "code": [(r"^```", "code-end")],
            "code-end": [(r"^```", "stdin")],
            "stdin": [(r"^```", "stdin-end")],
            "stdin-end": [(r"^```", "stdout")],
            "stdout": [(r"^```", "stdout-end")],
            "stdout-end": [(r"^```", "stderr")],
            "stderr": [(r"^```", "stderr-end")],
            "stderr-end": [(r"^### ", "unit"), (r"^## ", "section")],
        }

        entry_state = state
        for target, next in FSM[state]:
            if re.match(target, line):
                state = next

        if entry_state == state:
            full_path = os.path.abspath(self.test_path)
            msg = "stale state transition found"
            if state not in {None, "title", "section", "unit"}:
                msg += ". Incorrect number of code blocks or a typo."
                marks = (1, len(line))
            elif line and line.startswith("#"):
                msg += ". Possibly an incorrectly nested heading"
                marks = (1, line.count("#"))
            else:
                msg += ". This may be a typo"
                marks = (1, len(line))

            raise ParseError(msg, full_path, lnum, line, marks)

        match state, entry_state:
            case "title", None:
                self.__ttree[line] = dict()
                self.__key_map.append(self.__ttree[line])

            case ("section", "title"):
                self.add_level(self.__key_map[-1], line, dict())

            case "section", "stderr-end":
                self.__key_map.pop()
                self.__key_map.pop()
                self.add_level(self.__key_map[-1], line, dict())

            case ("unit", "section"):
                self.add_level(self.__key_map[-1], line, dict({"linenum": lnum}))

            case "unit", "stderr-end":
                self.__key_map.pop()
                self.add_level(self.__key_map[-1], line, dict({"linenum": lnum}))

            case ("code", _) | ("stdin", _) | ("stdout", _) | ("stderr", _):
                self.add_item(self.__key_map[-1], state, [])

            case (
                ("code-end", _)
                | ("stdin-end", _)
                | ("stdout-end", _)
                | ("stderr-end", _)
            ):
                pass

            case _:
                full_path = os.path.abspath(self.test_path)
                raise ParseError(
                    "unexpected error due to invalid state transition",
                    full_path,
                    lnum,
                    line,
                    (0, 0),
                )

        return state


class Tester(TesterBase):
    def __init__(self, proj_path, test_path: str, callback, cb_kwargs: dict[str]):
        super().__init__(test_path, callback, cb_kwargs)
        self.result = TestResults(proj_path, test_path)

    def run_section(self, unit: dict[str, list[str]], raise_errors: bool):
        program_source = "\n".join(unit[TesterBase.CODE])
        user_input = unit[TesterBase.USER_INPUT]
        line_num = unit[TesterBase.LINE_NUMBER]
        error_definition = None

        _, flag_exists = self.get_kwarg("debug_print")
        if flag_exists:
            debug_buff = io.StringIO()
            self.set_kwarg("debug_print", debug_buff.write)

        with patch("builtins.input", side_effect=user_input):
            stdout_buff = io.StringIO()
            stderr_buff = io.StringIO()
            sys.stdout = stdout_buff
            sys.stderr = stderr_buff

            try:
                self.callback(program_source)

            except Exception as e:
                err_1st = e.args[0] if e.args else str(e)
                err_split = err_1st.split(":", 1)
                if len(err_split) == 2:
                    error_name, error_definition = err_split
                else:
                    error_name, error_definition = (err_1st, "")
                print(error_name, file=sys.stderr)
                if raise_errors:
                    raise e
            finally:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

        prog_out = [f"> ./{os.path.relpath(self.test_path)} line {line_num}"]
        prog_out.append("")
        out_passed, out_msg = self.match_buffer(
            stdout_buff.getvalue(), unit[TesterBase.PROG_OUTPUT], "stdout"
        )
        err_passed, err_msg = self.match_buffer(
            stderr_buff.getvalue(), unit[TesterBase.ERROR_OUTPUT], "stderr"
        )

        unit_passed = out_passed and err_passed
        self.result.add_entry(unit_passed)
        prog_out.extend(out_msg)
        prog_out.extend(err_msg)

        if error_definition and not err_passed:
            prog_out.append(f"{TesterBase.TAB}- {error_definition}")
        prog_out.append("")

        return (unit_passed, prog_out)

    def generate_md_table(self, out_a: list[str], out_b: list[str]):
        s = difflib.SequenceMatcher(None, out_a, out_b)
        num_pad_a = len(str(len(out_a)))
        num_pad_b = len(str(len(out_b)))
        diff_table: list[tuple[str, str, str, str]] = [
            (f"{'#':>{num_pad_a}}", "received", "expected", f"{'#':>{num_pad_b}}")
        ]
        dot_a = f"{'.': >{num_pad_a}}"
        dot_b = f"{'.': >{num_pad_b}}"

        # Adapted from https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.get_opcodes
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            match tag:
                case "insert":
                    diff_table.extend(
                        [
                            (dot_a, "", out_b[e], f"{e+1:0{num_pad_b}}")
                            for e in range(j1, j2)
                        ]
                    )
                case "delete":
                    diff_table.extend(
                        [
                            (f"{e+1:0{num_pad_a}}", out_a[e], "", dot_b)
                            for e in range(i1, i2)
                        ]
                    )
                case "replace":
                    diff_table.extend(
                        [
                            (
                                f"{e1+1:0{num_pad_a}}",
                                out_a[e1],
                                out_b[e2],
                                f"{e2+1:0{num_pad_b}}",
                            )
                            for e1, e2 in zip(range(i1, i2), range(j1, j2))
                        ]
                    )
                case "equal":
                    pass

        col_span = [0, 0, 0, 0]
        for row in diff_table:
            for i, c in enumerate(row):
                col_span[i] = max(len(c), col_span[i])

        l1, l2, l3, l4 = col_span
        diff_table.insert(1, ("-" * l1, "-" * l2, "-" * l3, "-" * l4))

        str_out = [""]

        for r1, r2, r3, r4 in diff_table:
            str_out.append(
                f"{TesterBase.TAB}| {r1:<{l1}} | {r2:<{l2}} | {r3:<{l3}} | {r4:<{l4}} |"
            )
        str_out.append("")

        return str_out

    def match_buffer(self, received: str, unit_block: list[str], msg: str):
        if received.endswith("\n"):
            received = received[:-1]

        expected = "\n".join(unit_block)
        if received == expected:
            return (True, [f"- {msg}: pass ✔️"])
        else:
            out_msg = [f"- {msg}: FAIL ❌"]
            received = [f"`{l}`" for l in received.splitlines()]
            expected = [f"`{l}`" for l in expected.splitlines()]
            diff_table = self.generate_md_table(received, expected)
            return (False, out_msg + diff_table)


class BatchRun(TesterBase):
    def __init__(self, proj_path, test_path: str, callback, cb_kwargs: dict[str]):
        super().__init__(test_path, callback, cb_kwargs)
        self.result = ProfilerStats(proj_path, test_path)

    def trim_output(self, received: str):
        if received.endswith("\n"):
            received = received[:-1]
        return received

    def run_section(self, unit: dict[str, list[str]], raise_errors: bool):
        program_source = "\n".join(unit[TesterBase.CODE])
        user_input = unit[TesterBase.USER_INPUT]
        line_num = unit[TesterBase.LINE_NUMBER]
        prog_out: list[str] = [f"> ./{os.path.relpath(self.test_path)} line {line_num}"]

        with patch("builtins.input", side_effect=user_input):
            stdout_buff = io.StringIO()
            debug_buff = None
            sys.stdout = stdout_buff

            _, flag_exists = self.get_kwarg("debug_print")
            if flag_exists:
                debug_buff = io.StringIO()
                self.set_kwarg("debug_print", debug_buff.write)

            print("```")
            try:
                self.result.start()
                self.callback(program_source)

            except Exception as e:
                error_message = e.args[0] if e.args else str(e)
                print(error_message)
                if raise_errors:
                    raise e
            finally:
                self.result.record()
            print("```")
            sys.stdout = sys.__stdout__

        if debug_buff is not None:
            prog_out.append(self.trim_output(debug_buff.getvalue()))
        prog_out.append(self.trim_output(stdout_buff.getvalue()))
        prog_out.append("")

        return (False, prog_out)
