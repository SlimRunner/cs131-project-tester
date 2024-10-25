Index
-
- [CS 131 Fall 2024: Project Starter](#cs-131-fall-2024-project-starter)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Test Case Formatting](#test-case-formatting)
  - [Licensing and Attribution](#licensing-and-attribution)

# CS 131 Fall 2024: Project Tester

I made this project as an alternative light version of the [official autograder](autograder). For the instructions on the project visit the [original project repo](upstream).

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
Add a project to the root of this repo. The program automatically seeks from `interpreterv4` in reverse to `interpreterv1` so later projects will take precedence to define the `Interpreter`. If none are found, then the program will exit with error. The main program is very simple so you can easily modify it, if it does not suit your needs.

To test run:
```
python ./main.py
```

This will read from [testCases.md](./testCases.md) to run each test case in there and check its output against correctness. If you wish to simply see the output of each program run:
```
python ./main.py -t timeit
```
It will also show some simple timing information. There is only one flag but if you want to quickly check the options call the help flag:
```
python ./main.py -h
```

## Test Case Formatting
I used a rather makeshift unit tester. It essentially lets you write your Brewin code in a markdown file ([testCases.md](./testCases.md)). Its benefits are that since Brewin is pretty similar to Go, you get syntax highlighting for free in code blocks.

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

## Licensing and Attribution

This is an unlicensed repository. My only contribution are the files `tester.py`, `testCases.md`, `main.py`, and `arghelper.py`.

Anything else was primarily written by [Carey Nachenberg](http://careynachenberg.weebly.com/), with support from his TAs for the [Fall 2024 iteration of CS 131](https://ucla-cs-131.github.io/fall-24-website/).

[upstream]: https://github.com/UCLA-CS-131/fall-24-project-starter
[autograder]: https://github.com/UCLA-CS-131/fall-24-autograder.git
