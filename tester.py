import io
import os
import re
import sys
import time
import difflib
from unittest.mock import patch


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

    def print_report():
        raise NotImplementedError("print_report must be derived")


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
        print()
        print("=" * 40)
        print(f"{'module:':<{COLSIZE}}{self.module_name}")
        print(f"{'suite:':<{COLSIZE}}{self.suite_name}")
        print(f"{'score:':<{COLSIZE}}{passed}/{total}\n")


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
        return self.total_time() / len(self.__records)

    def print_report(self):
        COLSIZE = 14
        print()
        print("=" * 40)
        print(f"{'module:':<{COLSIZE}}{self.module_name}")
        print(f"{'suite:':<{COLSIZE}}{self.suite_name}")
        print(f"{'average time:':<{COLSIZE}}{1000 * self.average_time()} ms")
        print(f"{'total time:':<{COLSIZE}}{1000 * self.total_time()} ms\n")


class TesterBase:
    CODE = "code"
    USER_INPUT = "stdin"
    PROG_OUTPUT = "stdout"
    ERROR_OUTPUT = "error"
    TAB = "  "

    def __init__(self, test_path: str, callback, **kwargs):
        self.__callback = callback
        self.__kwargs = kwargs
        self.__ttree: dict[str, dict[str, dict[str, dict[str, list[str]]]]] = dict()
        self.__test_path = test_path
        self.__key_map = []

        state = None
        whitelist = re.compile(r"^$|\*[\w ]+\*|^>")

        with open(test_path) as file:
            for line in file:
                line = line.rstrip()

                if self.update_sections(state, line):
                    continue

                if whitelist.match(line):
                    continue  # ignore line

                state = self.advance_fsm(state, line)

    def callback(self, prog_arg: str):
        if len(self.__kwargs):
            return self.__callback(prog_arg, **self.__kwargs)
        else:
            return self.__callback(prog_arg)

    def blank_section(self):
        return {"code": [], "stdin": [], "stdout": [], "error": []}

    def validate_uniqueness(self, item: dict, key: str):
        if key in item:
            nice_path = os.path.relpath(self.__test_path)
            raise SystemExit(f"`{key}' is a duplicate entry in {nice_path}")

    def add_level(self, active_item: dict, key: str, payload):
        self.validate_uniqueness(active_item, key)
        active_item[key] = payload
        self.__key_map.append(active_item[key])

    def add_item(self, active_item: dict, key: str, payload):
        self.validate_uniqueness(active_item, key)
        active_item[key] = payload

    def run_section(self, unit: dict[str, list[str]]):
        raise NotImplementedError("print_report must be derived")

    def run_tests(self, section_filter: set[str] = set(), unit_filter: set[str] = set()):
        print_buffer: list[str] = []

        for name, title in self.__ttree.items():
            print_buffer.append(name)
            for name, section in title.items():
                has_children = False
                print_buffer.append(name)
                if len(section_filter) > 0 and name not in section_filter:
                    print_buffer.pop()
                    continue
                for name, unit in section.items():
                    print_buffer.append(name)
                    if len(unit_filter) > 0 and name not in unit_filter:
                        print_buffer.pop()
                        continue
                    has_children = True
                    print("\n".join(print_buffer))
                    self.run_section(unit)
                    print_buffer.clear()
                if not has_children:
                    print_buffer.pop()

    def update_sections(self, state, line):
        if line == "```":
            return False

        match state:
            case "code" | "stdin" | "stdout" | "error":
                self.__key_map[-1][state].append(line)
                return True

            case _:
                return False

    def advance_fsm(self, state, line):
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
            "stdout-end": [(r"^```", "error")],
            "error": [(r"^```", "error-end")],
            "error-end": [(r"^### ", "unit"), (r"^## ", "section")],
        }

        entry_state = state
        for target, next in FSM[state]:
            if re.match(target, line):
                state = next

        if entry_state == state:
            raise SyntaxError(
                f"Incorrectly formatted test cases. It failed at:" + f"`{line}'"
            )

        match state, entry_state:
            case "title", None:
                self.__ttree[line] = dict()
                self.__key_map.append(self.__ttree[line])

            case ("section", "title") | ("unit", "section"):
                self.add_level(self.__key_map[-1], line, dict())

            case "section", "error-end":
                self.__key_map.pop()
                self.__key_map.pop()
                self.add_level(self.__key_map[-1], line, dict())

            case "unit", "error-end":
                self.__key_map.pop()
                self.add_level(self.__key_map[-1], line, dict())

            case ("code", _) | ("stdin", _) | ("stdout", _) | ("error", _):
                self.add_item(self.__key_map[-1], state, [])

            case (
                ("code-end", _)
                | ("stdin-end", _)
                | ("stdout-end", _)
                | ("error-end", _)
            ):
                pass

            case _:
                raise SyntaxError(
                    f"Fatal error at:" + f"`{line}'.\nInvalid state transition."
                )
                # self.run_section()

        return state


class Tester(TesterBase):
    def __init__(self, proj_path, test_path: str, callback, **kwargs):
        self.result = TestResults(proj_path, test_path)
        super().__init__(test_path, callback, **kwargs)

    def run_section(self, unit: dict[str, list[str]]):
        program_source = "\n".join(unit[TesterBase.CODE])
        user_input = unit[TesterBase.USER_INPUT]
        error_definition = None

        with patch("builtins.input", side_effect=user_input):
            stdout_buff = io.StringIO()
            stderr_buff = io.StringIO()
            sys.stdout = stdout_buff
            sys.stderr = stderr_buff
            try:
                self.callback(program_source)

            except Exception as e:
                err_split = e.args[0].split(":", 1)
                if len(err_split) == 2:
                    error_name, error_definition = err_split
                else:
                    error_name, error_definition = (e.args[0], "")
                print(error_name, file=sys.stderr)
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        print()
        out_passed = self.match_buffer(
            stdout_buff.getvalue(), unit[TesterBase.PROG_OUTPUT], "stdout"
        )
        err_passed = self.match_buffer(
            stderr_buff.getvalue(), unit[TesterBase.ERROR_OUTPUT], "stderr"
        )
        self.result.add_entry(out_passed and err_passed)
        if error_definition and not err_passed:
            print(f"    {TesterBase.TAB}{error_definition}")
        print()

    def match_buffer(self, recieved: str, unit_block: list[str], msg: str):
        if recieved.endswith("\n"):
            recieved = recieved[:-1]

        expected = "\n".join(unit_block)
        if recieved == expected:
            print(f"- {msg}: pass ✔")
            return True
        else:
            print(f"- {msg}: FAIL ❌")
            diff = list(difflib.ndiff(recieved.splitlines(), expected.splitlines()))
            rec_str = {
                i: f"{TesterBase.TAB}[R]: {l[2:]}"
                for i, l in enumerate(diff)
                if l.startswith("-")
            }
            exp_str = {
                i: f"{TesterBase.TAB}[e]: {l[2:]}"
                for i, l in enumerate(diff)
                if l.startswith("+")
            }
            print("\n".join([i for _, i in sorted((rec_str | exp_str).items())]))
            return False


class BatchRun(TesterBase):
    def __init__(self, proj_path, test_path: str, callback, **kwargs):
        self.result = ProfilerStats(proj_path, test_path)
        super().__init__(test_path, callback, **kwargs)

    def run_section(self, unit: dict[str, list[str]]):
        program_source = "\n".join(unit[TesterBase.CODE])
        user_input = unit[TesterBase.USER_INPUT]

        with patch("builtins.input", side_effect=user_input):
            print("```")
            try:
                self.result.start()
                self.callback(program_source)

            except Exception as e:
                error_message = e.args[0]
                print(error_message, file=sys.stderr)
            finally:
                self.result.record()
            print("```\n")
