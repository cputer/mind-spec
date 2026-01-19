# mic@2 Text Format Specification

**Version:** 2.0
**Status:** Release Candidate
**Date:** 2026-01-18

## Overview

mic@2 is a compact, line-oriented text format for Mind IR graphs, designed for:

- **Minimal token usage**: ~40% reduction vs mic@1 through implicit IDs
- **LLM-friendly**: Compact representation ideal for AI agent prompts
- **Git-friendly**: One operation per line for clean diffs
- **Deterministic**: Canonical output ensures reproducibility

## Grammar

```ebnf
mic2        ::= header lines*
header      ::= "mic@2" LF
lines       ::= (symbol | type | value | output | comment | empty)*
comment     ::= "#" [^\n]* LF
empty       ::= WS* LF

symbol      ::= "S" WS name LF
type        ::= "T" idx WS dtype (WS dim)* LF
value       ::= arg | param | node
arg         ::= "a" WS name WS type_ref LF
param       ::= "p" WS name WS type_ref LF
node        ::= opcode (WS input)* (WS param)* LF
output      ::= "O" WS value_id

name        ::= [A-Za-z_][A-Za-z0-9_]*
idx         ::= [0-9]+
value_id    ::= [0-9]+
type_ref    ::= "T" idx
dtype       ::= "f16" | "f32" | "f64" | "bf16"
              | "i8" | "i16" | "i32" | "i64"
              | "u8" | "u16" | "u32" | "u64" | "bool"
dim         ::= [0-9]+ | name | "?"

opcode      ::= "m" | "+" | "-" | "*" | "/" | "r" | "s"
              | "sig" | "th" | "gelu" | "ln" | "t"
              | "rshp" | "sum" | "mean" | "max" | "cat"
              | "split" | "gth"

input       ::= value_id
param       ::= [0-9]+ | "-"? [0-9]+

WS          ::= [ \t]+
LF          ::= "\n"
```

## Sections

### Header

The first non-empty, non-comment line MUST be:

```
mic@2
```

### Symbols (Optional)

Declare symbolic dimension names used in shapes:

```
S B
S seq
S hidden
```

Symbols are advisory; dimension tokens in types are always strings.

### Types

Define tensor types with sequential indices starting at 0:

```
T0 f16 128 128
T1 f16 128
T2 f32 B seq hidden
```

Format: `T<idx> <dtype> <dim0> <dim1>...`

- Type indices MUST be sequential: T0, T1, T2...
- Dimensions can be:
  - Fixed: `128`, `256`
  - Symbolic: `B`, `seq`
  - Wildcard: `?`

### Values

Values are assigned **implicit sequential IDs** starting at 0, in the order they appear:

#### Arguments

```
a X T0      # value id 0
a Y T1      # value id 1
```

#### Parameters

```
p W T0      # value id 2
p b T1      # value id 3
```

#### Nodes

```
m 0 2       # value id 4: matmul(X, W)
+ 4 3       # value id 5: add(matmul, b)
r 5         # value id 6: relu(add)
```

### Output

Exactly one output line specifying the result value:

```
O 6
```

## Opcodes

| Token | Name | Arity | Description |
|-------|------|-------|-------------|
| `m` | Matmul | 2 | Matrix multiplication |
| `+` | Add | 2 | Element-wise addition |
| `-` | Sub | 2 | Element-wise subtraction |
| `*` | Mul | 2 | Element-wise multiplication |
| `/` | Div | 2 | Element-wise division |
| `r` | Relu | 1 | ReLU activation |
| `s` | Softmax | 1 | Softmax (optional axis param) |
| `sig` | Sigmoid | 1 | Sigmoid activation |
| `th` | Tanh | 1 | Tanh activation |
| `gelu` | GELU | 1 | GELU activation |
| `ln` | LayerNorm | 1 | Layer normalization |
| `t` | Transpose | 1 | Transpose (permutation params) |
| `rshp` | Reshape | 1 | Reshape |
| `sum` | Sum | 1 | Sum reduction (axis params) |
| `mean` | Mean | 1 | Mean reduction (axis params) |
| `max` | Max | 1 | Max reduction (axis params) |
| `cat` | Concat | N | Concatenate (axis param) |
| `split` | Split | 1 | Split (axis, count params) |
| `gth` | Gather | 2 | Gather along axis |

## Canonicalization Rules

For deterministic output:

1. Use Unix line endings (`\n`)
2. Exactly one space between tokens
3. No trailing whitespace on lines
4. No trailing newline after output line
5. Section order: header, symbols, types, values, output
6. Comments are not preserved in canonical output

## Example: Residual Block

```
mic@2
T0 f16 128 128
T1 f16 128
a X T0
p W T0
p b T1
m 0 1
+ 3 2
r 4
+ 5 0
O 6
```

This represents: `Y = relu(X @ W + b) + X`

| Line | ID | Description |
|------|-----|-------------|
| `a X T0` | 0 | Input tensor X |
| `p W T0` | 1 | Weight matrix W |
| `p b T1` | 2 | Bias vector b |
| `m 0 1` | 3 | X @ W |
| `+ 3 2` | 4 | (X @ W) + b |
| `r 4` | 5 | relu((X @ W) + b) |
| `+ 5 0` | 6 | relu(...) + X (residual) |
| `O 6` | - | Output is value 6 |

## Validation Rules

1. Type indices must be sequential starting at 0
2. Type references must refer to defined types
3. Node inputs must reference earlier values (no forward refs)
4. Output must reference a valid value
5. Opcode arity must match input count

## Security Limits

Implementations SHOULD enforce:

- Maximum input size: 10 MB
- Maximum line count: 1,000,000
- Maximum value count: 100,000
- Maximum shape dimensions: 32

## Comparison with mic@1

| Feature | mic@1 | mic@2 |
|---------|-------|-------|
| Node IDs | Explicit (`N0`, `N1`) | Implicit by order |
| Type syntax | `[f32;3,4]` | `f32 3 4` |
| Opcodes | Verbose (`add`, `matmul`) | Compact (`+`, `m`) |
| Token efficiency | Baseline | ~40% reduction |

## Appendix: Format Comparison

Residual block example `Y = relu(X @ W + b) + X`:

### Size Comparison

| Format | Tokens | Bytes | vs JSON (tokens) | vs JSON (bytes) |
|--------|--------|-------|------------------|-----------------|
| JSON | ~180 | ~450 | baseline | baseline |
| TOML | ~151 | ~380 | 1.2x | 1.2x |
| TOON | ~67 | ~170 | 2.7x | 2.6x |
| mic@1 | ~45 | ~120 | 4.0x | 3.8x |
| **mic@2** | **~28** | **~85** | **6.4x** | **5.3x** |
| **MIC-B v2** | - | **~40** | - | **11.3x** |

### Feature Comparison

| Feature | JSON | TOON | mic@1 | mic@2 | MIC-B v2 |
|---------|------|------|-------|-------|----------|
| Human readable | Yes | Yes | Yes | Yes | No |
| Git-friendly | No | Partial | Yes | Yes | No |
| Deterministic | No | No | Yes | Yes | Yes |
| LLM-optimized | No | No | Partial | Yes | N/A |
| Binary format | No | No | No | No | Yes |
| Implicit IDs | No | No | No | Yes | Yes |

### Syntax Comparison

**JSON**
```json
{"nodes":[{"id":0,"op":"param","name":"X"},{"id":3,"op":"matmul","inputs":[0,1]}]}
```

**TOON**
```
nodes=[{id=0 op=param name=X},{id=3 op=matmul inputs=[0,1]}]
```

**mic@1**
```
N0 param "X" T0
N3 matmul N0 N1 T0
```

**mic@2**
```
a X T0
m 0 1
```
