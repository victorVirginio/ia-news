#!/usr/bin/env python3
"""
Atualizar o site público com as notícias aprovadas
"""

import os
import json
from datetime import datetime

def update_index_html():
    """Atualizar index.html com notícias aprovadas"""
    approved_dir = 'dados/aprovados'
    
    # Carregar notícias aprovadas
    articles = []
    if os.path.exists(approved_dir):
        for filename in os.listdir(approved_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(approved_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        article = json.load(f)
                        articles.append(article)
                except Exception as e:
                    print(f"Erro ao ler {filename}: {e}")
    
    # Ordenar por qualidade (melhores primeiro)
    articles.sort(key=lambda x: x.get('quality', 0), reverse=True)
    
    # Limitar a 10 artigos mais recentes
    recent_articles = articles[:10]
    
    # Template HTML com espaços publicitários
    html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA News - Notícias sobre Inteligência Artificial</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: #f8fafc;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Header com espaço publicitário */
        .top-ad {
            background: #e5e7eb;
            text-align: center;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            color: #6b7280;
            font-size: 0.9rem;
        }

        header {
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            color: white;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            font-size: 2rem;
            font-weight: bold;
            color: white;
            text-decoration: none;
        }

        .logo::before {
            content: "🤖";
            margin-right: 0.5rem;
            font-size: 2.5rem;
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: opacity 0.3s ease;
        }

        .nav-links a:hover {
            opacity: 0.8;
        }

        /* Main Layout com sidebar */
        .main-layout {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 2rem;
            padding: 2rem 0;
        }

        .content-area {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }

        .hero-banner h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        .hero-banner p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* News Section */
        .news-section {
            padding: 2rem;
        }

        .section-title {
            font-size: 1.8rem;
            color: #1e40af;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #3b82f6;
            display: inline-block;
        }

        .news-grid {
            display: grid;
            gap: 1.5rem;
        }

        .news-card {
            display: flex;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            border: 2px solid transparent;
        }

        .news-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
            border-color: #3b82f6;
        }

        .news-card.featured {
            grid-column: 1 / -1;
        }

        .news-card.featured .news-image {
            width: 400px;
            height: 250px;
        }

        .news-image {
            width: 200px;
            height: 140px;
            background: linear-gradient(135deg, #3b82f6, #1e40af);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            flex-shrink: 0;
        }

        .news-content {
            padding: 1.5rem;
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .news-meta {
            display: flex;
            gap: 1rem;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            color: #6b7280;
        }

        .news-source {
            background: #3b82f6;
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }

        .news-quality {
            background: #10b981;
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }

        .news-title {
            font-size: 1.3rem;
            font-weight: bold;
            color: #1e40af;
            margin-bottom: 0.8rem;
            line-height: 1.4;
        }

        .news-card.featured .news-title {
            font-size: 1.6rem;
        }

        .news-summary {
            color: #4b5563;
            margin-bottom: 1rem;
            flex: 1;
        }

        .read-more {
            color: #3b82f6;
            font-weight: bold;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: color 0.3s ease;
        }

        .read-more:hover {
            color: #1e40af;
        }

        /* Espaços publicitários */
        .ad-banner {
            background: #f3f4f6;
            border: 2px dashed #d1d5db;
            text-align: center;
            padding: 2rem;
            margin: 2rem 0;
            border-radius: 8px;
            color: #6b7280;
        }

        .sidebar-ad {
            background: #f3f4f6;
            border: 2px dashed #d1d5db;
            text-align: center;
            padding: 1.5rem;
            border-radius: 8px;
            color: #6b7280;
        }

        /* Sidebar Widgets */
        .widget {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .widget-header {
            background: #1e40af;
            color: white;
            padding: 1rem;
            font-weight: bold;
        }

        .widget-content {
            padding: 1rem;
        }

        .stats-widget .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid #e5e7eb;
        }

        .stats-widget .stat-item:last-child {
            border-bottom: none;
        }

        .stat-number {
            font-weight: bold;
            color: #3b82f6;
        }

        /* Article Page */
        .article-page {
            display: none;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .article-header {
            padding: 2rem;
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            color: white;
        }

        .back-button {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            cursor: pointer;
            margin-bottom: 1rem;
            transition: background 0.3s ease;
        }

        .back-button:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        .article-title {
            font-size: 2.2rem;
            margin-bottom: 1rem;
            line-height: 1.3;
        }

        .article-meta {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .article-content {
            padding: 2rem;
        }

        .article-image {
            width: 100%;
            height: 300px;
            background: linear-gradient(135deg, #3b82f6, #1e40af);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3rem;
            margin-bottom: 2rem;
        }

        .article-text {
            font-size: 1.1rem;
            line-height: 1.8;
            color: #374151;
        }

        .article-text p {
            margin-bottom: 1.5rem;
        }

        /* Footer */
        footer {
            background: #1f2937;
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-top: 3rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .main-layout {
                grid-template-columns: 1fr;
            }

            .news-card {
                flex-direction: column;
            }

            .news-card .news-image,
            .news-card.featured .news-image {
                width: 100%;
                height: 200px;
            }

            .hero-banner h1 {
                font-size: 2rem;
            }

            .nav-links {
                display: none;
            }
        }
    </style>
</head>
<body>
    <!-- Espaço publicitário superior -->
    <div class="container">
        <div class="top-ad">
            📢 Espaço Publicitário Premium - 728x90px
        </div>
    </div>

    <header>
        <nav class="container">
            <a href="#" class="logo" onclick="showHomePage()">IA News</a>
            <ul class="nav-links">
                <li><a href="#" onclick="showHomePage()">Início</a></li>
                <li><a href="#tecnologia">Tecnologia</a></li>
                <li><a href="#pesquisa">Pesquisa</a></li>
                <li><a href="#empresas">Empresas</a></li>
                <li><a href="admin.html">Admin</a></li>
            </ul>
        </nav>
    </header>

    <div class="container">
        <!-- HOME PAGE -->
        <div id="home-page">
            <div class="hero-banner">
                <h1>IA News</h1>
                <p>As principais notícias sobre Inteligência Artificial em português</p>
            </div>

            <div class="main-layout">
                <div class="content-area">
                    <div class="news-section">
                        <h2 class="section-title">Últimas Notícias</h2>
                        <div class="news-grid" id="news-grid">
                            <!-- Notícias serão carregadas aqui -->
                        </div>
                        
                        <!-- Espaço publicitário entre artigos -->
                        <div class="ad-banner">
                            📢 Espaço Publicitário - Banner 728x250px
                        </div>
                    </div>
                </div>

                <div class="sidebar">
                    <!-- Espaço publicitário sidebar -->
                    <div class="sidebar-ad">
                        📢 Anúncio Lateral<br>300x250px
                    </div>

                    <!-- Widget de Estatísticas -->
                    <div class="widget stats-widget">
                        <div class="widget-header">📊 Estatísticas</div>
                        <div class="widget-content">
                            <div class="stat-item">
                                <span>Notícias Hoje</span>
                                <span class="stat-number" id="news-today">0</span>
                            </div>
                            <div class="stat-item">
                                <span>Total Publicadas</span>
                                <span class="stat-number" id="total-published">0</span>
                            </div>
                            <div class="stat-item">
                                <span>Nota Média</span>
                                <span class="stat-number" id="avg-quality">0</span>
                            </div>
                        </div>
                    </div>

                    <!-- Outro espaço publicitário -->
                    <div class="sidebar-ad">
                        📢 Anúncio Lateral<br>300x600px
                    </div>
                </div>
            </div>
        </div>

        <!-- ARTICLE PAGE -->
        <div id="article-page" class="article-page">
            <!-- Conteúdo do artigo será inserido dinamicamente -->
        </div>
    </div>

    <footer>
        <div class="container">
            <p>&copy; 2025 IA News. Mantendo você informado sobre o futuro da Inteligência Artificial.</p>
        </div>
    </footer>

    <script>
        // Dados das notícias (atualizados automaticamente)
        const newsData = ARTICLES_DATA_PLACEHOLDER;

        // Função para carregar notícias na página inicial
        function loadNews() {
            const newsGrid = document.getElementById('news-grid');
            if (!newsData || newsData.length === 0) {
                newsGrid.innerHTML = '<p>Nenhuma notícia disponível no momento.</p>';
                return;
            }

            newsGrid.innerHTML = '';

            newsData.forEach((news, index) => {
                const newsCard = document.createElement('div');
                newsCard.className = `news-card ${index === 0 ? 'featured' : ''}`;
                newsCard.onclick = () => showArticle(news.id);
                
                const icon = '🤖';
                
                newsCard.innerHTML = `
                    <div class="news-image">${icon}</div>
                    <div class="news-content">
                        <div class="news-meta">
                            <span class="news-source">${news.source}</span>
                            <span class="news-quality">★ ${news.quality}</span>
                            <span>${news.time}</span>
                        </div>
                        <div class="news-title">${news.title}</div>
                        <div class="news-summary">${news.summary}</div>
                        <a href="#" class="read-more" onclick="event.preventDefault(); showArticle('${news.id}')">
                            Ler mais →
                        </a>
                    </div>
                `;
                
                newsGrid.appendChild(newsCard);
            });

            // Atualizar estatísticas
            updateStats();
        }

        // Função para mostrar artigo individual
        function showArticle(newsId) {
            const news = newsData.find(n => n.id === newsId);
            if (!news) return;

            const homePage = document.getElementById('home-page');
            const articlePage = document.getElementById('article-page');
            
            homePage.style.display = 'none';
            articlePage.style.display = 'block';
            
            const icon = '🤖';
            
            articlePage.innerHTML = `
                <div class="article-header">
                    <button class="back-button" onclick="showHomePage()">← Voltar</button>
                    <h1 class="article-title">${news.title}</h1>
                    <div class="article-meta">
                        <span class="news-source">${news.source}</span>
                        <span class="news-quality">★ ${news.quality}</span>
                        <span>${news.date} às ${news.time}</span>
                    </div>
                </div>
                <div class="article-content">
                    <div class="article-image">${icon}</div>
                    
                    <!-- Espaço publicitário no meio do artigo -->
                    <div class="ad-banner">
                        📢 Anúncio no Artigo - 728x200px
                    </div>
                    
                    <div class="article-text">
                        ${formatArticleContent(news.content)}
                    </div>
                </div>
            `;
            
            window.scrollTo(0, 0);
        }

        // Função para formatar conteúdo do artigo
        function formatArticleContent(content) {
            // Dividir em parágrafos
            const paragraphs = content.split('\\n').filter(p => p.trim());
            return paragraphs.map(p => `<p>${p}</p>`).join('');
        }

        // Função para mostrar página inicial
        function showHomePage() {
            const homePage = document.getElementById('home-page');
            const articlePage = document.getElementById('article-page');
            
            homePage.style.display = 'block';
            articlePage.style.display = 'none';
            
            window.scrollTo(0, 0);
        }

        // Função para atualizar estatísticas
        function updateStats() {
            const today = new Date().toISOString().split('T')[0];
            const todayNews = newsData.filter(n => n.date === today);
            
            document.getElementById('news-today').textContent = todayNews.length;
            document.getElementById('total-published').textContent = newsData.length;
            
            if (newsData.length > 0) {
                const avgQuality = (newsData.reduce((sum, n) => sum + n.quality, 0) / newsData.length).toFixed(1);
                document.getElementById('avg-quality').textContent = avgQuality;
            }
        }

        // Inicializar página
        document.addEventListener('DOMContentLoaded', function() {
            loadNews();
        });
    </script>
</body>
</html>"""

    # Substituir dados das notícias
    news_js_data = json.dumps(recent_articles, ensure_ascii=False, indent=2)
    final_html = html_template.replace('ARTICLES_DATA_PLACEHOLDER', news_js_data)
    
    # Salvar novo index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"✅ Site atualizado com {len(recent_articles)} notícias")

if __name__ == "__main__":
    update_index_html()
