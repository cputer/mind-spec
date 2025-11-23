# Tensor Library

The `std::tensor` module provides the core primitives for N-dimensional array construction and linear algebra.

## Constructors

### `zeros`
```
fn zeros(shape: [i64]) -> Tensor
```
Allocates a new contiguous tensor of the specified shape, initialized with 0.0.

### `ones`
```
fn ones(shape: [i64]) -> Tensor
```
Allocates a new contiguous tensor initialized with 1.0.

## Operations

### `matmul`
```
fn matmul(a: Tensor, b: Tensor) -> Tensor
```
Performs matrix multiplication. Supports broadcasting.
**Complexity:** O(M * N * K).
