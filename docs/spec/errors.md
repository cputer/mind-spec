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

﻿# Errors & Diagnostics

> **Status:** Core v1 normative catalog
>
> **Last updated:** 2026-09-08
>
> **MIND Spec Section**

The canonical error-code assignments and stability rules are maintained in
[Error Catalog (Normative)](../../spec/v1.0/errors.md). Diagnostic codes remain
stable within Core v1; adding a code requires a minor specification release,
while renumbering or reusing an existing code requires a major release.

The E6xxx catalog distinguishes two current compilation refusals:

- `E6002` means the requested backend is unavailable.
- `E6009` means compiler-side aggregate materialization exceeded a deterministic
  limit or reached an operation that cannot be represented by the runnable ABI.
  The current reference profile executes fixed-array struct fields whose cells
  are `i64` or `f64`; nested `[Struct; N]` element-field receivers remain
  unsupported and must receive the same structured refusal.

An `E6009` refusal terminates compilation with a non-zero status and does not
publish a partial runnable artifact. It does not imply that the source is
ill-typed.

---

[ Back to Spec Index](index.md)
