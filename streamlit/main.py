import os
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Dashboard Codaqui",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = "data"
ALL_FILES = []
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        ALL_FILES.append(os.path.join(root, file))


def intro():
    st.write("# Dashboard de Analytics da Codaqui! �")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://github.com/codaqui/institucional/raw/main/images/header.png", use_column_width=True)
    
    st.write(
        """
        ## 🎯 Bem-vindo ao Centro de Analytics da Codaqui!
        
        Este dashboard oferece insights abrangentes sobre o desempenho do site da Codaqui.dev,
        permitindo análises detalhadas de:
        
        - 📈 **Métricas Gerais**: Usuários ativos, visualizações, sessões e bounce rate
        - 📄 **Análise de Páginas**: Performance de conteúdos específicos
        - 🌐 **Fontes de Tráfego**: De onde vêm nossos visitantes
        - 📅 **Tendências Temporais**: Evolução dos dados ao longo do tempo
        - 🔍 **Comparações**: Análises comparativas entre períodos
        
        ### 🚀 Como usar:
        1. **Navegue** pelas seções no menu lateral
        2. **Selecione** os períodos de interesse
        3. **Explore** os gráficos interativos
        4. **Compare** diferentes métricas e períodos
        
        ---
        
        **Codaqui.dev** - Capacitando nossos alunos com análise de dados para decisões inteligentes!
        
        [🌐 Visite nosso site](https://www.codaqui.dev) | [📧 Entre em contato](mailto:contato@codaqui.dev)
        """
    )


def load_all_data():
    """Carrega todos os dados dos arquivos JSON organizados por mês"""
    website_data = []
    pages_data = []
    dimensions_data = []
    
    # Padrão para extrair ano e mês do caminho
    for root, dirs, files in os.walk(DATA_DIR):
        if 'website_info.json' in files:
            # Extrai ano e mês do caminho (ex: data/2024-01/)
            path_parts = root.split('/')
            if len(path_parts) >= 2:
                year_month = path_parts[-1]  # ex: 2024-01
                try:
                    year, month = year_month.split('-')
                    
                    # Carrega website_info.json
                    with open(os.path.join(root, 'website_info.json'), 'r') as f:
                        data = json.load(f)[0]  # Assumindo que é uma lista com um item
                        data['year'] = int(year)
                        data['month'] = int(month)
                        data['year_month'] = year_month
                        # Converte strings para números
                        for key in ['activeUsers', 'screenPageViews', 'sessions']:
                            if key in data:
                                data[key] = int(data[key])
                        for key in ['averageSessionDuration', 'bounceRate']:
                            if key in data:
                                data[key] = float(data[key])
                        website_data.append(data)
                    
                    # Carrega pages_info.json
                    pages_file = os.path.join(root, 'pages_info.json')
                    if os.path.exists(pages_file):
                        with open(pages_file, 'r') as f:
                            pages_list = json.load(f)
                            for page in pages_list:
                                page['year'] = int(year)
                                page['month'] = int(month)
                                page['year_month'] = year_month
                                # Converte strings para números
                                for key in ['activeUsers', 'screenPageViews']:
                                    if key in page:
                                        page[key] = int(page[key])
                                pages_data.append(page)
                    
                    # Carrega website_dimensions_info.json
                    dimensions_file = os.path.join(root, 'website_dimensions_info.json')
                    if os.path.exists(dimensions_file):
                        with open(dimensions_file, 'r') as f:
                            dims = json.load(f)
                            # Transforma em lista de dicionários
                            for source, count in dims.items():
                                dimensions_data.append({
                                    'source': source,
                                    'count': int(count),
                                    'year': int(year),
                                    'month': int(month),
                                    'year_month': year_month
                                })
                
                except ValueError:
                    # Ignora diretórios que não seguem o padrão YYYY-MM
                    continue
    
    return pd.DataFrame(website_data), pd.DataFrame(pages_data), pd.DataFrame(dimensions_data)


def overview_dashboard():
    st.title("📊 Visão Geral - Analytics")
    
    # Carrega todos os dados
    website_df, pages_df, dimensions_df = load_all_data()
    
    if website_df.empty:
        st.error("Nenhum dado encontrado. Verifique se os arquivos estão no formato correto.")
        return
    
    # Sidebar para filtros
    st.sidebar.header("🔧 Filtros")
    
    # Filtro de período
    years = sorted(website_df['year'].unique())
    months = sorted(website_df['month'].unique())
    
    selected_years = st.sidebar.multiselect(
        "Selecione os anos:",
        years,
        default=years
    )
    
    selected_months = st.sidebar.multiselect(
        "Selecione os meses:",
        months,
        default=months
    )
    
    # Filtrar dados
    filtered_website = website_df[
        (website_df['year'].isin(selected_years)) & 
        (website_df['month'].isin(selected_months))
    ]
    
    if filtered_website.empty:
        st.warning("Nenhum dado encontrado para o período selecionado.")
        return
    
    # Métricas principais
    st.header("🎯 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = filtered_website['activeUsers'].sum()
        st.metric(
            label="👥 Usuários Ativos",
            value=f"{total_users:,}",
            delta=f"{total_users/len(filtered_website):.0f} média/mês"
        )
    
    with col2:
        total_views = filtered_website['screenPageViews'].sum()
        st.metric(
            label="👀 Visualizações",
            value=f"{total_views:,}",
            delta=f"{total_views/len(filtered_website):.0f} média/mês"
        )
    
    with col3:
        avg_duration = filtered_website['averageSessionDuration'].mean()
        st.metric(
            label="⏱️ Duração Média (s)",
            value=f"{avg_duration:.1f}",
            delta=f"{avg_duration/60:.1f} minutos"
        )
    
    with col4:
        avg_bounce = filtered_website['bounceRate'].mean()
        st.metric(
            label="📉 Taxa de Rejeição",
            value=f"{avg_bounce:.1%}",
            delta="Menor é melhor"
        )
    
    # Gráficos de tendência
    st.header("📈 Tendências Temporais")
    
    # Ordena por ano e mês
    filtered_website = filtered_website.sort_values(['year', 'month'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_users = px.line(
            filtered_website, 
            x='year_month', 
            y='activeUsers',
            title='Evolução de Usuários Ativos',
            markers=True
        )
        fig_users.update_layout(xaxis_title="Período", yaxis_title="Usuários Ativos")
        st.plotly_chart(fig_users, use_container_width=True)
    
    with col2:
        fig_views = px.line(
            filtered_website, 
            x='year_month', 
            y='screenPageViews',
            title='Evolução de Visualizações',
            markers=True,
            color_discrete_sequence=['#ff6b6b']
        )
        fig_views.update_layout(xaxis_title="Período", yaxis_title="Visualizações")
        st.plotly_chart(fig_views, use_container_width=True)
    
    # Gráfico combinado
    fig_combined = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Usuários Ativos', 'Visualizações', 'Duração Média da Sessão', 'Taxa de Rejeição'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig_combined.add_trace(
        go.Scatter(x=filtered_website['year_month'], y=filtered_website['activeUsers'], 
                  mode='lines+markers', name='Usuários'),
        row=1, col=1
    )
    
    fig_combined.add_trace(
        go.Scatter(x=filtered_website['year_month'], y=filtered_website['screenPageViews'], 
                  mode='lines+markers', name='Visualizações'),
        row=1, col=2
    )
    
    fig_combined.add_trace(
        go.Scatter(x=filtered_website['year_month'], y=filtered_website['averageSessionDuration'], 
                  mode='lines+markers', name='Duração'),
        row=2, col=1
    )
    
    fig_combined.add_trace(
        go.Scatter(x=filtered_website['year_month'], y=filtered_website['bounceRate'], 
                  mode='lines+markers', name='Bounce Rate'),
        row=2, col=2
    )
    
    fig_combined.update_layout(height=600, title_text="Dashboard Completo de Métricas", showlegend=False)
    st.plotly_chart(fig_combined, use_container_width=True)


def pages_analysis():
    st.title("📄 Análise de Páginas")
    
    # Carrega dados
    website_df, pages_df, dimensions_df = load_all_data()
    
    if pages_df.empty:
        st.error("Nenhum dado de páginas encontrado.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔧 Filtros de Páginas")
    
    years = sorted(pages_df['year'].unique())
    months = sorted(pages_df['month'].unique())
    
    selected_years = st.sidebar.multiselect(
        "Anos:", years, default=years, key="pages_years"
    )
    selected_months = st.sidebar.multiselect(
        "Meses:", months, default=months, key="pages_months"
    )
    
    # Filtrar dados
    filtered_pages = pages_df[
        (pages_df['year'].isin(selected_years)) & 
        (pages_df['month'].isin(selected_months))
    ]
    
    if filtered_pages.empty:
        st.warning("Nenhum dado encontrado para o período selecionado.")
        return
    
    # Top páginas
    st.header("🏆 Top 20 Páginas Mais Acessadas")
    
    # Agrupa por página e soma usuários ativos
    top_pages = filtered_pages.groupby('pagePath').agg({
        'activeUsers': 'sum',
        'screenPageViews': 'sum'
    }).reset_index().sort_values('activeUsers', ascending=False).head(20)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pages_users = px.bar(
            top_pages.head(10), 
            x='activeUsers', 
            y='pagePath',
            orientation='h',
            title='Top 10 - Usuários Ativos',
            color='activeUsers',
            color_continuous_scale='Blues'
        )
        fig_pages_users.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_pages_users, use_container_width=True)
    
    with col2:
        fig_pages_views = px.bar(
            top_pages.head(10), 
            x='screenPageViews', 
            y='pagePath',
            orientation='h',
            title='Top 10 - Visualizações',
            color='screenPageViews',
            color_continuous_scale='Reds'
        )
        fig_pages_views.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_pages_views, use_container_width=True)
    
    # Tabela detalhada
    st.header("📋 Tabela Detalhada")
    
    # Adiciona filtro de busca
    search_term = st.text_input("🔍 Buscar página (digite parte da URL):")
    
    if search_term:
        top_pages = top_pages[top_pages['pagePath'].str.contains(search_term, case=False, na=False)]
    
    # Adiciona métricas calculadas
    top_pages['views_per_user'] = (top_pages['screenPageViews'] / top_pages['activeUsers']).round(2)
    
    st.dataframe(
        top_pages.rename(columns={
            'pagePath': 'Página',
            'activeUsers': 'Usuários Ativos',
            'screenPageViews': 'Visualizações',
            'views_per_user': 'Views/Usuário'
        }),
        use_container_width=True
    )
    
    # Análise temporal de páginas específicas
    st.header("📈 Evolução Temporal de Páginas")
    
    # Selecionar páginas para análise
    available_pages = pages_df['pagePath'].unique()
    selected_pages = st.multiselect(
        "Selecione páginas para comparar:",
        available_pages[:20],  # Limita para não sobrecarregar
        default=available_pages[:3] if len(available_pages) >= 3 else available_pages
    )
    
    if selected_pages:
        temporal_data = filtered_pages[filtered_pages['pagePath'].isin(selected_pages)]
        temporal_summary = temporal_data.groupby(['year_month', 'pagePath']).agg({
            'activeUsers': 'sum'
        }).reset_index()
        
        fig_temporal = px.line(
            temporal_summary,
            x='year_month',
            y='activeUsers',
            color='pagePath',
            title='Evolução de Usuários Ativos por Página',
            markers=True
        )
        fig_temporal.update_layout(xaxis_title="Período", yaxis_title="Usuários Ativos")
        st.plotly_chart(fig_temporal, use_container_width=True)


def traffic_sources_analysis():
    st.title("🌐 Análise de Fontes de Tráfego")
    
    # Carrega dados
    website_df, pages_df, dimensions_df = load_all_data()
    
    if dimensions_df.empty:
        st.error("Nenhum dado de fontes de tráfego encontrado.")
        return
    
    # Filtros
    st.sidebar.header("🔧 Filtros de Tráfego")
    
    years = sorted(dimensions_df['year'].unique())
    months = sorted(dimensions_df['month'].unique())
    
    selected_years = st.sidebar.multiselect(
        "Anos:", years, default=years, key="traffic_years"
    )
    selected_months = st.sidebar.multiselect(
        "Meses:", months, default=months, key="traffic_months"
    )
    
    # Filtrar dados
    filtered_dimensions = dimensions_df[
        (dimensions_df['year'].isin(selected_years)) & 
        (dimensions_df['month'].isin(selected_months))
    ]
    
    if filtered_dimensions.empty:
        st.warning("Nenhum dado encontrado para o período selecionado.")
        return
    
    # Métricas principais
    st.header("📊 Distribuição de Fontes de Tráfego")
    
    # Agrupa por fonte
    traffic_summary = filtered_dimensions.groupby('source').agg({
        'count': 'sum'
    }).reset_index().sort_values('count', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza
        fig_pie = px.pie(
            traffic_summary.head(10), 
            values='count', 
            names='source',
            title='Top 10 Fontes de Tráfego'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Gráfico de barras
        fig_bar = px.bar(
            traffic_summary.head(10),
            x='count',
            y='source',
            orientation='h',
            title='Volume por Fonte',
            color='count',
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Evolução temporal das principais fontes
    st.header("📈 Evolução das Principais Fontes")
    
    # Top 5 fontes
    top_sources = traffic_summary.head(5)['source'].tolist()
    
    temporal_traffic = filtered_dimensions[filtered_dimensions['source'].isin(top_sources)]
    temporal_summary = temporal_traffic.groupby(['year_month', 'source']).agg({
        'count': 'sum'
    }).reset_index()
    
    fig_temporal_traffic = px.line(
        temporal_summary,
        x='year_month',
        y='count',
        color='source',
        title='Evolução das Top 5 Fontes de Tráfego',
        markers=True
    )
    fig_temporal_traffic.update_layout(xaxis_title="Período", yaxis_title="Volume de Tráfego")
    st.plotly_chart(fig_temporal_traffic, use_container_width=True)
    
    # Tabela detalhada
    st.header("📋 Tabela de Fontes Detalhada")
    
    # Calcula porcentagem
    total_traffic = traffic_summary['count'].sum()
    traffic_summary['percentage'] = (traffic_summary['count'] / total_traffic * 100).round(2)
    
    st.dataframe(
        traffic_summary.rename(columns={
            'source': 'Fonte',
            'count': 'Volume',
            'percentage': 'Porcentagem (%)'
        }),
        use_container_width=True
    )


def comparative_analysis():
    st.title("🔍 Análise Comparativa")
    
    # Carrega dados
    website_df, pages_df, dimensions_df = load_all_data()
    
    if website_df.empty:
        st.error("Nenhum dado encontrado.")
        return
    
    st.header("📅 Comparação entre Períodos")
    
    # Seleção de períodos para comparação
    col1, col2 = st.columns(2)
    
    available_periods = sorted(website_df['year_month'].unique())
    
    with col1:
        st.subheader("Período 1")
        period1 = st.selectbox("Selecione o primeiro período:", available_periods, key="period1")
    
    with col2:
        st.subheader("Período 2")
        period2 = st.selectbox("Selecione o segundo período:", available_periods, 
                              index=len(available_periods)-1 if len(available_periods) > 1 else 0, key="period2")
    
    if period1 == period2:
        st.warning("Selecione períodos diferentes para comparação.")
        return
    
    # Dados dos períodos
    data1 = website_df[website_df['year_month'] == period1].iloc[0] if not website_df[website_df['year_month'] == period1].empty else None
    data2 = website_df[website_df['year_month'] == period2].iloc[0] if not website_df[website_df['year_month'] == period2].empty else None
    
    if data1 is None or data2 is None:
        st.error("Dados não encontrados para os períodos selecionados.")
        return
    
    # Comparação de métricas
    st.header("📊 Comparação de Métricas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        diff_users = data2['activeUsers'] - data1['activeUsers']
        pct_users = (diff_users / data1['activeUsers'] * 100) if data1['activeUsers'] != 0 else 0
        st.metric(
            "👥 Usuários Ativos",
            f"{data2['activeUsers']:,}",
            delta=f"{diff_users:+,} ({pct_users:+.1f}%)"
        )
    
    with col2:
        diff_views = data2['screenPageViews'] - data1['screenPageViews']
        pct_views = (diff_views / data1['screenPageViews'] * 100) if data1['screenPageViews'] != 0 else 0
        st.metric(
            "👀 Visualizações",
            f"{data2['screenPageViews']:,}",
            delta=f"{diff_views:+,} ({pct_views:+.1f}%)"
        )
    
    with col3:
        diff_duration = data2['averageSessionDuration'] - data1['averageSessionDuration']
        pct_duration = (diff_duration / data1['averageSessionDuration'] * 100) if data1['averageSessionDuration'] != 0 else 0
        st.metric(
            "⏱️ Duração Média",
            f"{data2['averageSessionDuration']:.1f}s",
            delta=f"{diff_duration:+.1f}s ({pct_duration:+.1f}%)"
        )
    
    with col4:
        diff_bounce = data2['bounceRate'] - data1['bounceRate']
        pct_bounce = (diff_bounce / data1['bounceRate'] * 100) if data1['bounceRate'] != 0 else 0
        st.metric(
            "📉 Taxa de Rejeição",
            f"{data2['bounceRate']:.1%}",
            delta=f"{diff_bounce:+.1%} ({pct_bounce:+.1f}%)"
        )
    
    # Gráfico de comparação
    comparison_data = pd.DataFrame({
        'Métrica': ['Usuários Ativos', 'Visualizações', 'Duração Média', 'Taxa de Rejeição'],
        period1: [data1['activeUsers'], data1['screenPageViews'], data1['averageSessionDuration'], data1['bounceRate']],
        period2: [data2['activeUsers'], data2['screenPageViews'], data2['averageSessionDuration'], data2['bounceRate']]
    })
    
    # Normaliza os dados para melhor visualização (exceto bounce rate)
    normalized_data = comparison_data.copy()
    for col in [period1, period2]:
        normalized_data.loc[0, col] = normalized_data.loc[0, col] / 1000  # Usuários em milhares
        normalized_data.loc[1, col] = normalized_data.loc[1, col] / 1000  # Views em milhares
        normalized_data.loc[2, col] = normalized_data.loc[2, col] / 100   # Duração em centenas
        normalized_data.loc[3, col] = normalized_data.loc[3, col] * 100   # Bounce rate em percentual
    
    fig_comparison = px.bar(
        normalized_data,
        x='Métrica',
        y=[period1, period2],
        title=f'Comparação: {period1} vs {period2}',
        barmode='group'
    )
    fig_comparison.update_layout(yaxis_title="Valores Normalizados")
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Análise de páginas nos dois períodos
    if not pages_df.empty:
        st.header("📄 Comparação de Páginas Populares")
        
        pages1 = pages_df[pages_df['year_month'] == period1]
        pages2 = pages_df[pages_df['year_month'] == period2]
        
        if not pages1.empty and not pages2.empty:
            top_pages1 = pages1.nlargest(10, 'activeUsers')[['pagePath', 'activeUsers']]
            top_pages2 = pages2.nlargest(10, 'activeUsers')[['pagePath', 'activeUsers']]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"Top 10 - {period1}")
                st.dataframe(top_pages1.rename(columns={'pagePath': 'Página', 'activeUsers': 'Usuários'}), 
                           use_container_width=True)
            
            with col2:
                st.subheader(f"Top 10 - {period2}")
                st.dataframe(top_pages2.rename(columns={'pagePath': 'Página', 'activeUsers': 'Usuários'}), 
                           use_container_width=True)


def monthly_report():
    st.title("📈 Relatório Mensal Completo")
    
    # Carrega dados
    website_df, pages_df, dimensions_df = load_all_data()
    
    if website_df.empty:
        st.error("Nenhum dado encontrado.")
        return
    
    # Seleção do mês
    available_periods = sorted(website_df['year_month'].unique(), reverse=True)
    selected_period = st.selectbox("Selecione o período:", available_periods)
    
    # Dados do período selecionado
    period_data = website_df[website_df['year_month'] == selected_period]
    period_pages = pages_df[pages_df['year_month'] == selected_period] if not pages_df.empty else pd.DataFrame()
    period_traffic = dimensions_df[dimensions_df['year_month'] == selected_period] if not dimensions_df.empty else pd.DataFrame()
    
    if period_data.empty:
        st.error("Nenhum dado encontrado para o período selecionado.")
        return
    
    data = period_data.iloc[0]
    
    st.header(f"📊 Resumo Executivo - {selected_period}")
    
    # Métricas principais em destaque
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Usuários Ativos", f"{data['activeUsers']:,}")
    with col2:
        st.metric("👀 Visualizações", f"{data['screenPageViews']:,}")
    with col3:
        st.metric("🕐 Duração Média", f"{data['averageSessionDuration']:.1f}s")
    with col4:
        st.metric("📉 Taxa de Rejeição", f"{data['bounceRate']:.1%}")
    
    # Análise de performance
    if len(website_df) > 1:
        # Comparação com média histórica
        avg_users = website_df['activeUsers'].mean()
        avg_views = website_df['screenPageViews'].mean()
        avg_duration = website_df['averageSessionDuration'].mean()
        avg_bounce = website_df['bounceRate'].mean()
        
        st.header("📈 Performance vs Média Histórica")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            diff_users = data['activeUsers'] - avg_users
            pct_users = (diff_users / avg_users * 100) if avg_users != 0 else 0
            st.metric("Usuários", "vs Média", delta=f"{pct_users:+.1f}%")
        
        with col2:
            diff_views = data['screenPageViews'] - avg_views
            pct_views = (diff_views / avg_views * 100) if avg_views != 0 else 0
            st.metric("Visualizações", "vs Média", delta=f"{pct_views:+.1f}%")
        
        with col3:
            diff_duration = data['averageSessionDuration'] - avg_duration
            pct_duration = (diff_duration / avg_duration * 100) if avg_duration != 0 else 0
            st.metric("Duração", "vs Média", delta=f"{pct_duration:+.1f}%")
        
        with col4:
            diff_bounce = data['bounceRate'] - avg_bounce
            pct_bounce = (diff_bounce / avg_bounce * 100) if avg_bounce != 0 else 0
            st.metric("Rejeição", "vs Média", delta=f"{pct_bounce:+.1f}%")
    
    # Top páginas do mês
    if not period_pages.empty:
        st.header("🏆 Top 10 Páginas do Mês")
        top_pages_month = period_pages.nlargest(10, 'activeUsers')[['pagePath', 'activeUsers', 'screenPageViews']]
        
        fig_top_month = px.bar(
            top_pages_month,
            x='activeUsers',
            y='pagePath',
            orientation='h',
            title=f'Páginas Mais Acessadas - {selected_period}',
            color='activeUsers',
            color_continuous_scale='Blues'
        )
        fig_top_month.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top_month, use_container_width=True)
    
    # Fontes de tráfego do mês
    if not period_traffic.empty:
        st.header("🌐 Fontes de Tráfego do Mês")
        
        col1, col2 = st.columns(2)
        
        with col1:
            traffic_month = period_traffic.nlargest(8, 'count')
            fig_traffic_pie = px.pie(
                traffic_month,
                values='count',
                names='source',
                title=f'Distribuição de Tráfego - {selected_period}'
            )
            st.plotly_chart(fig_traffic_pie, use_container_width=True)
        
        with col2:
            fig_traffic_bar = px.bar(
                traffic_month,
                x='count',
                y='source',
                orientation='h',
                title='Volume por Fonte',
                color='count',
                color_continuous_scale='Viridis'
            )
            fig_traffic_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_traffic_bar, use_container_width=True)
    
    # Insights e Recomendações
    st.header("💡 Insights e Recomendações")
    
    insights = []
    
    if len(website_df) > 1:
        if data['activeUsers'] > avg_users:
            insights.append("✅ **Crescimento positivo** de usuários ativos acima da média histórica")
        else:
            insights.append("⚠️ **Usuários ativos** abaixo da média - considere campanhas de marketing")
    
    if data['bounceRate'] < 0.5:
        insights.append("✅ **Excelente taxa de rejeição** - conteúdo está engajando bem os usuários")
    else:
        insights.append("⚠️ **Taxa de rejeição alta** - revise a relevância e velocidade das páginas")
    
    if data['averageSessionDuration'] > 120:
        insights.append("✅ **Boa duração de sessão** - usuários estão consumindo o conteúdo")
    else:
        insights.append("💡 **Duração de sessão** pode ser melhorada com conteúdo mais interativo")
    
    if not period_pages.empty:
        top_page = period_pages.nlargest(1, 'activeUsers').iloc[0]
        insights.append(f"🏆 **Página mais popular**: {top_page['pagePath']} com {top_page['activeUsers']} usuários")
    
    for insight in insights:
        st.write(insight)
    
    # Exportar dados
    st.header("📥 Exportar Dados")
    
    if st.button("💾 Gerar Relatório CSV"):
        # Cria um DataFrame com todos os dados do período
        report_data = {
            'Periodo': selected_period,
            'Usuarios_Ativos': data['activeUsers'],
            'Visualizacoes': data['screenPageViews'],
            'Duracao_Media': data['averageSessionDuration'],
            'Taxa_Rejeicao': data['bounceRate']
        }
        
        if not period_pages.empty:
            report_data['Top_Pagina'] = period_pages.nlargest(1, 'activeUsers').iloc[0]['pagePath']
        
        if not period_traffic.empty:
            report_data['Principal_Fonte'] = period_traffic.nlargest(1, 'count').iloc[0]['source']
        
        report_df = pd.DataFrame([report_data])
        csv = report_df.to_csv(index=False)
        
        st.download_button(
            label="📄 Baixar Relatório CSV",
            data=csv,
            file_name=f"relatorio_codaqui_{selected_period}.csv",
            mime="text/csv"
        )


page_names_to_funcs = {
    "🏠 Início": intro,
    "📊 Visão Geral": overview_dashboard,
    "📄 Análise de Páginas": pages_analysis,
    "🌐 Fontes de Tráfego": traffic_sources_analysis,
    "🔍 Comparativo": comparative_analysis,
    "📈 Relatório Mensal": monthly_report
}

# Interface principal
st.sidebar.title("🚀 Dashboard Codaqui")
st.sidebar.markdown("---")

page_name = st.sidebar.selectbox(
    "📍 Navegação:",
    page_names_to_funcs.keys(),
    help="Selecione uma seção para explorar os dados"
)

# Informações na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 Sobre")
st.sidebar.markdown("""
**Dashboard de Analytics da Codaqui**

Versão: 2.0  
Dados atualizados mensalmente

🌟 **Recursos:**
- Visão geral completa
- Análise de páginas
- Fontes de tráfego
- Comparações temporais
- Relatórios detalhados
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center'>
    <p><strong>🔗 Links Úteis</strong></p>
    <a href='https://codaqui.dev' target='_blank'>🌐 Site Principal</a><br>
    <a href='https://github.com/codaqui' target='_blank'>💻 GitHub</a><br>
    <a href='mailto:contato@codaqui.dev'>📧 Contato</a>
</div>
""", unsafe_allow_html=True)

# Executa a função da página selecionada
page_names_to_funcs[page_name]()
