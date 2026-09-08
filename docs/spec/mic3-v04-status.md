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

**Status: unreleased implementation draft.** The public reference-compiler
candidate is [PR #256](https://github.com/star-ga/mind/pull/256), currently at
[`66f43a6b`](https://github.com/star-ga/mind/commit/66f43a6bed42709047682b28cef6bd8e27118c7b)
against `main`. This page is an informative cross-reference rather than a
versioned or normative wire specification; the v04 wire contract, shared
golden vectors, and release status remain unfrozen.

The proposed first stage carries canonical scalar IR together with owner-
qualified record schemas, fixed or dynamic array descriptors, function
identities and signatures, resolved call targets, and function-scoped semantic
value types. It is intended to preserve logical identity supplied by the
compiler. It does not authorize a physical record ABI or infer identity from
host paths, source order, or scalar handles.

The public candidate provides checked v04 admission and decoder validation. It
bounds input size, nesting, allocation, and semantic descriptors, stages
declarations before cumulative validation, and rejects malformed or unsupported
content. Its checked evidence path applies the size limit to the complete body
plus MAP artifact before publication. These are implementation checks for the
draft candidate and do not establish a released wire contract.

The proposal is limited to a scalar instruction subset. Standard-surface and
tensor instructions, source-to-native aggregate execution, pure-MIND codec
parity, cross-profile or cross-substrate identity, a frozen protocol, and
promotion remain separate work. A successful scalar-stage transport result is
not evidence that those dependencies are complete.

Existing `mic@3` versions, including their `0x03` compatibility behavior, remain
unchanged. This status page establishes no normative v04 byte contract, shared
vectors, reader/writer contract, or Core v1 requirement. Any future v04
specification must be accepted separately and must define its own strict
version, malformed-input, resource, canonicality, and backward-compatibility
rules before publication.

[Back to Spec Index](./index.md) | [Project status](../../STATUS.md)
