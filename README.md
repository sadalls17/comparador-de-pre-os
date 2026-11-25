# CP — Comparador de Preços

Aplicação em Python para comparar preços de produtos de hardware/tecnologia entre varejistas brasileiros, com versão web e versão desktop (Tkinter).

## Status

🚧 Em desenvolvimento inicial — projeto individual.

- ✅ Coleta de preços no KaBuM! (`scraper/kabum.py`)
- ⏳ Outros varejistas ainda não implementados

## Estrutura do repositório

```
.
├── web/        # Versão web do comparador de preços
├── desktop/    # Versão desktop em Python/Tkinter
├── scraper/    # Módulos de coleta/atualização de preços por site
├── tests/      # Testes automatizados
└── docs/       # Documentação técnica (inclui o PGCS)
```

## Sites suportados

- KaBuM! (https://www.kabum.com.br)

Para testar só o coletor de preços, sem abrir a interface:

```bash
python -m scraper.kabum "rtx 4060"
```

## Como rodar

### Requisitos

```bash
pip install -r requirements.txt
```

### Desktop

Sempre execute a partir da pasta raiz do projeto (a que contém `README.md`), usando `-m`:

```bash
python -m desktop.main
```

### Web

```bash
python -m web.app
```

> ⚠️ Não rode com `python web/app.py` ou `python desktop/main.py` (caminho direto) — isso causa `ModuleNotFoundError: No module named 'scraper'`, porque o Python não localiza o pacote `scraper/` quando o arquivo é executado assim. Use sempre o formato `-m` acima, a partir da raiz do projeto.

## Documentação

Consulte `docs/` para o Plano de Gerenciamento de Configuração (PGCS) e demais documentos técnicos do projeto.

## Autor

Marcio Moreira Kuskowski
