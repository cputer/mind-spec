# Lexical Structure

This chapter provides the normative specification for the lexical analysis of the MIND programming language.

## 1. Source Text Representation
MIND source files must be encoded as **UTF-8**. The compiler performs normalization on line endings prior to tokenization.

## 2. Comments and Whitespace
- **Line Comments:** Begin with `//`.
- **Block Comments:** Begin with `/*` and end with `*/`. Block comments **can be nested**.

## 3. Identifiers
MIND follows Unicode Standard Annex #31:
```regex
Identifier := [\p{XID_Start}_] [\p{XID_Continue}_]*
```

## 4. Keywords
The following tokens are reserved:
| | | | | |
| :--- | :--- | :--- | :--- | :--- |
| `fn` | `let` | `type` | `struct` | `trait` |
| `if` | `else` | `match` | `while` | `for` |

## 5. Literals
- **Integers:** `123`, `0xFF`, `0b101`
- **Floats:** `3.14`, `1.0e-4`
- **Tangents:** `1.0^` (Differentiable literal)
