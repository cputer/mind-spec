<!--
MIND Language Specification — Community Edition

Copyright 2025 STARGA Inc.
Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Type System (Normative)

The MIND type system enforces static correctness and enables efficient differentiation. This chapter
formalises type formation, typing judgements, inference constraints, and trait coherence. It aligns
with the reference notes in
[`star-ga/mind/docs/type-system.md`](https://github.com/star-ga/mind/blob/main/docs/type-system.md).

## Type formation

The following forms are part of the core language:

- **Primitive types**: `i32`, `f64`, `bool`, `unit`.
- **Composite types**: tuples `(T1, T2, ...)`, arrays `[T; n]`, and structs defined via `struct`.
- **Function types**: `(T1, ..., Tn) -> U`.
- **Trait objects**: `dyn Trait` for traits marked as object-safe *(specified for full v1.0; not
  yet implemented in the executable subset — see [Traits and generics](#traits-and-generics))*.
- **Differentiable wrappers**: `diff T` identifies values that participate in differentiation (see
  [Automatic differentiation](./autodiff.md)).

Implementations MAY extend the set of primitive types but MUST document the extensions.

## Typing judgements

Typing rules are written using natural deduction. The primary judgement `Γ ⊢ e : T` reads “under
context Γ, expression e has type T”. Implementations MUST reject programs that violate any
applicable rule. Selected core rules include:

- **Variable**: if `x : T ∈ Γ` then `Γ ⊢ x : T`.
- **Let binding**: if `Γ ⊢ e1 : T1` and `Γ, x : T1 ⊢ e2 : T2` then `Γ ⊢ let x = e1 in e2 : T2`.
- **Function abstraction**: if `Γ, x1 : T1, ..., xn : Tn ⊢ e : U` then `Γ ⊢ fn(x1 : T1, ..., xn : Tn) -> U { e } : (T1, ..., Tn) -> U`.

A comprehensive derivation catalogue is maintained in the implementation notes
([informative](https://github.com/star-ga/mind/blob/main/docs/type-system.md)).

## Type inference

Implementations MUST support bidirectional type inference:

- Expressions without annotations are checked by propagating expected types from their context.
- When inference fails, diagnostics MUST include the expression span and the conflicting types.
- Generic functions MUST infer type parameters when sufficient information is available. Otherwise
  the caller MUST provide explicit type arguments.

Inference relies on unification with occurs checks. Implementations SHOULD emit informative error
messages when inference requires additional annotations.

### Struct literal bindings

A literal of a declared struct denotes that struct, including when its local
binding omits an annotation. Integer field initializers such as `0` MUST NOT
turn the aggregate binding into an `i32` scalar. Replacing a mutable binding
with a value of the same struct type MUST NOT produce an integer-narrowing
diagnostic merely because the replacement comes from a function.

The declared field widths govern field values. A genuine implicit `i64` to
`i32` scalar assignment still requires the narrowing diagnostic. A known
struct binding cannot be replaced with a numeric scalar; the implemented
confident-scalar check reports `E2026`. A fresh lexical binding shadows the
previous binding and does not inherit its struct identity.

Implementation status: pending compiler integration. The regression exercises
check/build agreement, full-width values and deterministic shared-library
emission. It does not promote full structural type inference or native-ELF
coverage beyond the independently verified backend subset.

### Core IR integration

The type checker participates directly in Core IR construction:

- **Symbol tables** feed module inputs. Each declared value is materialised as an `Input` instruction
  carrying its resolved tensor type so that the IR verifier can enforce the single-definition rule.
- **Shape validation** rejects tensors with zero or negative extents. Scalars (rank-0) are exempt and
  remain represented with an empty shape.
- **Operation typing** mirrors the IR instruction set. For arithmetic operations the operands MUST
  share a dtype; shape compatibility follows the broadcasting rules in
  [Shapes](./shapes.md#broadcasting). Scalar operands implicitly broadcast to the non-scalar
  operand's shape. Batched `MatMul` operations additionally broadcast leading dimensions and enforce
  that the contracting dimension matches.
- **Verification before emission**: translators are expected to reject programs with unknown dtypes,
  incompatible shapes, or undeclared symbols before emitting IR. This aligns the surface-language
  diagnostics with the invariants described in [Core IR](./ir.md#verification).

## Module-qualified type ownership

> **Compiler integration update, pending release.** The project-module source
> implementation under review resolves qualified imported types and enum
> variants as described here. This does not change the published v0.10.2
> artifact.

For a manifest project, the defining source module owns each enum, struct, and
type alias. A qualifier MUST resolve to the current module or to exactly one
imported module, and a type referenced from another module MUST be exported by
that owner. The terminal import alias (`defs.Color`), full module path
(`nested.defs.Color`), and crate-qualified path (`crate.nested.defs.Color`) all
retain the same defining owner. The rule applies recursively in reference,
fixed-array, tuple, generic-argument, raw-pointer, and external-function type
positions. Same-named types in different modules remain distinct.

An unknown, unimported, non-exported, or ambiguous owner MUST be refused with
`E2002` during both checking and artifact-producing builds. A refused build
MUST leave no artifact.

Inline `module name { ... }` blocks are transparent syntax containers in the
current parser. The parser accepts and preserves dotted type names and
qualified enum-pattern paths inside them, but an inline name does not create a
module-table owner. A project loader instead assigns the enclosing source
file's canonical module path and flattens a transparent block's declarations
into that file. Therefore parsing `config.Mode` in an inline block does not
establish `config` as a semantic owner; compiling that source without a
manifest-resolved module MUST refuse the qualified type and variants with
`E2002`.

The pending integration's executable coverage is the compiler-side
`qualified_enum_run` test together with the parser and single-source refusal
controls in `parse_match_and_ref`.

## Slice call implementation boundary

> **Compiler integration update, pending release.** The `std-surface` source
> implementation under review defines a bounded dynamic-array-to-slice call
> ABI. This describes the pending integration; it does not change the
> published v0.10.2 artifact.

A compatible `array<T>` value or array literal MAY be passed to `&[T]` or
`&mut [T]` parameters. Both use the existing `std.vec` Option-C dynamic-array
handle layout, an opaque handle to the `[addr, len, cap]` record. A mutable
slice parameter accepts an `array<T>` value or a mutable slice value; a
read-only parameter also accepts a mutable slice value. Read-only slices
permit indexing, `get`, and length queries. Mutable slices add indexed
assignment and `set`; ownership operations such as `push`, `free`, and
capacity access are unavailable through either slice form. Inferred aliases
retain their slice capabilities across branches, loop iterations, and loop
transfers, including `break` and `continue` paths.

The compiler MUST refuse an unproven or incompatible call-boundary layout
with `E2032` before artifact emission. This includes an unsupported element
form, an explicit slice-typed local binding, a scalar/map/opaque integer
argument, an incompatible array, and a slice or array result that is not
proven on every required path. The current ABI guard refuses floating-point,
tensor, fixed-array, and nested-slice element layouts. Opaque integer and map
handles cannot establish slice provenance merely by annotation.

Capability erasure, read-only mutation, borrowed values passed to non-slice
parameters, borrowed values returned through non-slice returns, and
slice-containing struct fields MUST produce `E2033`. A declared slice return
may preserve a compatible slice capability. General lifetime and
alias-exclusivity analysis remains outside this implementation. These limits
are separate from the general byte-slice design in [Future Extensions](./future-extensions.md#systems-programming-primitives).

For an owned `array<T>`, `push` returns the replacement owner handle. The
pending compiler accepts an explicit same-binding update such as
`xs = xs.push(value)` and rewrites a bare statement `xs.push(value)` to that
same owner-preserving form. A collection mutation used where its replacement
handle cannot be rebound, including assignment to a different binding or a
nested expression, MUST be refused with `E2300`. This rule follows the
receiver's collection type; a user-defined method with the same name on a
non-collection value is unaffected.

`set` has a different result contract: it updates existing storage and returns
a scalar status. Consequently `xs.set(index, value)` is valid as a statement
for an owned array or mutable slice, while `xs = xs.set(index, value)` cannot
replace an owned array and MUST be refused with `E2032`. Neither read-only nor
mutable borrowed slices provide `push`; attempts MUST be refused with `E2033`.

The pending integration's executable coverage is the compiler-side
`slice_call_abi_run` and `lowering_refusal_diagnostics_run` tests; they are not
yet shipped conformance artifacts.

## Traits and generics

> **Implementation status (v0.10.x, honest boundary).** The rules in this section specify the
> *full* v1.0 type system; they are **not yet implemented** in the reference implementation's
> executable subset. Shipped today: generics limited to a **single type parameter over scalar
> types** (a bounded slice — no multi-parameter generics, no generic containers, no `where`-clause
> bounds). **Not shipped:** `trait` declarations, trait implementations, `dyn Trait` objects, and
> closures / first-class function values. See
> [Future Extensions](./future-extensions.md#deferred-core-language-features) for the roadmap.
> None of these are required for Core v1 conformance.

- Traits declare associated functions, types, and laws. Implementations MUST enforce that all
  required items are provided by conforming types.
- Trait implementations MUST be coherent: for any type and trait pair there MAY be at most one
  implementation in scope.
- Generic type parameters use an explicit `where` clause to declare trait bounds.

Trait resolution strategies are implementation-defined but MUST respect lexical scoping. The reference
implementation uses a Rust-level trait-based plugin architecture internally for backend selection;
this is an implementation detail, not a MIND-language trait feature.

## Differentiable types

The `diff T` wrapper marks values that participate in automatic differentiation. Implementations
MUST track primal and tangent components as described in [Automatic differentiation](./autodiff.md).
Values of type `diff T` MAY be passed where `T` is expected only when an implicit projection rule is
available; otherwise an explicit conversion is required.

## Type soundness

The canonical proof of progress and preservation is maintained alongside the reference compiler
(informative). Implementations SHOULD aim to keep diagnostic examples synced with the canonical
proof obligations.
