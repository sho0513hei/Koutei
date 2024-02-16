# termainalで以下入力しておく。
#pip install streamlit
#pip install plotly-express
#pip install streamlit

import openpyxl
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                  layout="wide"
)

#Strleamlitをフレッシュするたびにエクセルを毎回読み込むのを防ぐ。新規に読み込む場合は、@st,def,retun,"df = get_data_from_excel()"の前に＃つける。
#@st.cache_data  
#def get_data_from_excel():
df = pd.read_excel(
    io='BUN4.xlsx',
    engine='openpyxl',
    sheet_name='Sheet1',
    skiprows=0,
    usecols='A:C',
    nrows=1000,
)
    #return df
#df = get_data_from_excel()

#st.dataframe(df)


#------Mainpage--------------
st.title(":bar_chart: 工程Rough CHK Dashboard")

# ----- sidebar----------
st.sidebar.header("Please filter here:")

dlb_dlv = st.sidebar.multiselect(
    "Select the DLB/DLV:",
    options=df["DLB/DLV"].unique(),
    default=df["DLB/DLV"].unique().tolist()
)

activity = st.sidebar.multiselect(
    "Select the Activity:",
    options=df["Activity"].unique(),
    default=df["Activity"].unique().tolist()
)


day = st.sidebar.multiselect(
    "Select the Day:",
    options=df["Day"].unique(),
    default=df["Day"].unique().tolist()
)

df_selection = df.query(
    #"Date == @Date & Location == @Location & Category1 == @Category1 & Category2 == @Category2"
    "`DLB/DLV` == @dlb_dlv & Activity == @activity & Day == @day"
)

st.dataframe(df_selection)


# 各Activityに対して要した時間をバーチャート（水平方向）にする。
df_koutei = df_selection[['Day', 'DLB/DLV']]
df_koutei['Row'] = df_koutei.index
total_days = df_koutei['Day'].sum()
fig_df_koutei = px.bar(
    df_koutei,
    x="Day",
    y="DLB/DLV",
    orientation="h",
    title="<b>Days for Activitis</b> <br>※PL=5km。<br>サイドバーのフィルタリング機能を用い、Activityをソートする。Fair season=8か月(240days),MOB/DeMOB、WOW(8%),DSVのSAT減圧含まない",
    color_discrete_sequence=["#0083B8"] * len(df_koutei),
    template="plotly_white",
    hover_data={"Row": True, "DLB/DLV": True, "Day": True}
)
fig_df_koutei.update_traces(hovertemplate="Row: %{customdata}<br>DLB/DLV: %{y}<br>Days: %{x}<extra></extra>", customdata=df_koutei['Row'])
 

# 合計時間を表示する
for i, loc in enumerate(df_koutei["DLB/DLV"]):
    fig_df_koutei.add_annotation(
        x=df_koutei["Day"].max() + 0.5,
        y=loc,
        text=f"Total Months: {df_koutei.groupby('DLB/DLV')['Day'].sum()[loc]/30:.2f} ({df_koutei.groupby('DLB/DLV')['Day'].sum()[loc]:.2f} days)",
        showarrow=False,
        font=dict(size=20),
        align="left"
    )
    
fig_df_koutei.update_layout(
    width=1200,  # グラフの幅
    height=650,  # グラフの高さ
    xaxis=dict(
        title=dict(font=dict(size=20)),
        tickfont=dict(size=15),
        tickmode='linear',
        dtick=30,
        showline=True,
        linewidth=1,
        linecolor='White',
        showgrid=True,
        zeroline=False,
    ),
    yaxis=dict(
        title=dict(font=dict(size=20)),
        tickfont=dict(size=15),
        showline=True,
        showgrid=False,
        zeroline=False
    )
)

st.plotly_chart(fig_df_koutei)

# バーチャート（水平方向）の作成終わり

