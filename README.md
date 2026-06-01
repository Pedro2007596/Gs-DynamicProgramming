# 🛰️ OrbitAlert — Monitoramento de Focos de Calor via Satélite

**FIAP | Global Solution 2026 | Dynamic Programming (2ESPY)**

---

## 👥 Integrantes

| Nome | RM |
|------|----|
| Rafael Felix Souza | 565855 |
| Pedro Henrique Sartorelli Ferreira | 563281 |
| Nathália dos Santos Cordeiro | 563072 |
| Bruno Bagattini Fernandes | 562863 |
| Matheus Brasil Borges Sevilha Angelotti | 561456 |

---

## 🌍 Problema Escolhido

O Brasil é um dos países mais vulneráveis a desastres naturais do mundo. Queimadas, enchentes e deslizamentos causam centenas de mortes e bilhões em prejuízos todos os anos. O principal desafio é o **tempo de resposta**: as equipes de defesa civil muitas vezes recebem alertas tarde demais para agir de forma preventiva.

Satélites da NASA detectam focos de calor em tempo real com latência inferior a 3 horas, cobrindo 100% do território nacional. O **OrbitAlert** processa esses dados para organizar e priorizar os alertas de forma eficiente.

---

## 💡 Solução Proposta

Sistema em Python que:

1. Carrega dados reais de focos de calor obtidos via NASA FIRMS (salvos em `alertas.json`)
2. Organiza os alertas em uma **Fila (Queue)** respeitando a ordem cronológica de detecção
3. Permite buscar qualquer alerta pelo ID usando **Busca Binária Recursiva**
4. Oferece um menu interativo para operadores de defesa civil

---

## 📁 Arquivos do Projeto

```
Gs-DynamicProgramming/
├── main.py          # Lógica principal: fila, busca binária, menu
├── alertas.json     # Base de dados com 59 focos de calor reais da NASA
└── README.md        # Documentação do projeto
```

---

## ▶️ Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- Nenhuma biblioteca externa necessária (usa apenas `json` da stdlib)

### Execução

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/Gs-DynamicProgramming.git
cd Gs-DynamicProgramming

# Execute
python main.py
```

---

## 🗂️ Base de Dados

**Fonte:** NASA FIRMS — Fire Information for Resource Management System  
**API:** https://firms.modaps.eosdis.nasa.gov/  
**Satélites:** MODIS (Terra) e VIIRS (SNPP / NOAA-20 / NOAA-21)  
**Registros:** 59 focos de calor detectados no Brasil  
**Arquivo:** `alertas.json`

Campos utilizados:

| Campo | Descrição |
|-------|-----------|
| `latitude` / `longitude` | Coordenadas geográficas do foco |
| `brightness` | Temperatura de brilho (Kelvin) |
| `frp` | Fire Radiative Power — intensidade do foco (MW) |
| `acq_date` / `acq_time` | Data e hora de detecção pelo satélite |
| `satellite` | Satélite que detectou o foco |
| `confidence` | Nível de confiança da detecção |
| `daynight` | D = período diurno, N = período noturno |

---

## 🗃️ Estrutura de Dados — Fila (Queue)

A fila segue o princípio **FIFO (First In, First Out)**: o primeiro alerta a entrar é o primeiro a ser processado.

**Por que Fila e não Pilha?**

- Alertas mais antigos têm prioridade de atendimento
- A telemetria de satélite é sequencial e cronológica
- FIFO garante que nenhum alerta fique "preso" indefinidamente

```
Entrada → [ ID1 | ID2 | ID3 | ... | ID59 ] → Saída (processamento)
            ↑ mais antigo                    ↑ mais recente
```

Operações implementadas:

- `carregar_alertas()` — preenche a fila com todos os registros
- `processar_alerta()` — remove e exibe o primeiro da fila (`pop(0)`)
- `mostrar_alertas()` — exibe todos os alertas sem remover

---

## 🔍 Algoritmo — Busca Binária Recursiva

A busca binária opera sobre a lista **ordenada por ID** e divide o espaço de busca pela metade a cada chamada recursiva.

```
Complexidade:
  Melhor caso : O(1)   — elemento é o meio
  Caso médio  : O(log n)
  Pior caso   : O(log n)

Para 59 alertas: no máximo 6 comparações (log₂ 59 ≈ 5.88)
```

**Lógica da recursão:**

```python
def busca_binaria(lista, alvo, inicio, fim):
    if inicio > fim:          # caso base: não encontrado
        return None
    meio = (inicio + fim) // 2
    if lista[meio]["id"] == alvo:   # caso base: encontrado
        return lista[meio]
    elif alvo < lista[meio]["id"]:  # recursão: metade esquerda
        return busca_binaria(lista, alvo, inicio, meio - 1)
    else:                           # recursão: metade direita
        return busca_binaria(lista, alvo, meio + 1, fim)
```

**Nota:** a busca é feita sobre `alertas_todos` (lista completa original), não sobre `fila_alertas`, para que alertas já processados ainda possam ser localizados.

---

## 🖥️ Funcionalidades do Menu

| Opção | Descrição |
|-------|-----------|
| 1 | Exibir todos os alertas na fila |
| 2 | Buscar alerta por ID (Busca Binária Recursiva) |
| 3 | Processar próximo alerta da fila — FIFO |
| 4 | Ver quantidade de alertas na fila |
| 5 | Sair |

---

## ✅ Requisitos Atendidos

- ✅ Problema alinhado ao tema da Indústria Espacial
- ✅ Dados carregados de arquivo externo `.json` com 59 registros (≥ 30)
- ✅ Dados gerenciados em memória usando **Fila (Queue)** — FIFO
- ✅ **Busca Binária** implementada com **Recursividade**
- ✅ Lógica encapsulada em funções (`def`)
- ✅ Código modular e documentado
- ✅ Repositório no GitHub com README completo
