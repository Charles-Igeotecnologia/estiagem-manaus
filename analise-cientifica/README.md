# Análise Científica — SAH-AM Monitor (protótipo)

Subpasta do `PROJETO 360`, com um painel Web GIS mais elaborado (ECharts) para análise hidrometeorológica da Amazônia — cotagramas, clima/vento, chuva, comparativo histórico 2023×2026 e indicador ENOS.

**Status: protótipo de layout, rotulado como tal na própria interface.** Publicado para validação de design e arquitetura de painéis — não para leitura operacional de dados em tempo real (ver tabela abaixo).

---

## 📁 Estrutura e relação com a pasta de rascunho

```
08 Projeto 360/
├── 09 PROJETO CLIMATICO/
│   └── monitor-amazonia-manaus.html   # Rascunho de trabalho (fora do repositório Git)
└── 01 ANO 2023/PROJETO 360/
    └── analise-cientifica/
        ├── index.html                 # Cópia publicada (este arquivo) — dentro do repositório Git
        └── README.md                  # Este documento
```

`analise-cientifica/index.html` é uma **cópia** de `09 PROJETO CLIMATICO/monitor-amazonia-manaus.html`, com 3 rótulos de status corrigidos (ver "Correções aplicadas" abaixo). A pasta `09 PROJETO CLIMATICO` fica fora do repositório Git — sempre que ela for atualizada, repita a cópia manualmente para `analise-cientifica/index.html` antes do commit/push, do mesmo jeito que já é feito com `pocos/TABELA POCOS 2026.csv`.

---

## ⚠️ Status real de cada fonte de dados (avaliação técnica)

| Fonte | Status na interface | Situação real |
|---|---|---|
| **Open-Meteo** (clima do portal principal) | — | ✅ Ao vivo, sem chave, já em produção em `index.html` — não faz parte deste módulo |
| **INMET · A101 Manaus** (temperatura/vento deste painel) | "conectando…" → "ativo" ou "token pendente" | 🟡 Código de fetch real implementado (`fetchInmetA101()`), mas a rota aberta da API responde 204 sem token. Cai em fallback simulado até haver token (solicitado a `cadastro.act@inmet.gov.br`) |
| **SGB/CPRM · SACE** (cotagramas) | "simulado" / "pendente" | 🔴 100% simulado — não há parsing de boletim implementado. Rótulo corrigido nesta rodada (antes dizia "ativo"/"concluído", o que era enganoso) |
| **ANA · HidroWebService** | "token pendente" | 🔴 Não implementado — API real exige fluxo SOAP/REST multi-etapa, incompatível com fetch direto do navegador em site estático |
| **CEMADEN** (chuva) | "token pendente" | 🔴 Não implementado |
| Cotagramas, KPIs, alerta de cheia, gauge de vazante | — | 🔴 Todos os valores (28,50 m, previsão de 7 dias, indicador ENOS etc.) são dados ilustrativos gerados por função (`curve()`, `simulate()`) para validar o layout — **não usar em decisões operacionais** |

Esta tabela reflete a avaliação feita antes da publicação (2026-07-11) e deve ser revisada sempre que uma nova fonte for conectada de verdade.

---

## 🔧 Correções aplicadas antes da publicação

Rótulos de status do **SGB/CPRM · SACE** que diziam "ativo"/"concluído" foram corrigidos para "simulado"/"pendente" em 3 pontos da interface (painel "Fontes conectadas", "Checklist de Integração" e "Log de ingestão"), e o resumo do rodapé da barra lateral mudou de "4 fontes ativas" para "4 fontes mapeadas" — nenhuma fonte está de fato ativa hoje.

---

## 🧩 O que é reaproveitável deste protótipo

- **`fetchInmetA101()`** (linhas ~937 em diante do script): única integração real do painel — busca a estação INMET A101, converte UTC→horário de Manaus e m/s→km/h, com fallback honesto para simulação quando falha. Serve de modelo direto para conectar a estação automática assim que o token chegar.
- **Padrão de navegação por abas** (`data-nav` + `applyView()`): troca de painéis sem recarregar página, reaproveitável em outras seções do portal.
- **Painéis "Fontes conectadas" / "Checklist de Integração" / "Log de ingestão"**: modelo de transparência de dados (mostrar o que é real vs. simulado na própria UI) — alinhado ao princípio de não fabricar dados já adotado no restante do portal.
- **Config ECharts** dos painéis de cotagrama, comparativo histórico e gauge de vazante: prontos para receber série real assim que houver fonte (ANA/SACE) sem precisar redesenhar o gráfico.

---

## 🌐 Publicação

Publicado junto com o restante do `PROJETO 360` (mesmo repositório GitHub Pages), acessível a partir de um link "Análise Científica" na navegação principal (`index.html`, `equipe.html`) e de um link de volta ao portal na barra lateral deste painel.
