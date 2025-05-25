#!/usr/bin/env python3
"""
Sistema de Coleta e Tradução de Notícias - IA News
Coleta notícias de fontes confiáveis, traduz e prepara para revisão
"""

import os
import json
import requests
import feedparser
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin
import time
import random
from googletrans import Translator
from bs4 import BeautifulSoup
import hashlib

class NewsCollector:
    def __init__(self):
        self.translator = Translator()
        self.sources = {
            'techcrunch': {
                'rss': 'https://techcrunch.com/category/artificial-intelligence/feed/',
                'quality_base': 8.0,
                'keywords': ['ai', 'artificial intelligence', 'machine learning', 'neural', 'openai', 'google ai']
            },
            'mit_news': {
                'rss': 'https://news.mit.edu/rss/topic/artificial-intelligence2',
                'quality_base': 9.0,
                'keywords': ['artificial intelligence', 'ai research', 'machine learning', 'deep learning']
            },
            'wired': {
                'rss': 'https://www.wired.com/feed/tag/ai/latest/rss',
                'quality_base': 8.5,
                'keywords': ['artificial intelligence', 'ai', 'machine learning', 'automation']
            },
            'reuters_tech': {
                'rss': 'https://www.reuters.com/technology/artificial-intelligence/rss',
                'quality_base': 8.8,
                'keywords': ['ai', 'artificial intelligence', 'tech companies', 'innovation']
            },
            'ai_news': {
                'rss': 'https://www.artificialintelligence-news.com/feed/',
                'quality_base': 7.5,
                'keywords': ['ai', 'artificial intelligence', 'machine learning', 'deep learning']
            },
            'google_ai': {
                'rss': 'https://ai.googleblog.com/feeds/posts/default',
                'quality_base': 9.2,
                'keywords': ['ai', 'machine learning', 'research', 'google ai']
            }
        }
        
        self.output_dir = 'dados/pendentes'
        self.processed_file = 'dados/processed_urls.json'
        self.ensure_directories()
        
    def ensure_directories(self):
        """Criar diretórios necessários"""
        os.makedirs('dados/pendentes', exist_ok=True)
        os.makedirs('dados/aprovados', exist_ok=True)
        os.makedirs('dados/rejeitados', exist_ok=True)
        
    def load_processed_urls(self):
        """Carregar URLs já processadas"""
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()
        
    def save_processed_urls(self, urls):
        """Salvar URLs processadas"""
        with open(self.processed_file, 'w', encoding='utf-8') as f:
            json.dump(list(urls), f, indent=2)
            
    def clean_text(self, text):
        """Limpar texto removendo HTML e caracteres especiais"""
        if not text:
            return ""
        
        # Remover HTML
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
        
        # Limpar caracteres especiais
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
        
    def translate_text(self, text, max_retries=3):
        """Traduzir texto para português com retry"""
        if not text:
            return text
            
        for attempt in range(max_retries):
            try:
                # Dividir texto longo em chunks
                if len(text) > 4000:
                    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
                    translated_chunks = []
                    
                    for chunk in chunks:
                        time.sleep(1)  # Rate limiting
                        result = self.translator.translate(chunk, dest='pt', src='en')
                        translated_chunks.append(result.text)
                        
                    return ' '.join(translated_chunks)
                else:
                    result = self.translator.translate(text, dest='pt', src='en')
                    return result.text
                    
            except Exception as e:
                print(f"Erro na tradução (tentativa {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Backoff exponencial
                else:
                    print("Falha na tradução, retornando texto original")
                    return text
                    
        return text
        
    def calculate_quality_score(self, article, source_info):
        """Calcular nota de qualidade da notícia"""
        score = source_info['quality_base']
        
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        content = title + ' ' + summary
        
        # Bonus por palavras-chave relevantes
        keyword_count = sum(1 for keyword in source_info['keywords'] 
                          if keyword in content)
        score += keyword_count * 0.2
        
        # Bonus por comprimento adequado
        word_count = len(summary.split())
        if 100 <= word_count <= 800:
            score += 0.3
        elif word_count < 50:
            score -= 1.0
            
        # Penalidade por títulos muito genéricos
        generic_words = ['new', 'latest', 'breaking', 'update']
        if any(word in title for word in generic_words):
            score -= 0.2
            
        # Bonus por recência
        pub_date = article.get('published_parsed')
        if pub_date:
            days_old = (datetime.now() - datetime(*pub_date[:6])).days
            if days_old == 0:
                score += 0.5
            elif days_old <= 2:
                score += 0.2
                
        return min(10.0, max(1.0, round(score, 1)))
        
    def extract_content_from_url(self, url):
        """Extrair conteúdo completo de uma URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover elementos desnecessários
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                tag.decompose()
                
            # Tentar encontrar o conteúdo principal
            content_selectors = [
                'article', '.post-content', '.entry-content', 
                '.article-content', '.story-body', '.content'
            ]
            
            content = ""
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text()
                    break
                    
            if not content:
                # Fallback: pegar todos os parágrafos
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text() for p in paragraphs])
                
            return self.clean_text(content)[:2000]  # Limitar tamanho
            
        except Exception as e:
            print(f"Erro ao extrair conteúdo de {url}: {e}")
            return ""
            
    def process_feed(self, source_name, source_info):
        """Processar feed RSS de uma fonte"""
        print(f"Processando {source_name}...")
        
        try:
            feed = feedparser.parse(source_info['rss'])
            articles = []
            
            for entry in feed.entries[:10]:  # Limitar a 10 artigos por fonte
                # Verificar se já foi processado
                article_id = hashlib.md5(entry.link.encode()).hexdigest()
                
                # Extrair conteúdo adicional se necessário
                full_content = ""
                if len(entry.get('summary', '')) < 200:
                    full_content = self.extract_content_from_url(entry.link)
                
                # Combinar resumo e conteúdo
                content = entry.get('summary', '') + ' ' + full_content
                content = self.clean_text(content)
                
                # Garantir tamanho adequado (150-500 palavras)
                words = content.split()
                if len(words) > 500:
                    content = ' '.join(words[:500])
                elif len(words) < 150 and full_content:
                    # Tentar pegar mais conteúdo
                    additional_content = self.extract_content_from_url(entry.link)
                    content = (content + ' ' + additional_content)[:2000]
                    words = content.split()
                    if len(words) > 500:
                        content = ' '.join(words[:500])
                
                article = {
                    'id': article_id,
                    'title': entry.title,
                    'summary': entry.get('summary', ''),
                    'content': content,
                    'url': entry.link,
                    'source': source_name,
                    'published': entry.get('published', ''),
                    'collected_at': datetime.now().isoformat()
                }
                
                # Calcular qualidade
                article['quality'] = self.calculate_quality_score(article, source_info)
                
                # Filtrar por qualidade mínima
                if article['quality'] >= 6.0:
                    articles.append(article)
                    
            return articles
            
        except Exception as e:
            print(f"Erro ao processar {source_name}: {e}")
            return []
            
    def translate_article(self, article):
        """Traduzir artigo completo"""
        print(f"Traduzindo: {article['title'][:50]}...")
        
        # Traduzir título
        article['title_pt'] = self.translate_text(article['title'])
        
        # Traduzir resumo
        article['summary_pt'] = self.translate_text(article['summary'])
        
        # Traduzir conteúdo
        article['content_pt'] = self.translate_text(article['content'])
        
        # Verificar se as traduções ficaram boas
        if len(article['content_pt'].split()) < 150:
            # Tentar traduzir novamente com mais contexto
            full_text = f"{article['title']}. {article['summary']}. {article['content']}"
            translated_full = self.translate_text(full_text)
            article['content_pt'] = translated_full
            
        return article
        
    def save_article(self, article):
        """Salvar artigo como JSON"""
        filename = f"noticia_{article['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Estrutura final do artigo
        final_article = {
            'id': article['id'],
            'title': article['title_pt'],
            'summary': article['summary_pt'],
            'content': article['content_pt'],
            'source': article['source'].replace('_', ' ').title(),
            'quality': article['quality'],
            'url_original': article['url'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M'),
            'status': 'pending',
            'collected_at': article['collected_at'],
            'word_count': len(article['content_pt'].split())
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(final_article, f, indent=2, ensure_ascii=False)
            
        print(f"Artigo salvo: {filename}")
        return filepath
        
    def collect_news(self, max_articles=10):
        """Função principal para coletar notícias"""
        print("🤖 IA NEWS - COLETA AUTOMÁTICA DE NOTÍCIAS")
        print("=" * 50)
        
        processed_urls = self.load_processed_urls()
        all_articles = []
        
        # Coletar de todas as fontes
        for source_name, source_info in self.sources.items():
            articles = self.process_feed(source_name, source_info)
            
            # Filtrar URLs já processadas
            new_articles = [a for a in articles if a['url'] not in processed_urls]
            
            all_articles.extend(new_articles)
            
            # Atualizar URLs processadas
            for article in new_articles:
                processed_urls.add(article['url'])
                
            time.sleep(2)  # Rate limiting entre fontes
            
        # Ordenar por qualidade e pegar os melhores
        all_articles.sort(key=lambda x: x['quality'], reverse=True)
        selected_articles = all_articles[:max_articles]
        
        print(f"\n📊 Coletados {len(all_articles)} artigos, selecionados {len(selected_articles)}")
        
        # Traduzir e salvar artigos selecionados
        saved_files = []
        for i, article in enumerate(selected_articles):
            print(f"\n[{i+1}/{len(selected_articles)}] Processando...")
            
            # Traduzir
            translated_article = self.translate_article(article)
            
            # Salvar
            filepath = self.save_article(translated_article)
            saved_files.append(filepath)
            
            time.sleep(1)  # Rate limiting
            
        # Salvar URLs processadas
        self.save_processed_urls(processed_urls)
        
        print(f"\n✅ Coleta concluída! {len(saved_files)} artigos salvos em {self.output_dir}")
        return saved_files

def main():
    collector = NewsCollector()
    collector.collect_news()

if __name__ == "__main__":
    main()
