# Math Library

The `std::math` module provides essential mathematical functions and constants.

## Constants
- **PI**: `3.14159...`
- **E**: `2.71828...`

## Functions

### `sqrt`
```
fn sqrt(x: f64) -> Result<f64, DomainError>
```
Computes the non-negative square root. Returns error if x < 0.

### `tanh`
```
fn tanh(x: f32) -> f32
```
Computes the hyperbolic tangent (activation function).
