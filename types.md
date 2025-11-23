# Types & Variables

MIND is a statically typed language with a focus on tensor operations and safety.

## Primitive Types
- **i32 / i64**: Signed integers.
- **f32 / f64**: IEEE 754 floating point numbers.
- **bool**: Boolean (`true` / `false`).
- **str**: UTF-8 string slices.

## Tensor Type
Tensors are the core primitive, defined by a data type and a shape.
```rust
let image: Tensor<f32, [3, 224, 224]>;
```

## Structs
User-defined compound types.
```rust
struct Model {
    layers: i32,
    learning_rate: f32,
}
```
