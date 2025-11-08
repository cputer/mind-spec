# 🧠 MIND Language Specification

Welcome to the **MIND Specification**, the authoritative reference for the MIND programming language and runtime model.

This specification defines the core semantics, syntax, and typing rules for MIND, including its autodiff-enabled execution model and tensor algebra extensions.

---

## 📖 Purpose

The goal of this specification is to provide a stable foundation for:
- Compiler and runtime implementors.
- Contributors proposing extensions via RFCs.
- Researchers and integrators targeting MIND’s intermediate representation (MIR/MLIR).

---

## 🧩 Specification Structure

| Section | Description |
|----------|--------------|
| **Language Core** | Syntax, type system, and evaluation semantics. |
| **Semantics** | Runtime and compile-time behavior, diagnostics, and safety. |
| **Design Docs** | Internal architecture, autodiff engine, and optimizer design. |
| **RFCs** | Proposed or implemented extensions to the language. |

---

## 🚀 Status

**Spec version:** `v1.0-draft`  
**Language tag:** `mind-2025a`  
**Last update:** _Auto-populated from CI build timestamp_

---

## 📚 Related Projects

| Repo | Purpose |
|------|----------|
| [`cputer/mind`](https://github.com/cputer/mind) | Public compiler + CLI (front-end). |
| [`cputer/mind-runtime`](https://github.com/cputer/mind-runtime) | Private runtime backend (MLIR, GPU, autodiff). |
| [`cputer/mind-spec`](https://github.com/cputer/mind-spec) | This specification and design docs. |

---

> 🧩 **Tip:** Use the sidebar to navigate the spec modules.  
> All documents are Markdown-based and auto-rendered by Docsify.

---

<footer style="text-align:center; color:#777; font-size:12px; margin-top:40px;">
  © 2025 MIND Language Project — All Rights Reserved
</footer>
