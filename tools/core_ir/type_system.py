from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

from .core_ir import CoreIR


@dataclass(frozen=True)
class TensorType:
    dtype: str
    shape: tuple[int, ...] = ()

    def __str__(self) -> str:  # pragma: no cover - simple representation
        shape_suffix = f"[{', '.join(map(str, self.shape))}]" if self.shape else "[]"
        return f"tensor<{self.dtype}{shape_suffix}>"

    def is_scalar(self) -> bool:
        return not self.shape


class TypeSystem:
    """Minimal type environment for static validation.

    The prototype models a small subset of the specification: scalar and tensor
    types with shape metadata. It enforces that binary operations use compatible
    dtypes and shapes, and materialises inputs directly into the Core IR module.
    """

    def __init__(self, known_dtypes: Iterable[str] | None = None) -> None:
        self.known_dtypes = set(known_dtypes or {"i32", "i64", "f32", "f64"})
        self.symbols: Dict[str, TensorType] = {}
        self._materialized_symbols: Dict[str, int] = {}

    def ensure_known_dtype(self, dtype: str) -> None:
        if dtype not in self.known_dtypes:
            raise TypeError(f"Unknown dtype '{dtype}'")

    def add_symbol(self, name: str, tensor_type: TensorType) -> None:
        self.ensure_known_dtype(tensor_type.dtype)
        self.symbols[name] = tensor_type

    def resolve_symbol(self, name: str) -> TensorType:
        try:
            return self.symbols[name]
        except KeyError as exc:
            raise TypeError(f"Symbol '{name}' is not declared") from exc

    def materialize_symbol(self, ir: CoreIR, name: str, tensor_type: TensorType) -> int:
        if name not in self._materialized_symbols:
            value_id = ir.declare_input(name, result_type=str(tensor_type))
            self._materialized_symbols[name] = value_id
        return self._materialized_symbols[name]

    def validate_binop(self, op: str, lhs: TensorType, rhs: TensorType) -> TensorType:
        if lhs.dtype != rhs.dtype:
            raise TypeError(f"Type mismatch for {op}: {lhs.dtype} vs {rhs.dtype}")

        if lhs.shape == rhs.shape:
            return lhs

        if lhs.is_scalar():
            return rhs
        if rhs.is_scalar():
            return lhs

        raise TypeError(f"Shape mismatch for {op}: {lhs.shape} vs {rhs.shape}")

    def validate_program(self) -> None:
        for name, tensor_type in self.symbols.items():
            self.ensure_known_dtype(tensor_type.dtype)

