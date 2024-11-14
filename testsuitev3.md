# Unit Tests V3

## Type Validity

### Valid Print

*code*
```go
func main() : void {
  var a: string;
  print(a);
  a = "it wasn't str arghhhh.";
  print(a);
}
```

*stdin*
```
```

*stdout*
```

it wasn't str arghhhh.
```

*stderr*
```
```

### Missing Return Type in main

*code*
```go
func main() {
  return;
}
```

*stdin*
```
```

*stdout*
```
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Missing Return Type in foo

*code*
```go
func main() : void {
  return;
}

func bar() : int {
  return 5;
}

func foo() {
  return;
}
```

*stdin*
```
```

*stdout*
```
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Return Type Does Not Match Value

*code*
```go
func main() : void {
  return 5;
}
```

*stdin*
```
```

*stdout*
```
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Labeled Function Return with Undefined Type

*code*
```go
func main() : void {
  return;
}

func invalid_type() : GLaDOS {
  return;
}
```

*stdin*
```
```

*stdout*
```
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Main Must be Void

*code*
```go
func main() : int {
  print("barista says this is valid?");
  print("may be undefined behavior");
  print("I am not sure");
  return 6;
}
```

*stdin*
```
```

*stdout*
```
barista says this is valid?
may be undefined behavior
I am not sure
```

*stderr*
```
```

### Simple Parameter Passing

*code*
```go
func main() : void {
  var a: int;
  a = 0;
  print(a);
  foo(a);
}

func foo(a: int) : void {
  print(a);
}
```

*stdin*
```
```

*stdout*
```
0
0
```

*stderr*
```
```

### Parameter Type Mismatch Int -> String

*code*
```go
func main() : void {
  var a: int;
  foo(a);
  print("not fine");
}

func foo(a: string) : void {
  print(a);
}
```

*stdin*
```
```

*stdout*
```
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Labeled Parameter with Undefined Type

*code*
```go
func main() : void {
  return;
}

func foo(a: Glados) {return nil;}
```

*stdin*
```
```

*stdout*
```
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Matched Return Type

*code*
```go
func main() : void {
  var a: int;
  var b: bool;
  a = five();
  print(a);
  b = frive();
  print(b);
  b = five();
  print(b);
  b = zero();
  print(b);
}

func five(): int {
  return 5;
}

func zero(): int {
  return 0;
}

func frive(): bool {
  return 5;
}
```

*stdin*
```
```

*stdout*
```
5
true
true
false
```

*stderr*
```
```

### Mismatched Return Assignment

*code*
```go
func main() : void {
  var a: int;
  a = five();
  print("should not print");
}

func five(): string {
  return "five";
}
```

*stdin*
```
```

*stdout*
```
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Mismatched Return Value

*code*
```go
func main() : void {
  var a: string;
  a = five();
  print("should not print");
}

func five(): string {
  return 5;
}
```

*stdin*
```
```

*stdout*
```
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Type Coercion, input, shadowing, and void call

*code*
```go
func main(): void {
  var a: bool;
  a = 10;
  print(a);
  if (a) {
    var a:string;
    a = "shadowed";
    print(a);
  }
  print(a);
  var b: int;
  b = inputi("input prompt");
  print(b);
  foo(5);
  foo(0);
  foo(b);
  print(bar());
  print("should not print");
}

func foo(a: bool) : void {
  print(a);
  return;
}

func bar() : void {
  return;
}
```

*stdin*
```
-5432
```

*stdout*
```
true
shadowed
true
input prompt
-5432
true
false
true
```

*stderr*
```
ErrorType.TYPE_ERROR
```

## Structs

### Simple Struct Definition

*code*
```go
struct foo {
  a: int;
}

func main() : void {
  var bar: foo;
  bar = new foo;
  print(bar == nil);
  bar.a = 5
  print(bar.a);
  print("all good!");
  return;
}
```

*stdin*
```
```

*stdout*
```
true
5
all good!
```

*stderr*
```
```

### Composition of Structs

*code*
```go
struct woo {
  main: int;
}

struct foo {
  bar: woo;
}

func main() : void {
  var foo: woo;
  print(foo != nil);
  foo = new woo;
  var bar: foo;
  bar = new foo;
  print(bar.bar == nil);
  bar.bar = foo;
  bar.bar.main = 13
  print(bar.bar.main);
  print("all good!");
  return;
}
```

*stdin*
```
```

*stdout*
```
false
true
13
all good!
```

*stderr*
```
```

### Struct Definition Must Come First

> this error is handled by the parser

*code*
```go
func main() {
  print("all good!");
  return;
}

struct foo {
  a: int;
}
```

*stdin*
```
```

*stdout*
```
Syntax error at 'struct' on line 6
```

*stderr*
```
Syntax error
```

### Struct matches nil but not void

*code*
```go
struct bar {
  a: int;
}

func main(): void {
  var a: int;
  var b: bar;
  b = nil;
  print("fine so far");
  b = foo();
  print("not fine");
  print(b);
}

func foo() : void {return;}
```

*stdin*
```
```

*stdout*
```
fine so far
```

*stderr*
```
ErrorType.TYPE_ERROR
```
