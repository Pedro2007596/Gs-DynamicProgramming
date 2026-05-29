import json

with open("alertas.json", "r", encoding="utf-8") as arquivo:
    alertas = json.load(arquivo)

fila_alertas = []

def carregar_alertas(alertas):

    for alerta in alertas:
        fila_alertas.append(alerta)

def processar_alerta():

    if len(fila_alertas) == 0:
        print("\nFila vazia.")
        return

    alerta = fila_alertas.pop(0)

    print(f"""
ID: {alerta['id']}
Latitude: {alerta['latitude']}
Longitude: {alerta['longitude']}
Intensidade: {alerta['brightness']}
Data: {alerta['data']}
Hora: {alerta['hora']}
""")

def mostrar_alertas():

    if len(fila_alertas) == 0:
        print("\nNenhum alerta na fila.")
        return

    for alerta in fila_alertas:

        print(f"""
ID: {alerta['id']}
Latitude: {alerta['latitude']}
Longitude: {alerta['longitude']}
Intensidade: {alerta['brightness']}
Data: {alerta['data']}
Hora: {alerta['hora']}
------------------------------
""")

def busca_binaria(lista, alvo, inicio, fim):

    if inicio > fim:
        return None

    meio = (inicio + fim) // 2

    if lista[meio]["id"] == alvo:
        return lista[meio]

    elif alvo < lista[meio]["id"]:

        return busca_binaria(
            lista,
            alvo,
            inicio,
            meio - 1
        )

    else:

        return busca_binaria(
            lista,
            alvo,
            meio + 1,
            fim
        )

def menu():

    if len(alertas) < 30:
        print("Menos de 30 registros encontrados.")
        return

    carregar_alertas(alertas)

    print(f"\n{len(fila_alertas)} alertas carregados.\n")

    while True:

        print("""
1 - Mostrar alertas
2 - Buscar alerta por ID
3 - Processar primeiro alerta
4 - Mostrar tamanho da fila
5 - Sair
""")

        opcao = input("Escolha: ")

        if opcao == "1":

            mostrar_alertas()

        elif opcao == "2":

            try:

                busca_id = int(input("Digite o ID do alerta: "))

                lista_ordenada = sorted(
                    fila_alertas,
                    key=lambda x: x["id"]
                )

                resultado = busca_binaria(
                    lista_ordenada,
                    busca_id,
                    0,
                    len(lista_ordenada) - 1
                )

                if resultado:

                    print(f"""
ID: {resultado['id']}
Latitude: {resultado['latitude']}
Longitude: {resultado['longitude']}
Intensidade: {resultado['brightness']}
Data: {resultado['data']}
Hora: {resultado['hora']}
""")

                else:

                    print("\nAlerta não encontrado.")

            except:

                print("\nDigite um número válido.")

        elif opcao == "3":

            processar_alerta()

        elif opcao == "4":

            print(f"\nQuantidade na fila: {len(fila_alertas)}")

        elif opcao == "5":

            print("\nSaindo...")
            break

        else:

            print("\nOpção inválida.")

menu()