Index
-

- [CS 131 Fall 2024: Project Starter](#cs-131-fall-2024-project-starter)
  - [Setup](#setup)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Test Case Formatting](#test-case-formatting)
  - [Scorer Output](#scorer-output)
  - [Licensing and Attribution](#licensing-and-attribution)

# CS 131 Fall 2024: Project Tester

I made this project as an alternative light version of the [official autograder](https://github.com/UCLA-CS-131/fall-24-project-starter). For the instructions on the project visit the [original project repo](https://github.com/UCLA-CS-131/fall-24-autograder).

## Setup

As instructed in the spec **do not fork from this directory**. If you clone from here, and plan to publish a private repo in GitHub, delete this repo as origin:
```sh
git remote rm origin
```
Then verify that the following outputs nothing.
```
git remote -v
```
Now you can publish without a link to this repo.

## Requirements
My tester was developed and tested on **Python v3.10.0**. Earlier version might not work.

Also, it only depends on standard libraries and _your_ project files, so you do not need to install any dependencies.

## Usage
Add a project to the root of this repo. The program automatically seeks all files named `interpreterv#.py` and `testsuitev#.md` where `#` can be any number (including zero padded numbers). If you pass no flags, the command will run the project with the highest version that has **both an interpreter and a testsuite** and it will run in testing mode. If you want to change the behavior of how it starts up, `main.py` was made as simple as possible to make editing it easy.

### Default
The highest (lexicographically sorted) version will be run, and the project will be run in test mode. Also, it will show only the test case that fail.

#### Example
```sh
python ./main.py
```

### Run specifc version
The `-p` flag allows to select a specific version of the project. The input is a string not a number (i.e. `01` is not equal to `1`).

#### Example
```sh
python ./main.py -p 2 # runs project v2
```

### Run mode
The `-t` flag allows to select what mode to run the program on. There are two modes. The default is `testit` which tests and scores each program. The other mode is `timeit` which times how long each program takes to run and it prints their output.

```sh
python ./main.py -t timeit
```

### Exporting
You do not vibe with my tester? No problem run the tester with the `-X` flag and it will generate a zip file with all the test cases converted to individual files you can drop in the [official tester](https://github.com/UCLA-CS-131/fall-24-autograder). You may only use this flag alone to export the most recent project or combine it with `-p` to choose a project manually. If you mix it with other flags this will supercede them all.

It will ask you if you want to override an existing file.

#### Example
```sh
# imports the default project tests cases one folder up
python ./main.py -X ../
```

### Filtering
You may filter the test cases by their direct subtitle (`-u` or `--unit`) or by the subtitle one level up (`-s` or `--section`). These flags are mutually exlusive and expect one or more strings (remember to use quotes for multi word titles).

#### Example

```sh
python ./main.py -s "variables" "functions"
python ./main.py -u "simple loop" "call to print"
```

### Verbose
The `-v` flag allows to print all the sections including the ones that passed. The hidden cases still count towards the total unlike with filtering. 
#### Example

```sh
python ./main.py -v
```

### Parameter Pass-Thru
The `--args` flag allows passing parameters to the tester callback. In the case of this project that is `interpreter.run`. Since the callback does not allow to provide parameters other than the program code, then this option allows to pass other such as the ones inherited from `InterpreterBase` or custom of your own.

The parameters must be passed in sets of triples that contain (1) name of parameter, (2) type of parameter, and (3) value of parameter. If your option causes the program to print extra debugging info, I recommend to use it in combination with `-t timeit` so that you can inspect the program output more easily.

#### Example
The following command runs the interpreter with the custom argument named `trace_output` set to `True`:
```sh
python ./main.py --args trace_output bool True
```

### Crash On Error
The flag `-E` allows you to waive the error handling; thus, when the tester encounters an error it will crash and you can see Python extended error message. The recommended use of this flag is in combination with `-u` to choose only the test case you want to test because incorrectness passing tests will crash as well.

#### Example
```sh
python ./main.py -u 'simple loop' -E
```

### Help
The `-h` flag shows extended information about each flag.
```
python ./main.py -h
```
It always has the up-to-date information about all flags. You can also feed its output to ChatGPT so that it knows how to generate a command for you.

## Test Case Formatting
The tester lets you write your Brewin code in a markdown file (i.e. [testsuitev2.md](./testsuitev2.md)). Its benefits are that since Brewin is pretty similar to Go, you get syntax highlighting for free in code blocks.

The markdown file is formatted as follows
```md
# Title
## Name of Unit Section 1
### name of unit test 1
> section 1, test 1 definition
### name of unit test 2
> section 1, test 2 definition
### ...
### name of unit test i
> section 1, test i definition

## Name of Unit Section 2
### name of unit test 1
> section 2, test 1 definition
> and so on
```

There may only by one title and it must be first. If you do not follow that you will get an error.

Each individual unit test is formatted as follows:
````md
*code*
```go
func main() {
  return;
}
```

*user input*
```
```

*expected stdout*
```
```

*expected stderr*
```
```
````

Fill in the code blocks as appropriate. **Also if you use VSCode I added a custom snippet to add the boilerplate**. To use the snippet type `addunit` then press `ctrl+space` to get the suggestions (since markdown files do not automatically bring up the autocomplete). Finally, press enter and fill in the blanks as you want.

The tags such as `*code*` are optional and can contain any text you want, so long as they are enclosed in asterisks. Additionally, you may add remarks anywhere with `> ...`. These along with empty lines (or lines containing only spaces) **are ignored**. Any type of text anywhere will cause an error when parsing the test cases.

> Note: the test cases in this repo are mostly my own with a few ones from the autograder. They are NOT exhaustive, and some entries test undefined behavior as per the spec (which I defined).

## Scorer Output
The output of the scorer may look like this:
```
# Unit Tests V4
## Meta Test
### Diff Test
> ./testsuitev4.md line 5

- stdout: FAIL ❌

  |  # | received | expected |  # |
  | -- | -------- | -------- | -- |
  | 01 | `asd`    | `qwe`    | 01 |
  | 02 | ``       | `l`      | 02 |
  | 04 | `l`      |          |  . |
  | 05 | `g`      |          |  . |
  | 06 | `o`      |          |  . |
  | 11 | `m`      | `n`      | 10 |

- stderr: FAIL ❌

  | # | received               | expected               | # |
  | - | ---------------------- | ---------------------- | - |
  | 1 | `ErrorType.TYPE_ERROR` | `ErrorType.NAME_ERROR` | 1 |

  -  if-statement condition must evaluate to boolean
```
It is formatted to look good in markdown and in plain text, so you can redirect the output to a markdown file to inspect it more easily. **It also includes the source with line number to allow VS Code link navigation**. [See more about that here](https://code.visualstudio.com/docs/terminal/basics#_links).

You may notice some lines have back ticks. These help you differentiate if there was an empty line expected (\`\`). In general if there is a backticked message in both matching lines it means that received does not match expected. If either has a non-backticked message it means either recieved something extra or expected something that is not there. Also, if an error was emitted by the interpreter, the description will be put below. However, exact descriptions are _not_ matched. That is to keep the test easier to write.

This diff report is generated with Python's difflib, so it is a diff between the program output and the expected output. Shows the line numbers of both the recieved and expected output. That library may sometimes generate diffs that are unintuitive if diff is large enough, but it gives you a rough idea of what is going wrong. It works fine for most errors.

In the example above you would navigate to the unit test titled `Diff Test` in the appropriate `testsuite` file to see the snippet that generated the error. In this case this is the test that _purposefully_ generated this error:
````md
### Diff Test

*code*
```go
func main() {
  print("asd");
  print();
  print("a");
  print("l");
  print("g");
  print("o");
  print("r");
  print("i");
  print("t");
  print("h");
  print("m");
  if (1) {
    print();
  }
}
```

*stdin*
```
```

*stdout*
```
qwe
l
o
g
a
r
i
t
h
n
```

*stderr*
```
ErrorType.NAME_ERROR
```
````

## Licensing and Attribution

This is an unlicensed repository. My contribution are the files `tester.py`, `testersetup.py`, `testsuitev#.md`, `main.py`, and `arghelper.py`.

Anything else was primarily written by [Carey Nachenberg](http://careynachenberg.weebly.com/), with support from his TAs for the [Fall 2024 iteration of CS 131](https://ucla-cs-131.github.io/fall-24-website/).
