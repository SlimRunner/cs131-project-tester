# Unit Tests V4

## Exceptions

### Uncaught Division by Zero

*code*
```go
func main() {
  print(1 / 0);
  print("must not print");
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
ErrorType.FAULT_ERROR
```

### Lazy Uncaught Division by Zero

*code*
```go
func foo(a) {
  return a / 0;
}

func main() {
  var x;
  x = 123;
  print(x);
  x = foo(x);
  print("omae wa...");
  print(x);
}
```

*stdin*
```
```

*stdout*
```
123
omae wa...
```

*stderr*
```
ErrorType.FAULT_ERROR
```

### Deeply Nested Division by Zero

*code*
```go
func mult3(n) {
  print(1000 / (n + 868));
  var res;
  res = div5shift(n * 3);
  return res;
}

func div5shift(n) {
  if (n == -1161) {
    print(n);
  } else {
    print(1000 / (n + 400));
  }
  var res;
  res = mult3(n / 5 - 400);
  return res;
}

func main() {
  var x;
  x = mult3(23);
  print("no error yet");
  print(x);
  print("must not print");
}
```

*stdin*
```
```

*stdout*
```
no error yet
1
2
2
-1161
4
-1
11
-1
```

*stderr*
```
ErrorType.FAULT_ERROR
```

### Uncaught Raised Error

*code*
```go
func main() {
  raise "foobar";
  print("must not print");
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
ErrorType.FAULT_ERROR
```

### Lazy Uncaught Raised Error

*code*
```go
func foo(a) {
  raise a;
  print("must not print");
  return "404: return value not found";
}

func main() {
  var x;
  x = "lazy error";
  print(x);
  x = foo(x);
  print("omae wa...");
  print(x);
}
```

*stdin*
```
```

*stdout*
```
lazy error
omae wa...
```

*stderr*
```
ErrorType.FAULT_ERROR
```

### Deeply Nested Lazy Error

*code*
```go
func seppuku(err) {
  raise err;
}

func bar(s, n) {
  var res;
  print("bar -> ", s, ":", n);
  if (n < 20) {
    res = "y" + foo("b", n - 1) + s;
  } else {
    res = "|";
  }
  return res;
}

func foo(s, n) {
  var res;
  print("foo -> ", s, ":", n);
  if (n < 7) {
    res = s + bar("x", n * 2) + "a";
  } else {
    res = "&";
  }
  if (n == 3) {
    seppuku(res);
  }
  return res;
}

func main() {
  var x;
  x = foo("-", 2);
  print(x);
  print("this should not print");
  print(x);
}
```

*stdin*
```
```

*stdout*
```
foo -> -:2
bar -> x:4
foo -> b:3
bar -> x:6
foo -> b:5
bar -> x:10
foo -> b:9
```

*stderr*
```
ErrorType.FAULT_ERROR
```

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

### Try Catch Shadowing

*code*
```go
func main() {
  var a;
  try {
    var a;
    print("a has been shadowed");
    var a;
  }
  catch "miss" {
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
a has been shadowed
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Try Catch Shadowing Validity

*code*
```go
func main() {
  var a;
  a = 45;
  try {
    print(a);
    a = 12;
    var a;
    a = "abc";
    print("a has been shadowed and modified");
    print(a);
    raise "raid shadow legends";
  }
  catch "raid shadow legends" {
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
45
a has been shadowed and modified
abc
12
12
```

*stderr*
```
```

### Try Catch Fallthrough

*code*
```go
func main() {
  try {
    try {
      try {
        if (true) {
          var a;
          for (a = ""; a != "00000"; a = a + "0") {
            print(a);
            if (a == "000") {
              raise "inception";
              print("if did not unwind");
            }
          }
          print("for and/or if did not unwind");
        }
        print("try did not catch");
      }
      catch "noop" {
        print("noop is not meant to match inception");
      }
    }
    catch "noop" {
      print("noop is not meant to match inception");
    }
  }
  catch "inception" {
    print("inception was caught");
  }
  print("normal exit");
}
```

*stdin*
```
```

*stdout*
```

0
00
000
inception was caught
normal exit
```

*stderr*
```
```

### Try Catch Scope Unwinding

*code*
```go
func main() {
  var a;
  a = 45;
  print(a);
  try {
    var a;
    a = "first try";
    print(a);
    try {
      var a;
      a = "second try";
      print(a);
      try {
        var a;
        a = "third try";
        print(a);
        if (true) {
          var a;
          for (a = ""; a != "00000"; a = a + "0") {
            print(a);
            if (a == "000") {
              raise "E1";
            }
            var a;
            a = "for body scope";
            print(a);
          }
        }
      }
      catch "E1" {
        print(a);
        raise "E2";
      }
    }
    catch "E2" {
      print(a);
      raise "E3";
    }
  }
  catch "E3" {
    print(a);
    var a;
    a = nil;
    print(a != nil);
  }
  print(a);
}
```

*stdin*
```
```

*stdout*
```
45
first try
second try
third try

for body scope
0
for body scope
00
for body scope
000
second try
first try
45
false
45
```

*stderr*
```
```

### Try Catch Error Unwinding

*code*
```go
func main() {
  try {
    try {
      try {
        if (true) {
          var a;
          for (a = ""; a != "00000"; a = a + "0") {
            print(a);
            if (a == "000") {
              raise "E1";
              print("if failed to unwind");
            }
          }
          print("for failed to propagate error");
        }
        print("if failed to propagate error");
      }
      catch "E1" {
        raise "E2";
        print("catch E1 failed to unwind");
      }
    }
    catch "E2" {
      raise "E3";
      print("catch E2 failed to unwind");
    }
  }
  catch "E3" {
    print("E1 E2 and E3 were caught");
  }
}
```

*stdin*
```
```

*stdout*
```

0
00
000
E1 E2 and E3 were caught
```

*stderr*
```
```

### Ill formed raise statement nil

*code*
```go
func main() {
  print("entry");
  raise nil;
  print("exit");
}
```

*stdin*
```
```

*stdout*
```
entry
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Ill formed raise statement int

*code*
```go
func main() {
  print("entry");
  raise 5;
  print("exit");
}
```

*stdin*
```
```

*stdout*
```
entry
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Ill formed raise statement bool

*code*
```go
func main() {
  print("entry");
  raise true;
  print("exit");
}
```

*stdin*
```
```

*stdout*
```
entry
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Bad variable value for raise (lazy)

*code*
```go
func foo() {
  print("lazy int");
  return 24;
}

func main() {
  var x;
  x = foo();
  print("entry");
  raise x;
  print("exit");
}
```

*stdin*
```
```

*stdout*
```
entry
lazy int
```

*stderr*
```
ErrorType.TYPE_ERROR
```

### Except within expression

*code*
```go
func f1() {
  print("f1");
  return 1;
}

func f2() {
  print("f2");
  return 2;
}

func f3() {
  print("f3");
  return 3;
}

func fe() {
  print("fe");
  raise "ferr";
  print("must not print");
  return nil;
}

func main() {
  var x;
  x = f1() + f2() + f3() + f2() + f1() + f2() + f3() + fe() + f2() + f3() + f4() + f5() + f6();
  print("no error yet");
  try {
    print("inside try");
    print(x);
    print("post try error. must not print");
  }
  catch "ferr" {
    x = f1() + f3() + f3() + f2() + f2() + f3()+ f1();
    print(x);
    print("ferr was caught");
  }
  print(x + 3);
  print("exit");
}
```

*stdin*
```
```

*stdout*
```
no error yet
inside try
f1
f2
f3
f2
f1
f2
f3
fe
f1
f3
f3
f2
f2
f3
f1
15
ferr was caught
18
exit
```

*stderr*
```
```

### Indirect Except Catch

*code*
```go
func foo() {
  print("foo");
  raise "foo";
  print("must not print");
  return 1;
}

func main() {
  try {
    print("before error");
    foo();
    print("after error");
  }
  catch "foo" {
    print("error from foo");
  }
  print("normal exit");
}
```

*stdin*
```
```

*stdout*
```
before error
foo
error from foo
normal exit
```

*stderr*
```
```

### Except in if-condition

*code*
```go
func foo() {
  print("foo ran");
  return 0 / 1;
}

func main() {
  try {
    if (1 / 0 == foo()) {
      print("whoops");
    }
  }
  catch "div0" {
    print("div0 in if-condition");
    raise "div0";
  }
  print("must not print");
}
```

*stdin*
```
```

*stdout*
```
div0 in if-condition
```

*stderr*
```
ErrorType.FAULT_ERROR
```

### Except in for-header

> this exception depends heavily on correct scoping so make sure you
> pass that before checking this one

*code*
```go
func ferr() {
  raise "ferr";
}

func div0() {
  print(0 / 0);
}

func main() {
  var i;
  i = 5;

  print("test assignment");
  try {
    var i;
    for (i = ferr(); i < 5; i = i + 1) {
      print("noop");
    }
  }
  catch "div0" {
    print("must not print");
    raise "div0";
  }
  catch "ferr" {
    print("ferr: i -> ", i);
    i = i + 5;
  }

  print("test condition");
  try {
    var i;
    for (i = 0; ferr(); i = i + 1) {
      print("noop");
    }
  }
  catch "div0" {
    print("must not print");
    raise "div0";
  }
  catch "ferr" {
    print("ferr: i -> ", i);
    i = i + 5;
  }

  print("test update");
  try {
    var i;
    for (i = 0; i < 5; i = ferr()) {
      print("noop");
    }
  }
  catch "div0" {
    print("must not print");
    raise "div0";
  }
  catch "ferr" {
    print("ferr: i -> ", i);
    i = i + 5;
  }

  print("test body");
  try {
    var i;
    for (i = 0; i < 5; i = i + 1) {
      div0();
      print("noop");
    }
  }
  catch "div0" {
    print("caught last div0");
  }
  catch "ferr" {
    print("ferr: i -> ", i);
    i = i + 5;
    raise "ferr";
  }

  print("final i = ", i);
}
```

*stdin*
```
```

*stdout*
```
test assignment
ferr: i -> 5
test condition
ferr: i -> 10
test update
noop
ferr: i -> 15
test body
caught last div0
final i = 20
```

*stderr*
```
```

### Test nested try-catch

*code*
```go
func ferr() {
  raise "ferr";
}

func main() {
  try {
    print(5, "asd", nil == nil, false, ferr());
  }
  catch "ferr" {
    print("first catch");
    try {
      inputs(ferr());
    }
    catch "ferr" {
      print("second catch");
      try {
        inputi(ferr());
      }
      catch "ferr" {
        print("last catch");
      }
    }
  }
}
```

*stdin*
```
```

*stdout*
```
first catch
second catch
last catch
```

*stderr*
```
```

### Name Error always Falls through

*code*
```go
func main() {
  try {
    var a;
    var a;
  }
  catch "no match" {
    print("must not print");
  }
  print("must not print");
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

### Type Error always Falls through

*code*
```go
func main() {
  try {
    var a;
    a = 1 + "1";
    print(a);
  }
  catch "no match" {
    print("must not print");
  }
  print("must not print");
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

### Empty String is a valid catch

*code*
```go
func main() {
  try {
    try {
      raise "";
    }
    catch "name" {
      return;
    }
  }
  catch "no match" {
    print("must not print");
  }
  catch "" {
    print("hello");
  }
  print("world");
}
```

*stdin*
```
```

*stdout*
```
hello
world
```

*stderr*
```
```

### Return inside Try Catch 1

*code*
```go
func catch_ret() {
  print("catch_ret entry");
  try {
    print("in try");
    raise "err";
  }
  catch "err" {
    return "ret from catch";
    print("after return in catch (unreachable)");
  }
  print("catch_ret normal exit");
}

func main() {
  print(catch_ret());
}
```

*stdin*
```
```

*stdout*
```
catch_ret entry
in try
ret from catch
```

*stderr*
```
```

### Return inside Try Catch 2

*code*
```go
func try_ret(a) {
  print("t_ret");
  try {
    return a * 2;
  }
  catch "A" {
    raise "B";
  }
  print("must not print");
}

func catch_ret(a) {
  print("c_ret");
  try {
    raise "A";
  }
  catch "A" {
    return a + "_is_bestagon";
    raise "B";
  }
  print("must not print");
}

func main() {
  var x;
  var y;
  x = try_ret(3);
  y = catch_ret("_hexagon");
  print("---");
  print(x, y);
  print(try_ret(3), catch_ret("_hexagon"));
  print(x, y);
}
```

*stdin*
```
```

*stdout*
```
---
t_ret
c_ret
6_hexagon_is_bestagon
t_ret
c_ret
6_hexagon_is_bestagon
6_hexagon_is_bestagon
```

*stderr*
```
```

### Eager Try-Catch FSM

*code*
```go
func main() {
  try {
    /* start the FSM at "state1" */
    fsm_eager("state1");
  }
  catch "lazy_final_state" {
    print("this should not be caught");
  }
  catch "final_state" {
    print("Caught final_state in main");
  }

  print("normal exit");
}

func fsm_eager(state) {
  try {
    print("In ", state);
    raise state;
  }
  catch "state1" {
    print("Caught state1, transitioning...");
    fsm_eager("state2");
  }
  catch "state2" {
    print("Caught state2, transitioning...");
    fsm_eager("state3");
  }
  catch "state3" {
    print("Caught state3, transitioning...");
    fsm_eager("final_state");
  }
  print("this point should not be reached");
}
```

*stdin*
```
```

*stdout*
```
In state1
Caught state1, transitioning...
In state2
Caught state2, transitioning...
In state3
Caught state3, transitioning...
In final_state
Caught final_state in main
normal exit
```

*stderr*
```
```

### Lazy Try-Catch FSM

*code*
```go
func main() {
  var fsmr;
  try {
    /* start the FSM at "state1" */
    fsmr = fsm_lazy("state1");
  }
  catch "lazy_final_state" {
    print("this should not be caught");
  }
  catch "final_state" {
    print("Caught final_state in main");
  }

  print("normal exit");
}

func fsm_lazy(state) {
  try {
    print("In ", state);
    raise state;
  }
  catch "state1" {
    print("Caught state1, transitioning...");
    return fsm_lazy("state2");
  }
  catch "state2" {
    print("Caught state2, transitioning...");
    return fsm_lazy("state3");
  }
  catch "state3" {
    print("Caught state3, transitioning...");
    return fsm_lazy("final_state");
  }
  print("this point should not be reached");
}
```

*stdin*
```
```

*stdout*
```
normal exit
```

*stderr*
```
```

### Challenge Lazy Error Early Return and Named Errors

*code*
```go
func main() {
  var cz; cz = catchzy();
  print("no error yet");
  print(cz);
}

func catchzy() {
  var r1;
  var r2;
  var r4;

  r4 = lazy_fn(4, "");
  r2 = lazy_fn(2, "");
  r1 = lazy_fn(1, "");
  try {
    print(r2);
  }
  catch "AB" {
    try {
      print(r1);
    }
    catch "A" {
      try {
        return print(r4);
      }
      catch "ABCD" {
        print("unreachable");
      }
      print("unreachable");
    }
    print("unreachable");
  }

  print("unreachable");
}

func lazy_fn(n, s) {
  if (n == 0) {
    raise s;
    print("unreachable");
  }
  print(n);
  return lazy_fn(n - 1, letter(n) + s);
  print("unreachable");
}

func letter(n) {
  if (n == 0) { return "0"; }
  if (n == 1) { return "A"; }
  if (n == 2) { return "B"; }
  if (n == 3) { return "C"; }
  if (n == 4) { return "D"; }
  if (n == 5) { return "E"; }
  if (n == 6) { return "F"; }
  return X;
}
```

*stdin*
```
```

*stdout*
```
no error yet
2
1
1
4
3
2
1
```

*stderr*
```
ErrorType.FAULT_ERROR
```

### Challenge Branching Exceptions

*code*
```go
func main() {
  var i;
  try {
    for (i = ""; true; i = i) {
      try {
        try {
          print("A1");
          raise "A1";
          print("raise A1 failed");
        }
        catch "A1" {
          try {
            print("B1");
            raise "B1";
            print("raise B1 failed");
          }
          catch "B1" {
            try {
              try {
                print("D1");
                raise "D1";
                print("raise D1 failed");
              }
              catch "D1" {
                print("C1");
                raise "C1";
                print("raise C1 failed");
              }
            }
            catch "C1" {
              if (i == "") {
                print("root1");
                raise "root1";
                print("raise root1 failed");
              } else {
                print("root2");
                raise "root2";
                print("raise root2 failed");
              }
            }
          }
        }
      }
      catch "root1" {
        print("'",i,"'");
        i = "not empty";
      }
      catch "root2" {
        print("err");
        raise "err";
        print("raise err failed");
      }
    }
  }
  catch "err" {
    print(i);
  }
}
```

*stdin*
```
```

*stdout*
```
A1
B1
D1
C1
root1
''
A1
B1
D1
C1
root2
err
not empty
```

*stderr*
```
```

### Short Circuits Avoid Errors

*code*
```go
func dyn_err(b, e) {
  print(b, ":", e);
  if (b) {
    raise e;
  }
  return e;
}

func main() {
  var x1; var x2; var x3; var x4;
  var x5; var x6; var x7; var x8;
  x1 = (dyn_err(false, true) || dyn_err(false, "avoid1")) && (dyn_err(false, false) && dyn_err(false, "avoid2"));
  x2 = (dyn_err(false, true) || 0) && (dyn_err(false, false) && 0);
  x3 = (dyn_err(false, true) || "0") && (dyn_err(false, false) && "0");
  x4 = (dyn_err(false, true) || nil) && (dyn_err(false, false) && nil);
  x5 = (dyn_err(false, true) || no_var) && (dyn_err(false, false) && no_var);
  x6 = (dyn_err(false, true) || no_func()) && (dyn_err(false, false) && no_func());
  x7 = (dyn_err(false, true) || inputi(1,2)) && (dyn_err(false, false) && inputi(1,2));
  x8 = (dyn_err(false, true) || inputs(1,2)) && (dyn_err(false, false) && inputs(1,2));
  print(x1); print(x2); print(x3); print(x4);
  print(x5); print(x6); print(x7); print(x8);
}
```

*stdin*
```
```

*stdout*
```
false:true
false:false
false
false:true
false:false
false
false:true
false:false
false
false:true
false:false
false
false:true
false:false
false
false:true
false:false
false
false:true
false:false
false
false:true
false:false
false
```

*stderr*
```
```

### Raise to Return to Catch

*code*
```go
func lzy_err(a, b) {
  print("lzy_err entry");
  print(a);
  try {
    print(b);
    print("after return (unreachable)");
  }
  catch "lazy ret" {
    print("lazy ret caught");
    raise "other err";
  }
  print("lzy_err normal exit");
}

func exp_raise(a) {
  raise a;
}

func call_proxy() {
  print("call_proxy entry");
  return lzy_err(42, exp_raise("lazy ret"));
  print("call_proxy normal exit");
}

func main() {
  print("main entry");
  try {
    print(call_proxy());
    print("after return (unreachable)");
  }
  catch "other err" {
    print("other err caught");
  }
  print("main normal exit");
}
```

*stdin*
```
```

*stdout*
```
main entry
call_proxy entry
lzy_err entry
42
lazy ret caught
other err caught
main normal exit
```

*stderr*
```
```

### Lazy Discarded Exeptions lazy_except2

*code*
```go
func main() {
  try {
    /* start the FSM at "state1" */
    fsm_lazy("state1");
  }
  catch "lazy_final_state" {
    print("this should not be caught");
  }
  catch "final_state" {
    print("Caught final_state in main");
  }

  print("normal exit");
}

func fsm_lazy(state) {
  try {
    print("In ", state);
    raise state;
  }
  catch "state1" {
    print("Caught state1, transitioning...");
    return fsm_lazy("state2");
  }
  catch "state2" {
    print("Caught state2, transitioning...");
    return fsm_lazy("state3");
  }
  catch "state3" {
    print("Caught state3, transitioning...");
    return fsm_lazy("final_state");
  }
  print("this point should not be reached");
}
```

*stdin*
```
```

*stdout*
```
In state1
Caught state1, transitioning...
normal exit
```

*stderr*
```
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

### nil comparison

*code*
```go
func foo() {
  var x;
}

func bar() {
  return;
}

func baz() {
  return nil;
}

func main() {
  var a;
  var b;
  var c;
  c = foo();
  print(a == b);
  print(a == 0);
  print(a == false);
  print(nil == b);
  print(nil == 0);
  print(nil == false);
  print(c == b);
  print(c == 0);
  print(c == false);
  print(foo() != bar());
  print(bar() != baz());
  print(baz() != foo());
  c = print(baz() != foo());
  print(c == nil);
}
```

*stdin*
```
```

*stdout*
```
true
false
false
true
false
false
true
false
false
false
false
false
false
true
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

### If-Return Termination

*code*
```go
func main() {
  if (true) {
    print("entry");
    return;
    print("if-statement failed to stop on return");
  }
  print("if-statement failed to exit parent function");
}
```

*stdin*
```
```

*stdout*
```
entry
```

*stderr*
```
```

### For-Return Termination

*code*
```go
func main() {
  var i;
  for (i = 0; i < 5; i = i + 1) {
    print("entry");
    return;
    print("for-loop failed to stop on return");
  }
  print("for-loop failed to exit parent function");
}
```

*stdin*
```
```

*stdout*
```
entry
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
  print(print("-") == a);
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
-
42
true
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

### Deeply Nested Lazy Evaluation and Cache

*code*
```go
func bar(s, n) {
  var res;
  print("bar -> ", s, ":", n);
  if (n < 20) {
    res = "y" + foo("b", n - 1) + s;
  } else {
    res = "|";
  }
  return res;
}

func foo(s, n) {
  var res;
  print("foo -> ", s, ":", n);
  if (n < 7) {
    res = s + bar("x", n * 2) + "a";
  } else {
    res = "&";
  }
  return res;
}

func main() {
  var x;
  var y;
  x = foo("-", 2);
  y = bar("-", 3);
  print(x);
  print(y);
  print(x);
  print(y);
}
```

*stdin*
```
```

*stdout*
```
foo -> -:2
bar -> x:4
foo -> b:3
bar -> x:6
foo -> b:5
bar -> x:10
foo -> b:9
-ybyby&xaxaxa
bar -> -:3
foo -> b:2
bar -> x:4
foo -> b:3
bar -> x:6
foo -> b:5
bar -> x:10
foo -> b:9
ybybyby&xaxaxa-
-ybyby&xaxaxa
ybybyby&xaxaxa-
```

*stderr*
```
```

### Function Order of Eval

*code*
```go
func foo() {
  print("first");
  return 1;
}

func bar() {
  print("second");
  return 2;
}

func baz() {
  print("third");
  return 3;
}

func main() {
  var x;
  x = foo() + bar() * baz();
  print(x);
}
```

*stdin*
```
```

*stdout*
```
first
second
third
7
```

*stderr*
```
```

### Lazy as non-eval param

*code*
```go
func foo() {
  print("first");
  return 1;
}

func bar() {
  print("second");
  return 2;
}

func baz() {
  print("third");
  return 3;
}

func noop(a) {
  return nil;
}

func eval(a) {
  return nil == noop(a);
}

func eval_direct(a) {
  return nil == a;
}

func main() {
  var x;
  x = foo() + bar() * baz();
  print("nothing");
  noop(x);
  print("still nothing");
  noop(x);
  print("still nothing");
  print(eval(x));
  print(eval_direct(x));
}
```

*stdin*
```
```

*stdout*
```
nothing
still nothing
still nothing
true
first
second
third
false
```

*stderr*
```
```

### Lazy Undef Var Error

*code*
```go
func main() {
  var a;
  a = x;
  print("should not crash yet");
  print(x);
}
```

*stdin*
```
```

*stdout*
```
should not crash yet
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Lazy Undef Func Error

*code*
```go
func main() {
  var a;
  a = foo(5);
  print("should not crash yet");
  print(x);
}
```

*stdin*
```
```

*stdout*
```
should not crash yet
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Lazy Undef Func and Vars Error

*code*
```go
func main() {
  var a;
  a = foo(a ,b, c, d, e);
  print("should not crash yet");
  print(x);
}
```

*stdin*
```
```

*stdout*
```
should not crash yet
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Lazy argument correctness

*code*
```go
func foo(a, b, c, d) {
  print(a);
  print(c);
  return "all good";
}

func get_num() {
  print("get num");
  return 5 * 6;
}

func get_str() {
  print("get string");
  return "5 * 6";
}

func get_bool() {
  print("get bool");
  return !false;
}

func get_error1() {
  print("should not get called");
  var a;
  var a;
}

func get_error2() {
  print("should not get called");
  undefinedvar = 5;
}

func raise_error() {
  print("should not get called");
  raise "err";
}

func main() {
  var x;
  var y;
  x = foo(get_num(), get_error2(), get_bool(), does_not_exist());
  y = foo(get_str(), raise_error(), get_num(), get_error1());

  print(y);
  print(x);
}
```

*stdin*
```
```

*stdout*
```
get string
5 * 6
get num
30
all good
get num
30
get bool
true
all good
```

*stderr*
```
```

### Lazy Invalid Call to input

*code*
```go
func main() {
  var a;
  var b;
  print("entry");
  a = inputi(1, 2, 3);
  b = inputs("a", "b", "c");
  print("all good, error was lazy");
}
```

*stdin*
```
123
abc
```

*stdout*
```
entry
all good, error was lazy
```

*stderr*
```
```

### Eager Invalid Call to inputs

*code*
```go
func main() {
  var a;
  print("entry");
  inputs("a", "b", "c");
  print("eager error was not raised");
}
```

*stdin*
```
```

*stdout*
```
entry
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Eager Invalid Call to inputi

*code*
```go
func main() {
  var a;
  print("entry");
  inputi("a", "b", "c");
  print("eager error was not raised");
}
```

*stdin*
```
abc
```

*stdout*
```
entry
```

*stderr*
```
ErrorType.NAME_ERROR
```

### Eager Function Lazy Return

*code*
```go
func eager_call(a, b) {
  print(a);
  return lazy_call(b, "lazy msg");
}

func lazy_call(a, b) {
  print(a, b);
}

func main() {
  eager_call("doit", lazy_call("no show", 6));
  print("normal exit");
  return main();
}
```

*stdin*
```
```

*stdout*
```
doit
normal exit
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

### Valid Parameter Shadow

*code*
```go
func main() {
  var a;
  foo("entered function");
}

func foo(a) {
  print(a);
  var a;
  a = 12;
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
