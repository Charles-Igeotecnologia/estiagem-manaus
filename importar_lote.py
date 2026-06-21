import os
import sys
import json
import shutil
from datetime import datetime

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

def get_decimal_from_dms(dms, ref):
    """Converte coordenadas em Graus, Minutos e Segundos para Decimal"""
    try:
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
    except (TypeError, ValueError, IndexError):
        try:
            degrees = float(dms[0][0]) / float(dms[0][1])
            minutes = float(dms[1][0]) / float(dms[1][1])
            seconds = float(dms[2][0]) / float(dms[2][1])
        except Exception:
            return None

    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def extrair_gps_da_imagem(caminho_imagem):
    """Tenta extrair a latitude e longitude dos metadados da imagem"""
    if not PILLOW_AVAILABLE:
        return None

    try:
        img = Image.open(caminho_imagem)
        exif = img._getexif()
        if not exif:
            return None

        gps_info = {}
        for tag, value in exif.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]
                break

        if gps_info:
            lat_dms = gps_info.get("GPSLatitude")
            lat_ref = gps_info.get("GPSLatitudeRef")
            lon_dms = gps_info.get("GPSLongitude")
            lon_ref = gps_info.get("GPSLongitudeRef")

            if lat_dms and lat_ref and lon_dms and lon_ref:
                lat = get_decimal_from_dms(lat_dms, lat_ref)
                lon = get_decimal_from_dms(lon_dms, lon_ref)
                return lat, lon
    except Exception as e:
        print(f"[!] Erro ao ler metadados de {os.path.basename(caminho_imagem)}: {e}")
    
    return None

def main():
    print("=" * 70)
    print("   IMPORTADOR DE FOTOS 360° EM LOTE - WEB GIS")
    print("=" * 70)

    if not PILLOW_AVAILABLE:
        print("[-] Erro: A biblioteca 'Pillow' é necessária para a importação em lote.")
        print("    Instale rodando: pip install Pillow")
        sys.exit(1)

    # Diretório raiz para buscar fotos (pasta pai de PROJETO 360, ou seja, 01 ANO 2023)
    diretorio_busca = os.path.dirname(os.path.abspath(__file__))
    # Se o script está na pasta PROJETO 360, a busca será na pasta pai dela
    diretorio_busca_pai = os.path.abspath(os.path.join(diretorio_busca, ".."))
    pasta_projeto_nome = os.path.basename(diretorio_busca)

    print(f"[*] Escaneando arquivos em: {diretorio_busca_pai}")
    print(f"[*] Ignorando a pasta do projeto: {pasta_projeto_nome}")

    imagens_por_pasta = {}
    total_imagens_encontradas = 0

    # Varre recursivamente as subpastas
    for root, dirs, files in os.walk(diretorio_busca_pai):
        # Ignora a pasta do próprio projeto e seus subdiretórios
        if pasta_projeto_nome in root.split(os.sep) or ".git" in root.split(os.sep):
            continue

        pasta_rel = os.path.relpath(root, diretorio_busca_pai)
        if pasta_rel == ".":
            continue

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png']:
                caminho_completo = os.path.join(root, file)
                if root not in imagens_por_pasta:
                    imagens_por_pasta[root] = []
                imagens_por_pasta[root].append(caminho_completo)
                total_imagens_encontradas += 1

    print(f"[+] Encontradas {total_imagens_encontradas} imagens em {len(imagens_por_pasta)} pastas.")

    if total_imagens_encontradas == 0:
        print("[-] Nenhuma foto encontrada para processar.")
        sys.exit(0)

    # Dicionário temporário para guardar os dados de cada imagem
    dados_imagens = []
    imagens_sem_gps = []

    # Passo 1: Extrair GPS de todas as imagens que possuem
    print("\n[*] Passo 1: Extraindo coordenadas GPS das fotos...")
    gps_por_pasta = {} # Guarda a primeira coordenada GPS válida de cada pasta para usar como fallback

    for pasta, caminhos in imagens_por_pasta.items():
        nome_pasta = os.path.basename(pasta)
        for caminho in caminhos:
            nome_arquivo = os.path.basename(caminho)
            coords = extrair_gps_da_imagem(caminho)
            
            # Obtém a data de modificação original do arquivo
            mtime = os.path.getmtime(caminho)
            data_foto = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

            # Categoria automática: DJI ou aérea no nome -> Aérea, senão Terrestre
            if "dji" in nome_arquivo.lower() or "aerea" in nome_arquivo.lower() or "aérea" in nome_arquivo.lower():
                categoria = "Aérea"
            else:
                categoria = "Terrestre"

            # Detecta o tipo de visualização (360 ou flat) analisando aspect ratio (largura/altura)
            view_type = "flat"
            if PILLOW_AVAILABLE:
                try:
                    with Image.open(caminho) as img_obj:
                        w, h = img_obj.size
                        ratio = w / h
                        # Imagens 360 equirecionais possuem proporção de aproximadamente 2:1
                        if 1.85 <= ratio <= 2.15:
                            view_type = "360"
                except Exception:
                    pass

            titulo = f"{nome_pasta} - {os.path.splitext(nome_arquivo)[0]}"

            dados_img = {
                "caminho_origem": caminho,
                "nome_arquivo": nome_arquivo,
                "nome_pasta": nome_pasta,
                "titulo": titulo,
                "categoria": categoria,
                "data": data_foto,
                "gps": coords,
                "viewType": view_type
            }

            if coords:
                lat, lon = coords
                # Salva a primeira coordenada válida desta pasta como fallback para outras fotos da mesma pasta
                if pasta not in gps_por_pasta:
                    gps_por_pasta[pasta] = coords
                dados_imagens.append(dados_img)
            else:
                imagens_sem_gps.append(dados_img)

    print(f"[+] GPS extraído com sucesso de {len(dados_imagens)} de {total_imagens_encontradas} fotos.")

    # Passo 2: Verificar fotos sem GPS (fallback inteligente desativado)
    print("\n[*] Passo 2: Verificando fotos sem GPS (importação restrita a coordenadas nativas)...")
    nao_importados = imagens_sem_gps

    if nao_importados:
        print(f"[!] {len(nao_importados)} fotos não puderam ser importadas pois não possuem GPS nativo:")
        for ni in nao_importados:
            print(f"    - {ni['nome_pasta']}/{ni['nome_arquivo']}")

    # Passo 3: Copiar arquivos e atualizar data.geojson
    print("\n[*] Passo 3: Copiando fotos e registrando no data.geojson...")
    pasta_destino = os.path.join(diretorio_busca, "media", "uploads")
    os.makedirs(pasta_destino, exist_ok=True)

    # Carrega geojson existente ou cria novo
    geojson_path = os.path.join(diretorio_busca, "data.geojson")
    if os.path.exists(geojson_path):
        try:
            with open(geojson_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"type": "FeatureCollection", "features": []}
    else:
        data = {"type": "FeatureCollection", "features": []}

    erros_copia = 0
    sucessos = 0

    for img in dados_imagens:
        caminho_origem = img["caminho_origem"]
        nome_arquivo = img["nome_arquivo"]
        
        # Gera um nome de arquivo único para o destino baseado no nome da pasta e do arquivo
        nome_pasta_limpo = img["nome_pasta"].lower().replace(" ", "_").replace(".", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ã", "a").replace("õ", "o").replace("ç", "c")
        nome_arquivo_destino = f"{nome_pasta_limpo}_{nome_arquivo}"
        caminho_destino_rel = f"media/uploads/{nome_arquivo_destino}"
        caminho_destino_abs = os.path.join(pasta_destino, nome_arquivo_destino)

        # Copia o arquivo
        try:
            shutil.copy2(caminho_origem, caminho_destino_abs)
            sucessos += 1
        except Exception as e:
            print(f"[-] Erro ao copiar {nome_arquivo} para {nome_arquivo_destino}: {e}")
            erros_copia += 1
            continue

        # Registra no GeoJSON usando o ID único
        file_id = os.path.splitext(nome_arquivo_destino)[0].lower().replace(" ", "_")
        lat, lon = img["gps"]

        # Verifica se já existe uma feature com este ID para preservar metadados editados manualmente no front-end
        feature_existente = next((f for f in data["features"] if f["properties"]["id"] == file_id), None)
        
        properties_mescladas = {
            "id": file_id,
            "title": img["titulo"],
            "date": img["data"],
            "image360Url": caminho_destino_rel.replace("\\", "/"),
            "category": img["category"] if "category" in img else img["categoria"],
            "viewType": img["viewType"]
        }
        
        if feature_existente:
            for key in ["description", "hotspotPitch", "hotspotYaw"]:
                if key in feature_existente["properties"]:
                    properties_mescladas[key] = feature_existente["properties"][key]
                    
        nova_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(lon), float(lat)] # GeoJSON usa [Longitude, Latitude]
            },
            "properties": properties_mescladas
        }

        # Remove duplicatas pelo ID e insere a nova/mesclada
        data["features"] = [f for f in data["features"] if f["properties"]["id"] != file_id]
        data["features"].append(nova_feature)

    # Salva o GeoJSON
    try:
        with open(geojson_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n[OK] Banco de dados 'data.geojson' atualizado com sucesso!")
    except Exception as e:
        print(f"[-] Erro ao salvar data.geojson: {e}")

    # Resumo final
    print("\n" + "=" * 70)
    print("   RESUMO DA IMPORTAÇÃO EM LOTE")
    print("=" * 70)
    print(f"Total de imagens detectadas:  {total_imagens_encontradas}")
    print(f"Importadas com sucesso:       {sucessos}")
    print(f"Falhas na cópia:              {erros_copia}")
    print(f"Fotos sem coordenadas (puladas): {len(nao_importados)}")
    if nao_importados:
        print("Dica: Adicione coordenadas GPS manualmente nas fotos listadas acima ou coloque-as")
        print("      em pastas que possuam pelo menos uma foto com GPS válido.")
    print("=" * 70)

if __name__ == "__main__":
    main()
