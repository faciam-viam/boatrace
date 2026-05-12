import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    .waku-1.0 { border-left-color: #ffffff; }
    .waku-2 { border-left-color: #111111; }
    .waku-2.0 { border-left-color: #111111; }
    .waku-3 { border-left-color: #ff3333; }
    .waku-3.0 { border-left-color: #ff3333; }
    .waku-4 { border-left-color: #3333ff; }
    .waku-4.0 { border-left-color: #3333ff; }
    .waku-5 { border-left-color: #ffcc00; }
    .waku-5.0 { border-left-color: #ffcc00; }
    .waku-6 { border-left-color: #00aa00; }
    .waku-6.0 { border-left-color: #00aa00; }

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

    .konsetsu-table {
        width: 100%;
        background: #1a1f2e;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .ks-header {
        display: grid;
        grid-template-columns: 120px repeat(12, 1fr);
        background: #2563eb;
        font-weight: 700;
        font-size: 14px;
        color: white;
        text-align: center;
        padding: 8px 0;
    }
    /* 傾向表用のヘッダー調整（120px + 6カラム） */
    .trend-header {
        display: grid;
        grid-template-columns: 120px repeat(6, 1fr);
        background: #2563eb;
        font-weight: 700;
        font-size: 16px;
        color: white;
        text-align: center;
        padding: 8px 0;
    }
    .ks-day-label {
        grid-column: span 2;
        border-right: 1px solid rgba(255,255,255,0.2);
    }
    .ks-subheader {
        display: grid;
        grid-template-columns: 120px repeat(12, 1fr);
        background: #1e40af;
        font-size: 11px;
        color: white;
        text-align: center;
        padding: 3px 0;
    }
    .ks-row {
        display: grid;
        grid-template-columns: 120px repeat(12, 1fr);
        border-bottom: 1px solid #2a3349;
        min-height: 40px;
    }
    /* 傾向表用の行調整 */
    .trend-row {
        display: grid;
        grid-template-columns: 120px repeat(6, 1fr);
        border-bottom: 1px solid #2a3349;
        min-height: 45px;
    }
    .ks-name {
        padding: 0 10px;
        font-weight: 700;
        font-size: 14px;
        color: white;
        display: flex;
        align-items: center;
        border-right: 2px solid #3498db;
    }
    .ks-cell {
        padding: 2px;
        text-align: center;
        border-right: 1px solid #2a3349;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .ks-waku {
        font-size: 16px;
        font-weight: 800;
        padding: 2px;
        border-radius: 4px;
        margin-bottom: 0;
    }
    .waku-bg-white { color: #fff; }
    </style>
""", unsafe_allow_html=True)

# --- データの読み込み ---
@st.cache_data
def load_data():
    file_path = "merged_results.csv"
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="shift-jis")
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception as e:
        st.error(f"CSVファイル読み込みエラー: {e}")
        return pd.DataFrame()
    
    df.columns = df.columns.str.strip().str.replace('‐', '-').str.replace('−', '-')
    
    if 'レース場' in df.columns:
        df['レース場'] = df['レース場'].astype(str).str.strip()
    if 'レース回' in df.columns:
        df['レース回'] = df['レース回'].astype(str).str.strip()
    if '枠番' in df.columns:
        df['枠番'] = df['枠番'].astype(str).str.strip()
    
    # 修正点：str_colsから '出足', '伸び足' を除外して数値を保持
    str_cols = ['activepoint', 'M総合評価', '支部', '級別', 'FL', '選手名']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].fillna('')
            df[col] = df[col].astype(str)
            df[col] = df[col].replace(['nan', 'NaN', 'None', ''], '-')
            df[col] = df[col].apply(lambda x: '-' if (isinstance(x, str) and x.strip() in ['', '-']) else (x if isinstance(x, str) else '-'))

    numeric_cols = [
        '全国勝率', '当地勝率', '1着率', '2着率', '3着率', '1-2率', '1-3率', 'M指数', 
        '差し率', 'まくり率', 'まくり差し率',
        'コースstトップ率', 'コースst最下位率',
        '差し数', 'まくり数', 'まくり差し数',
        '出足', '伸び足'
    ]
    # 追加の「2着がn号艇」も数値化
    for i in range(1, 7):
        numeric_cols.append(f'2着が{i}号艇')

    # スタート関連列（NaNのまま残す）
    st_cols = ['コース平均st', '今節平均st', 'コース平均st順位', '今節平均st順位']
    
    # スタート関連以外の数値列は0で埋める
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # スタート関連列はNaNのまま（0で埋めない）
    for col in st_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if '締切予定時刻' in df.columns:
        df['締切予定時刻'] = df['締切予定時刻'].astype(str).replace('nan', '')
    
    return df

# --- ドットプロット形式のグラフ関数 ---
def create_rank_dot_fig(data, column_name, title_text, is_st=False):
    fig = go.Figure()
    colors = ["#FFFFFF", "#000000", "#FF3333", "#3333FF", "#FFCC00", "#00AA00"]
    display_df = data.sort_values('w_num').reset_index(drop=True).copy()
    
    # スタートデータの場合は無効データを除外
    if is_st:
        # NaN、0.00を除外
        display_df = display_df[
            (display_df[column_name].notna()) & 
            (display_df[column_name] > 0)
        ].copy()
    
    if display_df.empty:
        # データがない場合は空のグラフを返す
        fig.update_layout(
            template="plotly_dark",
            title=dict(text=title_text + " (データなし)", x=0.5, font=dict(size=18, color="#FFFFFF")),
            height=280,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig
    
    # 枠番に応じた色を取得
    waku_colors = []
    for w in display_df['枠番']:
        try:
            w_int = int(float(w))
            if 1 <= w_int <= 6:
                waku_colors.append(colors[w_int - 1])
            else:
                waku_colors.append(colors[0])
        except:
            waku_colors.append(colors[0])
    
    fig.add_trace(go.Scatter(
        x=display_df['枠番'],
        y=display_df[column_name],
        mode="markers+text+lines",
        marker=dict(size=18, color=waku_colors, line=dict(width=2, color="white")),
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
    display_df = data.sort_values('w_num').reset_index(drop=True)
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
        race_time = ""
        if '締切予定時刻' in race_data.columns and not race_data.empty:
            time_value = str(race_data.iloc[0]['締切予定時刻']).strip()
            if time_value and time_value not in ['', 'nan', 'NaN', '-']:
                race_time = f" - {time_value}締切予定"
        
        st.markdown(f'<div class="main-title"><h1>{selected_venue} {selected_race} データ{race_time}</h1></div>', unsafe_allow_html=True)
        
        m_col1, m_col2, m_col3 = st.columns([1.5, 1, 1])
        p1_data = race_data[pd.to_numeric(race_data['枠番'], errors='coerce') == 1.0].head(1)
        
        if not p1_data.empty:
            p1 = p1_data.iloc[0]
            with m_col1:
                v = pd.to_numeric(p1['1着率'], errors='coerce')
                v = 0 if pd.isna(v) else v
                r = v * 100 if v <= 1.0 and v > 0 else v
                fig = go.Figure(data=[go.Pie(labels=['逃', '他'], values=[r, max(0, 100 - r)], hole=0.72, marker_colors=['#FFFFFF', '#444444'], textinfo='none', sort=False)])
                fig.update_layout(template="plotly_dark", showlegend=False, height=340, margin=dict(t=20, b=30, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)",
                    annotations=[
                        dict(text=f'<span style="font-size:20px;">{p1["選手名"]}</span>', x=0.5, y=0.68, showarrow=False, font=dict(color="#ffffff")),
                        dict(text=f'<span style="font-size:52px; font-weight:bold;">{int(r)}%</span>', x=0.5, y=0.32, showarrow=False, font=dict(color="#ffffff"))
                    ])
                st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_pie")
            
            for col, field, label, color in zip([m_col2, m_col3], ['1-2率', '1-3率'], ["1-2率", "1-3率"], ['#000000', '#FF3333']):
                val = pd.to_numeric(p1[field], errors='coerce')
                val = 0 if pd.isna(val) else val
                rate = val * 100 if val <= 1.0 and val > 0 else val
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
            # 枠番を安全に取得
            try:
                waku_num = pd.to_numeric(r['枠番'], errors='coerce')
                if pd.isna(waku_num):
                    continue  # 無効な枠番はスキップ
                waku_display = int(waku_num)
                w_cls = f"waku-{waku_display}"
            except:
                continue  # エラーが発生した場合はスキップ
            
            def safe_display(value):
                if pd.isna(value): return "-"
                str_val = str(value).strip()
                if str_val in ['', '-', 'nan', 'NaN', 'None']: return "-"
                return str_val
            
            # M総合評価の変換
            m_eval = safe_display(r['M総合評価'])
            m_eval_map = {'S': '超絶', 'A': '上位', 'B': '中堅上位', 'C': '中堅下位', 'D': '下位'}
            m_eval_display = m_eval_map.get(m_eval, '-')
            
            # 修正点：モーター型の判定ロジック
            deashi_val = pd.to_numeric(r.get('出足'), errors='coerce')
            nobashi_val = pd.to_numeric(r.get('伸び足'), errors='coerce')

            if pd.isna(deashi_val) or pd.isna(nobashi_val) or (deashi_val == 0 and nobashi_val == 0):
                motor_type = '-'
                motor_color = '#ffffff'
            else:
                if deashi_val > nobashi_val:
                    motor_type = '出足型'
                elif nobashi_val > deashi_val:
                    motor_type = '伸び型'
                else:
                    motor_type = 'バランス型'
                
                # 出足または伸び足が4以上なら色を変更
                motor_color = '#ff6b6b' if (deashi_val >= 4 or nobashi_val >= 4) else '#ffffff'
            
            # pointの生成（M指数ランク + activepoint記号）
            m_shisu = r['M指数'] if pd.notna(r['M指数']) else 0
            if m_shisu >= 5:
                m_rank = 'S'
            elif m_shisu >= 4:
                m_rank = 'A'
            elif m_shisu >= 3:
                m_rank = 'B'
            elif m_shisu >= 2:
                m_rank = 'C'
            elif m_shisu >= 1:
                m_rank = 'D'
            else:
                m_rank = '-'
            
            activepoint_str = safe_display(r['activepoint'])
            ap_map = {
                'S+': '++++', 'S': '+++', 
                'A+': '++', 'A': '+',
                'B+': '+-', 'B': '-',
                'C+': '--', 'C': '--',
                'D+': '---', 'D': '---'
            }
            ap_symbol = ap_map.get(activepoint_str, '')
            point_display = f"{m_rank}{ap_symbol}" if m_rank != '-' and ap_symbol else '-'
            
            fl_val = safe_display(r['FL'])
            fl_display = f"<span class='val-fl'>{fl_val}</span>" if fl_val != "-" else "<span class='pc-val'>-</span>"
            
            st.markdown(f"""
                <div class="player-card {w_cls}">
                    <div class="pc-waku">{waku_display}</div>
                    <div class="pc-name-area"><div class="pc-name">{r['選手名']}</div></div>
                    <div class="pc-stats-grid">
                        <div class="pc-item"><span class="pc-label">級別</span><span class="pc-val val-large">{safe_display(r['級別'])}</span></div>
                        <div class="pc-item"><span class="pc-label">支部</span><span class="pc-val val-small">{safe_display(r['支部'])}</span></div>
                        <div class="pc-item"><span class="pc-label">FL</span>{fl_display}</div>
                        <div class="pc-item"><span class="pc-label">全国勝率</span><span class="pc-val val-large">{r['全国勝率']:.2f}</span></div>
                        <div class="pc-item"><span class="pc-label">当地勝率</span><span class="pc-val val-large">{r['当地勝率']:.2f}</span></div>
                        <div class="pc-item"><span class="pc-label">評価</span><span class="pc-val">{m_eval_display}</span></div>
                        <div class="pc-item"><span class="pc-label">モーター</span><span class="pc-val" style="color:{motor_color}">{motor_type}</span></div>
                        <div class="pc-item"><span class="pc-label">point</span><span class="pc-val" style="font-size:13px">{point_display}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

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
                    fig_rentai.add_trace(go.Bar(y=race_data['選手名'], x=vals, name=n, orientation='h', marker_color=clr, text=vals.apply(lambda x: f"{int(x)}%" if x > 0 else ""), textposition='inside'))
            fig_rentai.update_layout(template="plotly_dark", barmode='stack', height=420, xaxis=dict(range=[0, 100]), yaxis=dict(autorange="reversed"), legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(color="#ffffff", size=16)), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=30, t=60, b=60), showlegend=True)
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
                    fig_kimari.add_trace(go.Bar(x=race_data['選手名'], y=rates, name=n, marker_color=clr, text=labels, textposition='outside'))
            fig_kimari.update_layout(template="plotly_dark", barmode='group', height=420, yaxis=dict(range=[0, 40], tickvals=[0, 10, 20, 30, 40], gridcolor="#333"), legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(color="#ffffff", size=16)), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=40, t=60, b=60), showlegend=True)
            st.plotly_chart(fig_kimari, use_container_width=True, key=f"{key_prefix}_kimari")

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

        st.markdown('<div class="section-header">今節成績</div>', unsafe_allow_html=True)
        html = '<div class="konsetsu-table"><div class="ks-header"><div>選手名</div>'
        for day in range(1, 7): html += f'<div class="ks-day-label">{day}日目</div>'
        html += '</div><div class="ks-subheader"><div></div>'
        for _ in range(6): html += '<div>1走</div><div>2走</div>'
        html += '</div>'
        for _, r in race_data.iterrows():
            html += f'<div class="ks-row"><div class="ks-name">{r["選手名"]}</div>'
            for day in range(1, 7):
                for run in [1, 2]:
                    col_name = f'今節成績_{day}-{run}'
                    waku_val = r.get(col_name, '')
                    if pd.notna(waku_val) and str(waku_val).strip() not in ['', '-', 'nan']:
                        try:
                            val_str = str(int(float(waku_val)))
                            html += f'<div class="ks-cell"><div class="ks-waku waku-bg-white">{val_str}</div></div>'
                        except:
                            html += '<div class="ks-cell"></div>'
                    else: html += '<div class="ks-cell"></div>'
            html += '</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

        # --- 枠番進入・1着時2着傾向 ---
        st.markdown('<div class="section-header">枠番進入・1着時2着傾向</div>', unsafe_allow_html=True)
        t_html = '<div class="konsetsu-table"><div class="trend-header"><div>選手名</div>'
        for i in range(1, 7): t_html += f'<div>{i}</div>'
        t_html += '</div>'
        
        for _, r in race_data.iterrows():
            try:
                c_waku_num = pd.to_numeric(r['枠番'], errors='coerce')
                if pd.isna(c_waku_num):
                    continue
                c_waku = int(c_waku_num)
            except:
                continue
                
            t_html += f'<div class="trend-row"><div class="ks-name">{r["選手名"]}</div>'
            for t_waku in range(1, 7):
                if c_waku == t_waku:
                    t_html += '<div class="ks-cell"><div class="pc-val" style="color:#555;">ー</div></div>'
                else:
                    col_name = f'2着が{t_waku}号艇'
                    val = r.get(col_name, 0)
                    try:
                        d_val = int(float(val)) if pd.notna(val) else 0
                    except:
                        d_val = 0
                    t_html += f'<div class="ks-cell"><div class="pc-val">{d_val}</div></div>'
            t_html += '</div>'
        t_html += '</div>'
        st.markdown(t_html, unsafe_allow_html=True)

# --- メインロジック ---
try:
    df = load_data()
    if df.empty:
        st.warning("📊 'merged_results.csv' が見つかりません。")
    else:
        venues = sorted([v for v in df['レース場'].unique() if pd.notna(v) and str(v) != 'nan'])
        if venues:
            selected_venue = st.sidebar.selectbox("レース場", venues)
            venue_df = df[df['レース場'] == selected_venue]
            race_numbers = sorted([r for r in venue_df['レース回'].unique() if pd.notna(r) and str(r) != 'nan'], key=lambda x: int(x) if str(x).isdigit() else 0)
            if race_numbers:
                selected_race = st.sidebar.selectbox("レース番号", race_numbers)
                race_data = venue_df[venue_df['レース回'] == selected_race].copy()
                race_data['w_num'] = pd.to_numeric(race_data['枠番'], errors='coerce').fillna(0)
                race_data = race_data.sort_values('w_num').reset_index(drop=True)
                show_all = st.sidebar.button("全レース一覧")
                if show_all:
                    for race_num in race_numbers:
                        rd = venue_df[venue_df['レース回'] == race_num].copy()
                        rd['w_num'] = pd.to_numeric(rd['枠番'], errors='coerce').fillna(0)
                        rd = rd.sort_values('w_num').reset_index(drop=True)
                        render_race(rd, selected_venue, race_num, key_prefix=f"all_{race_num}")
                        st.markdown("---")
                else: render_race(race_data, selected_venue, selected_race, key_prefix="single")
except Exception as e:
    st.error(f"システムエラーが発生しました: {e}")