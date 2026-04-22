import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 画面設定
st.set_page_config(layout="wide", page_title="Boat Race Data Analysis")

# ── 視覚性向上のためのカスタムCSS ──
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    .main-title {
        background: linear-gradient(90deg, #1e2538 0%, #0e1117 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #3498db;
        margin-bottom: 30px;
    }
    .main-title h1 {
        color: #ffffff !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .section-header {
        color: #ffffff !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        border-left: 5px solid #3498db;
        padding-left: 15px;
        margin: 40px 0 20px 0 !important;
        background: rgba(52, 152, 219, 0.1);
        line-height: 1.6;
    }

    .graph-label {
        color: #ecf0f1 !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        margin-bottom: 10px;
    }

    .stPlotlyChart {
        background-color: #1a1f2e !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        padding: 16px !important;
        border: 1px solid #2a3349 !important;
    }

    .player-card {
        background: #1a1f2e;
        border: 1px solid #2a3349;
        border-radius: 8px;
        padding: 12px 20px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        border-left: 10px solid #ccc;
    }
    .waku-1 { border-left-color: #ffffff; }
    .waku-2 { border-left-color: #111111; }
    .waku-3 { border-left-color: #ff3333; }
    .waku-4 { border-left-color: #3333ff; }
    .waku-5 { border-left-color: #ffcc00; }
    .waku-6 { border-left-color: #00aa00; }

    .pc-waku { font-size: 24px; font-weight: 900; color: #ffffff; min-width: 40px; }
    .pc-name-area { min-width: 160px; padding-left: 10px; }
    .pc-name { font-size: 20px; font-weight: 800; color: #ffffff; }

    .pc-stats-grid { 
        display: flex; 
        flex-grow: 1; 
        justify-content: space-between; 
        padding-left: 20px;
        border-left: 1px solid #3498db;
    }
    .pc-item { text-align: center; flex: 1; }
    .pc-label { font-size: 11px; color: #7fa7d9; display: block; margin-bottom: 2px; }
    
    .pc-val { font-size: 15px; font-weight: 700; color: #ffffff; }
    .val-large { font-size: 18px; }
    .val-small { font-size: 13px; color: #9bb2cc; }
    .val-fl { font-size: 18px; font-weight: 800; color: #ffcc00; }
    </style>
""", unsafe_allow_html=True)

# --- データの読み込み ---
@st.cache_data
def load_data():
    file_path = ""race_today.csv""
    
    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except:
        df = pd.read_csv(file_path, encoding="shift-jis")
    
    df.columns = df.columns.str.strip().str.replace('‐', '-').str.replace('−', '-')
    
    if 'レース場' in df.columns:
        df['レース場'] = df['レース場'].astype(str)
    if 'レース回' in df.columns:
        df['レース回'] = df['レース回'].astype(str)
    if '枠番' in df.columns:
        df['枠番'] = df['枠番'].astype(str)
    
    str_cols = ['activepoint', 'M総合評価', '支部', '級別', 'FL', '出足', '伸び足']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).replace('nan', '')

    numeric_cols = [
        'コース平均st', '今節平均st', 'コース平均st順位', '今節平均st順位', 
        '全国勝率', '当地勝率', '1着率', '2着率', '3着率', '1-2率', '1-3率', 'M指数', 
        '差し率', 'まくり率', 'まくり差し率',
        'コースstトップ率', 'コースst最下位率'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

# --- ドットプロット形式のグラフ関数 ---
def create_rank_dot_fig(data, column_name, title_text, is_st=False):
    fig = go.Figure()
    colors = ["#FFFFFF", "#000000", "#FF3333", "#3333FF", "#FFCC00", "#00AA00"]
    
    display_df = data.sort_values('w_num')
    
    fig.add_trace(go.Scatter(
        x=display_df['枠番'],
        y=display_df[column_name],
        mode="markers+text+lines",
        marker=dict(size=18, color=colors, line=dict(width=2, color="white")),
        text=display_df[column_name].apply(lambda x: f"<b>{x:.2f}</b>" if is_st else f"<b>{x:.1f}</b>"),
        textposition="top center",
        cliponaxis=False,
        line=dict(color="rgba(255,255,255,0.2)", dash="dash"),
        showlegend=False
    ))

    y_range = [0.3, 0] if is_st else [6.5, 0.5]
    tick_vals = None if is_st else [1, 2, 3, 4, 5, 6]

    fig.update_layout(
        template="plotly_dark",
        title=dict(text=title_text, x=0.5, font=dict(size=18, color="#FFFFFF")),
        xaxis=dict(title="枠番", gridcolor="#333"),
        yaxis=dict(range=y_range, tickvals=tick_vals, gridcolor="#333", zeroline=False),
        height=280,
        margin=dict(l=40, r=40, t=80, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# --- 率専用棒グラフ関数 ---
def create_rate_bar_fig(data, column_name, title_text):
    display_df = data.sort_values('w_num')
    vals = display_df[column_name].apply(lambda x: x * 100 if x <= 1.0 else x)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=display_df['枠番'],
        y=vals,
        text=vals.apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
        showlegend=False
    ))

    fig.update_layout(
        template="plotly_dark",
        title=dict(text=title_text, x=0.5, font=dict(size=18, color="#FFFFFF")),
        xaxis=dict(title="枠番", gridcolor="#333"),
        yaxis=dict(range=[0, 110], tickvals=[0, 20, 40, 60, 80, 100], gridcolor="#333", zeroline=False),
        height=280,
        margin=dict(l=40, r=40, t=80, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# --- レース詳細レンダリング ---
def render_race(race_data, selected_venue, selected_race, key_prefix=""):
    if not race_data.empty:
        st.markdown(f'<div class="main-title"><h1>{selected_venue} {selected_race} データ</h1></div>', unsafe_allow_html=True)
        
        m_col1, m_col2, m_col3 = st.columns([1.5, 1, 1])
        p1_data = race_data[race_data['枠番'] == '1'].head(1)
        if not p1_data.empty:
            p1 = p1_data.iloc[0]
            with m_col1:
                v = p1['1着率']
                r = v * 100 if v <= 1.0 else v
                fig = go.Figure(data=[go.Pie(labels=['逃', '他'], values=[r, 100 - r], hole=0.72, marker_colors=['#FFFFFF', '#444444'], textinfo='none', sort=False)])
                fig.update_layout(template="plotly_dark", showlegend=False, height=340, margin=dict(t=20, b=30, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)",
                    annotations=[
                        dict(text=f'<span style="font-size:20px;">{p1["選手名"]}</span>', x=0.5, y=0.68, showarrow=False, font=dict(color="#ffffff")),
                        dict(text=f'<span style="font-size:52px; font-weight:bold;">{int(r)}%</span>', x=0.5, y=0.32, showarrow=False, font=dict(color="#ffffff"))
                    ])
                st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_pie")
            
            for col, field, label, color in zip([m_col2, m_col3], ['1-2率', '1-3率'], ["1-2率", "1-3率"], ['#000000', '#FF3333']):
                val = p1[field]
                rate = val * 100 if val <= 1.0 else val
                fig_bar = go.Figure(go.Bar(x=[label], y=[rate], marker_color=color, width=0.4))
                fig_bar.update_layout(
                    template="plotly_dark", height=300, yaxis=dict(range=[0, 80], gridcolor="#333"),
                    xaxis=dict(tickfont=dict(size=18, color="white", weight="bold")),
                    margin=dict(t=20, b=70, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    annotations=[dict(x=label, y=rate + 2, text=f"{int(rate)}%", showarrow=False, xanchor='center', yanchor='bottom', font=dict(size=24, color="white", weight="bold"))]
                )
                col.plotly_chart(fig_bar, use_container_width=True, key=f"{key_prefix}_bar_{field}")

        st.markdown('<div class="section-header">選手データ</div>', unsafe_allow_html=True)
        for _, r in race_data.iterrows():
            w_cls = f"waku-{r['枠番']}"
            fl_display = f"<span class='val-fl'>{r['FL']}</span>" if r['FL'] != "" else "<span class='pc-val'>-</span>"
            st.markdown(f"""
                <div class="player-card {w_cls}">
                    <div class="pc-waku">{r['枠番']}</div>
                    <div class="pc-name-area"><div class="pc-name">{r['選手名']}</div></div>
                    <div class="pc-stats-grid">
                        <div class="pc-item"><span class="pc-label">級別</span><span class="pc-val val-large">{r['級別']}</span></div>
                        <div class="pc-item"><span class="pc-label">支部</span><span class="pc-val val-small">{r['支部']}</span></div>
                        <div class="pc-item"><span class="pc-label">FL</span>{fl_display}</div>
                        <div class="pc-item"><span class="pc-label">全国勝率</span><span class="pc-val val-large">{r['全国勝率']:.2f}</span></div>
                        <div class="pc-item"><span class="pc-label">当地勝率</span><span class="pc-val val-large">{r['当地勝率']:.2f}</span></div>
                        <div class="pc-item"><span class="pc-label">M指数</span><span class="pc-val">{r['M指数']}</span></div>
                        <div class="pc-item"><span class="pc-label">point</span><span class="pc-val">{r['activepoint']}</span></div>
                        <div class="pc-item"><span class="pc-label">評価</span><span class="pc-val">{r['M総合評価']}</span></div>
                        <div class="pc-item"><span class="pc-label">出足</span><span class="pc-val">{r['出足']}</span></div>
                        <div class="pc-item"><span class="pc-label">伸び足</span><span class="pc-val">{r['伸び足']}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">スタートデータ</div>', unsafe_allow_html=True)
        st_col1, st_col2 = st.columns(2)
        with st_col1: 
            st.plotly_chart(create_rank_dot_fig(race_data, 'コース平均st', 'コース平均ST', is_st=True), use_container_width=True, key=f"{key_prefix}_st1")
            st.plotly_chart(create_rank_dot_fig(race_data, 'コース平均st順位', 'コース平均ST順位'), use_container_width=True, key=f"{key_prefix}_st2")
            st.plotly_chart(create_rate_bar_fig(race_data, 'コースstトップ率', 'コースSTトップ率'), use_container_width=True, key=f"{key_prefix}_st3")
        with st_col2: 
            st.plotly_chart(create_rank_dot_fig(race_data, '今節平均st', '今節平均ST', is_st=True), use_container_width=True, key=f"{key_prefix}_st4")
            st.plotly_chart(create_rank_dot_fig(race_data, '今節平均st順位', '今節平均ST順位'), use_container_width=True, key=f"{key_prefix}_st5")
            st.plotly_chart(create_rate_bar_fig(race_data, 'コースst最下位率', 'コースST最下位率'), use_container_width=True, key=f"{key_prefix}_st6")

        st.divider()
        st.markdown('<div class="section-header">着順・決まり手データ</div>', unsafe_allow_html=True)
        an_col1, an_col2 = st.columns(2)

        with an_col1:
            st.markdown('<div class="graph-label">3連対率 (1着/2着/3着)</div>', unsafe_allow_html=True)
            fig_rentai = go.Figure()
            cols, names, colors_rentai = ['1着率', '2着率', '3着率'], ['1着', '2着', '3着'], ['#444444', '#888888', '#CCCCCC']
            for c, n, clr in zip(cols, names, colors_rentai):
                if c in race_data.columns:
                    vals = race_data[c].apply(lambda x: x*100 if x <= 1.0 else x)
                    fig_rentai.add_trace(go.Bar(y=race_data['選手名'], x=vals, name=n, orientation='h', marker_color=clr,
                        text=vals.apply(lambda x: f"{int(x)}%" if x > 0 else ""), textposition='inside'))
            fig_rentai.update_layout(template="plotly_dark", barmode='stack', height=420,
                xaxis=dict(range=[0, 100]), yaxis=dict(autorange="reversed"),
                legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(color="#ffffff", size=14)),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=30, t=60, b=60))
            st.plotly_chart(fig_rentai, use_container_width=True, key=f"{key_prefix}_rentai")

        with an_col2:
            st.markdown('<div class="graph-label">決まり手データ</div>', unsafe_allow_html=True)
            fig_kimari = go.Figure()
            rate_cols, count_cols, names_k, colors_k = ['差し率', 'まくり率', 'まくり差し率'], ['差し数', 'まくり数', 'まくり差し数'], ['差し', 'まくり', 'まくり差し'], ['#FFFFFF', '#FF3333', '#FFCC00']
            for r_col, c_col, n, clr in zip(rate_cols, count_cols, names_k, colors_k):
                if r_col in race_data.columns:
                    rates = race_data[r_col].apply(lambda x: x*100 if x <= 1.0 else x)
                    counts = race_data[c_col] if c_col in race_data.columns else [0]*len(rates)
                    labels = [f"{int(r)}%<br>({int(c)}回)" if r > 0 else "" for r, c in zip(rates, counts)]
                    fig_kimari.add_trace(go.Bar(x=race_data['選手名'], y=rates, name=n, marker_color=clr,
                        text=labels, textposition='outside'))
            fig_kimari.update_layout(template="plotly_dark", barmode='group', height=420, 
                yaxis=dict(range=[0, 40], tickvals=[0, 10, 20, 30, 40], gridcolor="#333"),
                legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(color="#ffffff", size=14)),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=40, t=60, b=60))
            st.plotly_chart(fig_kimari, use_container_width=True, key=f"{key_prefix}_kimari")

# --- メインロジック ---
try:
    df = load_data()
    
    if df.empty:
        st.warning("📊 '本日のレース.csv' が見つかりません。")
        st.info("リポジトリのルートディレクトリにCSVファイルを配置してください。")
    else:
        venues = sorted(df['レース場'].unique())
        selected_venue = st.sidebar.selectbox("レース場", venues)
        venue_df = df[df['レース場'] == selected_venue]
        selected_race = st.sidebar.selectbox("レース番号", sorted(venue_df['レース回'].unique()))

        race_data = venue_df[venue_df['レース回'] == selected_race].copy()
        race_data['w_num'] = pd.to_numeric(race_data['枠番'], errors='coerce')
        race_data = race_data.sort_values('w_num')

        show_all = st.sidebar.button("全レース一覧")

        if show_all:
            for race_num in sorted(venue_df['レース回'].unique()):
                rd = venue_df[venue_df['レース回'] == race_num].copy()
                rd['w_num'] = pd.to_numeric(rd['枠番'], errors='coerce')
                rd = rd.sort_values('w_num')
                render_race(rd, selected_venue, race_num, key_prefix=f"all_{race_num}")
                st.markdown("---")
        else:
            render_race(race_data, selected_venue, selected_race, key_prefix="single")
            
except Exception as e:
    st.error(f"システムエラーが発生しました: {e}")
