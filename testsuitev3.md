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

### Nil Return Attempt on Primitive

*code*
```go
func main() : void {
  var a: string;
  a = five();
  print("should not print");
}

func five(): string {
  return nil;
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

### Type Coercion With Operators

*code*
```go
func main(): void {
  direct_print();
  assign_var();
  print_rets();
  return;
}

func direct_print(): void {
  print(-0);
  print(-1);
  print(!1);
  print(!0);
  print(!!-1);
  print(!!false);
  print(!false);
  print(!!true);
  print(!true);
}

func assign_var() : void {
  var i: int;
  i = 6;
  var b: bool;
  b = i;
  i = 0;
  print(b);
  b = -2;
  print(b);
  b = 1 / 2;
  print(b);
}

func print_rets() : void {
  print(ret_bool(4));
  print(ret_bool(0));
  print(ret_bool(-20));
  print(impl_ret());
  print(!impl_ret());
}

func ret_bool(a: int) : bool {
  return a;
}

func impl_ret() : bool {
  var a: int;
}

func bool_expr() : bool {
  var a: int;
}
```

*stdin*
```
```

*stdout*
```
0
-1
false
true
true
false
true
true
false
true
true
false
true
false
true
false
true
```

*stderr*
```
```

### Int-Boolean If-For Condition

*code*
```go
func main() : void {
  var vd: bool;
  vd = false;
  if (inputs() == "I'm in") {
    var i: int;
    for (i = 0; i - 10; i = i + 1) {
      var x: int;
      x = i * i - 7 * i + 10;
      if (!x) {
        vd = x;
        print("is zero:    ", i, " -> ", x);
      } else {
        if (x < 0) {
          print("below zero: ", i, " -> ", x);
        } else {
          print("above zero: ", i, " -> ", x);
        }
      }
    }
  }
}
```

*stdin*
```
I'm in
```

*stdout*
```
above zero: 0 -> 10
above zero: 1 -> 4
is zero:    2 -> 0
below zero: 3 -> -2
below zero: 4 -> -2
is zero:    5 -> 0
above zero: 6 -> 4
above zero: 7 -> 10
above zero: 8 -> 18
above zero: 9 -> 28
```

*stderr*
```
```

### Tagged nil Validity

*code*
```go
struct A {x: int;}
struct B {x: int;}

func main(): void {
  var a: A;
  var b: B;
  a = getAnil();
  b = getBnil();
  print(a);
  print(b);
  print("fine so far");
  getB();
  return;
}

func getA() : A {
  var b: B;
  b = nil;
  return b;
}

func getB() : B {
  var a: A;
  a = nil;
  return a;
}

func getAnil() : A {
  return nil;
}

func getBnil() : B {
  return nil;
}
```

*stdin*
```
```

*stdout*
```
nil
nil
fine so far
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

### Primitives Have no Members

*code*
```go
func main() : void {
  var a : int;
  print(a.b);
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

### Non-Existent Member in Struct

*code*
```go
struct A {
  a:int;
}

func main() : void {
  var a : A;
  print(a.b);
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

### Nil Validity with Primitives

*code*
```go
func incorrect() : int{
  var x : int;
}
func main() : void{
  print("hi");
  incorrect();
  var x : int;
  x = nil;
  print(x);
}
```

*stdin*
```
```

*stdout*
```
hi
```

*stderr*
```
ErrorType.TYPE_ERROR
```

## Structs

### Attempt to Print Struct

*code*
```go
struct A {x: bool;}

func main() : void {
  var a: A;
  print(a);
  /*
  this is undefined behavior
  a = new A;
  print(a);
  */
}
```

*stdin*
```
```

*stdout*
```
nil
```

*stderr*
```
```

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
false
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
  print(nil != foo);
  foo = new woo;
  var bar: foo;
  bar = new foo;
  print(bar.bar == nil);
  print(nil == bar.bar);
  bar.bar = foo;
  bar.bar.main = 13;
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
false
true
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

### Linked List

*code*
```go
struct node {
  value: int;
  next: node;
}

func main(): void {
  var root: node;
  var here: node;
  root = new node;
  here = root;
  root.value = 21;
  var i: int;
  for (i = 20; i; i = i - 1) {
    here = insert_node(here, i);
  }

  for (here = root; here != nil; here = here.next) {
    print(here.value);
  }
  return;
}

func insert_node(nd: node, val: int): node {
  var new_nd: node;
  new_nd = new node;
  new_nd.value = val;
  nd.next = new_nd;
  return new_nd;
}
```

*stdin*
```
```

*stdout*
```
21
20
19
18
17
16
15
14
13
12
11
10
9
8
7
6
5
4
3
2
1
```

*stderr*
```
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

### Struct Comparison

*code*
```go
struct A {a:int;}
struct B {b:int;}

func main() : void {
  var a1: A;
  var a2: A;
  print(a1 != a2);
  a1 = new A;
  print(a1 != a2);
  a2 = a1;
  a1.a = 42;
  print(a1 == a2);
	print(a2.a);
}
```

*stdin*
```
```

*stdout*
```
false
true
true
42
```

*stderr*
```
```

### Structs by Object Reference Complex

*code*
```go
struct ErrObj {
  a: string;
}

struct Msg {
  a: string;
  b: int;
  c: ErrObj;
}

func main(): void {
  var m: Msg;
  m = new Msg;
  var o: ErrObj;
  print(o);
  o = new ErrObj;
  o.a = "new obj";
  print(o.a);
  print(m.c);
  m.c = new ErrObj;
  print(m.c.a);
  m.c.a = "overriden string";
  print(m.c.a);
  print(o.a);
  return;
}

func foo(): Msg {
  return;
}
```

*stdin*
```
```

*stdout*
```
nil
new obj
nil

overriden string
new obj
```

*stderr*
```
```

### Invalid New Type

*code*
```go
func main(): void {
  var foo: int;
  foo = new A;
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

### test nil to struct func

*code*
```go
struct p {
  x:int;
}

func foop(s: p): void {
  print(s == nil);
}

func main(): void {
  var x: p;
  foop(x);
  foop(nil);
}
```

*stdin*
```
```

*stdout*
```
true
true
```

*stderr*
```
```

### Nil Validity in Struct

*code*
```go
struct circle {
  r: int;
}

struct square {
  s: int;
}


func main(): void {
  var c: circle;
  var s: square;

  print(c == s);

  s = new square;
  print(c == s);
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

### Invalid Paramter with Structs

*code*
```go
struct animal {
    name : string;
    noise : string;
    color : string;
    extinct : bool;
    ears: int;
}
struct person {
  name: string;
  height: int;
}
func main() : void {
   var pig : animal;
   var p : person;
   var noise : string;
   noise = make_pig(p, "oink");
   print(noise);
}
func make_pig(a : animal, noise : string) : string{
  if (a == nil){
    print("making a pig");
    a = new animal;
  }
  a.noise = noise;
  return a.noise;
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

## Spec Tests

### Default Return Values

*code*
```go
func main() : void {
  print(foo());
  print(bar());
}

func foo() : int {
  return; /* returns 0 */
}

func bar() : bool {
  print("bar");
}  /* returns false*/
```

*stdin*
```
```

*stdout*
```
0
bar
false
```

*stderr*
```
```

### Coercion

*code*
```go
func main() : void {
  print(5 || false);
  var a:int;
  a = 1;
  if (a) {
    print("if works on integers now!");
  }
  foo(a-1);
}

func foo(b : bool) : void {
  print(b);
}
```

*stdin*
```
```

*stdout*
```
true
if works on integers now!
false
```

*stderr*
```
```

### Structures

*code*
```go
struct Person {
  name: string;
  age: int;
  student: bool;
}

func main() : void {
  var p: Person;
  p = new Person;
  p.name = "Carey";
  p.age = 21;
  p.student = false;
  foo(p);
}

func foo(p : Person) : void {
  print(p.name, " is ", p.age, " years old.");
}
```

*stdin*
```
```

*stdout*
```
Carey is 21 years old.
```

*stderr*
```
```

### Function Definitions

*code*
```go
func foo(a:int, b:string, c:int, d:bool) : int {
  print(b, d);
  return a + c;
}

func talk_to(name:string): void {
  if (name == "Carey") {
     print("Go away!");
     return;  /* using return is OK w/void, just don't specify a value */
  }
  print("Greetings");
}

func main() : void {
  print(foo(10, "blah", 20, false));
  talk_to("Bonnie");
}
```

*stdin*
```
```

*stdout*
```
blahfalse
30
Greetings
```

*stderr*
```
```

### User Defined Structs (Stress Test)

*code*
```go
struct cat {
  name: string;
  scratches: bool;
}

struct person {
  name: string;
  age: int;
  address: string;
  kitty: cat;
}

struct node {
  value: int;
  next: node;    /* this works since node is defined above! */
}

func main(): void {
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
```

### User Defined Structs (Dog Flea)

*code*
```go
struct flea {
  age: int;
  infected : bool;
}

struct dog {
  name: string;
  vaccinated: bool;
  companion: flea;
}

func main() : void {
  var d: dog;
  d = new dog;   /* sets d object reference to point to a dog structure */

  print(d.vaccinated); /* prints false - default bool value */
  print(d.companion); /* prints nil - default struct object reference */

  /* we may now set d's fields */
  d.name = "Koda";
  d.vaccinated = true;
  d.companion = new flea;
  d.companion.age = 3;
}
```

*stdin*
```
```

*stdout*
```
false
nil
```

*stderr*
```
```

### Parameter Passing

*code*
```go
struct person {
  name: string;
  age: int;
}

func foo(a:int, b: person) : void {
  a = 10;
  b.age = b.age + 1;  /* changes p.age from 18 to 19 */

  b = new person;  /* this changes local b variable, not p var below */
  b.age = 100;     /* this does NOT change the p.age field below */
}

func main() : void {
  var x: int;
  x = 5;
  var p:person;
  p = new person;
  p.age = 18;
  foo(x, p);
  print(x);      /* prints 5, since x is passed by value */
  print(p.age);  /* prints 19, since p is passed by object reference */
}
```

*stdin*
```
```

*stdout*
```
5
19
```

*stderr*
```
```

### Return Statement

*code*
```go
struct dog {
  bark: int;
  bite: int;
}

func bar() : int {
  return;  /* no return value specified - returns 0 */
}

func bletch() : bool {
  print("hi");
  /* no explicit return; bletch must return default bool of false */
}

func boing() : dog {
  return;  /* returns nil */
}

func main() : void {
   var val: int;
   val = bar();
   print(val);  /* prints 0 */
   print(bletch()); /* prints false */
   print(boing()); /* prints nil */
}
```

*stdin*
```
```

*stdout*
```
0
hi
false
nil
```

*stderr*
```
```

### Return a UDS

*code*
```go
struct dog {
 bark: int;
 bite: int;
}

func foo(d: dog) : dog {  /* d holds the same object reference that the koda variable holds */
  d.bark = 10;
  return d;  		/* this returns the same object reference that the koda variable holds */
}

 func main() : void {
  var koda: dog;
  var kippy: dog;
  koda = new dog;
  kippy = foo(koda);	/* kippy holds the same object reference as koda */
  kippy.bite = 20;
  print(koda.bark, " ", koda.bite); /* prints 10 20 */
}
```

*stdin*
```
```

*stdout*
```
10 20
```

*stderr*
```
```

### Print Prints Nils

*code*
```go
struct dog {
  name: string;
  vaccinated: bool;
}

func main() : void {
  var d: dog;    /* d is an object reference whose value is nil */

  print (d);  /* prints nil, because d was initialized to nil */
  print (nil);
  d = new dog;
  d = nil;
  print(d);
}
```

*stdin*
```
```

*stdout*
```
nil
nil
nil
```

*stderr*
```
```

### Print Has Void Return Type

*code*
```go
func main() : void {
  print(1 + print());
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
