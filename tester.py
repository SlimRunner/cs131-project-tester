import io
import os
import re
import sys
import difflib
from unittest.mock import patch


class Tester:
    CODE = "code"
    USER_INPUT = "stdin"
    PROG_OUTPUT = "stdout"
    ERROR_OUTPUT = "error"

    def __init__(self, filepath: str, callback, *args):
        self.collecting = True
        self.callback = callback
        self.arguments = args
        self.sections = self.blank_section()
        self.stats = []

        state = None
        whitelist = re.compile(r"^$|\*[\w ]+\*")

        with open(filepath) as file:
            for line in file:
                line = line.rstrip()

                if self.update_sections(state, line):
                    continue

                if whitelist.match(line):
                    continue  # ignore line

                state = self.advance_fsm(state, line)

        # print(self.sections)
        pass

    def blank_section(self):
        return {"code": [], "stdin": [], "stdout": [], "error": []}

    def run_section(self):
        program_source = "\n".join(self.sections[Tester.CODE])
        user_input = self.sections[Tester.USER_INPUT]

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
            sys.stdout = sys.__stdout__  # Restore original stdout

        print()
        self.match_buffer(stdout_buff.getvalue(), Tester.PROG_OUTPUT, "output")
        self.match_buffer(stderr_buff.getvalue(), Tester.ERROR_OUTPUT, "error")
        print()

    def match_buffer(self, recieved: str, tag: str, msg: str):
        if recieved.endswith("\n"):
            recieved = recieved[:-1]

        expected = "\n".join(self.sections[tag])
        if recieved == expected:
            print(f"{msg}: pass ✔")
        else:
            TAB = "  "
            print(f"{msg}: FAIL ❌")
            diff = difflib.ndiff(recieved.splitlines(), expected.splitlines())
            print('\n'.join([TAB + l for l in diff if l.startswith("-") or l.startswith("+")]))

    def update_sections(self, state, line):
        if line == "```":
            return False

        match state:
            case "code" | "stdin" | "stdout" | "error":
                self.collecting = True
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
