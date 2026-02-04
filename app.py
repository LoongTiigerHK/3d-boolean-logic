import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- 1. 页面全局配置 ---
st.set_page_config(
    page_title="576 Abyss Logic 实验室",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 强制深色模式 CSS (解决全白看不清的问题) ---
st.markdown("""
    <style>
    /* 强制背景为深黑色 */
    .stApp {
        background-color: #050505;
    }
    /* 侧边栏样式定制 */
    section[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #333;
    }
    /* 文字颜色统一 */
    h1, h2, h3, p, span {
        color: #E0E0E0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 侧边栏控制中心 ---
st.sidebar.title("🛠️ 观测控制面板")
mode = st.sidebar.selectbox("选择观测模式", ["基础维度 (0-3 Bit)", "576 逻辑阵列 (24x24)"])

# 字体回退设置：确保在未安装花园明朝的设备上也能显示
FONT_FAMILY = "'HanaMinA', 'HanaMinB', 'STKaiti', 'Microsoft YaHei', serif"

# --- 4. 绘图核心函数 ---
def generate_logic_plot(bit_depth, phi, theta):
    fig = go.Figure()
    
    # 颜色与视觉定义
    colors = {'point': '#FF3131', 'line': '#FFD700', 'plane': '#00FFFF', 'cube': '#FF00FF'}
    font_cfg = dict(family=FONT_FAMILY, size=20, color="white")

    if bit_depth == 0:
        fig.add_trace(go.Scatter3d(
            x=[1.5], y=[1.5], z=[1.5], mode='markers+text',
            marker=dict(size=22, color=colors['point'], opacity=0.9),
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
        # 八卦节点
        labels = ["坤 ☷", "震 ☳", "坎 ☵", "兑 ☱", "巽 ☴", "离 ☲", "艮 ☶", "乾 ☰"]
        pts = [(i,j,k) for k in [1,2] for j in [1,2] for i in [1,2]]
        px, py, pz = zip(*pts)
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz, mode='markers+text',
            marker=dict(size=12, color=colors['cube']),
            text=labels, textposition="top center", textfont=font_cfg
        ))
        # 棱线
        edges = [([1,2],[1,1],[1,1]), ([1,1],[1,2],[1,1]), ([1,1],[1,1],[1,2]),
                 ([2,2],[1,2],[1,1]), ([2,2],[1,1],[1,2]), ([1,2],[2,2],[1,1]),
                 ([1,1],[2,2],[1,2]), ([1,2],[1,1],[2,2]), ([1,1],[1,2],[2,2]),
                 ([2,2],[2,2],[1,2]), ([2,2],[1,2],[2,2]), ([1,2],[2,2],[2,2])]
        for lx, ly, lz in edges:
            fig.add_trace(go.Scatter3d(
                x=lx, y=ly, z=lz, mode='lines', 
                line=dict(color='rgba(255,255,255,0.2)', width=2), showlegend=False
            ))

    # 计算相机视角 (阴阳翻转)
    x_eye = 2 * np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi))
    y_eye = 2 * np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi))
    z_eye = 2 * np.cos(np.deg2rad(theta))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)', # 透明背景以匹配 Streamlit
        plot_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(eye=dict(x=x_eye, y=y_eye, z=z_eye))
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=750
    )
    return fig

# --- 5. 主界面渲染逻辑 ---
if mode == "基础维度 (0-3 Bit)":
    st.title("🌌 576 Abyss Logic 维度演化")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        dim = st.radio("比特深度", [0, 1, 2, 3], index=3)
        phi = st.slider("经向旋转", 0, 360, 45)
        theta = st.slider("纬向翻转", 0, 180, 60)
    
    with col2:
        st.plotly_chart(generate_logic_manifesto_plot := generate_logic_plot(dim, phi, theta), use_container_width=True)

else:
    st.title("🌀 576 逻辑阵列 (24x24 Matrix)")
    size = 24
    x, y = np.meshgrid(np.arange(size), np.arange(size))
    z = np.sin(x/3.5) * np.cos(y/3.5) # 模拟纠错逻辑曲面
    
    fig_576 = go.Figure(data=[go.Surface(
        z=z, colorscale='Magma', showscale=False, opacity=0.9
    )])
    fig_576.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        margin=dict(l=0, r=0, b=0, t=0),
        height=800
    )
    st.plotly_chart(fig_576, use_container_width=True)

st.markdown("---")
st.caption("576 Abyss Logic Laboratory | 基于花园明朝 (HanaMin) 符号体系")
