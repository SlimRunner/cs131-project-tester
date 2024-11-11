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

## Structs

### Simple Struct Definition

*code*
```go
struct foo {
  a: int;
}

func main() {
  var bar: foo;
  bar.a = 5;
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
5
all good!
```

*stderr*
```
Syntax error
```

### Composition of Structs

*code*
```go
struct foo {
  bar: woo;
}

struct woo {
  main: int;
}

func main() : void {
  var foo: woo;
  foo = new woo;
  var bar: foo;
  bar = new foo;
  print(bar.bar == nil);
  bar.bar = foo;
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
5
all good!
```

*stderr*
```
```

### Struct Definition Must Come First

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
