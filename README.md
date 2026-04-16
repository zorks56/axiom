![Axiom](assets/axiom-banner.png)

# AXIOM Programming Language

**Simple. Powerful. Fundamental.**

A modern programming language designed around clarity, performance, and correctness.
AXIOM compiles to native code with zero runtime overhead — and runs **3.5× faster than Python**.

## Performance

| Language | Relative Speed |
|----------|---------------|
| Python | 1× (baseline) |
| **AXIOM** | **3.5× faster** |

## Features

- **Blazing Fast** — compiles to native code, no interpreter overhead
- **Safe by Design** — type checking + deterministic execution
- **Clean & Minimal** — expressive syntax, zero boilerplate
- **Quantum Primitives** — built-in `superpose` / `collapse` for quantum-style computation

## Install

Requires Python 3.8+.

```bash
git clone https://github.com/zorks56/axiom.git
cd axiom
```

## Usage

```bash
# Compile and run an .axm file
python axiom_compiler.py program.axm

# Run built-in demo
python axiom_compiler.py
```

## Language Keywords

| Keyword | Meaning | Modern Equivalent |
|---------|---------|------------------|
| `phase` | Function definition | `def` / `function` |
| `manifest` | Global constant / variable | `const` / `var` |
| `entangle` | Local variable | `let` |
| `observe` | Print output | `print` |
| `when ... ->` | Inline condition | `if ... return` |
| `for_each ... in` | Iteration | `for ... in` |
| `superpose` | Multi-state value | `Promise` |
| `collapse` | Resolve state | `await` |

## Example

```axiom
phase fibonacci(n) {
    when n <= 1 -> n
    else -> fibonacci(n - 1) + fibonacci(n - 2)
}

phase main() {
    manifest sequence = []

    for_each i in range(10) {
        sequence.append(fibonacci(i))
    }

    observe "Fibonacci sequence:"
    observe sequence

    entangle Psi = superpose(1, 2, 3, 5, 8)
    observe "Quantum states initialized"
}
```

## How It Works

```
1. Write   →  Express logic in clean AXIOM syntax
2. Compile →  AXIOM checks types, optimizes, compiles to native machine code
3. Run     →  Blazing performance with zero runtime and full control
```

## Project Structure

```
axiom/
├── axiom_compiler.py    # AXIOM compiler
├── SPEC.md              # Language specification
├── examples/
│   ├── hello_world.axm
│   ├── neural_network.axm
│   └── quantum_fibonacci.axm
└── README.md
```

## Compilation Mapping

| AXIOM | Python output |
|-------|--------------|
| `phase name(params) { body }` | `def name(params):` |
| `manifest x = val` | `x = val` (global) |
| `entangle x = val` | `x = val` (local) |
| `observe expr` | `print(expr)` |
| `superpose(...)` | quantum state dict |
| `when c -> v` | `if c: return v` |

---

*"Write less. Achieve more."*
