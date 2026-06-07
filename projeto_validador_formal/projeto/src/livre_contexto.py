"""
Reconhecedor de Linguagem Livre de Contexto - Expressões com parênteses balanceados
=====================================================================================
Linguagem: L = { w ∈ Σ* | os símbolos de abertura e fechamento em w
                          estão corretamente balanceados e aninhados }
Alfabeto: Σ = { '(', ')', '[', ']', '{', '}',
                 qualquer letra/dígito como símbolo neutro }
Modelo: PDA (Autômato com Pilha) implementado manualmente.

GLC equivalente (simplificada para {( )}, generalizável):
  S → ε | (S) | [S] | {S} | SS | x S  (onde x é símbolo neutro)

O PDA lê a cadeia símbolo a símbolo e mantém uma pilha explícita.

ATENÇÃO: Nenhuma biblioteca de parsing é usada como reconhecedor.
"""

import sys

# definicao formal do PDA

ESTADOS = {"q0", "q_aceita", "q_rejeita"}

SIGMA = set("()[]{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 +-*/=<>!@#$%^&_|~;:,.")

GAMMA = {"(", "[", "{", "Z0"}  # alfabeto da pilha; Z0 = marcador de fundo

Q0 = "q0"
ESTADOS_FINAIS = {"q_aceita"}

# Mapeamento: abre → fecha
ABRE  = {"(": ")", "[": "]", "{": "}"}
FECHA = {v: k for k, v in ABRE.items()}

def reconhece_balanceado(cadeia: str, verbose: bool = False):
    """
    Simula o PDA sobre `cadeia`.
    Retorna (aceito: bool, passos: int, historico: list[dict])
    """
    pilha = ["Z0"]   # fundo da pilha
    passos = 0
    historico = []

    estado = Q0

    for simbolo in cadeia:
        topo_antes = pilha[-1] if pilha else "∅"

        if simbolo in ABRE:
            pilha.append(simbolo)
            acao = f"PUSH '{simbolo}'"
            passos += 1
            historico.append({
                "estado": estado,
                "simbolo": simbolo,
                "topo_antes": topo_antes,
                "acao": acao,
                "pilha": list(pilha),
                "passo": passos,
            })

        elif simbolo in FECHA:
            esperado = FECHA[simbolo] 
            passos += 1
            if len(pilha) > 0 and pilha[-1] == esperado:
                pilha.pop()
                acao = f"POP '{esperado}'"
                historico.append({
                    "estado": estado,
                    "simbolo": simbolo,
                    "topo_antes": topo_antes,
                    "acao": acao,
                    "pilha": list(pilha),
                    "passo": passos,
                })
            else:
                #rejeita
                acao = f"ERRO: esperado '{ABRE.get(pilha[-1], '?')}' mas encontrou '{simbolo}'"
                historico.append({
                    "estado": "q_rejeita",
                    "simbolo": simbolo,
                    "topo_antes": topo_antes,
                    "acao": acao,
                    "pilha": list(pilha),
                    "passo": passos,
                })
                estado = "q_rejeita"
                break
        else:
            passos += 1
            acao = "SKIP (neutro)"
            historico.append({
                "estado": estado,
                "simbolo": simbolo,
                "topo_antes": topo_antes,
                "acao": acao,
                "pilha": list(pilha),
                "passo": passos,
            })

    # pilha deve conter apenas Z0 para ser aceita
    if estado != "q_rejeita":
        if pilha == ["Z0"]:
            estado = "q_aceita"
        else:
            estado = "q_rejeita"

    aceito = estado in ESTADOS_FINAIS

    if verbose:
        _imprimir_execucao(cadeia, historico, aceito, passos, pilha)

    return aceito, passos, historico


def _imprimir_execucao(cadeia, historico, aceito, passos, pilha_final):
    print(f"\n{'='*70}")
    print(f"  PDA — Balanceamento   |   Entrada: '{cadeia}'")
    print(f"{'='*70}")
    print(f"  {'Passo':<6} {'Estado':<12} {'Símbolo':<10} {'Topo antes':<12} {'Ação':<30} {'Pilha depois'}")
    print(f"  {'-'*80}")
    for h in historico:
        pilha_str = str(h["pilha"])
        print(f"  {h['passo']:<6} {h['estado']:<12} {repr(h['simbolo']):<10} "
              f"{repr(h['topo_antes']):<12} {h['acao']:<30} {pilha_str}")
    print(f"  {'-'*80}")
    resultado = "ACEITA ✓" if aceito else "REJEITA ✗"
    print(f"  Resultado: {resultado}   |   Passos: {passos}")
    print(f"  Pilha final: {pilha_final}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/livre_contexto.py \"<cadeia>\"")
        print("Exemplo: python src/livre_contexto.py \"((x+y)*z)\"")
        sys.exit(1)

    entrada = sys.argv[1]
    aceito, passos, _ = reconhece_balanceado(entrada, verbose=True)
    sys.exit(0 if aceito else 1)
