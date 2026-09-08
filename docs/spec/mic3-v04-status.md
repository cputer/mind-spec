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

**Status: unreleased proposal.** The reference-compiler work is an unpublished
candidate, and this page is an informative cross-reference rather than a
versioned wire specification. The [compiler draft for candidate `75f82e03`](https://github.com/star-ga/mind/blob/75f82e03/docs/mic3-v04-draft.md)
is the proposal being reviewed; the link is provisional until that candidate is
landed and root updates it to the final public revision.

The proposed first stage carries canonical scalar IR together with owner-
qualified record schemas, fixed or dynamic array descriptors, function
identities and signatures, resolved call targets, and function-scoped semantic
value types. It is intended to preserve logical identity supplied by the
compiler. It does not authorize a physical record ABI or infer identity from
host paths, source order, or scalar handles.

The proposal is limited to a scalar instruction subset. Standard-surface and
tensor instructions, source-to-native aggregate execution, pure-MIND codec
parity, cross-profile or cross-substrate identity, a frozen protocol, and
promotion remain separate work. A successful scalar-stage transport result is
not evidence that those dependencies are complete.

Existing `mic@3` versions, including their `0x03` compatibility behavior, remain
unchanged. No v04 bytes, shared vectors, reader/writer contract, or normative
Core v1 requirement is established by this status page. Any future v04
specification must be accepted separately and must define its own strict
version, malformed-input, resource, canonicality, and backward-compatibility
rules before publication.

[Back to Spec Index](./index.md) | [Project status](../../STATUS.md)
