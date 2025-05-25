#!/usr/bin/env python3
"""
Auto-aprovação das 5 melhores notícias quando não há revisão manual
"""

import os
import json
import shutil
from datetime import datetime

def auto_approve_best():
    """Auto-aprovar as 5 melhores notícias pendentes"""
    pending_dir = 'dados/pendentes'
    approved_dir = 'dados/aprovados'
    
    if not os.path.exists(pending_dir):
        return
        
    # Carregar todas as notícias pendentes
    articles = []
    for filename in os.listdir(pending_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(pending_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    article = json.load(f)
                    article['filename'] = filename
                    articles.append(article)
            except Exception as e:
                print(f"Erro ao ler {filename}: {e}")
                
    if not articles:
        print("Nenhuma notícia pendente encontrada")
        return
        
    # Ordenar por qualidade (melhores primeiro)
    articles.sort(key=lambda x: x.get('quality', 0), reverse=True)
    
    # Pegar as 5 melhores
    best_articles = articles[:5]
    
    print(f"Auto-aprovando {len(best_articles)} notícias...")
    
    # Mover para aprovados
    os.makedirs(approved_dir, exist_ok=True)
    
    for article in best_articles:
        old_path = os.path.join(pending_dir, article['filename'])
        new_path = os.path.join(approved_dir, article['filename'])
        
        # Atualizar status
        article['status'] = 'approved'
        article['approved_at'] = datetime.now().isoformat()
        article['approved_by'] = 'auto_system'
        
        # Salvar no diretório de aprovados
        with open(new_path, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
            
        # Remover do pendente
        os.remove(old_path)
        
        print(f"✅ Auto-aprovado: {article['title'][:50]}... (Nota: {article['quality']})")

if __name__ == "__main__":
    auto_approve_best()
