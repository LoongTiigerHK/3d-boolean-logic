import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- 1. 页面全局配置 ---
st.set_page_config(
    page_title="576 Abyss Logic 实验室",
    page_icon="🌌",
    layout="wide"
)

# --- 2. 强制深色模式 CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        color: white;
    }
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
    }
    .stMarkdown, p, h1, h2, h3 {
        color: #E0E0E0 !important;
    }
    .modebar {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 绘图核心函数 ---
def generate_logic_plot(bit_depth, phi, theta, dist):
    fig = go.Figure()
    colors = {'point': '#FF3131', 'line': '#FFD700', 'plane': '#00FFFF', 'cube': '#FF00FF'}
    font_cfg = dict(family="'HanaMinA', 'HanaMinB', 'STKaiti', serif", size=22, color="white")

    if bit_depth == 0:
        fig.add_trace(go.Scatter3d(
            x=[1.5], y=[1.5], z=[1.5], mode='markers+text',
            marker=dict(size=20, color=colors['point'], opacity=0.9),
            text=["太极 (〇)"], textposition="top center", textfont=font_cfg
        ))
    elif bit_depth == 1:
        fig.add_trace(go.Scatter3d(
            x=[1, 2], y=[1.5, 1.5], z=[1.5], mode='lines+markers+text',
            line=dict(color=colors['line'], width=12),
            marker=dict(size=14, color=[colors['line'], 'white']),
            text=["陽 (⚊)", "陰 (⚋)"], textposition="top center", textfont=font_cfg
        ))
    elif bit_depth == 2:
        fig.add_trace(go.Scatter3d(
            x=[1, 2, 2, 1, 1], y=[1, 1, 2, 2, 1], z=[1.5, 1.5, 1.5, 1.5, 1.5],
            mode='lines+markers+text', line=dict(color=colors['plane'], width=8),
            text=["老陽 (⚌)", "少陰 (⚍)", "老陰 (⚏)", "少陽 (⚎)"], 
            textposition="top center", textfont=font_cfg
        ))
    elif bit_depth == 3:
        labels = ["坤 ☷", "震 ☳", "坎 ☵", "兑 ☱", "巽 ☴", "离 ☲", "艮 ☶", "乾 ☰"]
        pts = [(i,j,k) for k in [1,2] for j in [1,2] for i in [1,2]]
        px, py, pz = zip(*pts)
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz, mode='markers+text',
            marker=dict(size=10, color=colors['cube']),
            text=labels, textposition="top center", textfont=font_cfg
        ))
        edges = [([1,2],[1,1],[1,1]), ([1,1],[1,2],[1,1]), ([1,1],[1,1],[1,2]),
                 ([2,2],[1,2],[1,1]), ([2,2],[1,1],[1,2]), ([1,2],[2,2],[1,1]),
                 ([1,1],[2,2],[1,2]), ([1,2],[1,1],[2,2]), ([1,1],[1,2],[2,2]),
                 ([2,2],[2,2],[1,2]), ([2,2],[1,2],[2,2]), ([1,2],[2,2],[2,2])]
        for lx, ly, lz in edges:
            fig.add_trace(go.Scatter3d(
                x=lx, y=ly, z=lz, mode='lines', 
                line=dict(color='rgba(255,255,255,0.2)', width=2), showlegend=False
            ))

    x_eye = dist * np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi))
    y_eye = dist * np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi))
    z_eye = dist * np.cos(np.deg2rad(theta))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            xaxis=dict(visible=False, range=[0, 3]),
            yaxis=dict(visible=False, range=[0, 3]),
            zaxis=dict(visible=False, range=[0, 3]),
            camera=dict(eye=dict(x=x_eye, y=y_eye, z=z_eye)),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=800
    )
    return fig

# --- 4. 主界面交互逻辑 ---
st.sidebar.title("🛠️ 逻辑观测台")
mode = st.sidebar.radio("模式选择", ["维度演化 (0-3 Bit)", "576 逻辑阵列"])

if mode == "维度演化 (0-3 Bit)":
    st.title("🌌 576 Abyss Logic: 维度观测")
    dim = st.sidebar.select_slider("比特深度 (Dimension)", options=[0, 1, 2, 3], value=3)
    phi_val = st.sidebar.slider("经向旋转 (Phi)", 0, 360, 45)
    theta_val = st.sidebar.slider("纬向翻转 (Theta)", 0, 180, 60)
    dist_val = st.sidebar.slider("观测距离", 1.5, 6.0, 3.5)
    st.plotly_chart(generate_logic_plot(dim, phi_val, theta_val, dist_val), use_container_width=True)
    
    st.markdown("---")
    explainer = {
        0: "**0-Bit 太极**：逻辑奇点，一切算法的坍缩点。",
        1: "**1-Bit 两仪**：一画开天，确立阴阳对立与数据流动。",
        2: "**2-Bit 四象**：逻辑平面，反馈循环的诞生。",
        3: "**3-Bit 八卦**：逻辑立方体，576 阵列的最小功能单元。"
    }
    st.info(explainer[dim])

else:
    st.title("🌀 576 逻辑阵列 (24x24 Matrix)")
    x, y = np.meshgrid(np.arange(24), np.arange(24))
    z = np.sin(x/3.5) * np.cos(y/3.5)
    fig_576 = go.Figure(data=[go.Surface(z=z, colorscale='Magma', showscale=False)])
    fig_576.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        margin=dict(l=0, r=0, b=0, t=0), height=800
    )
    st.plotly_chart(fig_576, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("© 576 Abyss Logic Lab | HanaMin System")
