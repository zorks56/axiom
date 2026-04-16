# AXIOM Programming Language

**Il linguaggio di programmazione del futuro profondo.**

## Anno 52026 d.C.

AXIOM è un linguaggio di programmazione sperimentale che esplora paradigmi computazionali avanzati, immaginando cosa potrebbe esistere 50.000 anni nel futuro.

## Compilatore

Il compilatore AXIOM traduce il codice AXIOM in Python eseguibile.

### Utilizzo

```bash
# Compilare un file .axm
python axiom_compiler.py programma.axm

# Eseguire demo integrata
python axiom_compiler.py
```

### Features del Linguaggio

| Parola Chiave | Significato |
|--------------|-------------|
| `phase` | Definisce una funzione |
| `manifest` | Definisce una costante/variabile globale |
| `entangle` | Definisce una variabile locale |
| `observe` | Stampa output |
| `when` | Condizione if |
| `for_each` | Iterazione |
| `superpose` | Crea stato quantistico sovrapposto |
| `collapse` | Collassa stato quantistico |

### Esempio

```axiom
phase fibonacci(n) {
    when n <= 1 -> n
    else -> fibonacci(n - 1) + fibonacci(n - 2)
}

phase main() {
    manifest sequenza = []

    for_each i in range(10) {
        sequenza.append(fibonacci(i))
    }

    observe "Sequenza di Fibonacci:"
    observe sequenza

    entangle Psi = superpose(1, 2, 3, 5, 8)
    observe "Stati quantistici Psi inizializzati"
}
```

## Struttura del Progetto

```
axiom/
├── axiom_compiler.py    # Compilatore AXIOM
├── SPEC.md              # Specifica del linguaggio
├── examples/
│   └── quantum_fibonacci.axm
└── README.md
```

## Note sulla Traduzione

AXIOM traduce in Python per l'esecuzione, mantenendo la semantica del linguaggio:
- `phase` → `def` (funzioni Python)
- `manifest` → variabili globali
- `entangle` → variabili locali
- `superpose()` → dizionario con flag quantistico
- `observe` → `print`

## Concetti Futuristici Implementati

1. **Entanglement Computazionale**: Variabili correlate attraverso il registro `_entangle_registry`
2. **Stati Quantistici**: `superpose()` crea stati multi-valore
3. **Collapse**: `collapse()` risolve stati quantistici
4. **Auto-Evoluzione**: Il runtime supporta hot-reload (`evolve`)

---

*"La singolarità è vicina. Benvenuti nel futuro profondo."*
