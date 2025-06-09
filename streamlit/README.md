# 📊 Dashboard Analytics Codaqui

Um dashboard interativo e abrangente para análise de dados de analytics do site da Codaqui.dev.

## 🚀 Funcionalidades

### 🏠 Página Inicial
- Introdução ao dashboard
- Links úteis e informações sobre a Codaqui

### 📊 Visão Geral
- **Métricas principais**: Usuários ativos, visualizações, duração média e taxa de rejeição
- **Gráficos de tendência**: Evolução temporal das métricas
- **Dashboard combinado**: Todas as métricas em uma visualização
- **Filtros interativos**: Por ano e mês

### 📄 Análise de Páginas
- **Top páginas mais acessadas**: Ranking por usuários ativos e visualizações
- **Busca de páginas**: Filtro por URL
- **Evolução temporal**: Acompanhamento de páginas específicas ao longo do tempo
- **Métricas por página**: Views por usuário e outras estatísticas

### 🌐 Fontes de Tráfego
- **Distribuição de fontes**: Gráficos de pizza e barras
- **Evolução temporal**: Acompanhamento das principais fontes
- **Análise detalhada**: Tabela com porcentagens e volumes

### 🔍 Análise Comparativa
- **Comparação entre períodos**: Métricas lado a lado
- **Diferenças percentuais**: Crescimento/declínio entre períodos
- **Top páginas comparativo**: Páginas populares em diferentes períodos

### 📈 Relatório Mensal
- **Resumo executivo**: Visão completa de um mês específico
- **Performance vs média**: Comparação com histórico
- **Insights automáticos**: Recomendações baseadas nos dados
- **Exportação**: Download de relatórios em CSV

## 🛠️ Como Executar

### Pré-requisitos
- Python 3.11+
- Poetry (recomendado) ou pip

### Instalação com Poetry
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd dados

# Instale as dependências
poetry install

# Execute o dashboard
poetry run streamlit run streamlit/main.py
```

### Instalação com pip
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd dados

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run streamlit/main.py
```

### Acesso
Após executar, acesse: `http://localhost:8501`

## 📁 Estrutura de Dados

O dashboard espera dados organizados na seguinte estrutura:

```
data/
├── 2024-01/
│   ├── website_info.json
│   ├── pages_info.json
│   └── website_dimensions_info.json
├── 2024-02/
│   ├── website_info.json
│   ├── pages_info.json
│   └── website_dimensions_info.json
└── ...
```

### Formato dos Dados

#### website_info.json
```json
[{
    "activeUsers": "8849",
    "screenPageViews": "22422", 
    "averageSessionDuration": "131.289",
    "bounceRate": "0.400",
    "sessions": "10190"
}]
```

#### pages_info.json
```json
[{
    "pagePath": "/trilhas/github-starter/",
    "year": "2024",
    "month": "01", 
    "activeUsers": "803",
    "screenPageViews": "1349",
    "screenPageViewsPerSession": "1.336",
    "screenPageViewPerUser": "1.679",
    "averageSessionDuration": "139.737"
}]
```

#### website_dimensions_info.json
```json
{
    "new": 8493,
    "google": 9679,
    "returning": 1408,
    "(direct)": 468,
    "(not set)": 346
}
```

## ⚙️ Configuração

Edite o arquivo `streamlit/config.py` para personalizar:

- **Cores e temas**: Paleta de cores dos gráficos
- **Textos**: Títulos e descrições
- **Métricas**: Critérios de "bom" desempenho
- **Exportação**: Formatos e nomes de arquivo

## 🎨 Recursos Visuais

- **Gráficos interativos**: Plotly para visualizações dinâmicas
- **Layout responsivo**: Adapta-se a diferentes tamanhos de tela
- **Filtros intuitivos**: Seleção fácil de períodos e dados
- **Cores consistentes**: Esquema visual harmonioso
- **Métricas destacadas**: Cards com deltas e comparações

## 📊 Tipos de Visualização

- **Gráficos de linha**: Tendências temporais
- **Gráficos de barras**: Rankings e comparações
- **Gráficos de pizza**: Distribuições e proporções
- **Métricas em cards**: KPIs principais
- **Tabelas interativas**: Dados detalhados

## 🔄 Atualização de Dados

1. Adicione novos dados na estrutura `data/YYYY-MM/`
2. Reinicie o dashboard
3. Os novos dados aparecerão automaticamente nos filtros

## 🐛 Resolução de Problemas

### Dashboard não carrega dados
- Verifique se os arquivos JSON estão no formato correto
- Confirme a estrutura de pastas `data/YYYY-MM/`
- Verifique se os arquivos contêm dados válidos

### Gráficos não aparecem
- Verifique se o Plotly está instalado: `pip install plotly`
- Confirme se há dados para o período selecionado

### Erro de dependências
```bash
# Reinstale as dependências
poetry install --no-cache
# ou
pip install -r requirements.txt --force-reinstall
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Contato

- **Site**: [codaqui.dev](https://www.codaqui.dev)
- **Email**: contato@codaqui.dev
- **GitHub**: [github.com/codaqui](https://github.com/codaqui)

---

**Codaqui.dev** - Transformando dados em conhecimento! 🚀📊
