# Unit Tests V2

## Input and Output

### Print Returns `nil`

*code*
```go
func main() {
  var a;
  a = print();
  print(a == nil);
}
```

*stdin*
```
```

> Note that I added an empty line because the empty print

*stdout*
```

true
```

*stderr*
```
```

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

### Input Return Type

*code*
```go
func main() {
  var a;
  a = inputs();
  print("string MatcH" == a);
  print("string Match" == a);
  print("string MatcH" != a);
  print("string Match" != a);
  var b;
  b = "-" + inputs() + "123";
  print(b);
  b = inputs();
  print(a == b);
  print(a != b);
  print(a != b + "asd");
}
```

*stdin*
```
string MatcH
456
string MatcH
42
```

*sdtout*
```
true
false
false
true
-456123
true
false
true
```

*stderr*
```
```

## Variables

### Declaration and Assignment

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

### Double Declaration

*code*
```go
func main() {
  var a;
  var a;
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

### Double Declaration Inside If-Scope

*code*
```go
func main() {
  var a;
  if (true) {
    var a;
    print("no error yet");
    var a;
  }
}
```

*stdin*
```
```

*stdout*
```
no error yet
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Double Declaration Inside For-Scope

*code*
```go
func main() {
  var a;
  for (a = 0; false; a = a) {
    var a;
    print("never happens");
    var a;
  }
  for (a = 0; true; a = a) {
    var a;
    print("no error yet");
    var a;
  }
}
```

*stdin*
```
```

*stdout*
```
no error yet
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
  c = (a * b - 11 * a / 3) / (b - a);

  print(c * c - (c + b));
}
```

*stdin*
```
```

*stdout*
```
49
```

*stderr*
```
```

### Type Compat - Int Bool

*code*
```go
func main() {
  print(1 + false);
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

### Type Compat - Arith Bool

*code*
```go
func main() {
  print(false - true);
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

### Type Compat - Cond Int

*code*
```go
func main() {
  print(1 || 1);
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

### Type Compat - Unary Bool

*code*
```go
func main() {
  print(-true);
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

### Boolean Correctness

*code*
```go
func main() {
  var X;
  var A;
  var B;
  var C;
  var D;
  var E;

  A = true;
  B = 5 < 3;
  C = nil != nil;
  D = false;
  E = 0 >= 0;

  print(A);
  print(B);
  print(C);
  print(D);
  print(E);

  X = ((A || !B) && (C || D)) || (!(A && C) && (B || !E));
  if (X) {
    print("X = True");
  } else {
    print("X = False");
  }

  if (inputi("...") < -5) {
    C = true;
    print("X = ", ((A || !B) && (C || D)) || (!(A && C) && (B || !E)));
  }
}
```

*stdin*
```
-100
```

*stdout*
```
true
false
false
false
true
X = False
...
X = true
```

*stderr*
```
```

### Mixed Comparison

*code*
```go
func main () {
  var a;
  var b;
  var c;
  var d;
  var e;
  a = true;
  b = 5;
  c = "5";
  d = "true";
  e = nil;

  print(a == b);
  print(b == c);
  print(a != d);
  print(c != d);

  print(e != a);
  print(e != b);
  print(e == c);
  print(e == d);
  print(e == e);
}
```

*stdin*
```
```

*stdout*
```
false
false
true
true
true
true
false
false
true
```

*stderr*
```
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

### Double Declaration in Function

*code*
```go
func main() {
  var a;
  foo();
}

func foo() {
  var a;
  a = "all good";
  print(a);
  var a;
}
```

*stdin*
```
```

*stdout*
```
all good
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Invalid Parameter Shadow

*code*
```go
func main() {
  var a;
  foo("entered function");
}

func foo(a) {
  print(a);
  var a;
}
```

*stdin*
```
```

*stdout*
```
entered function
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

### Simple Recursion - factorial

*code*
```go
func main() {
  print(fact(5));
  print(fact(inputi("Enter a number")));
}

func fact(n) {
  if (n <= 1) { return 1; }
  return n * fact(n-1);
}
```

*stdin*
```
8
```

*stdout*
```
120
Enter a number
40320
```

*stderr*
```
```

### Mutual Recursion

*code*
```go
func main() {
  print(no_ab(4));
  print(no_ab(inputi("Enter a number")));
}

func no_ab(n) {
  if (n == 0) { return 1; }
  if (n == 1) { return 4; }
  return 3 * no_ab(n - 1) + no_ab_helper(n);
}

func no_ab_helper(n) {
  if (n == 0) { return 0; }
  if (n == 1) { return 1; }
  return 2 * no_ab(n - 2) + no_ab_helper(n - 1);
}
```

*stdin*
```
9
```

*stdout*
```
209
Enter a number
151316
```

*stderr*
```
```

## Control Flow

### If-Statement Condition is Boolean

*code*
```go
func main() {
  if (1) {
    print("Condition MUST be boolean. This is int.");
  }
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

### For-Statement Condition is Boolean

*code*
```go
func main() {
  var i;
  for (i = "a"; 0; i = i) {
    print("Condition MUST be boolean. This is int.");
  }
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

### If-Statement Scope Lifetime

*code*
```go
func main() {
  if (true) {
    var x;
  }
  x = 5;
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

### Simple For Loop

*code*
```go
func main() {
  var i;
  for (i = 8; i > 0; i = i - 3) {
    print(i);
  }
}
```

*stdin*
```
```

*stdout*
```
8
5
2
```

*stderr*
```
```

### Mixed If-For

*code*
```go
func main() {
  var vd;
  vd = false;
  if (inputs() == "I'm in") {
    var i;
    for (i = 0; i < 10; i = i + 1) {
      var x;
      x = i * i - 7 * i + 10 > 0;
      if (x) {
        vd = x;
        print("above zero");
      } else {
        print("below zero");
      }
      var i;
      i = x;
    }
    print(i);
    print(x);
  }
}
```

*stdin*
```
I'm in
```

*stdout*
```
above zero
above zero
below zero
below zero
below zero
below zero
above zero
above zero
above zero
above zero
10
```

*stderr*
```
ErrorType.NAME_ERROR
```

### If-Statement Shadowing

*code*
```go
func main() {
  var A;
  A = 5;
  if (true) {
    print(A);
    var A;
    A = "foo";
    print(A);
    if (false) {
      var A;
    } else {
      print(A);
      var A;
      A = "bar";
      print(A);
    }
    print(A);
  }
  print(A);
}
```

*stdin*
```
```

*stdout*
```
5
foo
foo
bar
foo
5
```

*stderr*
```
```

### For-Statement Shadowing

*code*
```go
func main() {
  var varra;
  varra = 42;
  var i;
  for (i = -5; i <= 5; i = i + 1) {
    var B;
    B = varra + i;
    if (B == varra) {
      var B;
      B = " to the universe";
      print("The answer" + B);
    } else {
      print(B);
    }

    var varra;
    varra = i;
  }
  print(varra, " outer A");
}
```

*stdin*
```
```

*stdout*
```
37
38
39
40
41
The answer to the universe
43
44
45
46
47
42 outer A
```

*stderr*
```
```

### For Body Scope

*code*
```go
func main() {
  var a;
  for (a = ""; a != "00000"; a = a + "0") {
    print(a);
    if (a == "000") {
      return;
      print("if failed to unwind");
    }
    var a;
    a = "for body scope";
    print(a);
  }
  print("must not print");
}
```

*stdin*
```
```

*stdout*
```

for body scope
0
for body scope
00
for body scope
000
```

*stderr*
```
```
