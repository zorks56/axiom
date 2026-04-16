# AXIOM Language Specification
## Version 1.0 — Beyond the Singularity

### Philosophy

AXIOM transcends classical computational limits. Built on three principles:

- **Computational Entanglement** — variables correlated across execution contexts
- **Quantum Collapse** — lazy resolution of superposed states
- **Self-Evolution** — code adapts in response to runtime observation

### Core Syntax

```axiom
phase function_name(parameters) {
    // function body
}

manifest CONSTANT = value

entangle variable = expression
```

### Keywords Reference

| AXIOM | Meaning | Modern Equivalent |
|-------|---------|------------------|
| `phase` | Function | `def` / `function` |
| `manifest` | Global constant/variable | `const` / `var` |
| `entangle` | Local variable | `let` / `var` |
| `observe` | Output | `print` |
| `superpose` | Multi-state value | `Promise` |
| `collapse` | Resolve state | `await` |
| `when ... ->` | Inline condition | `if ... return` |
| `for_each ... in` | Iteration | `for ... in` |

### Expression Syntax

```axiom
when condition -> value
else -> alternative_value

entangle x = superpose(1, 2, 3)
entangle name = "value"
manifest MAX = 1000
```

### Supported Operators

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `<=`, `>=`, `!=`, `==`
- Logic: implicit through `when` expressions

### Full Example

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
    observe "Quantum states available"
}
```

### Compilation

AXIOM compiles to optimized Python. Transformations:

| AXIOM | Python |
|-------|--------|
| `phase name(params) { body }` | `def name(params):` |
| `manifest x = val` | `x = val` |
| `entangle x = val` | `x = val` |
| `observe expr` | `print(expr)` |
| `superpose(...)` | `{"_axiom_quantum": True, "states": [...]}` |
| `when c -> v` | `if c: return v` |

### AXIOM Runtime

The compiler ships a minimal runtime:

- `superpose(*states)` — create quantum state
- `is_quantum(val)` — check quantum type
- `collapse(qval)` — collapse to single value
