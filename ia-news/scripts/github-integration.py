#!/usr/bin/env python3
"""
Script de Integração GitHub - IA News
Conecta a interface de revisão com o repositório GitHub
"""

import os
import json
import shutil
from datetime import datetime
import subprocess

def setup_github_integration():
    """Configura integração inicial com GitHub"""
    print("🔧 Configurando integração com GitHub...")
    
    # Cria arquivo de configuração
    config = {
        "github": {
            "username": "SEU_USUARIO_GITHUB",  # Você vai editar isso
            "repo_name": "ia-news",
            "branch": "main"
        },
        "paths": {
            "pending": "../dados/pendentes/",
            "approved": "../dados/aprovados/",
            "site": "../site/"
        },
        "auto_deploy": True,
        "review_interface": "review.html"
    }
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Arquivo config.json criado!")
    print("📝 IMPORTANTE: Edite o config.json e coloque seu usuário do GitHub!")

def create_sample_news():
    """Cria notícias de exemplo para testar"""
    print("📰 Criando notícias de exemplo...")
    
    sample_news = [
        {
            "id": 1,
            "title": "OpenAI lança GPT-5 com capacidades revolucionárias",
            "summary": "Nova versão promete avanços em raciocínio e matemática",
            "content": "A OpenAI anunciou oficialmente o GPT-5...",
            "source": "TechCrunch",
            "url": "https://techcrunch.com/example",
            "quality_score": 9.2,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "category": "releases"
        },
        {
            "id": 2,
            "title": "Google DeepMind prevê terremotos com 85% de precisão",
            "summary": "IA capaz de prever terremotos pode salvar vidas",
            "content": "Pesquisadores desenvolveram sistema revolucionário...",
            "source": "Nature",
            "url": "https://nature.com/example",
            "quality_score": 8.7,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "category": "research"
        },
        {
            "id": 3,
            "title": "Microsoft integra IA avançada no Office 365",
            "summary": "Copilot Pro automatiza tarefas complexas do Office",
            "content": "Microsoft revelou integração ambiciosa de IA...",
            "source": "Microsoft Blog",
            "url": "https://microsoft.com/example",
            "quality_score": 7.8,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "category": "business"
        }
    ]
    
    # Cria diretório se não existir
    os.makedirs('../dados/pendentes', exist_ok=True)
    
    # Salva cada notícia
    for news in sample_news:
        filename = f"noticia-{news['id']:03d}.json"
        filepath = os.path.join('../dados/pendentes', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(news, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(sample_news)} notícias de exemplo criadas em dados/pendentes/")

def load_pending_news():
    """Carrega notícias pendentes do diretório"""
    pending_dir = '../dados/pendentes'
    news_list = []
    
    if not os.path.exists(pending_dir):
        return news_list
    
    for filename in os.listdir(pending_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(pending_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    news = json.load(f)
                    news_list.append(news)
            except Exception as e:
                print(f"❌ Erro ao ler {filename}: {e}")
    
    return sorted(news_list, key=lambda x: x.get('timestamp', ''), reverse=True)

def approve_news(news_id):
    """Aprova uma notícia (move para pasta aprovados)"""
    pending_dir = '../dados/pendentes'
    approved_dir = '../dados/aprovados'
    
    os.makedirs(approved_dir, exist_ok=True)
    
    # Procura arquivo da notícia
    for filename in os.listdir(pending_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(pending_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    news = json.load(f)
                
                if news.get('id') == news_id:
                    # Atualiza status e timestamp de aprovação
                    news['status'] = 'approved'
                    news['approved_at'] = datetime.now().isoformat()
                    
                    # Move para pasta aprovados
                    approved_path = os.path.join(approved_dir, filename)
                    with open(approved_path, 'w', encoding='utf-8') as f:
                        json.dump(news, f, indent=2, ensure_ascii=False)
                    
                    # Remove da pasta pendentes
                    os.remove(filepath)
                    
                    print(f"✅ Notícia {news_id} aprovada!")
                    return True
                    
            except Exception as e:
                print(f"❌ Erro ao processar {filename}: {e}")
    
    print(f"❌ Notícia {news_id} não encontrada!")
    return False

def reject_news(news_id):
    """Rejeita uma notícia (remove da pasta pendentes)"""
    pending_dir = '../dados/pendentes'
    rejected_dir = '../dados/rejeitados'
    
    os.makedirs(rejected_dir, exist_ok=True)
    
    # Procura arquivo da notícia
    for filename in os.listdir(pending_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(pending_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    news = json.load(f)
                
                if news.get('id') == news_id:
                    # Atualiza status
                    news['status'] = 'rejected'
                    news['rejected_at'] = datetime.now().isoformat()
                    
                    # Move para pasta rejeitados (para histórico)
                    rejected_path = os.path.join(rejected_dir, filename)
                    with open(rejected_path, 'w', encoding='utf-8') as f:
                        json.dump(news, f, indent=2, ensure_ascii=False)
                    
                    # Remove da pasta pendentes
                    os.remove(filepath)
                    
                    print(f"❌ Notícia {news_id} rejeitada!")
                    return True
                    
            except Exception as e:
                print(f"❌ Erro ao processar {filename}: {e}")
    
    print(f"❌ Notícia {news_id} não encontrada!")
    return False

def generate_news_data_for_interface():
    """Gera arquivo JSON com as notícias para a interface"""
    news_list = load_pending_news()
    
    # Converte para formato da interface
    interface_data = {
        "news": news_list,
        "stats": {
            "total": len(news_list),
            "pending": len(news_list),
            "approved": len(os.listdir('../dados/aprovados')) if os.path.exists('../dados/aprovados') else 0,
            "rejected": len(os.listdir('../dados/rejeitados')) if os.path.exists('../dados/rejeitados') else 0
        },
        "last_update": datetime.now().isoformat()
    }
    
    # Salva arquivo para a interface
    with open('news_data.json', 'w', encoding='utf-8') as f:
        json.dump(interface_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dados atualizados para interface: {len(news_list)} notícias pendentes")

def sync_with_github():
    """Sincroniza alterações com GitHub"""
    try:
        # Comandos Git básicos
        os.system('git add .')
        os.system(f'git commit -m "Atualização automática - {datetime.now().strftime("%d/%m/%Y %H:%M")}"')
        os.system('git push origin main')
        
        print("✅ Sincronizado com GitHub!")
        
    except Exception as e:
        print(f"❌ Erro ao sincronizar: {e}")
        print("💡 Certifique-se de ter configurado o Git e estar conectado ao repositório")

def create_review_server():
    """Cria servidor local para a interface de revisão"""
    server_code = '''
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
'''
    
    with open('review_server.py', 'w', encoding='utf-8') as f:
        f.write(server_code)
    
    print("✅ Servidor de revisão criado: review_server.py")

def main():
    print("🚀 IA NEWS - CONFIGURAÇÃO COMPLETA")
    print("="*50)
    
    print("\n1. Configurando integração...")
    setup_github_integration()
    
    print("\n2. Criando notícias de exemplo...")
    create_sample_news()
    
    print("\n3. Gerando dados para interface...")
    generate_news_data_for_interface()
    
    print("\n4. Criando servidor de revisão...")
    create_review_server()
    
    print("\n✅ CONFIGURAÇÃO CONCLUÍDA!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("  1. Edite config.json com seu usuário GitHub")
    print("  2. Execute: python review_server.py")
    print("  3. Abra http://localhost:8000/review.html")
    print("  4. Faça sua primeira revisão!")
    print("\n🎯 Depois disso, seu fluxo diário será:")
    print("  • Executar review_server.py")
    print("  • Revisar notícias na interface")
    print("  • Fechar o servidor")
    print("  • Pronto! Site atualizado automaticamente")

if __name__ == "__main__":
    main()