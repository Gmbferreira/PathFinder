# PathFinder A* - Resolvendo Labirintos 2D

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Descrição do Projeto

Este projeto implementa o **Algoritmo A*** para encontrar o menor caminho em labirintos 2D, simulando um robô de resgate que precisa navegar de um ponto inicial **S** até um ponto final **E**, evitando obstáculos e considerando diferentes custos de terreno.

O projeto foi desenvolvido como parte da disciplina de Teoria dos Grafos e demonstra a aplicação prática de algoritmos de busca informada em problemas de pathfinding.

## 🎯 Objetivo

Implementar o Algoritmo A* para:
- Encontrar o **menor caminho** entre dois pontos em um labirinto 2D
- Evitar obstáculos durante a navegação
- Considerar diferentes **custos de movimento** (terrenos com pesos variados)
- Suportar movimentos **ortogonais** (cima, baixo, esquerda, direita) e **diagonais**
- Visualizar o processo de exploração e o caminho encontrado

## 🚀 Funcionalidades

### Principais
- ✅ **Algoritmo A*** completo com heurística de Manhattan e Euclidiana
- ✅ **Validação automática** de labirintos (verificação de S, E, estrutura)
- ✅ **Suporte a movimentos diagonais** com custo √2
- ✅ **Terrenos com pesos diferentes** (ex: custo 1, 2, 3... para diferentes tipos de terreno)
- ✅ **Visualização em console** com cores e símbolos
- ✅ **Interface gráfica (GUI)** com Pygame mostrando exploração em tempo real
- ✅ **Estatísticas detalhadas** (nós explorados, custo total, eficiência)
- ✅ **Tratamento de labirintos sem solução**

### Extras Implementados
- 🎨 Visualização gráfica animada com Pygame
- 🎨 Cores diferentes para terrenos com custos variados
- 📊 Estatísticas completas de desempenho
- 🔧 Interface de linha de comando (CLI) com múltiplas opções
- 📦 5 exemplos de labirintos pré-configurados

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Pygame** - Interface gráfica
- **NumPy** - Manipulação de matrizes (opcional)

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/pathfinder-astar.git
cd pathfinder-astar
```

2. **Crie um ambiente virtual (recomendado)**

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

### Execução Básica

**macOS/Linux:**
```bash
# Executar exemplo padrão (Exemplo 1)
python3 main.py

# Executar exemplo específico (1-5)
python3 main.py --example 2

# Permitir movimentos diagonais
python3 main.py --diagonal

# Desabilitar GUI (apenas console)
python3 main.py --no-gui

# Usar heurística Euclidiana
python3 main.py --euclidean

# Combinar opções
python3 main.py --example 3 --diagonal --euclidean
```

**Windows:**
```cmd
# Executar exemplo padrão (Exemplo 1)
python main.py

# Executar exemplo específico (1-5)
python main.py --example 2

# Permitir movimentos diagonais
python main.py --diagonal

# Desabilitar GUI (apenas console)
python main.py --no-gui

# Usar heurística Euclidiana
python main.py --euclidean

# Combinar opções
python main.py --example 3 --diagonal --euclidean
```

### Carregar Labirinto de Arquivo

**macOS/Linux:**
```bash
python3 main.py --file meu_labirinto.txt
```

**Windows:**
```cmd
python main.py --file meu_labirinto.txt
```

### Formato do Arquivo de Labirinto

Crie um arquivo `.txt` com o seguinte formato:
```
S 0 1 0 0
0 0 1 0 1
1 0 1 0 0
1 0 0 E 1
```

**Legenda:**
- `S` = Ponto inicial (Start)
- `E` = Ponto final (End)
- `0` = Célula livre (custo 1)
- `1` = Obstáculo (bloqueia passagem)
- `2`, `3`, `4`... = Células com custo maior (terrenos difíceis)

### Opções da Linha de Comando

```
Opções:
  -h, --help            Mostra mensagem de ajuda
  --example N, -e N     Executa exemplo N (1-5)
  --diagonal, -d        Permite movimentos diagonais
  --no-gui, -ng         Desabilita interface gráfica
  --euclidean, -eu      Usa distância Euclidiana
  --file FILE, -f FILE  Carrega labirinto de arquivo
```

## 📚 Exemplos Incluídos

### Exemplo 1: Labirinto Simples (4x5)
Labirinto do enunciado do projeto
```
S 0 1 0 0
0 0 1 0 1
1 0 1 0 0
1 0 0 E 1
```

### Exemplo 2: Labirinto Médio (8x8)
Mais complexo com múltiplos caminhos possíveis

### Exemplo 3: Labirinto Grande (12x12)
Desafio maior com mais obstáculos

### Exemplo 4: Terrenos com Pesos Variados
Demonstra células com diferentes custos de travessia

### Exemplo 5: Sem Solução
Labirinto onde não existe caminho possível

## 🧠 Como Funciona o Algoritmo A*

O **Algoritmo A*** é um algoritmo de busca informada que encontra o menor caminho entre dois pontos usando uma função de avaliação:

```
f(n) = g(n) + h(n)
```

Onde:
- **g(n)** = Custo real do caminho do início até o nó atual
- **h(n)** = Estimativa heurística do custo do nó atual até o objetivo
- **f(n)** = Custo total estimado do caminho passando por n

### Heurísticas Implementadas

#### 1. Distância de Manhattan (Padrão)
Ideal para movimentos ortogonais (cima, baixo, esquerda, direita):

```
h(n) = |x_atual - x_final| + |y_atual - y_final|
```

**Exemplo:** Da posição (0,0) até (3,3):
```
h = |0 - 3| + |0 - 3| = 3 + 3 = 6
```

#### 2. Distância Euclidiana (Opcional)
Melhor para movimentos diagonais:

```
h(n) = √((x_atual - x_final)² + (y_atual - y_final)²)
```

**Exemplo:** Da posição (0,0) até (3,3):
```
h = √((0-3)² + (0-3)²) = √(9 + 9) = √18 ≈ 4.24
```

### Passo a Passo do Algoritmo

1. **Inicialização**
   - Adiciona o nó inicial à lista aberta (nós a explorar)
   - Calcula f(n) = g(n) + h(n) para o nó inicial

2. **Loop Principal**
   - Seleciona o nó com menor f(n) da lista aberta
   - Se for o objetivo → **sucesso**, reconstrói o caminho
   - Se não:
     - Marca como explorado (lista fechada)
     - Explora todos os vizinhos válidos
     - Para cada vizinho:
       - Calcula novo g(n) = g(atual) + custo_movimento × peso_célula
       - Calcula h(n) usando heurística escolhida
       - Se é um caminho melhor, atualiza e adiciona à lista aberta

3. **Resultado**
   - **Caminho encontrado**: Retorna lista de coordenadas e custo total
   - **Sem solução**: Retorna None (lista aberta vazia)

### Exemplo Prático

Dado o labirinto:
```
S 0 1 0 0
0 0 1 0 1
1 0 1 0 0
1 0 0 E 1
```

**Exploração:**
1. Inicia em S(0,0), g=0, h=6, f=6
2. Explora vizinhos: (0,1) e (1,0)
3. Escolhe nó com menor f
4. Continua até encontrar E(3,3)

**Caminho encontrado:**
```
[s(0,0), (1,0), (1,1), (2,1), (3,1), (3,2), e(3,3)]
Custo total: 7.0
```

### Por que A* é Eficiente?

- ✅ **Admissível**: Sempre encontra o caminho ótimo se a heurística for admissível (nunca superestima)
- ✅ **Completo**: Sempre encontra solução se existir
- ✅ **Otimamente eficiente**: Explora o mínimo de nós necessários
- ✅ **Informado**: Usa conhecimento do problema (heurística) para guiar a busca

## 📂 Estrutura do Projeto

```
TrabalhoGrupo1/
│
├── src/
│   ├── __init__.py           # Inicialização do pacote
│   ├── pathfinder.py         # Núcleo do algoritmo A* (Pedro Carbonaro)
│   ├── maze.py               # Parser e validação (Bruna Barbosa)
│   ├── visualizer.py         # Visualização console (Rafael Marques)
│   └── gui.py                # Interface gráfica (Guilherme Martini)
│
├── examples/
│   ├── __init__.py
│   └── maze_examples.py      # Exemplos pré-definidos (Felipe Evangelista)
│
├── tests/
│   └── (testes unitários)
│
├── main.py                   # Programa principal (Felipe Evangelista)
├── requirements.txt          # Dependências
├── .gitignore               # Arquivos ignorados pelo Git
└── README.md                # Esta documentação
```

## 👥 Divisão de Trabalho

### Pedro Carbonaro: Algoritmo A*
**Arquivo:** `src/pathfinder.py`
- Implementação do algoritmo A*
- Classe Node
- Funções heurísticas (Manhattan e Euclidiana)
- Suporte a movimentos diagonais
- Callback para visualização

### Bruna Barbosa: Parser e Validação
**Arquivo:** `src/maze.py`
- Classe Maze
- Leitura e parsing de labirintos
- Validação de estrutura (S, E, dimensões)
- Conversão entre formatos
- Estatísticas do labirinto

### Rafael Marques: Visualização Console
**Arquivo:** `src/visualizer.py`
- Funções de impressão formatada
- Visualização colorida no terminal
- Exibição de estatísticas
- Destaque de caminho e exploração

### Guilherme Martini: Interface Gráfica
**Arquivo:** `src/gui.py`
- Interface gráfica com Pygame
- Visualização animada do algoritmo
- Cores para diferentes pesos de terreno
- Painel de informações e legenda

### Felipe Evangelista: Integração e Exemplos
**Arquivos:** `main.py`, `examples/maze_examples.py`
- Programa principal com CLI
- 5 exemplos de labirintos
- Integração de todos os módulos
- Documentação e testes

## 🔄 Workflow Git e Branches

### Estratégia de Branches

```
main (branch principal)
├── feature/pathfinder-algorithm  (Pedro Carbonaro)
├── feature/maze-parser           (Bruna Barbosa)
├── feature/console-visualizer    (Rafael Marques)
├── feature/gui-pygame            (Guilherme Martini)
└── feature/main-integration      (Felipe Evangelista)
```

### Comandos Git para Cada Integrante

#### Pedro Carbonaro - Algoritmo A*
```bash
git checkout -b feature/pathfinder-algorithm
# ... desenvolver pathfinder.py
git add src/pathfinder.py
git commit -m "Implementa algoritmo A* com heurísticas Manhattan e Euclidiana"
git push origin feature/pathfinder-algorithm
# Criar Pull Request para main
```

#### Bruna Barbosa - Parser
```bash
git checkout -b feature/maze-parser
# ... desenvolver maze.py
git add src/maze.py
git commit -m "Implementa parser e validação de labirintos"
git push origin feature/maze-parser
# Criar Pull Request para main
```

#### Rafael Marques - Visualização Console
```bash
git checkout -b feature/console-visualizer
# ... desenvolver visualizer.py
git add src/visualizer.py
git commit -m "Adiciona visualização colorida no console"
git push origin feature/console-visualizer
# Criar Pull Request para main
```

#### Guilherme Martini - GUI
```bash
git checkout -b feature/gui-pygame
# ... desenvolver gui.py
git add src/gui.py
git commit -m "Implementa interface gráfica com Pygame"
git push origin feature/gui-pygame
# Criar Pull Request para main
```

#### Felipe Evangelista - Integração
```bash
git checkout -b feature/main-integration
# ... desenvolver main.py e examples
git add main.py examples/maze_examples.py
git commit -m "Integra módulos e adiciona exemplos de labirintos"
git push origin feature/main-integration
# Criar Pull Request para main
```

### Ordem de Merge Recomendada

1. **Primeiro:** `feature/maze-parser` → `main`
2. **Segundo:** `feature/pathfinder-algorithm` → `main`
3. **Terceiro:** `feature/console-visualizer` → `main`
4. **Quarto:** `feature/gui-pygame` → `main`
5. **Quinto:** `feature/main-integration` → `main`

## 🧪 Validação e Testes

### Casos de Teste Importantes

1. ✅ **Labirinto simples** - Verifica funcionamento básico
2. ✅ **Labirinto complexo** - Testa eficiência
3. ✅ **Labirinto sem solução** - Valida detecção
4. ✅ **Movimentos diagonais** - Confirma cálculo de √2
5. ✅ **Terrenos com pesos** - Verifica consideração de custos
6. ✅ **Validação de entrada** - Testa tratamento de erros

### Executar Todos os Exemplos

**macOS/Linux:**
```bash
python3 main.py --example 1
python3 main.py --example 2
python3 main.py --example 3
python3 main.py --example 4
python3 main.py --example 5
```

**Windows:**
```cmd
python main.py --example 1
python main.py --example 2
python main.py --example 3
python main.py --example 4
python main.py --example 5
```

## 📊 Exemplo de Saída

```
══════════════════════════════════════════════════════════════════════
          PATHFINDER A* - ENCONTRANDO O MENOR CAMINHO
══════════════════════════════════════════════════════════════════════

Configurações:
  • Movimentos diagonais: Não
  • Heurística: Manhattan
  • Interface: Gráfica (Pygame)

Dimensões do labirinto: 4x5
Início: (0, 0)
Fim: (3, 3)

🔍 Executando algoritmo A*...

✓ Caminho encontrado!
  Nós explorados: 9
  Custo total: 7.00
  Tamanho do caminho: 7 células

Labirinto (4x5):
┌──────────┐
│S · █ · · │
│• • █ · █ │
│█ • █ · · │
│█ • • E █ │
└──────────┘

Menor caminho encontrado:
Comprimento: 7 células

[s(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), e(3, 3)]

═══ Estatísticas ═══

Labirinto:
  • Dimensões: 4 × 5
  • Total de células: 20
  • Células livres: 12
  • Obstáculos: 8 (40.0%)
  • Peso médio: 1.00
  • Início: (0, 0)
  • Fim: (3, 3)

Caminho:
  • Comprimento: 7 células
  • Custo total: 7.00

Busca:
  • Nós explorados: 9
  • Eficiência: 77.8%

══════════════════════════════════════════════════════════════════════
```

## ❓ Perguntas Frequentes (FAQ)

**P: O algoritmo sempre encontra o caminho mais curto?**
R: Sim, desde que a heurística seja admissível (não superestime). As heurísticas Manhattan e Euclidiana implementadas são admissíveis.

**P: Qual heurística usar?**
R: Use Manhattan para movimentos apenas ortogonais e Euclidiana quando permitir diagonais.

**P: Como adicionar novos labirintos?**
R: Crie um arquivo .txt no formato especificado ou adicione em `examples/maze_examples.py`.

**P: A interface gráfica é obrigatória?**
R: Não, use `--no-gui` para executar apenas no console.

**P: Como contribuir?**
R: Crie uma branch, desenvolva sua feature, teste e abra um Pull Request.

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte da disciplina de Teoria dos Grafos.

## 🤝 Contribuidores

- **Pedro Carbonaro** - Algoritmo A*
- **Bruna Barbosa** - Parser e Validação
- **Rafael Marques** - Visualização Console
- **Guilherme Martini** - Interface Gráfica
- **Felipe Evangelista** - Integração e Exemplos

---