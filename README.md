# Artefact Agent — CLI Question-Answer Agent with Calculator

Um agente de IA via linha de comando que responde perguntas factuais
**e** realiza cálculos matemáticos com uma calculadora simbólica (SymPy).
Construído com [Agno](https://github.com/agno-agi/agno).

## Demonstração

```
$ uv run python -m src.cli
Artefact Agent — type 'exit' or 'quit' to stop.

> Qual a capital da França?
Paris

> 128 * 46
5888

> qual o seno de 60?
sqrt(3)/2

> quantos segundos há em um dia?
86400

> exit
```

---

## Como executar

### 1. Pré-requisitos

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes)

### 2. Instalar dependências

```bash
uv sync
```

### 3. Configurar chave da API

Crie ou edite o arquivo `.env` na raiz do projeto:

```
OPENAI_API_KEY=sk-proj-sua-chave-aqui
```

### 4. Rodar

```bash
# Modo normal
uv run python -m src.cli

# Modo verbose (mostra chamadas de ferramentas)
uv run python -m src.cli --verbose
```

Comandos dentro do CLI:

| Comando | Ação |
|---------|------|
| Qualquer pergunta textual | Responde do conhecimento do LLM |
| Expressão matemática (ex: `128 * 46`) | Calcula com SymPy |
| Pergunta com cálculo implícito (ex: "quantos segundos em um dia?") | LLM detecta e usa calculadora |
| `exit` ou `quit` | Sai do programa |

### 5. Rodar testes

```bash
uv run pytest tests/ -v
```

---

## Lógica de implementação

### Arquitetura

```
digraph {
    CLI (src/cli.py) -> run_with_context (src/agent.py)
    run_with_context -> router
    router -> evaluate [label="expressão pura"]
    router -> Agno Agent [label="linguagem natural"]
    Agno Agent -> OpenAIChat [label="pergunta factual"]
    Agno Agent -> calculator_tool [label="cálculo detectado"]
    calculator_tool -> evaluate
    evaluate -> SymPy
}
```

### Fluxo de uma pergunta

**1. Entrada do usuário** (`src/cli.py`)

O loop principal lê do terminal com `input("> ")`, trata `exit`/`quit`,
input vazio (re-prompt), e repetição de pergunta (reusa resposta anterior).

**2. Roteamento** (`src/agent.py` — `run_with_context`)

Toda entrada passa por `_is_pure_math()`, que verifica:

1. A string contém **apenas** caracteres válidos para matemática
   (números, operadores, parênteses, espaços)
2. Todas as palavras na string estão numa **whitelist** de funções/variáveis
   matemáticas conhecidas (`sin`, `cos`, `factor`, `simplify`, `pi`, `x`, …)

Se passa → roteia direto pra calculadora SymPy (sem custo de API).
Se não passa → envia pro LLM (OpenAI).

**3. Agente Agno** (`src/agent.py` — `create_agent`)

O Agno Agent recebe o modelo (OpenAIChat ou Groq), uma `calculator_tool`
registrada, e um conjunto de instruções que dizem ao LLM:

- Responder perguntas factuais do próprio conhecimento
- Usar a `calculator_tool` para qualquer cálculo numérico
- Nunca usar LaTeX na resposta
- Usar radianos em funções trigonométricas
- Comunicar incerteza quando não souber

**4. Calculadora SymPy** (`src/tools/calculator.py`)

A tool recebe uma string, chama `sympy.sympify()` para transformar em
expressão matemática, e retorna o resultado exato como string.

Trata erros de sintaxe, parênteses desbalanceados, e expressões inválidas.

**5. Contexto de conversação com SQLite**

O Agno Agent é configurado com `SqliteDb` e `session_id` fixo
(`"default-session"`). A cada `agent.run()`, Agno salva automaticamente
a interação no banco (`sessions/agent.db`). Na próxima execução (mesmo
que em outro terminal), o histórico é carregado via
`add_history_to_context=True`.

```
▶ uv run python -m src.cli
> Meu nome é Jady.
Prazer, Jady!

▶ (fecha terminal, abre de novo)
> Qual é meu nome?
Seu nome é Jady! ← carregou da sessão anterior no SQLite
```

> **Nota sobre sessões na API FastAPI** (`specs/002-fastapi-agent-api`):
> A API combina duas camadas de sessão:
> 1. **Dict em memória** (`_sessions` em `src/api/routes.py`) — cache de
>    objetos `Agent` para evitar recriar o cliente OpenAI a cada request.
> 2. **SQLite** (`sessions/agent.db`) — persistência real do histórico de
>    mensagens, gerenciada pelo Agno Agent via `session_id`.
>
> O dict não substitui o SQLite. Se o servidor reiniciar, o dict é perdido,
> mas o histórico no SQLite permanece. Um novo `Agent(session_id="X")`
> recria o cliente e carrega o histórico do banco.

Expressões puras roteadas diretamente para a calculadora (sem passar
pelo LLM) não persistem no banco — é um trade-off consciente para
economizar tokens de API.

### Graceful degradation

Quando o LLM está indisponível (API key inválida, rate limit 429, erro de
autenticação), o CLI detecta pelo status do `RunOutput` ou por palavras-chave
no conteúdo da resposta e:

1. Exibe um aviso: "AI knowledge source unavailable"
2. Entra em **modo calculadora-only**
3. Continua aceitando expressões matemáticas e calculando com SymPy

### Modo verbose (`--verbose`)

Quando ativado, o CLI extrai as `ToolExecution` do `RunOutput` e exibe:

```
[Tool: calculator] "sin(pi/6)" → 1/2
```

Tanto para chamadas de ferramenta feitas pelo LLM quanto para expressões
puras roteadas diretamente.

---

## Estrutura do projeto

```
src/
├── agent.py           # Criação do Agno Agent, roteamento, contexto
├── cli.py             # REPL loop, entrada/saída, --verbose
├── tools/
│   └── calculator.py  # Tool SymPy para Agno + função evaluate()

tests/
├── unit/
│   ├── test_agent.py       # Testes de roteamento, contexto, ambiguidade
│   └── test_calculator.py  # Testes de aritmética, simbólica, erros
└── integration/
    └── test_cli.py    # Testes de fluxo completo via stdin/stdout mockado
```

---

## Especificação completa

Documentos de design e planejamento em
[specs/001-cli-agent-calculator/](specs/001-cli-agent-calculator/):

| Documento | Conteúdo |
|-----------|----------|
| `spec.md` | User stories, critérios de aceitação, requisitos |
| `plan.md` | Stack, estrutura, constitution check |
| `tasks.md` | 40 tarefas em 7 fases, todas concluídas |
| `data-model.md` | Entidades: Session, Message, ToolCall |
| `contracts/` | CLI Interface e Calculator Tool contracts |
| `quickstart.md` | Guia rápido de setup e uso |
| `research.md` | Decisões técnicas e alternativas |