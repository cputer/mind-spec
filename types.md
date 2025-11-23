# Types & Variables

MIND is statically typed.

## Primitives
- **i32 / i64**: Signed integers.
- **f32 / f64**: IEEE floating point.
- **bool**: True/false.

## Tensors
Tensors are defined by type and shape:
```
let image: Tensor<f32, [3, 224, 224]>;
```
