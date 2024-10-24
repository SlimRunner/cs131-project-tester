import io
import os
import re
import sys
import time
import difflib
from unittest.mock import patch


class PrintableReport:
    def print_report():
        raise NotImplementedError("print_report must be derived")


class TestResults(PrintableReport):
    def __init__(self) -> None:
        super().__init__()
        self._entries = []

    def add_entry(self, passed: bool) -> None:
        self._entries.append(passed)

    def count_success(self):
        return len([i for i in self._entries if i])

    def give_score(self) -> tuple[int, int]:
        return (self.count_success(), len(self._entries))

    def print_report(self):
        passed, total = self.give_score()
        print()
        print("="*40)
        print(f"score: {passed}/{total}")


class ProfilerStats(PrintableReport):
    def __init__(self) -> None:
        super().__init__()
        self._start = None
        self._records: list[float] = []

    def start(self):
        self._start = time.time()

    def record(self):
        if self._start is None:
            raise RuntimeError("Cannot call end before start")
        self._records.append(time.time() - self._start)
        self._start = None

    def total_time(self):
        return sum(self._records)

    def average_time(self):
        return self.total_time() / len(self._records)

    def print_report(self):
        print()
        print("="*40)
        print("average time:", 1000 * self.average_time(), "ms")
        print("total time:", 1000 * self.total_time(), "ms")


class TesterBase:
    CODE = "code"
    USER_INPUT = "stdin"
    PROG_OUTPUT = "stdout"
    ERROR_OUTPUT = "error"

    def __init__(self, filepath: str, callback, *args):
        self.callback = callback
        self.arguments = args
        self.sections = self.blank_section()

        state = None
        whitelist = re.compile(r"^$|\*[\w ]+\*|^>")

        with open(filepath) as file:
            for line in file:
                line = line.rstrip()

                if self.update_sections(state, line):
                    continue

                if whitelist.match(line):
                    continue  # ignore line

                state = self.advance_fsm(state, line)

    def blank_section(self):
        return {"code": [], "stdin": [], "stdout": [], "error": []}

    def run_section(self):
        pass

    def update_sections(self, state, line):
        if line == "```":
            return False

        match state:
            case "code" | "stdin" | "stdout" | "error":
                if state not in self.sections:
                    self.sections[state] = [line]
                else:
                    self.sections[state].append(line)
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

        match state:
            case "title" | "section" | "unit":
                print(line)
                self.sections = self.blank_section()
            case "error-end":
                self.run_section()

        return state


class Tester(TesterBase):
    def __init__(self, filepath: str, callback, *args):
        self.result = TestResults()
        super().__init__(filepath, callback, *args)

    def run_section(self):
        program_source = "\n".join(self.sections[TesterBase.CODE])
        user_input = self.sections[TesterBase.USER_INPUT]

        with patch("builtins.input", side_effect=user_input):
            stdout_buff = io.StringIO()
            stderr_buff = io.StringIO()
            sys.stdout = stdout_buff
            sys.stderr = stderr_buff
            try:
                self.callback(program_source)

            except Exception as e:
                error_message = e.args[0].split(":", 1)[0]
                print(error_message, file=sys.stderr)
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        print()
        self.match_buffer(stdout_buff.getvalue(), TesterBase.PROG_OUTPUT, "stdout")
        self.match_buffer(stderr_buff.getvalue(), TesterBase.ERROR_OUTPUT, "stderr")
        print()

    def match_buffer(self, recieved: str, tag: str, msg: str):
        if recieved.endswith("\n"):
            recieved = recieved[:-1]

        expected = "\n".join(self.sections[tag])
        if recieved == expected:
            self.result.add_entry(True)
            print(f"{msg}: pass ✔")
        else:
            self.result.add_entry(False)
            TAB = "  "
            print(f"{msg}: FAIL ❌")
            diff = difflib.ndiff(recieved.splitlines(), expected.splitlines())
            print(
                "\n".join(
                    [
                        TAB + f"{i}: {l}"
                        for i, l in enumerate(diff)
                        if l.startswith("-") or l.startswith("+")
                    ]
                )
            )


class BatchRun(TesterBase):
    def __init__(self, filepath: str, callback, *args):
        self.result = ProfilerStats()
        super().__init__(filepath, callback, *args)

    def run_section(self):
        program_source = "\n".join(self.sections[TesterBase.CODE])
        user_input = self.sections[TesterBase.USER_INPUT]

        with patch("builtins.input", side_effect=user_input):
            print("```")
            try:
                self.result.start()
                self.callback(program_source)

            except Exception as e:
                error_message = e.args[0].split(":", 1)[0]
                print(error_message, file=sys.stderr)
            finally:
                self.result.record()
            print("```")
