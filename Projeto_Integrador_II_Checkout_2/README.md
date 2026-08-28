# Apoio Tecnológico à Pesquisa de Preços nas Contratações Públicas

Aplicação web dinâmica desenvolvida para o Projeto Integrador de Tecnologia da Informação III, evoluindo o protótipo do Projeto Integrador II.

## Funcionalidades
- consulta dinâmica por código CATMAT sem recarregamento da página;
- integração Vue 3 + Flask;
- integração com a API de Dados Abertos do Compras.gov.br;
- apresentação dos 53 registros reais do retorno usado no PI-II;
- indicação dos 28 registros considerados após o saneamento;
- referências às atas no PNCP;
- validação de entrada e tratamento de erros;
- HTML5 semântico;
- CSS3 responsivo.

## Tecnologias
Python, Flask, Vue 3, HTML5, CSS3, Requests, Pandas e pytest.

## Estrutura
```text
app.py
requirements.txt
README.md
.gitignore
templates/index.html
static/style.css
tests/test_app.py
data/demo.json
```

## Instalação
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução
```bash
python app.py
```
Acesse http://127.0.0.1:5000.

## Demonstração com o retorno real do PI-II
```bash
# Windows PowerShell
$env:DEMO_MODE="1"
python app.py

# Linux/macOS
DEMO_MODE=1 python app.py
```
Use o CATMAT `462546`.

## Testes
```bash
pytest -q
```

## Decisões técnicas
Flask mantém a compatibilidade com Python e funciona como backend; Vue 3 fornece a interação dinâmica no navegador; HTML5 organiza a interface semanticamente; CSS3 implementa a responsividade; Requests e Pandas preservam a lógica de consulta e tratamento desenvolvida anteriormente.

## GitHub
Depois de criar o repositório, publique toda esta pasta e insira a URL pública real no relatório.
