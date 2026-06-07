"""
Reconhecedor de Linguagem Regular - CPF no formato ddd.ddd.ddd-dd

Linguagem: L = { w ∈ Σ* | w é uma cadeia no formato ddd.ddd.ddd-dd,
                          onde d ∈ {0,...,9} }
Alfabeto: Σ = {0,1,2,3,4,5,6,7,8,9, '.', '-'}
"""

import sys


# estados
ESTADOS = {
    "q0",  "q1",  "q2",  "q3",  "q4",  "q5",  "q6",
    "q7",  "q8",  "q9",  "q10", "q11", "q12", "q13", "q14",
    "ERRO"
}

#alfabeto
SIGMA = set("0123456789.-")

# estado iincial
Q0 = "q0"

# Estados de aceitação
ESTADOS_FINAIS = {"q14"}

# Tabela de transicao: delta[estado][simbolo] = proximo_estado
#formato esperado: d d d . d d d . d d d - d d
#                   0 1 2 3 4 5 6 7 8 9 10 11 12 13
DIGITO = set("0123456789")

def _build_delta():
    delta = {}
    # Inicializa todos os estados com ERRO para qualquer simbolo
    for q in ESTADOS:
        delta[q] = {}
        for c in SIGMA:
            delta[q][c] = "ERRO"
        #simbolo fora do alfabeto tambem vai para ERRO (tratado no simulador)

    # transicoes validas: posicoes 0,1,2 → digitos
    for d in DIGITO:
        delta["q0"][d]  = "q1"
        delta["q1"][d]  = "q2"
        delta["q2"][d]  = "q3"
        delta["q4"][d]  = "q5"
        delta["q5"][d]  = "q6"
        delta["q6"][d]  = "q7"
        delta["q8"][d]  = "q9"
        delta["q9"][d]  = "q10"
        delta["q10"][d] = "q11"
        delta["q12"][d] = "q13"
        delta["q13"][d] = "q14"
        delta["q14"][d] = "ERRO"  # cadeia ficou longa

    # pontos separadores
    delta["q3"]["."]  = "q4"
    delta["q7"]["."]  = "q8"
    delta["q11"]["-"] = "q12"

    return delta

DELTA = _build_delta()

def reconhece_cpf(cadeia: str, verbose: bool = False):
    """
    Simula o DFA sobre `cadeia`.
    Retorna (aceito: bool, passos: int, historico: list[tuple])
    """
    estado = Q0
    passos = 0
    historico = [(estado, None, None)]  # (estado_atual, símbolo_lido, próx_estado)

    for simbolo in cadeia:
        # simbolos fora do alfabeto vao direto para ERRO
        if simbolo not in SIGMA:
            proximo = "ERRO"
        else:
            proximo = DELTA[estado].get(simbolo, "ERRO")

        passos += 1
        historico.append((estado, simbolo, proximo))
        estado = proximo

        if estado == "ERRO":
            break

    aceito = estado in ESTADOS_FINAIS

    if verbose:
        _imprimir_execucao(cadeia, historico, aceito, passos)

    return aceito, passos, historico


def _imprimir_execucao(cadeia, historico, aceito, passos):
    print(f"\n{'='*60}")
    print(f"  DFA — CPF   |   Entrada: '{cadeia}'")
    print(f"{'='*60}")
    print(f"  {'Passo':<6} {'Estado Atual':<14} {'Símbolo':<10} {'Próx. Estado':<14}")
    print(f"  {'-'*50}")
    for i, (q, s, qn) in enumerate(historico):
        if s is None:
            print(f"  {'–':<6} {q:<14} {'(início)':<10} {'–':<14}")
        else:
            print(f"  {i:<6} {q:<14} {repr(s):<10} {qn:<14}")
    print(f"  {'-'*50}")
    resultado = "ACEITA ✓" if aceito else "REJEITA ✗"
    print(f"  Resultado: {resultado}   |   Passos: {passos}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/regular.py \"<cadeia>\"")
        print("Exemplo: python src/regular.py \"123.456.789-00\"")
        sys.exit(1)

    entrada = sys.argv[1]
    aceito, passos, _ = reconhece_cpf(entrada, verbose=True)
    sys.exit(0 if aceito else 1)
