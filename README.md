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
