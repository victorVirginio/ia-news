
import http.server
import socketserver
import webbrowser
import json
import os
from urllib.parse import urlparse, parse_qs

class ReviewHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Processa ações da interface (aprovar/rejeitar)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            action = data.get('action')
            news_id = data.get('news_id')
            
            if action == 'approve':
                result = approve_news(news_id)
            elif action == 'reject':
                result = reject_news(news_id)
            else:
                result = False
            
            # Atualiza dados para interface
            generate_news_data_for_interface()
            
            # Resposta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': result}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

def start_review_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), ReviewHandler) as httpd:
        print(f"🌐 Servidor iniciado em http://localhost:{PORT}")
        print("📱 Interface de revisão disponível!")
        webbrowser.open(f'http://localhost:{PORT}/review.html')
        httpd.serve_forever()

if __name__ == "__main__":
    start_review_server()
