# Unit Tests

## Input and Output

### Simple User Input

*code*
```go
func main() {
  print(inputs());
  print(inputi());
  print(inputi());
}
```

*stdin*
```
user input
45
-45
```

*sdtout*
```
user input
45
-45
```

*error*
```
```

## Variables

### Declaration & Assignment

*code*
```go
func main() {
  var a;
  a = 5;
  print(a);
  a = 8;
  print(a);
  a = -2;
  print(a);
  a = "random text";
  print(a);
  a = false;
  print(a);
  a = true;
  print(a);
  var b;
  b = a;
  b = "new text";
  print(b);
  print(a);
  var a;
}
```

*stdin*
```
```

*sdtout*
```
5
8
-2
random text
false
true
new text
true
```

*error*
```
ErrorType.NAME_ERROR
```
