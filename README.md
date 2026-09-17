# AI Financial Agent Builder

> **Local-first financial intelligence builder** — transforma contexto financeiro estruturado em análise determinística e prepara a base para um agente conversacional.

## ✦ PROJECT PAGES — NEXA STUDIO

### **[ABRIR O CASE INTERATIVO →](https://sayjinblackbelt.github.io/AI-Financial-Agent-Builder/)**

Dashboard editorial com navegação por seções, arquitetura, snapshot técnico, roadmap e identidade **NEXA Studio**.

**Powered by [NEXA Studio](https://sayjinblackbelt.github.io/NEXA-Studio/)** · [Código-fonte](https://github.com/sayjinblackbelt/AI-Financial-Agent-Builder)

---

## 🎯 O projeto

O **AI Financial Agent Builder** é um projeto de portfólio focado em **organização financeira, análise de dados e arquitetura de agentes**.

A proposta não é substituir bancos ou criar uma plataforma de investimentos. O sistema constrói uma camada local de contexto financeiro que pode, posteriormente, ser utilizada por um agente de IA conversacional.

### MVP atual

- Guided financial onboarding
- Perfil financeiro estruturado
- Persistência local com SQLite
- Receitas e despesas
- Categorias
- Orçamentos e alertas
- Resumo mensal
- Comparação mês a mês
- Tendências
- Insights e narrativa baseada em regras
- Configuração/prompt do agente
- Flask API
- Dashboard web
- Testes automatizados
- GitHub Actions / CI

---

## 🧭 Core flow

```text
Guided Onboarding
      ↓
Financial Profile
      ↓
Flask API
      ↓
SQLite
      ↓
Financial Analyzer
      ↓
Insights / Alerts / Trends
      ↓
Agent Configuration
      ↓
Future Conversational AI
```

A arquitetura mantém a matemática financeira fora do modelo de IA: **dados e regras produzem os fatos; a futura IA interpreta intenção e apresenta contexto**.

---

## 🧱 Architecture

```text
Browser UI
   │
   ▼
Flask API
   │
   ├── Transaction Service
   ├── Budget Service
   ├── Financial Analyzer
   └── Financial Insights
            │
            ▼
          SQLite
            │
            ├── profile
            ├── categories
            ├── transactions
            ├── budgets
            ├── financial_goals
            ├── agent_settings
            └── financial_snapshot
```

### Repository structure

```text
app/
├── agent/
│   ├── config_builder.py
│   └── prompt_builder.py
├── database/
│   ├── connection.py
│   ├── schema.sql
│   └── financial_agent.db
├── models/
│   └── financial_profile.py
├── onboarding/
│   ├── questions.py
│   └── profile_builder.py
├── services/
│   ├── budget_service.py
│   ├── financial_analyzer.py
│   ├── financial_insights.py
│   ├── financial_profile_service.py
│   └── transaction_service.py
├── main.py
└── web_app.py

web/
├── app.js
└── styles.css

tests/
index.html
requirements.txt
```

---

## 🧠 Intelligence layer

O analyzer atual é determinístico e consulta os dados persistidos no SQLite para calcular:

- receitas, despesas e saldo do mês;
- principais categorias de despesa;
- utilização e excesso de orçamento;
- alertas financeiros;
- comparação com o mês anterior;
- tendências de despesas e saldo;
- insights e narrativa baseada em regras.

A futura camada de IA deverá trabalhar **sobre esses resultados estruturados**, e não substituir os cálculos financeiros.

---

## 🤖 Agent architecture

A configuração do agente consolida:

- contexto financeiro;
- categorias;
- objetivos;
- preferências de comunicação;
- regras de monitoramento;
- limiares de alerta;
- restrições de segurança.

### Restrições atuais

- não executa transações financeiras;
- não solicita credenciais bancárias;
- não toma decisões autônomas de investimento;
- não deve inventar dados financeiros;
- deve solicitar esclarecimento quando os dados forem insuficientes.

---

## 🧪 Quality & testing

O projeto possui testes para:

- banco de dados;
- transações;
- budgets;
- histórico mensal;
- analyzer;
- insights;
- geração de prompt;
- integração Flask/API;
- fluxo financeiro;
- preservação dos dados ao reexecutar configuração.

### Local

```bash
pip install -r requirements.txt
pip install pytest ruff

python -m compileall -q app tests
ruff check app tests --ignore DTZ011
PYTHONPATH=app pytest -q
```

### CI

O GitHub Actions executa os gates de qualidade do projeto, incluindo sintaxe Python, Ruff, testes, smoke test Flask, documentação e verificação de padrões de segredo.

**Status atual: CI — PASS.**

---

## 🚀 Run locally

```bash
pip install -r requirements.txt
cd app
python web_app.py
```

Depois, abra o endereço local exibido pelo Flask.

> A experiência completa depende do backend Flask, porque onboarding, persistência e análise utilizam a API Python e o SQLite.

---

## 🗺️ Roadmap

| Versão | Foco | Estado |
|---|---|---|
| **v0.1** | Builder + onboarding | ✓ |
| **v0.2** | Transactions + budgets | ✓ |
| **v0.3** | Analysis + dashboard + CI | **CURRENT** |
| **v0.4** | Conversational agent | NEXT |
| **v0.5+** | Import/export + reports + expansion | PLANNED |
| **v1.0** | Demonstrable portfolio product | PLANNED |

---

## 🔒 Privacy principles

**Local-first by design.**

- Sem credenciais bancárias.
- Sem execução automática de transações.
- Sem decisões autônomas de investimento.
- Integração de IA opcional.
- Dados financeiros podem permanecer no ambiente local.

---

## 📌 Status

**MVP v0.3 — validated core / browser validation next.**

A camada técnica principal está implementada e a suíte automatizada está integrada ao CI. A próxima etapa é a validação manual da experiência completa no ambiente local, incluindo navegador, fluxo E2E e dados simulados de múltiplos meses.

---

## 🎨 NEXA Studio

Este projeto é apresentado como um **concept case tecnológico do NEXA Studio**, combinando design de produto, desenvolvimento, dados e arquitetura de agentes.

**Powered by [NEXA Studio](https://sayjinblackbelt.github.io/NEXA-Studio/)**

---

## 👤 Author

**Filipe G Morais**

[GitHub](https://github.com/sayjinblackbelt) · [AI Financial Agent Builder](https://github.com/sayjinblackbelt/AI-Financial-Agent-Builder)
