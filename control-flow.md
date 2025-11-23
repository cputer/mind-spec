# Control Flow

## If Expressions
In MIND, `if` is an expression that returns a value.
```rust
let y = if x > 0 { 1 } else { -1 };
```

## Loops
- **loop**: Infinite loop.
- **while**: Condition-based loop.
- **for**: Iterator-based loop.

## Match
Pattern matching is exhaustive.
```rust
match value {
    0 => print!("Zero"),
    _ => print!("Non-zero"),
}
```
