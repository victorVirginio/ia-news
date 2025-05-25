#!/usr/bin/env python3
"""
Publicar próxima notícia aprovada (publicação programada a cada 30min)
"""

import os
import json
import shutil
from datetime import datetime

def publish_next_article():
    """Publicar próxima notícia da fila de aprovadas"""
    approved_dir = 'dados/aprovados'
    published_dir = 'dados/publicados'
    
    if not os.path.exists(approved_dir):
        print("Diretório de aprovados não existe")
        return
        
    # Criar diretório de publicados
    os.makedirs(published_dir, exist_ok=True)
    
    # Listar arquivos aprovados
    approved_files = [f for f in os.listdir(approved_dir) if f.endswith('.json')]
    
    if not approved_files:
        print("Nenhuma notícia aprovada para publicar")
        return
        
    # Pegar o primeiro arquivo (mais antigo)
    next_file = sorted(approved_files)[0]
    approved_path = os.path.join(approved_dir, next_file)
    published_path = os.path.join(published_dir, next_file)
    
    # Ler artigo
    try:
        with open(approved_path, 'r', encoding='utf-8') as f:
            article = json.load(f)
            
        # Atualizar status
        article['status'] = 'published'
        article['published_at'] = datetime.now().isoformat()
        
        # Mover para publicados
        with open(published_path, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
            
        # Remover de aprovados (já foi publicado)
        os.remove(approved_path)
        
        print(f"📰 Publicado: {article['title'][:50]}...")
        print(f"Arquivo movido para: {published_path}")
        
        return True
        
    except Exception as e:
        print(f"Erro ao publicar {next_file}: {e}")
        return False

if __name__ == "__main__":
    success = publish_next_article()
    if success:
        print("✅ Publicação realizada com sucesso!")
    else:
        print("❌ Falha na publicação")
