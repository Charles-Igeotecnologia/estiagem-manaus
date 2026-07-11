# Web GIS 360 - Modelo de Aplicação Interativa

Este projeto é um **modelo (template) reutilizável** para criar mapas interativos integrados com fotos panorâmicas 360° (equirecionais). Ele permite georreferenciar imagens terrestres ou aéreas (drone) e exibi-las em uma interface moderna (*Dark Mode*, painéis flutuantes e tabela de atributos).

Você pode copiar esta pasta e usá-la como base para qualquer outro conjunto de fotos em outros diretórios.

---

## 📁 Estrutura de Pastas Recomendada

Para criar um novo projeto usando este modelo, organize os arquivos da seguinte forma:

```text
MEU_NOVO_PROJETO/
│
├── index.html              # Interface Web GIS (Visualizador do Mapa + 360°)
├── processar_fotos.py      # Script Python de automação e georreferenciamento
├── data.geojson            # Banco de dados geográfico (gerado automaticamente)
│
└── media/                  # Pasta para armazenar as fotos do projeto
    └── uploads/            # Fotos processadas em alta resolução (copiadas pelo script)
```

---

## 🛠️ Pré-requisitos e Instalação

1. **Python**: Certifique-se de ter o Python 3 instalado no computador.
2. **Biblioteca Pillow**: O script Python utiliza a biblioteca `Pillow` para ler metadados EXIF e extrair coordenadas de GPS automaticamente das fotos. Instale-a executando o comando abaixo no terminal (PowerShell / Prompt):
   ```bash
   pip install Pillow
   ```

---

## 🚀 Como Usar o Modelo (Passo a Passo)

### Passo 1: Preparar suas Imagens 360°
Coloque as suas imagens originais (arquivos `.jpg`, `.jpeg` ou `.png` equirecionais inteiros de alta resolução obtidos de drones ou câmeras 360) em um diretório de sua escolha (ex: no seu computador ou no Google Drive).

### Passo 2: Rodar o Script de Processamento
Abra o terminal na pasta do projeto e execute o script informando o caminho da nova foto:
```bash
python processar_fotos.py "C:\Caminho\Para\Sua\Foto_Original.jpg"
```
* **Se a foto contiver coordenadas GPS nos metadados**: O script detectará e extrairá a latitude e longitude de forma automática.
* **Se a foto não contiver GPS (ou as coordenadas foram removidas)**: O script perguntará no terminal se você deseja inserir a **Latitude** e a **Longitude** manualmente.
* **Configuração de Atributos**: Digite um título amigável para a foto e defina a categoria (`Aérea` ou `Terrestre`).

O script irá:
1. Copiar a foto para a pasta local `media/uploads/`.
2. Registrar o ponto geográfico no arquivo `data.geojson`.

### Passo 3: Iniciar o Servidor de Testes Local
A aplicação precisa rodar sob um servidor HTTP local para contornar bloqueios de CORS e viabilizar o salvamento de dados (gravação de alterações no `data.geojson` diretamente pela página web). Inicie o servidor Python customizado abrindo o terminal na pasta do projeto e rodando:
```bash
python servidor.py
```

Acesse no navegador:
👉 **[http://localhost:8000/index.html](http://localhost:8000/index.html)**

---

## ⚙️ Customizações Avançadas no `index.html`

Se você deseja adaptar o mapa para uma região ou loteamento diferente, faça as seguintes alterações abrindo o arquivo `index.html` em um editor de texto:

### 1. Ajustar o Centro Inicial do Mapa
Localize no código a inicialização do mapa (por volta da linha 410) e altere as coordenadas de centro (Latitude, Longitude) e o nível de zoom inicial:
```javascript
// Altere [-15.7801, -47.9292] para as coordenadas centrais da sua área de estudo
// Altere 16 para o zoom desejado (número maior = mais aproximado)
const map = L.map('map', {
    center: [-15.7801, -47.9292],
    zoom: 16,
    zoomControl: false // O controle de zoom foi movido para o canto superior direito
});
```

### 2. Formato do Banco de Dados (`data.geojson`)
O arquivo `data.geojson` armazena a localização e as propriedades das fotos em formato JSON. Exemplo de estrutura padrão:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-47.9292, -15.7801] // [Longitude, Latitude]
      },
      "properties": {
        "id": "foto_exemplo",
        "title": "Lote 74 - Vista Aérea",
        "date": "2026-06-20",
        "image360Url": "media/uploads/foto_exemplo.jpg",
        "category": "Aérea"
      }
    }
  ]
}
```

---

## 🌐 Publicação no GitHub Pages (Gratuito)

Para compartilhar o mapa interativo na internet para que clientes ou parceiros possam acessar remotamente:

1. Crie um repositório no **GitHub** (ex: `webgis-360`).
2. Envie (Push) todos os arquivos deste projeto para o repositório.
3. Nas configurações do repositório no GitHub (*Settings*):
   * Vá em **Pages** (no menu lateral).
   * Em *Build and deployment*, defina a Source como **Deploy from a branch**.
   * Escolha a branch **main** (ou `master`) e a pasta **/ (root)**, e clique em *Save*.
4. O GitHub gerará um link público para o seu mapa (ex: `https://seu-usuario.github.io/webgis-360/index.html`).

---

## 📌 Nota de Consolidação (atualizado em 2026-07-11)

Este projeto contém dois arquivos de interface principal na raiz: `index.html` e `visao_redesign.html`. Após revisão técnica, ficou definido:

- **`index.html` é a versão de produção.** É o arquivo funcional, referenciado pela navegação (`mapa.html`, `equipe.html`) e que carrega dados reais (`data.geojson`, `escolas_rurais.geojson`, banners e carrosséis).
- **`visao_redesign.html` é uma maquete conceitual (mockup) de redesign**, sem integração com dados reais (não consome `data.geojson`, não usa Leaflet/Pannellum) — o próprio arquivo se identifica como "Maquete conceitual · proposta de evolução". Nenhum outro arquivo do projeto referencia ou depende dele.

**Nenhum arquivo de layout foi modificado** nesta consolidação — trata-se apenas de um registro de decisão para evitar manutenção duplicada. Caso a proposta visual de `visao_redesign.html` seja aprovada para produção futuramente, ela deve ser implementada como uma evolução controlada do `index.html` (preservando a estrutura de dados atual), e não como substituição direta.

## 🔍 Nota de QA — Dados Geoespaciais (atualizado em 2026-07-11)

Revisão de consistência em `escolas_rurais.geojson` (85 registros) e `data.geojson` (109 registros):

| Item | Status | Observação |
|---|---|---|
| CEP mal formatado (`escola_rural_85`, Creche Municipal Rosa Almeida) | ✅ Corrigido | `69000000` → `69000-000` (padronização de formato, sem impacto funcional) |
| `alunos: 0` na Creche Municipal Rosa Almeida (`escola_rural_85`) | ⚠️ Pendente de verificação | Valor pode ser um placeholder de cadastro incompleto — recomenda-se confirmar com a SEMED antes de usar esse dado em relatórios |
| Coordenadas quase idênticas entre fotos de E.M. São Sebastião II (`DJI_0950`) e E.M. Paulo Freire (`DJI_0951`) em `data.geojson` | ⚠️ Pendente de verificação em campo | Pode indicar ponto de decolagem do drone compartilhado entre as duas escolas (esperado, se são vizinhas) ou erro de atribuição de EXIF — não foi alterado por não haver como confirmar a coordenada correta sem validação de campo |
| IDs sem prefixo de escola (`dji_0118` a `dji_0125`, fotos de E.M. Francisco Coelho) em `data.geojson` | ℹ️ Registrado, não alterado | Inconsistente com o padrão `em_[escola]_djiXXXX` usado nos demais 104 registros, mas os títulos (`title`) estão corretos e nada no `mapa.html` depende do formato do `id` além de comparação interna (`find`) — manter como está evita risco de regressão |

Nenhuma correção foi feita em coordenadas ou em `id`s por não haver como validar o dado correto sem inspeção de campo — alterações "às cegas" nesses campos poderiam introduzir erro maior do que o atual.

## 🌊 Nota sobre Integração de APIs Climáticas (decisão registrada em 2026-07-11)

Foi avaliada a possibilidade de substituir os indicadores climáticos estáticos do `index.html` (temperatura, nível do rio) por consumo de API externa (ex: INMET, ANA/Hidroweb). **Decisão: não integrar.** O front-end e a estrutura visual do `index.html` permanecem exatamente como estão — nenhuma alteração de design, estrutura ou dado foi feita nesta rodada por conta dessa avaliação.

## 💧 Módulo: Monitoramento de Poços (`pocos/`)

Subpasta `pocos/` — Web Map + Dashboard de cenários de estiagem para os poços de abastecimento das 48 escolas ribeirinhas, com dados reais de campo (`pocos/TABELA POCOS 2026.csv`). Ver `pocos/README.md` para o schema completo, a regra de classificação de cenário e o fluxo de atualização dos dados.

Este módulo consome `escolas_rurais.geojson` apenas em leitura (cruzamento pelo nome da escola, para trazer nº de alunos atendidos) — nenhum arquivo do sistema principal (`index.html`, `mapa.html`, `equipe.html`) foi alterado para viabilizá-lo.

**Atenção ao publicar:** a planilha `pocos/TABELA POCOS 2026.csv` é uma cópia da planilha de trabalho em `03 TABELA DOS POCOS/` (fora deste repositório). Sempre sincronizar manualmente antes de cada commit — ver detalhes em `pocos/README.md`.
