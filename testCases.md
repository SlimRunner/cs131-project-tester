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

*stderr*
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

*stderr*
```
ErrorType.NAME_ERROR
```

## Functions

### Simple Call

*code*
```go
func get_42() {
  return 42;
}

func main() {
  print(get_42());
}
```

*stdin*
```
```

*stdout*
```
42
```

*stderr*
```
```

### Pass By Value

*code*
```go
func fake_modify(a) {
  a = "should not be modified";
}

func main() {
  var a;
  a = 42;
  fake_modify(a);
  print(a);
  var m;
  m = 31415;
  fake_modify(m);
  print(m);
}
```

*stdin*
```
```

*stdout*
```
42
31415
```

*stderr*
```
```

### No Declaration in Function

*description*
> Attempt to use a variable that doesn't exist in the function call

*code*
```go
func main() {
  foo();
  print(a);
}

func foo() {
  a = 5;
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

### Call Chain

*code*
```go
func main() {
  var str;
  str = chain4("0");
  print(str);
}

func chain1(a) {
  print("chain1: ",a);
  return a;
}

func chain2(a) {
  a = a + a;
  print("chain2: ", a);
  return chain1(a + "3");
}

func chain3(a) {
  print("chain3: ", a);
  var newstr;
  newstr = chain2(a + "22");
  print("chain3: ", a);
  return newstr;
}

func chain4(a) {
  print("chain4: ", a);
  return chain3(a + "1");
}
```

*stdin*
```
```

*stdout*
```
chain4: 0
chain3: 01
chain2: 01220122
chain1: 012201223
chain3: 01
012201223
```

*stderr*
```
```

### Early Return

*code*
```go
func main() {
  print("before return");
  call_ret();
  return;
  print("after return");
}

func call_ret() {
  print("func call");
  if (true) {
    if (false) {
      var void;
    } else {
      print("nested if");
      return;
      print("should not print");
    }
    print("should not print");
  }
  print("should not print");
}
```

*stdin*
```
```

*stdout*
```
before return
func call
nested if
```

*stderr*
```
```

## If Statements

### Shadowing

*description*
> Attempt to use a variable that doesn't exist in the function call

*code*
```go
func main() {
  var a;
  a = 5;
  if (true) {
    print(a);
    var a;
    a = "foo";
    print(a);
  }
  print(a);
}
```

*stdin*
```
```

*stdout*
```
5
foo
5
```

*stderr*
```
```
