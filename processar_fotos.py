import os
import sys
import json
import shutil
from datetime import datetime

# Tenta importar o Pillow para extração de EXIF, com fallback amigável
try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

def get_decimal_from_dms(dms, ref):
    """Converte coordenadas em Graus, Minutos e Segundos para Decimal"""
    try:
        # Tenta converter tratando os valores diretamente como números
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
    except (TypeError, ValueError, IndexError):
        # Caso os valores venham no formato de frações (numerador, denominador)
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
        print("[!] Biblioteca 'Pillow' não está instalada. Não foi possível extrair dados EXIF automaticamente.")
        print("    Para habilitar a extração automática, execute: pip install Pillow\n")
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
        print(f"[!] Erro ao ler metadados da imagem: {e}")
    
    return None

def registrar_no_geojson(caminho_foto_destino, lat, lon, titulo, categoria):
    """Adiciona as informações da imagem ao arquivo data.geojson"""
    geojson_path = "data.geojson"
    
    # Se o arquivo já existe, carrega; se não, cria um esqueleto
    if os.path.exists(geojson_path):
        try:
            with open(geojson_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"type": "FeatureCollection", "features": []}
    else:
        data = {"type": "FeatureCollection", "features": []}

    # Gera um ID a partir do nome do arquivo
    file_id = os.path.splitext(os.path.basename(caminho_foto_destino))[0].lower().replace(" ", "_")
    
    # Monta a nova feature geográfica
    nova_feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(lon), float(lat)] # GeoJSON usa [Longitude, Latitude]
        },
        "properties": {
            "id": file_id,
            "title": titulo,
            "date": datetime.today().strftime('%Y-%m-%d'),
            "image360Url": caminho_foto_destino.replace("\\", "/"),
            "category": categoria
        }
    }

    # Evita duplicatas pelo ID
    data["features"] = [f for f in data["features"] if f["properties"]["id"] != file_id]
    data["features"].append(nova_feature)

    # Salva o GeoJSON atualizado
    with open(geojson_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"[+] Registrado com sucesso no GeoJSON! Coordenadas: Lat {lat}, Lon {lon}")

def main():
    print("=" * 60)
    print("   PROCESSADOR DE FOTOS 360° PARA WEB GIS")
    print("=" * 60)

    if len(sys.argv) < 2:
        caminho_imagem = input("Digite o caminho da imagem 360 (ex: foto.jpg): ").strip()
    else:
        caminho_imagem = sys.argv[1]

    if not os.path.exists(caminho_imagem):
        print(f"[-] Erro: O arquivo '{caminho_imagem}' não foi encontrado.")
        sys.exit(1)

    print(f"\n[*] Analisando '{os.path.basename(caminho_imagem)}'...")
    coordenadas = extrair_gps_da_imagem(caminho_imagem)

    if coordenadas:
        lat, lon = coordenadas
        print(f"[+] Coordenadas GPS encontradas nos metadados: Latitude {lat}, Longitude {lon}")
    else:
        print("[-] Coordenadas GPS não encontradas automaticamente nos metadados da imagem.")
        res = input("[?] Deseja inserir as coordenadas manualmente? (S/N): ").strip().lower()
        if res == 's':
            try:
                lat = float(input("Latitude (ex: -15.7801): ").strip())
                lon = float(input("Longitude (ex: -47.9292): ").strip())
            except ValueError:
                print("[-] Coordenadas inválidas. Encerrando.")
                sys.exit(1)
        else:
            print("[-] Processo cancelado. Não foi possível geolocalizar a foto.")
            sys.exit(0)

    # Pede metadados adicionais
    titulo_sugerido = os.path.splitext(os.path.basename(caminho_imagem))[0]
    titulo = input(f"Título da foto [{titulo_sugerido}]: ").strip()
    if not titulo:
        titulo = titulo_sugerido

    categoria = input("Categoria (Aérea/Terrestre/Interna) [Terrestre]: ").strip()
    if not categoria:
        categoria = "Terrestre"

    # Cria pasta de mídias caso não exista
    pasta_destino = os.path.join("media", "uploads")
    os.makedirs(pasta_destino, exist_ok=True)

    nome_arquivo_destino = os.path.basename(caminho_imagem)
    caminho_destino_completo = os.path.join(pasta_destino, nome_arquivo_destino)

    # Copia a foto para o diretório local do projeto
    try:
        shutil.copy2(caminho_imagem, caminho_destino_completo)
        print(f"[+] Imagem copiada para: {caminho_destino_completo}")
    except Exception as e:
        print(f"[-] Erro ao copiar imagem para o projeto: {e}")
        sys.exit(1)

    # Registra no arquivo GeoJSON
    registrar_no_geojson(caminho_destino_completo, lat, lon, titulo, categoria)
    print("\n[OK] Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
