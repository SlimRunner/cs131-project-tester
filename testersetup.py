import os
import re
import sys
import importlib.util


class ProjectEntry:
    def __init__(self, version: str) -> None:
        self.interpreter: str | None = None
        self.testsuite: str | None = None
        self.interpreter_path: str | None = None
        self.testsuite_path: str | None = None
        self.__version: str = version

    @property
    def version(self) -> str:
        return self.__version

    def is_valid(self):
        return not (self.interpreter is None or self.testsuite is None)

    def what_is_missing(self):
        no_interpreter = self.interpreter is None
        no_testsuite = self.testsuite is None
        match no_interpreter, no_testsuite:
            case True, True:
                return "interpreter and testsuite"
            case True, False:
                return "an interpreter"
            case False, True:
                return "a testsuite"
            case _:  # missing both
                return None


def load_module(name: str, pckg: str) -> type | None:
    spec = importlib.util.find_spec(name)
    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return getattr(module, pckg)
    else:
        return None


def find_interpreters() -> dict[str, ProjectEntry]:
    proj_root = os.path.abspath("./")
    suites_regex = r"^(testsuitev(?=\d+\.md)|interpreterv(?=\d+\.py))(\d+)(\.md|\.py)$"
    suites_regex = re.compile(suites_regex)
    entries: dict[int, ProjectEntry] = dict()

    for filename in os.listdir(proj_root):
        match_result = suites_regex.match(filename)
        if not match_result:
            continue
        name, ver, _ = match_result.groups()
        if ver not in entries:
            entries[ver] = ProjectEntry(ver)
        setattr(entries[ver], name[:-1], name + ver)
        setattr(entries[ver], f"{name[:-1]}_path", os.path.join(proj_root, filename))

    return entries


def choose_project(
    proj_version: str, interpreters: dict[str, ProjectEntry], target_module: str
):
    if proj_version not in interpreters:
        raise SystemExit(f"There is no project version {proj_version}.")
    elif not interpreters[proj_version].is_valid():
        raise SystemExit(
            f"Project version {proj_version} is missing {interpreters[proj_version].what_is_missing()}."
        )
    Interpreter = load_module(interpreters[proj_version].interpreter, target_module)
    # valid_interpreters[0].testsuite narrowed from (str | None) to (str)
    test_path = interpreters[proj_version].testsuite_path
    proj_path = interpreters[proj_version].interpreter_path
    print("Running interpreter version", interpreters[proj_version].version, "\n")
    return Interpreter, proj_path, test_path


def choose_latest_project(interpreters: dict[str, ProjectEntry], target_module: str):
    sorted_interpreters = [
        entry for _, entry in sorted(interpreters.items(), reverse=True)
    ]
    valid_interpreters = [entry for entry in sorted_interpreters if entry.is_valid()]
    if not len(interpreters):
        raise SystemExit("There are no projects available in the root directory.")
    elif not len(valid_interpreters):
        raise SystemExit(
            "There are no projects with both an interpreter and testsuite."
        )

    Interpreter = load_module(valid_interpreters[0].interpreter, target_module)
    # valid_interpreters[0].testsuite narrowed from (str | None) to (str)
    test_path = valid_interpreters[0].testsuite_path
    proj_path = valid_interpreters[0].interpreter_path
    print("Running interpreter version", valid_interpreters[0].version, "\n")
    return Interpreter, proj_path, test_path
