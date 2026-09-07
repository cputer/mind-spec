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

﻿# Type System

> **Status:** Draft  
> **Last updated:** 2026-09-06
> **MIND Spec Section**

---

### Type checking

MIND is statically typed. The normative type formation and compatibility rules
are maintained in the [versioned type-system specification](https://github.com/star-ga/mind-spec/blob/main/spec/v1.0/types.md).

### Fixed-array literals

An explicit `let` or `const` binding of type `[T; n]` requires an array literal
with exactly `n` elements. This requirement applies inside functions, branches,
and loops as well as at module level. Parentheses do not suppress the check;
nested fixed-array literals must match every declared extent.

For example, `[1, 2, 3, 4]` has the required cardinality for `[i64; 4]`, while
three or five elements do not. A mismatch must produce a static diagnostic at
the literal with the expected and actual counts. Nonliteral initializers remain
subject to the ordinary type compatibility rules.

---

[ Back to Spec Index](index.md)
