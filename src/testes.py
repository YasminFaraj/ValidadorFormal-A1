"""
testes.py — Bateria completa de testes para os três reconhecedores
==================================================================
Lê os arquivos testes/*.txt e executa cada cadeia nos reconhecedores
correspondentes, imprimindo:
  - tabela esperado vs obtido
  - número de passos por cadeia
  - sumário geral

Uso:  python src/testes.py
"""

import os
import sys

# Adiciona src/ ao path para importar os módulos
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)

from livre_contexto import reconhece_balanceado
from recursiva import reconhece_wsharpw
from regular import reconhece_cpf

BASE_DIR   = os.path.join(SRC_DIR, "..", "testes")
SEPARADOR  = "|"

# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def carregar_testes(caminho: str):
    """Lê linhas do arquivo, ignora comentários (#) e vazias."""
    casos = []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            partes = linha.rsplit(SEPARADOR, 1)
            if len(partes) != 2:
                print(f"  [AVISO] Linha mal formatada ignorada: {repr(linha)}")
                continue
            cadeia, esperado = partes[0], partes[1].strip().upper()
            casos.append((cadeia, esperado))
    return casos


def rodar_bateria(nome: str, casos, reconhecedor, verbose_erros: bool = True):
    """Executa o reconhecedor em todos os casos e imprime a tabela."""
    largura = max((len(c) for c, _ in casos), default=10) + 2

    print(f"\n{'─'*70}")
    print(f"  BATERIA: {nome}")
    print(f"{'─'*70}")
    print(f"  {'Cadeia':<{largura}} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} {'Status'}")
    print(f"  {'─'*60}")

    total = 0; acertos = 0
    for cadeia, esperado in casos:
        aceito, passos, _ = reconhecedor(cadeia)
        obtido   = "ACEITA" if aceito else "REJEITA"
        correto  = obtido == esperado
        status   = "✓ OK" if correto else "✗ FALHA"
        total   += 1
        if correto:
            acertos += 1
        print(f"  {repr(cadeia):<{largura}} {esperado:<10} {obtido:<10} {passos:<8} {status}")

    print(f"  {'─'*60}")
    print(f"  Resultado: {acertos}/{total} corretos\n")
    return acertos, total


def rodar_verbose_passo_a_passo(nome: str, casos, reconhecedor):
    """Executa em modo verboso para uma cadeia aceita e uma rejeitada."""
    aceitas  = [(c, e) for c, e in casos if e == "ACEITA"]
    rejeitadas   = [(c, e) for c, e in casos if e == "REJEITA"]

    print(f"\n{'═'*70}")
    print(f"  EXECUÇÃO PASSO A PASSO — {nome}")
    print(f"{'═'*70}")

    for c, _ in aceitas:
        reconhecedor(c, verbose=True)
    for c, _ in rejeitadas:
        reconhecedor(c, verbose=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n" + "═"*70)
    print("  VALIDADOR FORMAL EM TRÊS NÍVEIS — Bateria de Testes")
    print("  Tema 1: CPF (LR) | Balanceamento (LLC) | w#w (R)")
    print("═"*70)

    configuracoes = [
        (
            "Linguagem Regular — CPF (ddd.ddd.ddd-dd)",
            os.path.join(BASE_DIR, "testes_regular.txt"),
            reconhece_cpf,
        ),
        (
            "Linguagem Livre de Contexto — Balanceamento",
            os.path.join(BASE_DIR, "testes_livre_contexto.txt"),
            reconhece_balanceado,
        ),
        (
            "Linguagem Recursiva — w#w",
            os.path.join(BASE_DIR, "testes_recursiva.txt"),
            reconhece_wsharpw,
        ),
    ]

    total_geral = 0; acertos_geral = 0

    for nome, caminho, reconhecedor in configuracoes:
        if not os.path.exists(caminho):
            print(f"\n  [ERRO] Arquivo não encontrado: {caminho}")
            continue

        casos = carregar_testes(caminho)
        acertos, total = rodar_bateria(nome, casos, reconhecedor)
        acertos_geral += acertos
        total_geral   += total

        # Passo a passo
        rodar_verbose_passo_a_passo(nome, casos, reconhecedor)

    print("═"*70)
    print(f"  TOTAL GERAL: {acertos_geral}/{total_geral} corretos")
    print("═"*70 + "\n")

    sys.exit(0 if acertos_geral == total_geral else 1)


if __name__ == "__main__":
    main()
