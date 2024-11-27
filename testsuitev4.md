# Unit Tests V4

## Exceptions

### Simple Try Catch Hit

*code*
```go
func main() {
  print("start");
  try {
    print("enter try");
    raise "name";
    print("MUST NOT PRINT");
  }
  catch "name" {
    print("caught");
  }
  print("continue");
}
```

*stdin*
```
```

*stdout*
```
start
enter try
caught
continue
```

*stderr*
```
```

### Simple Try Catch Miss

*code*
```go
func main() {
  print("start");
  try {
    print("enter try");
    raise "name";
    print("MUST NOT PRINT - try");
  }
  catch "not name" {
    print("MUST NOT PRINT - catch");
  }
  print("MUST NOT PRINT - main");
}
```

*stdin*
```
```

*stdout*
```
start
enter try
```

*stderr*
```
ErrorType.FAULT_ERROR
```

## Eager-Like Behavior

### Sequential Prints

*code*
```go
func main() {
  var x;
  x = "asd";
  print(x);
  x = 5;
  print(x);
  x = false;
  print(x);
}
```

*stdin*
```
```

*stdout*
```
asd
5
false
```

*stderr*
```
```

### For-header local scope access

*code*
```go
func main() {
  var x;
  for (x = 0; x == 1; x = x) {
    print("should not print");
  }
  print("asd");
}
```

*stdin*
```
```

*stdout*
```
asd
```

*stderr*
```
```

## Lazy Evaluation

### Phantom Print

*code*
```go
func main() {
  var x;
  x = print(x) + "asd";
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
```

### Phantom Input

*code*
```go
func main() {
  var x;
  x = inputi(x);
  var y;
  y = inputs(x);
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
```

### Override Lazy Input

> this test depends on [this other test](#phantom-input)

*code*
```go
func main() {
  var x;
  x = inputi(x);
  var y;
  y = inputs(x);
  x = "asd";
  y = 42;
  print(x + "f");
  print(y / 2);
}
```

*stdin*
```
1984
literally
```

*stdout*
```
asdf
21
```

*stderr*
```
```

### Eager input func call

*code*
```go
func main() {
  var x;
  x = 5;
  inputi("foo");
  print("bar");
  print(x);
}
```

*stdin*
```
0
```

*stdout*
```
foo
bar
5
```

*stderr*
```
```

### Lazy input func call

*code*
```go
func main() {
  var x;
  x = inputi("foo");
  print("bar");
  print(x);
}
```

*stdin*
```
57
```

*stdout*
```
bar
foo
57
```

*stderr*
```
```

### Test cached eval

*code*
```go
func foo(a) {
  print("a: ", a);
  return a + 1;
}

func main() {
  var x;
  x = foo(5);
  print("x: ", x);
  print("x: ", x);
  x = foo(-1);
  print("x: ", x);
  print("x: ", x);
}
```

*stdin*
```
```

*stdout*
```
a: 5
x: 6
x: 6
a: -1
x: 0
x: 0
```

*stderr*
```
```

### Lazy self-ref fcall arg

*code*
```go
func foo(a) {
  print("a: ", a);
  return a - a / 3;
}

func main() {
  var x;
  x = 42;
  x = foo(x);
  print(x);
}
```

*stdin*
```
```

*stdout*
```
a: 42
28
```

*stderr*
```
```

### Lazy self-ref print arg

*code*
```go
func foo(a) {
  print("in foo");
  print(a);
}

func main() {
  var x;
  x = 42;
  x = print(x);
  print("mark");
  foo(x);
}
```

*stdin*
```
```

> None is undefined behavior, but there was no other way of eagerly
> evaluating x. You may change that as you wish.

*stdout*
```
mark
in foo
42
None
```

*stderr*
```
```

### Lazy self-ref input arg

*code*
```go
func foo(a) {
  print("in foo");
  print(a);
}

func main() {
  var x;
  x = "prompt";
  x = inputi(x);
  print("mark");
  foo(x);
}
```

*stdin*
```
-53
```

*stdout*
```
mark
in foo
prompt
-53
```

*stderr*
```
```

### Lazy eval outside scope

*code*
```go
func foo(a) {
  print("a: ", a);
  return a + 1;
}

func bar(b) {
  print(b);
}

func main() {
  var x;
  x = foo(5);
  bar(x);
}
```

*stdin*
```
```

*stdout*
```
a: 5
6
```

*stderr*
```
```

### Eager for-stmt header

*code*
```go
func foo(a) {
  print("a: ", a);
  return a + 1;
}

func main() {
  var x;
  for (x = 0; x < 3; x = foo(x)) {
    print("x: ", x);
    var q;
  }
  print("end");
}
```

*stdin*
```
```

*stdout*
```
x: 0
a: 0
x: 1
a: 1
x: 2
a: 2
end
```

*stderr*
```
```

## Legacy V2 - Input and Output

### Print Returns nil

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

## Legacy V2 - Variables

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

## Legacy V2 - Operators

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

## Legacy V2 - Functions

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
chain3: 01
chain2: 01220122
chain1: 012201223
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

## Legacy V2 - Control Flow

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

## Incorrectness Autograder Cases

### text exception 2

*code*
```go
func main() {
  var r;
  r = 10;
  raise r;
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

### test lazy eval error 4

*code*
```go
func main() {
  var a;
  a = "a" <= "b";
  print("---");
  print(a);
}
```

*stdin*
```
```

*stdout*
```
---
```

*stderr*
```
ErrorType.TYPE_ERROR
```

## Correctness Autograder Cases

### test exception argument 1

*code*
```go
func foo() {
  raise "foo";
}

func main() {
  try {
    print("a",foo(),"c");
  }
  catch "foo" {
    print("X");
  }
  print("Y");
}
```

*stdin*
```
```

*stdout*
```
X
Y
```

*stderr*
```
```

### test exception basic 2

*code*
```go
func main() {
  print("0");
  try {
    print("1");
    raise "a";
    print("2");
  }
  catch "a" {
    print("3");
  }
  print("4");
}
```

*stdin*
```
```

*stdout*
```
0
1
3
4
```

*stderr*
```
```

### test exception condtion 1

*code*
```go
func foo() {
  raise "x";
  print("foo");
  return true;
}

func main() {
  try {
    if (foo()) {
    print("true");
    }
  }
  catch "x" {
    print("x");
  }
}
```

*stdin*
```
```

*stdout*
```
x
```

*stderr*
```
```

### test exception func call 1

*code*
```go
func foo() {
  print("F0");
  raise "a";
  print("F1");
}


func main() {
  print("0");
  try {
    print("1");
    foo();
    print("2");
  }
  catch "b" {
    print("5");
  }
  catch "a" {
    print("3");
  }
  catch "c" {
    print("6");
  }
  print("4");
}
```

*stdin*
```
```

*stdout*
```
0
1
F0
3
4
```

*stderr*
```
```

### test lazy eval basic 1

*code*
```go
func bar(x) {
  print("bar: ", x);
  return x;
}

func main() {
  var a;
  a = -bar(1);
  print("---");
  print(a);
}
```

*stdin*
```
```

*stdout*
```
---
bar: 1
-1
```

*stderr*
```
```

### test lazy eval cache 1

*code*
```go
func bar(x) {
  print("bar: ", x);
  return x;
}

func main() {
  var a;
  a = bar(0);
  a = a + bar(1);
  a = a + bar(2);
  a = a + bar(3);
  print("---");
  print(a);
  print("---");
  print(a);
}
```

*stdin*
```
```

*stdout*
```
---
bar: 0
bar: 1
bar: 2
bar: 3
6
---
6
```

*stderr*
```
```

### test lazy eval func call 1

*code*
```go
func foo() {
  print("foo");
  return 4;
}

func main() {
  foo();
  print("---");
  var x;
  x = foo();
  print("---");
  print(x);
}
```

*stdin*
```
```

*stdout*
```
foo
---
---
foo
4
```

*stderr*
```
```

### test lazy eval mutation 1

*code*
```go
func main() {
  var a;
  var b;
  a = 10;
  b = a + 1;
  a = a + 10;
  b = b + a;
  print(a);
  print(b);
}
```

*stdin*
```
```

*stdout*
```
20
31
```

*stderr*
```
```

### test lazy eval update 1

*code*
```go
func zero() {
  print("zero");
  return 0;
}

func inc(x) {
  print("inc:", x);
  return x + 1;
}

func main() {
  var a;
  for (a = 0; zero() + a < 3; a = inc(a)) {
    print("x");
  }
  print("d");
}
```

*stdin*
```
```

*stdout*
```
zero
x
zero
inc:0
x
zero
inc:1
x
zero
inc:2
d
```

*stderr*
```
```

### test bool shortcircuit 1

*code*
```go
func t() {
  print("t");
  return true;
}

func f() {
  print("f");
  return false;
}

func main() {
  print(t() || f());
  print("---");
  print(f() || t());
}
```

*stdin*
```
```

*stdout*
```
t
true
---
f
t
true
```

*stderr*
```
```

## Spec Examples

### Need Semantics Simple Prog

*code*
```go
func main() {
  var result;
  result = f(3) + 10;
  print("done with call!");
  print(result);  /* evaluation of result happens here */
  print("about to print result again");
  print(result);
}

func f(x) {
  print("f is running");
  var y;
  y = 2 * x;
  return y;
}
```

*stdin*
```
```

*stdout*
```
done with call!
f is running
16
about to print result again
16
```

*stderr*
```
```

### Except Handling Simple Prog

*code*
```go
func foo() {
  print("F1");
  raise "except1";
  print("F3");
}

func bar() {
  try {
    print("B1");
    foo();
    print("B2");
  }
  catch "except2" {
    print("B3");
  }
  print("B4");
}

func main() {
  try {
    print("M1");
    bar();
    print("M2");
  }
  catch "except1" {
    print("M3");
  }
  catch "except3" {
    print("M4");
  }
  print("M5");
}
```

*stdin*
```
```

*stdout*
```
M1
B1
F1
M3
M5
```

*stderr*
```
```

### Short Circuiting Example

*code*
```go
func foo() {
  print("foo");
  return true;
}

func bar() {
  print("bar");
  return false;
}

func main() {
  print(foo() || bar() || foo() || bar());
  print("done");
}
```

*stdin*
```
```

*stdout*
```
foo
true
done
```

*stderr*
```
```

### Lazy Eval Demo

> I took some liberties with this one

*code*
```go
func foo() {
  print("eager call");
  return 96;
}

func bar() {
  print("must never be seen");
  raise "foobar";
  return 1 / 0;
}

func pcall() {
  print("x");
  foo();
  inputi("Enter a number");
  var a;
  var n;
  a = bar();
  n = inputi("Enter a number");
  return (print(n) == nil);
}

func main() {
  print(pcall());
}
```

*stdin*
```
5
42
```

*stdout*
```
x
eager call
Enter a number
Enter a number
42
true
```

*stderr*
```
```

### Lazy Eval Example

*code*
```go
func main() {
  var result;
  result = f(3) + 10;
  print("first line");
  if (-result > 5) {
    print(result, " greater than 5");
  }

  var i;
  for (i = 0; i < 10; i = i + 1) {
    print(i);
  }

  result = "except" + "9";
  raise result;
}

func f(x) {
  print("f has been evaluated");
  return x * -8;
}
```

*stdin*
```
```

*stdout*
```
first line
f has been evaluated
-14 greater than 5
0
1
2
3
4
5
6
7
8
9
```

*stderr*
```
ErrorType.FAULT_ERROR
```

### Lazy Error Example

*code*
```go
func faultyFunction() {
  print(undefinedVar); /* Name error occurs here when evaluated */
}

func main() {
  var result;
  result = faultyFunction();
  print("Assigned result!");

  print(result);      /* Error will occur when result is evaluated */
}
```

*stdin*
```
```

*stdout*
```
Assigned result!
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Lazy Raise in Function Example

*code*
```go
func functionThatRaises() {
  raise "some_exception";  /* Exception occurs here when func is called */
  return 0;
}

func main() {
  var result;
  result = functionThatRaises();
  print("Assigned result!");
  /* Exception will occur when result is evaluated */
  print(result, " was what we got!");
}
```

*stdin*
```
```

*stdout*
```
Assigned result!
```

*stderr*
```
ErrorType.FAULT_ERROR
```

### Lazy error example

> this test case helped me fix test_error3 and test_lazy_error7

*code*
```go
func main() {
  var x;
  x = foo(y);
  print("OK");
  print(x);  /* NAME_ERROR due to undefined y is deferred to this line */
}
```

*stdin*
```
```

*stdout*
```
OK
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Eager error example

> this test case helped me fix test_error3 and test_lazy_error7

*code*
```go
func main() {
  x = foo();  /* generates NAME_ERROR immediately since x is undefined */
              /* and x is not part of expression */
  print("OK");
  print(x);
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

### Try Catch Example

*code*
```go
func foo() {
  try {
    raise "z";
  }
  catch "x" {
    print("x");
  }
  catch "y" {
    print("y");
  }
  catch "z" {
    print("z");
    raise "a";
  }
  print("q");
}

func main() {
  try {
    foo();
    print("b");
  }
  catch "a" {
    print("a");
  }
}
```

*stdin*
```
```

*stdout*
```
z
a
```

*stderr*
```
```

### Lazy Error Handling example

*code*
```go
func error_function() {
  raise "error";
  return 0;
}

func main() {
  var x;
  x = error_function() + 10;  /* Exception occurs when x is evaluated */
  print("Before x is evaluated");
  try {
    print(x);  /* Evaluation of x happens here */
  }
  catch "error" {
    print("Caught an error during evaluation of x");
  }
}
```

*stdin*
```
```

*stdout*
```
Before x is evaluated
Caught an error during evaluation of x
```

*stderr*
```
```

### Div0 Demo

*code*
```go
func divide(a, b) {
  return a / b;
}

func main() {
  try {
    var result;
    result = divide(10, 0);  /* evaluation deferred due to laziness */
    print("Result: ", result); /* evaluation occurs here */
  }
  catch "div0" {
    print("Caught division by zero!");
  }
}
```

*stdin*
```
```

*stdout*
```
Caught division by zero!
```

*stderr*
```
```

### Shortcircuit Eval Example

*code*
```go
func t() {
  print("t");
  return true;
}

func f() {
  print("f");
  return false;
}

func main() {
  print(t() && f());
  print("---");
  print(f() && t());
}
```

*stdin*
```
```

*stdout*
```
t
f
false
---
f
false
```

*stderr*
```
```
