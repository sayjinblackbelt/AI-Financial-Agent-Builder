# AI Financial Agent Builder

> Aplicación guiada y local-first que transforma preferencias financieras en una configuración estructurada para un futuro asistente financiero personal.

## Descripción

El MVP recopila preferencias financieras, crea un perfil estructurado, almacena los datos localmente con SQLite y genera la configuración y los parámetros del agente.

## Flujo principal

`Preguntas guiadas → Perfil financiero → SQLite → Configuración del agente → Futuro asistente de IA`

## Funcionalidades

- Onboarding financiero guiado
- Perfil financiero estructurado
- Persistencia local con SQLite
- Base para ingresos, gastos, presupuestos y objetivos
- Generación de reglas y prompts del agente
- Alertas presupuestarias e insights financieros
- Análisis de tendencias mensuales
- API Flask e interfaz web
- Diseño privacy-first y local-first

## Privacidad y seguridad

Este proyecto no es una plataforma bancaria ni de ejecución de inversiones. No solicita credenciales bancarias, no ejecuta transacciones financieras y no toma decisiones de inversión de forma autónoma. La integración con IA es opcional.

## Ejecución local

```bash
pip install -r requirements.txt
cd app
python web_app.py
```

Después, abre la dirección local mostrada por Flask.

## Pruebas

```bash
pytest
```

## CI

GitHub Actions valida la sintaxis de Python, la calidad con Ruff, la suite automatizada de pruebas y un smoke test de Flask en cada push y pull request hacia `main`.

## Roadmap

- **0.1** Builder MVP
- **0.2** Control financiero
- **0.3** Capa de inteligencia
- **0.4** Agente conversacional de IA

## Autor

**Filipe G Morais**

GitHub: https://github.com/sayjinblackbelt  
Repositorio: https://github.com/sayjinblackbelt/AI-Financial-Agent-Builder
