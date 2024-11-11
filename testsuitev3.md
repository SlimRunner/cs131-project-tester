# Unit Tests V3

## Type Annotations

### Function Type in Main

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

### Function Type Not Defined

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
Syntax error at 'struct' on line 7
```

*stderr*
```
Syntax error
```
