# Web Map & Dashboard de Poços — Monitoramento da Estiagem (Manaus)

Subpasta do `PROJETO 360`, dedicada à espacialização dos poços de abastecimento hídrico das escolas rurais ribeirinhas e à análise de cenários de criticidade frente à estiagem do Rio Negro/Rio Amazonas.

Este módulo consome `escolas_rurais.geojson` **em modo leitura** (cruzamento por nome de escola, para trazer o nº de alunos atendidos) e não escreve nada nos arquivos do `PROJETO 360` — nenhum arquivo de layout do sistema principal foi alterado por causa deste módulo.

---

## 📁 Estrutura

```
PROJETO 360/
├── index.html, mapa.html, equipe.html, ...   # Sistema principal (inalterado)
├── escolas_rurais.geojson                     # Consumido em leitura por este módulo
└── pocos/
    ├── index.html                # Web Map (Leaflet) + Dashboard de cenários (Chart.js)
    ├── TABELA POCOS 2026.csv     # Cópia versionada da base de poços (ver "Fonte dos dados")
    └── README.md                 # Este documento
```

---

## ⚠️ Fonte dos dados — importante para manutenção

A tabela advém da **Divisão Distrital Rural**, fornecida pela chefia da divisão.

O arquivo `TABELA POCOS 2026.csv` **dentro desta pasta é uma cópia** da planilha de trabalho que fica em `03 TABELA DOS POCOS/TABELA POCOS 2026.csv` (fora deste repositório Git, na estrutura local de pastas do projeto).

Essa cópia existe porque o GitHub Pages só publica o que está dentro do repositório — o app não consegue ler um arquivo de uma pasta fora dele quando publicado online.

**Fluxo de atualização:** sempre que a planilha de campo (`03 TABELA DOS POCOS/TABELA POCOS 2026.csv`) for atualizada, copie o conteúdo novo para cá (`pocos/TABELA POCOS 2026.csv`) **antes** de fazer commit/push — caso contrário o dashboard publicado fica com dados desatualizados.

---

## 🧬 Schema do CSV

Arquivo separado por `;` (ponto e vírgula), decimais com vírgula — padrão de exportação do Excel em pt-BR.

| Coluna | Descrição |
|---|---|
| `Nº` | Número sequencial do registro |
| `CALHA` | Bacia/corredor de acesso: `RIO NEGRO` ou `RIO AMAZONAS` |
| `ESCOLA` | Nome da escola (pode conter sufixo de ano, ex: `/2026`, indicando ano de referência do poço) |
| `ESCOLA (COORDENADA)` | Nome padronizado, **usado como chave de cruzamento** com `title` em `escolas_rurais.geojson` |
| `POÇO ESCOLA` / `POÇO COMUNIDADE` / `POÇO SEMSA` | Nº de poços por titularidade |
| `TOTAL POÇOS` | Soma dos três anteriores |
| `PROFUNDIDADE (m)` | Profundidade do poço principal |
| `BOMBA (CV)` | Potência da bomba (fração texto, ex. `1/2`, ou decimal — o dashboard converte ambos) |
| `FASE` | Monofásico / Bifásico / Trifásico |
| `CAIXA (L)` | Capacidade do reservatório |
| `OBSERVAÇÃO` | Texto livre de campo — principal fonte de sinal de risco |
| `LATITUDE` / `LONGITUDE` | Coordenadas decimais (vírgula) |

### Classificação de cenário (regra aprovada em 2026-07-11)

Não existe coluna de status pronta na planilha — o campo `_cenario` é **inferido automaticamente** em `index.html` (função `classifyScenario`):

| Cenário | Critério |
|---|---|
| **Crítico** | `TOTAL POÇOS = 0`, **ou** `OBSERVAÇÃO` contém "condenado"/"desativado" |
| **Atenção** | `OBSERVAÇÃO` contém "assoreando", "risco de perder/perda", "barranco", "aguardando", "precisa(ndo) de" ou "cacimba" |
| **Normal** | Nenhum dos gatilhos acima |

⚠️ **Leitura textual automatizada, não uma classificação oficial da SEMED.** Recomenda-se validação técnica de campo antes de uso em decisões públicas. Para ajustar os gatilhos, edite `classifyScenario()` em `index.html`.

---

## 🛠️ Como executar localmente

```bash
cd "PROJETO 360"
python -m http.server 8001
```

Acesse: [http://localhost:8001/pocos/index.html](http://localhost:8001/pocos/index.html)

(Pode usar o mesmo `servidor.py` já existente na raiz do `PROJETO 360`, já que ele só adiciona um endpoint de gravação em `/api/salvar` e serve arquivos estáticos normalmente para o resto.)

## 🌐 Publicação

Publicado junto com o restante do `PROJETO 360` (mesmo repositório GitHub Pages) — sem necessidade de configuração adicional, desde que `TABELA POCOS 2026.csv` esteja atualizado nesta pasta antes do push.
