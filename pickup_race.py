import streamlit as st
import pandas as pd
import re

st.set_page_config(layout="wide", page_title="本日のピックアップレース")

# カスタムCSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    .main-title {
        background: linear-gradient(90deg, #1e2538 0%, #0e1117 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #ff6b6b;
        margin-bottom: 30px;
    }
    .main-title h1 {
        color: #ffffff !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .pickup-card {
        background: #1a1f2e;
        border: 2px solid #ff6b6b;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .pickup-title {
        color: #ff6b6b !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("merged_results.csv", encoding="utf-8")
    df = df.replace('#N/A!', pd.NA)
    
    numeric_cols = ['1着率', 'コース平均st', 'コース平均st順位', '今節平均st', '今節平均st順位', '当該コース1着合計']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    def extract_number(val):
        if pd.isna(val) or val == '-' or val == '':
            return 0
        try:
            return int(val)
        except:
            return 0
    
    df['出足_数値'] = df['出足'].apply(extract_number)
    df['伸び足_数値'] = df['伸び足'].apply(extract_number)
    df['出足伸び足合計'] = df['出足_数値'] + df['伸び足_数値']
    
    return df

df = load_data()

st.markdown('<div class="main-title"><h1>本日のピックアップレース</h1></div>', unsafe_allow_html=True)

# タブ作成
tab1, tab2 = st.tabs(["条件別表示", "時系列表示"])

with tab1:
    # サイドバーにフィルター
    st.sidebar.header("フィルター設定")
    
    venues = ['全て'] + sorted(df['レース場'].unique().tolist())
    selected_venue = st.sidebar.selectbox("レース場", venues)
    
    st.sidebar.subheader("表示する条件")
    show_cond1 = st.sidebar.checkbox("条件1: B級コース1着率10%以上", value=True)
    show_cond2 = st.sidebar.checkbox("条件2: B級出足+伸び足8以上", value=True)
    show_cond3 = st.sidebar.checkbox("条件3: 外枠伸び足5以上", value=True)
    show_cond4 = st.sidebar.checkbox("条件4: 外枠ST上位", value=True)
    show_cond5 = st.sidebar.checkbox("条件5: 4枠有利", value=True)
    show_cond6 = st.sidebar.checkbox("条件6: 5枠有利", value=True)
    show_summary = st.sidebar.checkbox("総合ピックアップ", value=True)
    
    # データフィルター
    if selected_venue != '全て':
        filtered_df = df[df['レース場'] == selected_venue].copy()
    else:
        filtered_df = df.copy()
    
    # 条件1
    if show_cond1:
        st.markdown('<div class="pickup-card"><div class="pickup-title">条件1: B級選手でコース1着率10%以上（1枠除く）</div>', unsafe_allow_html=True)
        condition1 = filtered_df[(filtered_df['級別'].str.startswith('B')) & (filtered_df['1着率'] >= 0.10) & (filtered_df['枠番'] != 1)].copy()
        if not condition1.empty:
            condition1['コース1着率%'] = (condition1['1着率'] * 100).round(1)
            display1 = condition1[['レース場', 'レース回', '枠番', '選手名', '級別', 'コース1着率%', '全国勝率', '当地勝率', '締切予定時刻']].sort_values('締切予定時刻')
            st.dataframe(display1, use_container_width=True, hide_index=True)
        else:
            st.write("該当選手なし")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 条件2
    if show_cond2:
        st.markdown('<div class="pickup-card"><div class="pickup-title">条件2: B級選手で出足+伸び足が8以上</div>', unsafe_allow_html=True)
        condition2 = filtered_df[(filtered_df['級別'].str.startswith('B')) & (filtered_df['出足伸び足合計'] >= 8)].copy()
        if not condition2.empty:
            display2 = condition2[['レース場', 'レース回', '枠番', '選手名', '級別', '出足', '伸び足', '出足伸び足合計', '全国勝率', '締切予定時刻']].sort_values('締切予定時刻')
            st.dataframe(display2, use_container_width=True, hide_index=True)
        else:
            st.write("該当選手なし")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 条件1かつ条件2
    if show_cond1 and show_cond2:
        st.markdown('<div class="pickup-card"><div class="pickup-title">条件1&2: B級コース1着率10%以上 かつ 出足+伸び足8以上</div>', unsafe_allow_html=True)
        condition1_and_2 = filtered_df[
            (filtered_df['級別'].str.startswith('B')) & 
            (filtered_df['1着率'] >= 0.10) & 
            (filtered_df['枠番'] != 1) &
            (filtered_df['出足伸び足合計'] >= 8)
        ].copy()
        if not condition1_and_2.empty:
            condition1_and_2['コース1着率%'] = (condition1_and_2['1着率'] * 100).round(1)
            display1_2 = condition1_and_2[['レース場', 'レース回', '枠番', '選手名', '級別', 'コース1着率%', '出足', '伸び足', '出足伸び足合計', '全国勝率', '当地勝率', '締切予定時刻']].sort_values('締切予定時刻')
            st.dataframe(display1_2, use_container_width=True, hide_index=True)
        else:
            st.write("該当選手なし")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 条件3
    if show_cond3:
        st.markdown('<div class="pickup-card"><div class="pickup-title">条件3: 外枠選手(4,5,6枠)で伸び足が5以上</div>', unsafe_allow_html=True)
        condition3 = filtered_df[(filtered_df['枠番'].isin([4, 5, 6])) & (filtered_df['伸び足_数値'] >= 5)].copy()
        if not condition3.empty:
            display3 = condition3[['レース場', 'レース回', '枠番', '選手名', '級別', '伸び足', '出足', '全国勝率', '当地勝率', '締切予定時刻']].sort_values('締切予定時刻')
            st.dataframe(display3, use_container_width=True, hide_index=True)
        else:
            st.write("該当選手なし")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 条件4
    if show_cond4:
        st.markdown('<div class="pickup-card"><div class="pickup-title">条件4: 外枠(4,5,6枠)でレース内ST順位が1位または2位</div>', unsafe_allow_html=True)
        races = filtered_df.groupby(['レース場', 'レース回'])
        condition4_list = []
        
        for (venue, race_num), race_df in races:
            race_df = race_df.copy()
            race_df = race_df[race_df['コース平均st'].notna()]
            
            if len(race_df) > 0:
                race_df['レース内ST順位'] = race_df['コース平均st'].rank(method='min')
                outer_top = race_df[(race_df['枠番'].isin([4, 5, 6])) & (race_df['レース内ST順位'] <= 2)]
                
                for _, row in outer_top.iterrows():
                    condition4_list.append({
                        'レース場': venue,
                        'レース回': race_num,
                        '枠番': row['枠番'],
                        '選手名': row['選手名'],
                        '級別': row['級別'],
                        'レース内ST順位': int(row['レース内ST順位']),
                        'コース平均st': row['コース平均st'],
                        '全国勝率': row['全国勝率'],
                        '締切予定時刻': row['締切予定時刻']
                    })
        
        if condition4_list:
            df4 = pd.DataFrame(condition4_list).sort_values('締切予定時刻')
            st.dataframe(df4, use_container_width=True, hide_index=True)
        else:
            st.write("該当選手なし")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 条件5
    if show_cond5:
        st.markdown('<div class="pickup-card"><div class="pickup-title">条件5: 4枠が3枠よりSTが速い</div>', unsafe_allow_html=True)
        races = filtered_df.groupby(['レース場', 'レース回'])
        pickup5_list = []
        
        for (venue, race_num), race_df in races:
            waku3 = race_df[race_df['枠番'] == 3]
            waku4 = race_df[race_df['枠番'] == 4]
            
            if not waku3.empty and not waku4.empty:
                st3 = float(waku3.iloc[0]['コース平均st']) if pd.notna(waku3.iloc[0]['コース平均st']) else 0
                st4 = float(waku4.iloc[0]['コース平均st']) if pd.notna(waku4.iloc[0]['コース平均st']) else 0
                
                if st3 > 0 and st4 > 0:
                    deashi3 = waku3.iloc[0]['出足伸び足合計']
                    deashi4 = waku4.iloc[0]['出足伸び足合計']
                    
                    if st4 < st3:
                        pickup5_list.append({
                            'レース場': venue,
                            'レース回': race_num,
                            '3枠選手': waku3.iloc[0]['選手名'],
                            '3枠ST': st3,
                            '3枠出足+伸び足': deashi3,
                            '4枠選手': waku4.iloc[0]['選手名'],
                            '4枠ST': st4,
                            '4枠出足+伸び足': deashi4,
                            'ST差': round(st3 - st4, 2),
                            '出足差': deashi4 - deashi3,
                            '締切予定時刻': waku4.iloc[0]['締切予定時刻']
                        })
        
        if pickup5_list:
            df5 = pd.DataFrame(pickup5_list).sort_values('締切予定時刻')
            st.dataframe(df5, use_container_width=True, hide_index=True)
        else:
            st.write("該当レースなし")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 条件6
    if show_cond6:
        st.markdown('<div class="pickup-card"><div class="pickup-title">条件6: 5枠が3,4枠よりSTが速い</div>', unsafe_allow_html=True)
        races = filtered_df.groupby(['レース場', 'レース回'])
        pickup6_list = []
        
        for (venue, race_num), race_df in races:
            waku3 = race_df[race_df['枠番'] == 3]
            waku4 = race_df[race_df['枠番'] == 4]
            waku5 = race_df[race_df['枠番'] == 5]
            
            if not waku3.empty and not waku4.empty and not waku5.empty:
                st3 = float(waku3.iloc[0]['コース平均st']) if pd.notna(waku3.iloc[0]['コース平均st']) else 0
                st4 = float(waku4.iloc[0]['コース平均st']) if pd.notna(waku4.iloc[0]['コース平均st']) else 0
                st5 = float(waku5.iloc[0]['コース平均st']) if pd.notna(waku5.iloc[0]['コース平均st']) else 0
                
                if st3 > 0 and st4 > 0 and st5 > 0:
                    deashi3 = waku3.iloc[0]['出足伸び足合計']
                    deashi4 = waku4.iloc[0]['出足伸び足合計']
                    deashi5 = waku5.iloc[0]['出足伸び足合計']
                    
                    if st5 < st3 and st5 < st4:
                        pickup6_list.append({
                            'レース場': venue,
                            'レース回': race_num,
                            '3枠選手': waku3.iloc[0]['選手名'],
                            '3枠ST': st3,
                            '3枠出足+伸び足': deashi3,
                            '4枠選手': waku4.iloc[0]['選手名'],
                            '4枠ST': st4,
                            '4枠出足+伸び足': deashi4,
                            '5枠選手': waku5.iloc[0]['選手名'],
                            '5枠ST': st5,
                            '5枠出足+伸び足': deashi5,
                            '締切予定時刻': waku5.iloc[0]['締切予定時刻']
                        })
        
        if pickup6_list:
            df6 = pd.DataFrame(pickup6_list).sort_values('締切予定時刻')
            st.dataframe(df6, use_container_width=True, hide_index=True)
        else:
            st.write("該当レースなし")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 総合
    if show_summary:
        st.markdown('<div class="pickup-card"><div class="pickup-title">総合ピックアップ（複数条件該当）</div>', unsafe_allow_html=True)
        
        filtered_df['条件カウント'] = 0
        filtered_df.loc[(filtered_df['級別'].str.startswith('B')) & (filtered_df['1着率'] >= 0.10) & (filtered_df['枠番'] != 1), '条件カウント'] += 1
        filtered_df.loc[(filtered_df['級別'].str.startswith('B')) & (filtered_df['出足伸び足合計'] >= 8), '条件カウント'] += 1
        filtered_df.loc[(filtered_df['枠番'].isin([4, 5, 6])) & (filtered_df['伸び足_数値'] >= 5), '条件カウント'] += 1
        
        multi_pickup = filtered_df[filtered_df['条件カウント'] >= 2].copy()
        if not multi_pickup.empty:
            multi_pickup['コース1着率%'] = (multi_pickup['1着率'] * 100).round(1)
            display_multi = multi_pickup[['レース場', 'レース回', '枠番', '選手名', '級別', '条件カウント', 'コース1着率%', '出足伸び足合計', '全国勝率', '締切予定時刻']].sort_values('締切予定時刻')
            st.dataframe(display_multi, use_container_width=True, hide_index=True)
        else:
            st.write("該当選手なし")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="pickup-card"><div class="pickup-title">全レース時系列表示</div>', unsafe_allow_html=True)
    
    # レース場と時刻でソート
    time_sorted = df.sort_values(['締切予定時刻', 'レース場', 'レース回']).copy()
    
    # レースごとにグループ化
    for (venue, race_num), race_df in time_sorted.groupby(['レース場', 'レース回'], sort=False):
        race_time = race_df.iloc[0]['締切予定時刻'] if '締切予定時刻' in race_df.columns else ''
        
        st.markdown(f"### {venue} {race_num} - {race_time}")
        
        # そのレースの全選手を表示
        display_race = race_df[['枠番', '選手名', '級別', '全国勝率', '当地勝率', '出足', '伸び足', 'コース平均st', '1着率']].copy()
        display_race['1着率%'] = (display_race['1着率'] * 100).round(1)
        display_race = display_race.drop('1着率', axis=1)
        display_race = display_race.sort_values('枠番')
        
        st.dataframe(display_race, use_container_width=True, hide_index=True)
        st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)