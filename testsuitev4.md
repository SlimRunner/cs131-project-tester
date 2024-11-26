# Unit Tests V4

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
