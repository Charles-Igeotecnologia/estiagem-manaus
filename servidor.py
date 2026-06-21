import http.server
import json
import os
import sys

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Endpoint para salvar as atualizações do GeoJSON vindas do navegador
        if self.path == '/api/salvar':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Decodifica e valida o JSON recebido
                payload = json.loads(post_data.decode('utf-8'))
                
                # Caminho para gravar o arquivo no mesmo diretório do servidor
                geojson_path = os.path.join(os.getcwd(), 'data.geojson')
                
                # Grava o GeoJSON de volta no disco de forma formatada e legível
                with open(geojson_path, 'w', encoding='utf-8') as f:
                    json.dump(payload, f, indent=2, ensure_ascii=False)
                
                # Envia resposta de sucesso
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                # Suporte básico a CORS para desenvolvimento se necessário
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {"status": "success", "message": "data.geojson atualizado com sucesso!"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                print("[+] data.geojson atualizado com sucesso via API local.")
                
            except Exception as e:
                # Envia resposta de erro em caso de falha de gravação ou parse
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {"status": "error", "message": f"Erro ao salvar arquivo: {str(e)}"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                print(f"[-] Erro ao processar requisição POST /api/salvar: {e}")
        else:
            # Caso receba um POST para outro caminho
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Suporte a requisições prévias (preflight) de CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    # Garante que o servidor rode no diretório onde este arquivo está localizado
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, CustomHandler)
    
    print("=" * 70)
    print(f"   SERVIDOR WEB GIS 360° - ATIVO E ESCUTANDO NA PORTA {PORT}")
    print("=" * 70)
    print(f"   Diretório Servido: {os.getcwd()}")
    print("   Suporte a Salvamento Dinâmico (/api/salvar) HABILITADO.")
    print("=" * 70)
    print("   Pressione Ctrl+C para encerrar o servidor local.\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Encerrando o servidor local...")
        sys.exit(0)

if __name__ == '__main__':
    main()
