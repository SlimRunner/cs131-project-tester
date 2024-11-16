import io
import os
import re
import zipfile


def askUser(msg: str):
    MSG = f"{msg} [Y]es/[N]o: "
    userInput = input(MSG)
    while len(userInput) != 1 or userInput not in "YyNn":
        userInput = input(MSG)
    return len(userInput) > 0 and userInput in "Yy"


class TestCaseParser:
    CODE = "code"
    USER_INPUT = "stdin"
    PROG_OUTPUT = "stdout"
    ERROR_OUTPUT = "error"
    TAB = "  "

    def __init__(self, test_path: str):
        self.__ttree: dict[str, dict[str, dict[str, dict[str, list[str]]]]] = dict()
        self.__test_path = test_path
        self.__key_map = []

        state = None
        whitelist = re.compile(r"^$|\*[\w ]+\*|^>")

        with open(test_path) as file:
            for line in file:
                lnw = line.rstrip("\n")
                lsp = line.rstrip()

                if self.update_sections(state, lnw):
                    continue

                if whitelist.match(lsp):
                    continue  # ignore line

                state = self.advance_fsm(state, lnw)

    def get_cases_tree(self):        
        return self.__ttree.items()

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

        return state



class TestCaseExporter(TestCaseParser):
    def __init__(self, test_path: str):
        super().__init__(test_path)
    
    def export_case_as_zip(self, path: str):
        title, cases = self.get_cases_as_files()
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for fname, (ctype, case) in cases.items():
                # TODO: more thorough name cleaning
                fname = re.sub(r'[<>:"/\\|?*]', "", fname)
                zip_file.writestr(f"{ctype}/{fname}.br", case)

        title = re.sub(r'[<>:"/\\|?*]', "", title)
        _, ext = os.path.splitext(title)
        if ext != ".zip":
            title += ".zip"

        out_path = os.path.join(path, title)

        if os.path.exists(out_path) and not askUser(f"This action will override {title}\nProceed?"):
            print("Operation was aborted")
            return False

        zip_buffer.seek(0)
        with open(out_path, "wb") as f:
            f.write(zip_buffer.read())
        
        return True


    def get_cases_as_files(self):
        text_files: dict[str, tuple[str, str]] = dict()
        zip_fname = ""
        for tname, title in self.get_cases_tree():
            zip_fname = tname
            for sname, section in title.items():
                sname = sname[3:].replace(" ", "_").strip()
                for uname, unit in section.items():
                    uname = uname[4:].replace(" ", "_").strip()
                    code, stdin, stdout, stderr = (
                        "\n".join(unit[getattr(TestCaseParser, k)])
                        for k in ["CODE", "USER_INPUT", "PROG_OUTPUT", "ERROR_OUTPUT"]
                    )
                    this_file = [code]
                    this_file.append("")
                    this_file.append("/*")
                    if len(stdin):
                        this_file.append("*IN*")
                        this_file.append(stdin)
                        this_file.append("*IN*")
                    this_file.append("*OUT*")
                    pdir = "tests"
                    if len(stderr):
                        pdir = "fails"
                        this_file.append(stderr)
                    elif stdout != "":
                        this_file.append(stdout)
                    this_file.append("*OUT*")
                    this_file.append("*/")
                    text_files[f"{sname}-{uname}"] = (pdir, "\n".join(this_file))
        
        zip_fname = zip_fname[2:].replace(" ", "_")
        return zip_fname, text_files
