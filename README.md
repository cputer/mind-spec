# Mind Language Specification

The **MIND** language evolves through an open specification process. This repository is the
authoritative source for the normative language specification (`spec/`) and the guiding design
principles (`design/`). Content here is versioned, reviewed in the open, and kept in lockstep with
the reference implementation at [cputer/mind](https://github.com/cputer/mind).

## Table of contents

- [Language specification](./spec/)
  - [Version 1.0 overview](./spec/v1.0/overview.md)
  - [Lexical structure](./spec/v1.0/lexical.md)
  - [Type system](./spec/v1.0/types.md)
  - [Automatic differentiation](./spec/v1.0/autodiff.md)
  - [Intermediate representation](./spec/v1.0/ir.md)
- [Design documents](./design/)
  - [Design principles](./design/principles.md)
  - [RFC process](./design/rfc-process.md)

## Reading the spec

The specification is organised to mirror the reference compiler documentation in
[`cputer/mind/docs/`](https://github.com/cputer/mind/tree/main/docs). Each chapter notes
relationships to implementation details and links to the corresponding background materials when
informative context is helpful.

Normative sections use RFC 2119 terminology. When a document includes non-normative background or
examples it is explicitly marked as informative.

## Contributing

- **Read online:** <https://cputer.github.io/mind-spec/>
- **Preview locally:** `npx docsify-cli serve docs`
- **Guidelines:** See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for review expectations and local setup
  instructions.

Security disclosures should follow [`SECURITY.md`](./SECURITY.md). Project status tracking lives in
[`STATUS.md`](./STATUS.md).
