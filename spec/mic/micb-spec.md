# MIC-B v2 Binary Format Specification

**Version:** 2.0
**Status:** Release Candidate
**Date:** 2026-01-18

## Overview

MIC-B v2 is a compact binary format for Mind IR graphs, designed for:

- **Compact size**: ~4x smaller than mic@2 text
- **Fast parsing**: Direct memory mapping possible
- **Deterministic**: Same graph always produces identical bytes
- **Lossless**: Full roundtrip with mic@2

## Wire Format

All multi-byte integers are encoded as ULEB128 (variable-length).
Signed integers use zigzag encoding before ULEB128.

### Layout

```
┌─────────────────┬──────────────────────────────────┐
│ Offset          │ Content                          │
├─────────────────┼──────────────────────────────────┤
│ 0-3             │ Magic: "MICB" (4 bytes ASCII)    │
│ 4               │ Version: 0x02                    │
│ 5+              │ String Table                     │
│ ...             │ Symbol Table                     │
│ ...             │ Type Table                       │
│ ...             │ Value Table                      │
│ ...             │ Output (1 uleb128)               │
└─────────────────┴──────────────────────────────────┘
```

## ULEB128 Encoding

Unsigned Little-Endian Base-128 encoding:

- Each byte uses 7 bits for data
- MSB (bit 7) is continuation flag: 1 = more bytes follow
- Values 0-127 encode in 1 byte
- Maximum 10 bytes for u64

```
Value       Encoded bytes
0           [0x00]
127         [0x7F]
128         [0x80, 0x01]
16383       [0xFF, 0x7F]
16384       [0x80, 0x80, 0x01]
```

## Zigzag Encoding

Maps signed integers to unsigned for efficient varint encoding:

```
Signed  →  Unsigned
0       →  0
-1      →  1
1       →  2
-2      →  3
2       →  4
...
```

Formula: `encode(n) = (n << 1) ^ (n >> 63)`

## Tables

### 1. String Table

Interned strings for names and dimension tokens.

```
uleb128     count           # number of strings
repeat count:
  uleb128   byte_length     # UTF-8 byte length
  bytes     data            # UTF-8 content (no null terminator)
```

String order is deterministic: first-seen order during serialization:
1. Symbol names
2. Type dimension tokens
3. Value names (args, params)
4. Custom opcode names

### 2. Symbol Table

References to symbolic dimension names.

```
uleb128     count           # number of symbols
repeat count:
  uleb128   string_idx      # index into string table
```

### 3. Type Table

Tensor type definitions.

```
uleb128     count           # number of types
repeat count:
  u8        dtype           # data type (see below)
  uleb128   rank            # number of dimensions
  repeat rank:
    uleb128 dim_str_idx     # index into string table
```

#### Data Type Encoding

| Byte | Type |
|------|------|
| 0 | f16 |
| 1 | f32 |
| 2 | f64 |
| 3 | bf16 |
| 4 | i8 |
| 5 | i16 |
| 6 | i32 |
| 7 | i64 |
| 8 | u8 |
| 9 | u16 |
| 10 | u32 |
| 11 | u64 |
| 12 | bool |

### 4. Value Table

Values with implicit sequential IDs (0, 1, 2...).

```
uleb128     count           # number of values
repeat count:
  u8        tag             # 0=Arg, 1=Param, 2=Node
  ...       payload         # tag-specific data
```

#### Arg/Param Payload (tag 0 or 1)

```
uleb128     name_str_idx    # index into string table
uleb128     type_idx        # index into type table
```

#### Node Payload (tag 2)

```
u8          opcode          # opcode byte (see below)
...         opcode_params   # opcode-specific parameters
uleb128     input_count     # number of inputs
repeat input_count:
  uleb128   input_id        # value ID (must be < current ID)
```

#### Opcode Encoding

| Byte | Opcode | Additional Params |
|------|--------|-------------------|
| 0 | Matmul | none |
| 1 | Add | none |
| 2 | Sub | none |
| 3 | Mul | none |
| 4 | Div | none |
| 5 | Relu | none |
| 6 | Softmax | sleb128 axis |
| 7 | Sigmoid | none |
| 8 | Tanh | none |
| 9 | GELU | none |
| 10 | LayerNorm | none |
| 11 | Transpose | uleb128 n, n × sleb128 perm |
| 12 | Reshape | none |
| 13 | Sum | uleb128 n, n × sleb128 axes |
| 14 | Mean | uleb128 n, n × sleb128 axes |
| 15 | Max | uleb128 n, n × sleb128 axes |
| 16 | Concat | sleb128 axis |
| 17 | Split | sleb128 axis, uleb128 count |
| 18 | Gather | sleb128 axis |
| 255 | Custom | uleb128 name_str_idx |

### 5. Output

Single value ID indicating the graph output.

```
uleb128     output_id       # value ID of output
```

## Example: Residual Block

The canonical residual block `Y = relu(X @ W + b) + X`:

### mic@2 (85 bytes)

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

### MIC-B v2 (~40 bytes)

```hex
4D 49 43 42 02              # Magic "MICB" + version 2
05                          # 5 strings
03 31 32 38                 # "128"
01 58                       # "X"
01 57                       # "W"
01 62                       # "b"
00                          # 0 symbols
02                          # 2 types
00 02 00 00                 # T0: f16 [128, 128]
00 01 00                    # T1: f16 [128]
07                          # 7 values
00 01 00                    # Arg("X", T0)
01 02 00                    # Param("W", T0)
01 03 01                    # Param("b", T1)
02 00 02 00 01              # Node(Matmul, [0, 1])
02 01 02 03 02              # Node(Add, [3, 2])
02 05 01 04                 # Node(Relu, [4])
02 01 02 05 00              # Node(Add, [5, 0])
06                          # Output: 6
```

## Determinism Rules

1. String table uses first-seen insertion order
2. All tables maintain graph definition order
3. Varints use minimal encoding (no zero-padding)
4. No padding bytes between sections

## Validation

Decoders MUST verify:

1. Magic bytes are exactly "MICB"
2. Version is 0x02
3. All string indices are in bounds
4. All type indices are in bounds
5. Node inputs reference earlier values only
6. Output references a valid value

## Error Handling

On invalid input, decoders SHOULD:

- Return an error with byte offset
- Not panic or crash
- Not allocate unbounded memory

## Security Limits

Implementations SHOULD enforce:

- Maximum input size: 10 MB
- Maximum string count: 1,000,000
- Maximum value count: 100,000
- Maximum string length: 64 KB
