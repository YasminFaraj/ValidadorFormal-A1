"""
Reconhecedor de Linguagem Recursiva — Cópia de cadeia: L = { w#w | w ∈ {0,1}* }
=================================================================================
Linguagem: L = { w#w | w ∈ {0,1}* }
  - A cadeia deve conter exatamente um '#' no meio.
  - A subcadeia à esquerda de '#' deve ser idêntica à subcadeia à direita.
  - Exemplos aceitos : 0#0, 101#101, ε#ε (vazio#vazio → "#")
  - Exemplos rejeit. : 01#10, 0#00, ##, 1#0

Alfabeto de entrada: Σ = {0, 1, #}
Alfabeto da fita:   Γ = {0, 1, #, X, Y, B}   (X marca 0 processado,
                                                Y marca 1 processado,
                                                B = branco)

Modelo: Máquina de Turing de uma fita, implementada manualmente.

Estratégia da MT:
  Fase 1) Localiza o '#'.
          Se não houver '#' → rejeita.
  Fase 2) Repete até que não haja mais dígitos não-marcados à esquerda do '#':
    a) Lê o primeiro símbolo não-marcado à esquerda de '#' (0 ou 1).
       Marca-o com X (se 0) ou Y (se 1).
    b) Pula o '#'.
    c) Na porção direita, avança pelo mesmo número de símbolos já marcados,
       depois lê o primeiro símbolo não-marcado.
       Se coincide com o lido em (a) → marca com X/Y.
       Caso contrário → rejeita.
    d) Volta ao início da fita para repetir.
  Fase 3) Quando não há mais dígitos não-marcados à esquerda:
          Verifica se também não há dígitos não-marcados à direita → aceita.
          Caso contrário → rejeita.

ATENÇÃO: A contagem de passos segue a definição do professor:
  um passo = um movimento da cabeça (leitura + possível escrita + deslocamento).
"""

import sys

# ---------------------------------------------------------------------------
# Definição formal da MT
# ---------------------------------------------------------------------------

BRANCO = "B"

# Símbolos de entrada
SIGMA_ENTRADA = {"0", "1", "#"}

# Símbolos da fita (inclui marcadores e branco)
GAMMA = {"0", "1", "#", "X", "Y", BRANCO}

# Direções
DIREITA = "R"
ESQUERDA = "L"
PARADO = "N"  # não usado, mas definido por completude

# Estados
ESTADOS = {
    "q_inicio",         # estado inicial: vai buscar o '#'
    "q_busca_hash",     # avança procurando '#'
    "q_leu_0_esq",      # leu um 0 não-marcado à esquerda
    "q_leu_1_esq",      # leu um 1 não-marcado à esquerda
    "q_pula_dir_0",     # pulando marcados+# para encontrar correspondente de 0
    "q_pula_dir_1",     # pulando marcados+# para encontrar correspondente de 1
    "q_volta_inicio",   # voltando ao início para nova iteração
    "q_verifica_dir",   # verificando se direita está toda marcada
    "q_aceita",
    "q_rejeita",
}

ESTADO_INICIAL = "q_inicio"
ESTADOS_FINAIS = {"q_aceita"}

# ---------------------------------------------------------------------------
# Simulador da MT
# ---------------------------------------------------------------------------

def reconhece_wsharpw(cadeia: str, verbose: bool = False):
    """
    Simula a MT sobre `cadeia`.
    Retorna (aceito: bool, passos: int, historico: list[dict])
    """
    # Inicializa a fita
    if cadeia == "":
        # Cadeia vazia: rejeita (não contém '#')
        return False, 0, []

    fita = list(cadeia) + [BRANCO]
    cabeca = 0
    estado = ESTADO_INICIAL
    passos = 0
    historico = []

    def snapshot():
        fita_str = "".join(fita).rstrip(BRANCO) or BRANCO
        return {
            "passo": passos,
            "estado": estado,
            "fita": fita_str,
            "cabeca": cabeca,
            "lendo": fita[cabeca] if cabeca < len(fita) else BRANCO,
        }

    MAX_PASSOS = 100_000  # guarda-chuva contra loops infinitos

    while estado not in ("q_aceita", "q_rejeita") and passos < MAX_PASSOS:
        simbolo = fita[cabeca] if cabeca < len(fita) else BRANCO
        historico.append(snapshot())

        novo_simbolo = simbolo  # por padrão não escreve
        novo_estado  = estado
        movimento    = DIREITA

        # ------------------------------------------------------------------ #
        #  Tabela de transição                                                 #
        # ------------------------------------------------------------------ #

        if estado == "q_inicio":
            # Marca o início; vai para q_busca_hash procurando '#'
            if simbolo == BRANCO:
                # Fita vazia → rejeita
                novo_estado = "q_rejeita"; movimento = PARADO
            elif simbolo == "#":
                # '#' na posição 0: w é ε — vai verificar se direita também é ε
                novo_estado = "q_verifica_dir"; movimento = DIREITA
            elif simbolo in ("0", "1"):
                novo_estado = "q_busca_hash"; movimento = PARADO  # fica no lugar, muda estado
            elif simbolo in ("X", "Y"):
                novo_estado = "q_busca_hash"; movimento = PARADO

        elif estado == "q_busca_hash":
            # Procura o primeiro símbolo não-marcado à esquerda do '#'
            if simbolo == "0":
                novo_simbolo = "X"; novo_estado = "q_leu_0_esq"; movimento = DIREITA
            elif simbolo == "1":
                novo_simbolo = "Y"; novo_estado = "q_leu_1_esq"; movimento = DIREITA
            elif simbolo in ("X", "Y"):
                movimento = DIREITA; novo_estado = "q_busca_hash"
            elif simbolo == "#":
                # Não há mais dígitos não-marcados à esquerda → verifica direita
                novo_estado = "q_verifica_dir"; movimento = DIREITA
            else:
                novo_estado = "q_rejeita"; movimento = PARADO

        elif estado == "q_leu_0_esq":
            # Avança até o '#', então passa para direita
            if simbolo in ("0", "1", "X", "Y"):
                movimento = DIREITA
            elif simbolo == "#":
                novo_estado = "q_pula_dir_0"; movimento = DIREITA
            else:
                novo_estado = "q_rejeita"; movimento = PARADO

        elif estado == "q_leu_1_esq":
            if simbolo in ("0", "1", "X", "Y"):
                movimento = DIREITA
            elif simbolo == "#":
                novo_estado = "q_pula_dir_1"; movimento = DIREITA
            else:
                novo_estado = "q_rejeita"; movimento = PARADO

        elif estado == "q_pula_dir_0":
            # Na parte direita: pula marcados, lê o primeiro não-marcado
            if simbolo in ("X", "Y"):
                movimento = DIREITA
            elif simbolo == "0":
                novo_simbolo = "X"; novo_estado = "q_volta_inicio"; movimento = ESQUERDA
            elif simbolo in ("1", BRANCO):
                novo_estado = "q_rejeita"; movimento = PARADO
            else:
                novo_estado = "q_rejeita"; movimento = PARADO

        elif estado == "q_pula_dir_1":
            if simbolo in ("X", "Y"):
                movimento = DIREITA
            elif simbolo == "1":
                novo_simbolo = "Y"; novo_estado = "q_volta_inicio"; movimento = ESQUERDA
            elif simbolo in ("0", BRANCO):
                novo_estado = "q_rejeita"; movimento = PARADO
            else:
                novo_estado = "q_rejeita"; movimento = PARADO

        elif estado == "q_volta_inicio":
            # Volta ao início da fita para nova rodada
            if simbolo != BRANCO and cabeca > 0:
                movimento = ESQUERDA
            else:
                novo_estado = "q_busca_hash"; movimento = DIREITA if cabeca == 0 else PARADO

        elif estado == "q_verifica_dir":
            # Verifica se tudo à direita do '#' já está marcado
            if simbolo in ("X", "Y"):
                movimento = DIREITA
            elif simbolo == BRANCO:
                novo_estado = "q_aceita"; movimento = PARADO
            else:
                novo_estado = "q_rejeita"; movimento = PARADO

        # ------------------------------------------------------------------ #
        #  Aplica a transição                                                  #
        # ------------------------------------------------------------------ #

        # Garante tamanho da fita
        while cabeca >= len(fita):
            fita.append(BRANCO)

        fita[cabeca] = novo_simbolo
        estado = novo_estado
        passos += 1  # um passo = leitura + possível escrita + movimento

        if movimento == DIREITA:
            cabeca += 1
            while cabeca >= len(fita):
                fita.append(BRANCO)
        elif movimento == ESQUERDA:
            if cabeca > 0:
                cabeca -= 1
        # PARADO: cabeça não se move

    historico.append(snapshot())  # estado final

    aceito = estado in ESTADOS_FINAIS

    if verbose:
        _imprimir_execucao(cadeia, historico, aceito, passos)

    return aceito, passos, historico


def _imprimir_execucao(cadeia, historico, aceito, passos):
    print(f"\n{'='*80}")
    print(f"  MT — w#w   |   Entrada: '{cadeia}'")
    print(f"{'='*80}")
    print(f"  {'Passo':<6} {'Estado':<18} {'Lendo':<8} {'Fita (resumo)'}")
    print(f"  {'-'*70}")
    for h in historico:
        fita_display = list(h["fita"])
        pos = h["cabeca"]
        # Marca posição da cabeça com colchetes
        if pos < len(fita_display):
            fita_display[pos] = f"[{fita_display[pos]}]"
        fita_str = "".join(fita_display)
        print(f"  {h['passo']:<6} {h['estado']:<18} {repr(h['lendo']):<8} {fita_str}")
    print(f"  {'-'*70}")
    resultado = "ACEITA ✓" if aceito else "REJEITA ✗"
    print(f"  Resultado: {resultado}   |   Passos: {passos}")
    print(f"{'='*80}\n")


# ---------------------------------------------------------------------------
# Modo autônomo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/recursiva.py \"<cadeia>\"")
        print("Exemplo: python src/recursiva.py \"101#101\"")
        sys.exit(1)

    entrada = sys.argv[1]
    aceito, passos, _ = reconhece_wsharpw(entrada, verbose=True)
    sys.exit(0 if aceito else 1)
