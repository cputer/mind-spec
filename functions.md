# Functions

Functions are the primary unit of code organization in MIND.

## Syntax
Functions are declared using the `fn` keyword.
```rust
fn add(a: i32, b: i32) -> i32 {
    return a + b;
}
```

## Implicit Returns
If the last expression in a block has no semicolon, it is returned.
```rust
fn square(x: i32) -> i32 {
    x * x
}
```
