"""
OrbitAlert — Sistema de Monitoramento de Focos de Calor via Satélite
FIAP | Global Solution 2026 | Dynamic Programming (2ESPY)

Integrantes:
  - Rafael Felix Souza             (RM 565855)
  - Pedro Henrique S. Ferreira     (RM 563281)
  - Nathália dos Santos Cordeiro   (RM 563072)
  - Bruno Bagattini Fernandes      (RM 562863)
  - Matheus Brasil B. S. Angelotti (RM 561456)

Descrição:
  Sistema que processa dados reais de focos de calor detectados por satélites
  da NASA (fonte: NASA FIRMS — Fire Information for Resource Management System).
  Os dados foram obtidos via API pública e salvos em alertas.json para
  processamento local.

  Estrutura de dados utilizada: FILA (Queue) — princípio FIFO (First In, First Out).
  Algoritmo de busca: Busca Binária implementada com Recursividade.

Execução:
  python main.py
"""

import json


# =============================================================================
# CARREGAMENTO DOS DADOS
# Fonte: NASA FIRMS (Fire Information for Resource Management System)
# API: https://firms.modaps.eosdis.nasa.gov/
# Os dados contém focos de calor detectados por satélites MODIS/VIIRS no Brasil.
# =============================================================================

with open("alertas.json", "r", encoding="utf-8") as arquivo:
    alertas = json.load(arquivo)

# =============================================================================
# ESTRUTURA DE DADOS: FILA (Queue)
# A fila segue o princípio FIFO — o primeiro alerta a entrar é o primeiro
# a ser processado, garantindo que alertas mais antigos sejam atendidos
# antes dos mais recentes.
# =============================================================================

fila_alertas = []       # Fila de alertas aguardando processamento
alertas_todos = []      # Lista completa (usada para busca binária — não sofre pop)


# =============================================================================
# FUNÇÕES
# =============================================================================

def carregar_alertas(lista):
    """
    Carrega os alertas da lista original para a fila e para a lista completa.
    Atribui um ID sequencial a cada alerta.

    Parâmetros:
        lista (list): Lista de dicionários carregada do arquivo JSON.
    """
    for i, alerta in enumerate(lista, start=1):
        alerta["id"] = i
        fila_alertas.append(alerta)
        alertas_todos.append(alerta)


def exibir_alerta(alerta):
    """
    Exibe os campos de um alerta no console de forma formatada.

    Parâmetros:
        alerta (dict): Dicionário com os dados do alerta.
    """
    periodo = "Diurno" if alerta.get("daynight") == "D" else "Noturno"

    print(f"""
  ID         : {alerta['id']}
  Satélite   : {alerta.get('satellite', 'N/A')}
  Latitude   : {alerta['latitude']}
  Longitude  : {alerta['longitude']}
  Brilho     : {alerta['brightness']} K
  FRP        : {alerta.get('frp', 'N/A')} MW
  Confiança  : {alerta.get('confidence', 'N/A')}%
  Data       : {alerta['acq_date']}
  Hora       : {alerta['acq_time']}
  Período    : {periodo}
""")

def mostrar_alertas():
    """
    Exibe todos os alertas que ainda estão na fila, sem removê-los.
    Caso a fila esteja vazia, exibe uma mensagem informativa.
    """
    if len(fila_alertas) == 0:
        print("\n  Nenhum alerta na fila.")
        return

    print(f"\n  {len(fila_alertas)} alerta(s) na fila:\n")
    print("  " + "-" * 50)

    for alerta in fila_alertas:
        exibir_alerta(alerta)
        print("  " + "-" * 50)


def processar_alerta():
    """
    Remove e exibe o primeiro alerta da fila (princípio FIFO).
    O alerta processado não retorna mais à fila, mas permanece
    disponível para busca na lista completa (alertas_todos).
    """
    if len(fila_alertas) == 0:
        print("\n  Fila vazia. Nenhum alerta para processar.")
        return

    # Remove o primeiro elemento da fila — FIFO
    alerta = fila_alertas.pop(0)

    print("\n  Alerta processado e removido da fila:")
    print("  " + "-" * 50)
    exibir_alerta(alerta)
    print(f"  Alertas restantes na fila: {len(fila_alertas)}")


def busca_binaria(lista, alvo, inicio, fim):
    """
    Busca Binária RECURSIVA para localizar um alerta pelo ID.

    A lista deve estar ordenada por ID. A cada chamada recursiva,
    o espaço de busca é dividido ao meio, alcançando O(log n).

    Casos base:
      - inicio > fim → elemento não encontrado, retorna None
      - lista[meio] == alvo → elemento encontrado, retorna o alerta

    Parâmetros:
        lista  (list): Lista de alertas ordenada por ID.
        alvo   (int):  ID do alerta procurado.
        inicio (int):  Índice inicial do intervalo de busca.
        fim    (int):  Índice final do intervalo de busca.

    Retorno:
        dict | None: O alerta encontrado, ou None se não existir.
    """
    # Caso base: intervalo esgotado — alerta não existe na lista
    if inicio > fim:
        return None

    # Calcula o índice do meio do intervalo atual
    meio = (inicio + fim) // 2

    # Caso base: alerta encontrado no meio
    if lista[meio]["id"] == alvo:
        return lista[meio]

    # Recursão: alvo está na metade esquerda
    elif alvo < lista[meio]["id"]:
        return busca_binaria(lista, alvo, inicio, meio - 1)

    # Recursão: alvo está na metade direita
    else:
        return busca_binaria(lista, alvo, meio + 1, fim)


def buscar_por_id():
    """
    Solicita um ID ao usuário, ordena a lista completa de alertas
    e executa a busca binária recursiva.

    A busca é feita sobre alertas_todos (lista completa), e não sobre
    a fila_alertas, para que alertas já processados ainda possam ser
    encontrados.
    """
    try:
        busca_id = int(input("\n  Digite o ID do alerta (1 a {}): ".format(len(alertas_todos))))
    except ValueError:
        print("\n  Entrada inválida. Digite apenas números inteiros.")
        return

    # Ordena por ID antes de aplicar a busca binária (pré-requisito do algoritmo)
    lista_ordenada = sorted(alertas_todos, key=lambda x: x["id"])

    resultado = busca_binaria(lista_ordenada, busca_id, 0, len(lista_ordenada) - 1)

    if resultado:
        print("\n  Alerta encontrado:")
        print("  " + "-" * 50)
        exibir_alerta(resultado)
    else:
        print(f"\n  Alerta com ID {busca_id} não encontrado.")


def menu():
    """
    Função principal — inicializa o sistema e controla o loop do menu.

    Valida o mínimo de 30 registros, carrega os alertas na fila
    e apresenta as opções disponíveis ao usuário.
    """
    # Validação do mínimo de registros exigido
    if len(alertas) < 30:
        print(f"\n  ERRO: Apenas {len(alertas)} registros encontrados. Mínimo exigido: 30.")
        return

    carregar_alertas(alertas)

    print("\n" + "=" * 54)
    print("   OrbitAlert — Monitoramento de Focos de Calor")
    print("   FIAP | Global Solution 2026")
    print("=" * 54)
    print(f"\n  {len(fila_alertas)} alertas carregados da NASA FIRMS.")
    print("  Estrutura: Fila (Queue) — FIFO")
    print("  Busca: Busca Binária Recursiva\n")

    while True:

        print("""
  ┌─────────────────────────────────────────┐
  │  1 - Mostrar alertas na fila            │
  │  2 - Buscar alerta por ID               │
  │  3 - Processar próximo alerta (FIFO)    │
  │  4 - Mostrar tamanho da fila            │
  │  5 - Sair                               │
  └─────────────────────────────────────────┘""")

        opcao = input("\n  Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_alertas()

        elif opcao == "2":
            buscar_por_id()

        elif opcao == "3":
            processar_alerta()

        elif opcao == "4":
            print(f"\n  Alertas aguardando na fila: {len(fila_alertas)}")
            print(f"  Total de alertas carregados: {len(alertas_todos)}")

        elif opcao == "5":
            print("\n  Encerrando OrbitAlert. Até logo!\n")
            break

        else:
            print("\n  Opção inválida. Escolha entre 1 e 5.")


# =============================================================================
# PONTO DE ENTRADA
# =============================================================================

menu()
