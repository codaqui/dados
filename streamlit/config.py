# Configurações do Dashboard Codaqui
# Este arquivo contém configurações personalizáveis para o dashboard

# Configurações visuais
THEME_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'warning': '#ff6b6b',
    'info': '#17a2b8'
}

# Configurações de gráficos
CHART_CONFIG = {
    'color_scales': {
        'blues': 'Blues',
        'reds': 'Reds',
        'greens': 'Greens',
        'viridis': 'Viridis',
        'plasma': 'Plasma'
    },
    'default_height': 400,
    'default_width': 800
}

# Configurações de dados
DATA_CONFIG = {
    'max_top_pages': 20,
    'max_traffic_sources': 10,
    'default_comparison_periods': 3
}

# Textos personalizáveis
TEXTS = {
    'welcome_title': "Dashboard de Analytics da Codaqui! 📊",
    'about_description': """
    Este dashboard oferece insights abrangentes sobre o desempenho do site da Codaqui.dev,
    permitindo análises detalhadas de métricas de usuários, páginas e fontes de tráfego.
    """,
    'footer_text': "Codaqui.dev - Capacitando com dados para decisões inteligentes!"
}

# URLs importantes
URLS = {
    'main_site': 'https://www.codaqui.dev',
    'github': 'https://github.com/codaqui',
    'contact_email': 'contato@codaqui.dev'
}

# Configurações de métricas
METRICS_CONFIG = {
    'good_bounce_rate': 0.5,  # Taxa de rejeição considerada boa (abaixo de 50%)
    'good_session_duration': 120,  # Duração de sessão considerada boa (120 segundos)
    'metrics_format': {
        'users': '{:,}',
        'views': '{:,}',
        'duration': '{:.1f}s',
        'bounce_rate': '{:.1%}',
        'percentage': '{:.1f}%'
    }
}

# Configurações de exportação
EXPORT_CONFIG = {
    'csv_filename_template': 'relatorio_codaqui_{period}.csv',
    'include_charts_in_export': False
}
