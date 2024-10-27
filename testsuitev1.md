# Unit Tests V1

## Input and Output

### Empty Print

*code*
```go
func main() { print(); }
```

*stdin*
```
```

*stdout*
```

```

*stderr*
```
```

### Number Print

*code*
```go
func main() { print(12); }
```

*stdin*
```
```

*stdout*
```
12
```

*stderr*
```
```

### String Print

*code*
```go
func main() { print("12we"); print("?*^"); }
```

*stdin*
```
```

*stdout*
```
12we
?*^
```

*stderr*
```
```

### Multi Parameter Print

*code*
```go
func main() {
  print();
  print(1);
  print("asd");
  print(1,2,3,"-",3,2,1);
  print("h","w");
}
```

*stdin*
```
```

*stdout*
```

1
asd
123-321
hw
```

*stderr*
```
```

### Print Numbers and Empty Input

*code*
```go
func main() {
  var s;
  s = inputi();
  print(s);
  s = inputi();
  print(s);
}
```

*stdin*
```
0123
-00005
```

*stdout*
```
123
-5
```

*stderr*
```
```

### Input Parameter Validation

*code*
```go
func main() {
  var s;
  s = inputi("asd", "qwe");
  print(s);
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
ErrorType.NAME_ERROR
```

## Variables

### Declaration and Assignment

*code*
```go
func main() {
  var A; var B; var C; var a; var b; var c;
  a = 5;
  A = 6;
  b = 7;
  B = 8;
  c = 9;
  C = 10;
  print(a,A,b,B,c,C);
  A = "A";
  B = "B";
  C = "C";
  a = "a";
  b = "b";
  c = "c";
  print(a,A,b,B,c,C);
}
```

*stdin*
```
```

*stdout*
```
5678910
aAbBcC
```

*stderr*
```
```

### Double Declaration

*code*
```go
func main() {
  var a;
  print("should print");
  var a;
  print("should not print");
}
```

*stdin*
```
```

*stdout*
```
should print
```

*stderr*
```
ErrorType.NAME_ERROR
```

## Operators

### Arithmetic Correctness

*code*
```go
func main() {
  var a;
  var b;
  a = 5;
  b = 7;

  var c;
  c = a + 11 - (b - 1 + b + 1 + 0 + b);

  print(c);
  print(0 - c);
  print(0 - c + 5);
}
```

*stdin*
```
```

*stdout*
```
-5
5
10
```

*stderr*
```
```

## Expressions

### Inline `inputi`

*code*
```go
func main() {
  var a;
  var b;
  a = 5;
  b = 7;

  var c;
  c = a + 11 - (b - 1 + b + 1 + inputi("nested prompt") + b);

  print(c);
  print(0 - c);
  print(0 - c + 5);
}
```

*stdin*
```
9
```

*stdout*
```
nested prompt
-14
14
19
```

*stderr*
```
```

### Evaluated Arguments in `print`

*code*
```go
func main() {
  var a;
  var b;
  a = 5;
  b = 7;

  var c;
  print(a + 11);
  print(b - 1 + b + 1 + 9 + b);
  c = a + 11 - (b - 1 + b + 1 + 9 + b);

  print(c, 0 - c, 0 - c + 5);
}
```

*stdin*
```
```

*stdout*
```
16
30
-141419
```

*stderr*
```
```

### Type Error

*code*
```go
func main() {
  print(4 + "asd");
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


## Functions

### Only `print` and `inputi`

*code*
```go
func main() {
  var a;
  a = inputi("works!");
  print(a, ": Error not found");
  bogus();
  print("should not print");
  no_name();
  print("should also not print");
}
```

*stdin*
```
404
```

*stdout*
```
works!
404: Error not found
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Missing Main

*code*
```go
func not_main() {
  print();
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
ErrorType.NAME_ERROR
```
