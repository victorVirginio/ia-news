<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA News - Painel Administrativo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 1rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .header h1 { color: #1e40af; font-size: 2rem; margin-bottom: 0.5rem; }
        .header p { color: #6b7280; font-size: 1.1rem; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        .stat-number { font-size: 2.5rem; font-weight: bold; color: #3b82f6; margin-bottom: 0.5rem; }
        .stat-label { color: #6b7280; font-weight: 500; }
        .admin-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 0.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        .tab-button {
            flex: 1;
            background: transparent;
            border: none;
            padding: 1rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .tab-button.active { background: #3b82f6; color: white; }
        .tab-button:not(.active) { color: #6b7280; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .section-title {
            font-size: 1.5rem;
            color: #1e40af;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e5e7eb;
        }
        .news-item {
            background: #f8fafc;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        .news-item:hover { border-color: #3b82f6; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1); }
        .news-meta { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; }
        .badge {
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .badge-source { background: #3b82f6; color: white; }
        .badge-quality { background: #10b981; color: white; }
        .badge-time { background: #6b7280; color: white; }
        .news-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: #1e40af;
            margin-bottom: 0.5rem;
        }
        .news-summary { color: #4b5563; line-height: 1.6; margin-bottom: 1rem; }
        .news-actions { display: flex; gap: 0.5rem; }
        .btn {
            padding: 0.6rem 1.2rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-approve { background: #10b981; color: white; }
        .btn-approve:hover { background: #059669; }
        .btn-reject { background: #ef4444; color: white; }
        .btn-reject:hover { background: #dc2626; }
        .btn-delete { background: #ef4444; color: white; }
        .btn-delete:hover { background: #dc2626; }
        .success-message {
            background: #d1fae5;
            border: 2px solid #10b981;
            color: #065f46;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            display: none;
        }
        .floating-fab {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        }
        .empty-state { text-align: center; padding: 3rem; color: #6b7280; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 IA News - Painel Administrativo</h1>
            <p>Sistema simplificado e funcional</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="pending-count">1</div>
                <div class="stat-label">Pendentes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="published-count">2</div>
                <div class="stat-label">Publicadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="rejected-count">1</div>
                <div class="stat-label">Rejeitadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="avg-quality">8.0</div>
                <div class="stat-label">Nota Média</div>
            </div>
        </div>

        <div class="admin-tabs">
            <button class="tab-button active" onclick="showTab('pending')">📋 Pendentes</button>
            <button class="tab-button" onclick="showTab('published')">✅ Publicadas</button>
            <button class="tab-button" onclick="showTab('rejected')">❌ Rejeitadas</button>
        </div>

        <div id="pending-tab" class="tab-content active">
            <div class="section">
                <div class="section-title">📋 Notícias Pendentes</div>
                <div class="success-message" id="success-msg">✅ Ação realizada!</div>
                <div id="pending-news"></div>
            </div>
        </div>

        <div id="published-tab" class="tab-content">
            <div class="section">
                <div class="section-title">✅ Notícias Publicadas</div>
                <div id="published-news"></div>
            </div>
        </div>

        <div id="rejected-tab" class="tab-content">
            <div class="section">
                <div class="section-title">❌ Notícias Rejeitadas</div>
                <div id="rejected-news"></div>
            </div>
        </div>
    </div>

    <button class="floating-fab" onclick="refreshData()">🔄</button>

    <script>
        // Dados que funcionam (sem localStorage)
        const newsData = {
            pending: [
                {
                    id: 'nvidia_001',
                    title: 'Nvidia Revela Nova Estratégia para Dominar o Mercado de IA em 2025',
                    summary: 'Jensen Huang anuncia tecnologia NVLink Fusion e expande foco no setor empresarial durante evento em Taiwan.',
                    source: 'Computex Taiwan',
                    quality: 8.5,
                    time: '15:30'
                }
            ],
            published: [
                {
                    id: 'tesla_001',
                    title: 'Tesla apresenta robô humanoide com IA avançada',
                    summary: 'Optimus Gen-3 demonstra capacidades impressionantes de interação.',
                    source: 'Reuters',
                    quality: 8.7,
                    time: '08:00'
                },
                {
                    id: 'startup_001',
                    title: 'Startup brasileira desenvolve IA para diagnóstico médico',
                    summary: 'Empresa de São Paulo cria sistema que detecta doenças raras.',
                    source: 'Folha de S.Paulo',
                    quality: 8.9,
                    time: '09:20'
                }
            ],
            rejected: [
                {
                    id: 'apple_001',
                    title: 'Rumores sobre nova IA da Apple',
                    summary: 'Especulações não confirmadas sobre desenvolvimento interno.',
                    source: 'Blog Tech',
                    quality: 6.2,
                    time: '07:30'
                }
            ]
        };

        function loadNews(category) {
            const container = document.getElementById(`${category}-news`);
            const articles = newsData[category];

            if (!articles || articles.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">📭</div>
                        <p>Nenhuma notícia ${category}</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = articles.map(article => `
                <div class="news-item">
                    <div class="news-meta">
                        <span class="badge badge-source">${article.source}</span>
                        <span class="badge badge-quality">★ ${article.quality}</span>
                        <span class="badge badge-time">${article.time}</span>
                    </div>
                    <div class="news-title">${article.title}</div>
                    <div class="news-summary">${article.summary}</div>
                    <div class="news-actions">
                        ${getActionButtons(category, article.id)}
                    </div>
                </div>
            `).join('');
        }

        function getActionButtons(category, itemId) {
            if (category === 'pending') {
                return `
                    <button class="btn btn-approve" onclick="approveNews('${itemId}')">✅ Aprovar</button>
                    <button class="btn btn-reject" onclick="rejectNews('${itemId}')">❌ Rejeitar</button>
                `;
            } else if (category === 'published' || category === 'rejected') {
                return `
                    <button class="btn btn-delete" onclick="deleteNews('${itemId}', '${category}')">🗑️ Excluir</button>
                `;
            }
            return '';
        }

        function approveNews(itemId) {
            const article = newsData.pending.find(a => a.id === itemId);
            if (article) {
                // Mover para publicadas
                newsData.pending = newsData.pending.filter(a => a.id !== itemId);
                newsData.published.push(article);
                
                showSuccess('Artigo aprovado e publicado!');
                refreshAll();
            }
        }

        function rejectNews(itemId) {
            const article = newsData.pending.find(a => a.id === itemId);
            if (article) {
                // Mover para rejeitadas
                newsData.pending = newsData.pending.filter(a => a.id !== itemId);
                newsData.rejected.push(article);
                
                showSuccess('Artigo rejeitado');
                refreshAll();
            }
        }

        function deleteNews(itemId, category) {
            if (confirm('Excluir permanentemente?')) {
                newsData[category] = newsData[category].filter(a => a.id !== itemId);
                showSuccess('Artigo excluído');
                refreshAll();
            }
        }

        function showTab(tabName) {
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            loadNews(tabName);
        }

        function showSuccess(message) {
            const msg = document.getElementById('success-msg');
            msg.textContent = '✅ ' + message;
            msg.style.display = 'block';
            setTimeout(() => msg.style.display = 'none', 3000);
        }

        function refreshAll() {
            loadNews('pending');
            loadNews('published');
            loadNews('rejected');
            updateStats();
        }

        function updateStats() {
            document.getElementById('pending-count').textContent = newsData.pending.length;
            document.getElementById('published-count').textContent = newsData.published.length;
            document.getElementById('rejected-count').textContent = newsData.rejected.length;
            
            const all = [...newsData.pending, ...newsData.published, ...newsData.rejected];
            const avg = all.length > 0 ? (all.reduce((s, a) => s + a.quality, 0) / all.length).toFixed(1) : '0.0';
            document.getElementById('avg-quality').textContent = avg;
        }

        function refreshData() {
            document.querySelector('.floating-fab').style.transform = 'rotate(360deg)';
            setTimeout(() => {
                refreshAll();
                document.querySelector('.floating-fab').style.transform = 'rotate(0deg)';
                showSuccess('Dados atualizados!');
            }, 1000);
        }

        // Inicializar
        document.addEventListener('DOMContentLoaded', () => {
            loadNews('pending');
            updateStats();
        });
    </script>
</body>
</html>
