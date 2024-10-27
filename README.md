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

The command to run the default options is
```
python ./main.py
```

You can also manually select which project you want to run. If, for example, you want to run `interpreterv2.py` you would run
```
python ./main.py -p 2
```
If instead of making a test run you want to see the actual program output you can run the profiler
```
python ./main.py -t timeit
```
The profiler will also show some simple time average and total.

If you want to see extended information about these options call
```
python ./main.py -h
```

## Test Case Formatting
I used a rather makeshift unit tester. It essentially lets you write your Brewin code in a markdown file (i.e. [testsuitev2.md](./testsuitev2.md)). Its benefits are that since Brewin is pretty similar to Go, you get syntax highlighting for free in code blocks.

The markdown file is formatted as follows
```md
# Title
## Name of Unit Section 1
### name of unit test 1
<!-- test 1 definition -->
### name of unit test 2
<!-- test 2 definition -->
### ...
### name of unit test i
<!-- test i definition -->

## Name of Unit Section 2
### name of unit test 1
<!-- test 1 definition -->
<!-- and so on -->
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

> Note: the test cases in this repo are mostly my own with a few ones from the autograder. They are NOT exhaustive.

## Scorer Output
The output of the scorer may look like this:
```
# Unit Tests
## Control Flow
### If-Statement Shadowing

stdout: FAIL ❌
  [e]: foo
  [e]: foo
  [e]: bar
  [e]: foo
  [e]: 5
stderr: FAIL ❌
  [R]: ErrorType.NAME_ERROR
       Variable A defined more than once
```
What this is telling you is that both stdout and stderr failed to match the expected output. They have to both succeed for the snippet to count as passed. The `[e]` means that such line _was_ expected. An `[R]` means that such line was recieved (and not expected). Usually `[R]` appears before `[e]` if something was received but doesn't match what was expected. If the next letter is the same it means that either something was recieved and nothing was expected or something was expected but nothing was recieved. This is essentially a regular diff where `-` are `[R]` and `+` are `[e]`.

Either way, in the example above you would navigate to the section named `If-Statement Shadowing` in the appropriate `testsuite` file to see the snippet that generated the error.

## Licensing and Attribution

This is an unlicensed repository. My contribution are the files `tester.py`, `testersetup.py`, `testsuitev#.md`, `main.py`, and `arghelper.py`.

Anything else was primarily written by [Carey Nachenberg](http://careynachenberg.weebly.com/), with support from his TAs for the [Fall 2024 iteration of CS 131](https://ucla-cs-131.github.io/fall-24-website/).
