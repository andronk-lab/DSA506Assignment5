import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Knicks 2026 Analytics", layout="wide")
df = pd.read_csv("knicks.csv")

st.title("New York Knicks Performance Analytics")
st.markdown("""
**Analytical Objective:** In honor of March Madness coming around the corner, I chose basketball as my focus for the Assignment 5 project! 
This dashboard evaluates the scoring efficiency and defensive contributions 
of the 2026 New York Knicks roster to identify high impact players and offensive outliers. 
The goal is to determine which players provide the best return on playing time (MP).
""")

st.sidebar.header("Dashboard Controls")
min_pts = st.sidebar.slider("Minimum Points per Game:", 
                            float(df["PTS"].min()), float(df["PTS"].max()), 10.0)

all_players = df["Player"].unique()
selected_players = st.sidebar.multiselect("Filter by Player:", all_players, default=all_players[:8])

filtered_df = df[(df["PTS"] >= min_pts) & (df["Player"].isin(selected_players))]

top_scorer = df.loc[df['PTS'].idxmax()]
avg_pts = df['PTS'].mean()

m1, m2, m3 = st.columns(3)
m1.metric("Team Scoring Leader", top_scorer['Player'], f"{top_scorer['PTS']} PPG")
m2.metric("Average PPG", f"{avg_pts:.1f}")
m3.metric("Roster Size", len(df))

tab1, tab2 = st.tabs(["Scoring & Efficiency", "Workload & Defense"])

with tab1:
    st.header("Offensive Efficiency Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.scatter(filtered_df, x="FGA", y="FG%", size="PTS", color="Player", 
                          title="Shooting Efficiency vs Volume")
        st.plotly_chart(fig1, use_container_width=True, key="c1")
    
    with col2:
        fig2 = px.bar(filtered_df, x="Player", y="PTS", color="Age", 
                      title="Points Contribution")
        st.plotly_chart(fig2, use_container_width=True, key="c2")

    st.markdown("""
    **Interpretation:**
    - **Principal Pattern:** There is a clear correlation between field goal attempts (FGA) and total points, 
      but players like Jalen Brunson remain outliers by maintaining high efficiency (FG%) despite high volume.
    - **Actionable Insight:** Players appearing in the top left of the scatter plot are highly efficient, 
      increasing their usage rate could improve overall team offensive output.
    """)

with tab2:
    st.header("Defensive Impact & Minutes Distribution")

    fig3 = px.pie(filtered_df, values='MP', names='Player', 
                  title="Minutes Played Distribution")
    st.plotly_chart(fig3, use_container_width=True, key="c3")

    fig4 = px.line(filtered_df.sort_values("AST"), x="Player", y="AST", 
                   title="Assists/Playmaking Impact", markers=True)
    st.plotly_chart(fig4, use_container_width=True, key="chart_line_unique")

    st.markdown("""
    **Interpretation:**
    - **Workload Analysis:** The pie chart shows a heavy reliance on the starting five. 
      Significant drops in performance may occur if bench players are forced into high minute roles.
    - **Anomaly:** The line chart identifies playmaking outliers, players with high assists relative 
      to their minutes are key catalysts for the Knicks' offensive flow.
    """)
