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

# MIC@3 `0x04` implementation status

**Status: unreleased implementation draft.** The reference implementation landed
on compiler `main` through [PR #256](https://github.com/star-ga/mind/pull/256) at
[`66f43a6b`](https://github.com/star-ga/mind/commit/66f43a6bed42709047682b28cef6bd8e27118c7b).
This page is an informative cross-reference rather than a
versioned or normative wire specification; the v04 wire contract, shared
golden vectors, and release status remain unfrozen.

The proposed first stage carries canonical scalar IR together with owner-
qualified record schemas, fixed or dynamic array descriptors, function
identities and signatures, resolved call targets, and function-scoped semantic
value types. It is intended to preserve logical identity supplied by the
compiler. It does not authorize a physical record ABI or infer identity from
host paths, source order, or scalar handles.

The reference implementation provides checked v04 admission and decoder validation. It
bounds input size, nesting, allocation, and semantic descriptors, stages
declarations before cumulative validation, and rejects malformed or unsupported
content. Its checked evidence path applies the size limit to the complete body
plus MAP artifact before publication. These are implementation checks for the
draft format and do not establish a released wire contract.

The opt-in `compile_source_to_canonical_ir` Rust library API, introduced in
[compiler PR #259](https://github.com/star-ga/mind/pull/259), binds a source
snapshot to captured project scope. It preserves resolved function ownership
and call identities, carries scalar producer facts from the existing type
checker, and checks every canonical return in its defining function scope.
Missing facts, changed snapshots, and unsupported source forms are refused.
This bounded path requires `cross-module-imports`; it returns verified IR
before optimization or backend execution.

The canonical source slice excludes unit functions, functions without explicit
return annotations, and bare returns without values. Those restrictions do not
change ordinary compilation's inferred-return or evaluator unit-placeholder
behavior. This API supplies neither a standalone MIND driver nor native record
and array execution.

The proposal is limited to a scalar instruction subset. Standard-surface and
tensor instructions, source-to-native aggregate execution, pure-MIND codec
parity, cross-profile or cross-substrate identity, a frozen protocol, and
promotion remain separate work. A successful scalar-stage transport result is
not evidence that those dependencies are complete.

## Draft intrinsic contract alignment

The following table records the ten-row intrinsic registry implemented by
[compiler PR #261](https://github.com/star-ga/mind/pull/261), merged on compiler
`main` at
[`a334ead4`](https://github.com/star-ga/mind/commit/a334ead49cfe9e98501c4345d9ec64d6ce2db3b2).
This remains a draft alignment note and does not make v04 a released wire
contract. A canonical declaration using the reserved owner `__mind_intrinsic`
must use one of these exact logical names, physical symbols, arities, and
signatures. The registry has no generic or variadic intrinsic form.

| Logical name | Physical symbol | Wire signature | Effect metadata | Profiles metadata | Result-use metadata |
|---|---|---|---|---|---|
| `argc` | `__mind_argc` | `() -> i64` | argument count | `FrozenNative` | value |
| `argv` | `__mind_argv` | `(i64) -> i64` | argument vector | `FrozenNative` | value |
| `alloc` | `__mind_alloc` | `(i64) -> i64` | arena allocation | `FrozenNative`, `RustMlir` | value |
| `load_i64` | `__mind_load_i64` | `(i64) -> i64` | 8-byte memory read | `FrozenNative`, `RustMlir` | value |
| `load8` | `__mind_load_i8` | `(i64) -> i64` | 1-byte memory read | `FrozenNative`, `RustMlir` | value |
| `open` | `__mind_open` | `(i64) -> i64` | read-only open | `FrozenNative`, `RustMlir` | value |
| `read` | `__mind_read` | `(i64, i64, i64, i64) -> i64` | file-descriptor read; offset is `-1` and ignored | `FrozenNative`, `RustMlir` | value |
| `store_i64` | `__mind_store_i64` | `(i64, i64) -> i64` | 8-byte memory write | `FrozenNative`, `RustMlir` | `DiscardOnly` in `FrozenNative` |
| `store8` | `__mind_store_i8` | `(i64, i64) -> i64` | 1-byte memory write | `FrozenNative`, `RustMlir` | `DiscardOnly` in `FrozenNative` |
| `write` | `__mind_write` | `(i64, i64, i64, i64) -> i64` | file-descriptor write; offset is `-1` and ignored | `FrozenNative`, `RustMlir` | value |

Effect, profile, and result-use columns are registry metadata, not additional
fields in the encoded function signature. In particular,
`DiscardOnly` describes how a FrozenNative emitter may use a store result; it
does not change the historical `i64` wire return, and it does not grant native
admission or prove memory provenance. The offset rule for `read` and `write`
also leaves all four `i64` parameters in the wire signature. Unknown names,
wrong owners, wrong arities, wrong scalar types, and generic identities remain
structured refusals.

## Experimental body mirror and resource limits

[Compiler PR #264](https://github.com/star-ga/mind/pull/264) extends the
experimental pure-MIND mirror from the declared prefix through the supported
core body: module IDs, exports, instructions and scoped value rows. It checks
module bounds and selected function metadata, including return IDs isolated
across nested functions. Its native artifact is tested against reference
decoder outcomes and exact positive-fixture re-emission. This is a review
candidate, not a released protocol or the production decoder.

Wire-format acceptance is not full semantic validation. Parameter descriptors,
local-definition coverage, per-function semantic budgets, authority presence
and string-table minimality remain explicit parity obligations. A passing
mirror result does not authorize native execution of the represented program.
The candidate's implementation limits are:

| Resource | Draft mirror limit | Failure behavior |
|---|---:|---|
| Admitted input | 10,485,760 bytes (`10 MiB`) | refuse before decoding when larger |
| Temporary read buffer | admitted limit plus 2 bytes | bounded probe for oversize detection; the extra bytes are never admitted |
| Re-emitted core body | 65,536 bytes | refuse when the body exceeds the mirror limit |
| ULEB value | `2^62 - 1` (`4,611,686,018,427,387,903`) | refuse larger values without wrapping |
| Type-descriptor nesting | 64 | refuse deeper declared type descriptors |
| Instruction depth | less than 256, with root depth 0 | refuse depth 256 |
| Allocation budget | `min(128 MiB, 1 MiB + 32 × input bytes)` | refuse when checked charges exceed the budget |
| Implemented descriptor scopes | `2^40` elements | check each descriptor, schema fields and declaration/module totals; full per-function semantic accounting remains open |

The input cap, body cap, and budget are implementation limits for this
unreleased draft. They do not establish complete v04 reader/writer parity
or native aggregate execution. The reference allocation accounting charges
each instruction twice (640 logical bytes total); this is an admission budget,
not a measured heap allocation.

Existing `mic@3` versions, including their `0x03` compatibility behavior, remain
unchanged. This status page establishes no normative v04 byte contract, shared
vectors, reader/writer contract, or Core v1 requirement. Any future v04
specification must be accepted separately and must define its own strict
version, malformed-input, resource, canonicality, and backward-compatibility
rules before publication.

[Back to Spec Index](./index.md) | [Project status](../../STATUS.md)
