# Validador Formal em Três Níveis

**Disciplina:** Modelagem Computacional  
**Tema:** Tema 1 — Validador de cadastro, fórmulas e integridade

## Visão geral

| Nível | Linguagem | Modelo | Arquivo |
|---|---|---|---|
| LR | CPF no formato `ddd.ddd.ddd-dd` | DFA | `src/regular.py` |
| LLC | Parênteses/colchetes/chaves balanceados | PDA | `src/livre_contexto.py` |
| R | Cópia de cadeia: `w#w`, w ∈ {0,1}* | Máquina de Turing | `src/recursiva.py` |

## Requisitos

```
Python 3.8+
```

Sem dependências externas obrigatórias. Para diagramas opcionais: `pip install graphviz`.

## Executar a bateria completa (um único comando)

```bash
python src/testes.py
```

## Executar cada reconhecedor individualmente

```bash
python src/regular.py "123.456.789-00"
python src/livre_contexto.py "((x+y)*z)"
python src/recursiva.py "101#101"
```

O programa termina com código 0 (aceito) ou 1 (rejeitado).

## Estrutura do repositório

```
projeto/
├── README.md
├── requirements.txt
├── src/
│   ├── regular.py          ← reconhecedor LR (DFA)
│   ├── livre_contexto.py   ← reconhecedor LLC (PDA)
│   ├── recursiva.py        ← reconhecedor R (MT)
│   └── testes.py           ← bateria completa
├── testes/
│   ├── testes_regular.txt
│   ├── testes_livre_contexto.txt
│   └── testes_recursiva.txt
├── diagramas/
│   ├── dfa_regular.dot
│   ├── pda_livre_contexto.dot
└── └── mt_recursiva.dot

```

## Definição de "passo"

Conforme definição do professor:

- **DFA:** cada leitura de símbolo com mudança de estado.
- **PDA:** cada transição (empilhamento ou desempilhamento).
- **MT:** cada movimento da cabeça (leitura + possível escrita + deslocamento).
