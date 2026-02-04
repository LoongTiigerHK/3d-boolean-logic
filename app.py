import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- 页面设置 ---
st.set_page_config(page_title="576 Abyss Logic 实验室", layout="wide")

# --- 侧边栏：控制中心 ---
st.sidebar.title("🛠️ 观测控制面板")

# 1. 维度选择
dimension = st.sidebar.select_slider(
    "观测维度 (Bit Depth):",
    options=[0, 1, 2, 3],
    value=3
)

# 2. 视角控制：阴阳翻转 (控制 3D 旋转角度)
st.sidebar.subheader("视角调节 (阴阳翻转)")
angle_phi = st.sidebar.slider("经向角度 (Phi)", 0, 360, 45)
angle_theta = st.sidebar.slider("纬向角度 (Theta)", 0, 180, 45)

# 3. 视觉风格
show_lines = st.sidebar.checkbox("显示逻辑链接 (棱线)", value=True)

# --- 核心绘图逻辑 ---
def get_plot(bit_depth, phi, theta, show_l):
    fig = go.Figure()
    # 颜色定义
    colors = {'point': '#FF3131', 'line': '#FFD700', 'plane': '#00FFFF', 'cube': '#FF00FF'}
    
    # 字体配置 (兼容花园明朝与系统楷体)
    font_style = dict(family="STKaiti, 'HanaMinA', serif", size=18, color="white")

    # 逻辑点构造
    if bit_depth == 0:
        fig.add_trace(go.Scatter3d(x=[1.5], y=[1.5], z=[1.5], mode='markers+text',
                                   marker=dict(size=25, color=colors['point'], opacity=0.8),
                                   text=["太极 (〇)"], textposition="top center"))
    elif bit_depth == 1:
        fig.add_trace(go.Scatter3d(x=[1, 2], y=[1.5, 1.5], z=[1.5], mode='lines+markers+text',
                                   line=dict(color=colors['line'], width=12),
                                   marker=dict(size=14, color=[colors['line'], 'white']),
                                   text=["陽 (⚊)", "陰 (⚋)"], textfont=font_style, textposition="top center"))
    elif bit_depth == 2:
        fig.add_trace(go.Scatter3d(x=[1, 2, 2, 1, 1], y=[1, 1, 2, 2, 1], z=[1.5, 1.5, 1.5, 1.5, 1.5],
                                   mode='lines+markers+text', line=dict(color=colors['plane'], width=8),
                                   text=["老陽 (⚌)", "少陰 (⚍)", "老陰 (⚏)", "少陽 (⚎)"], 
                                   textfont=font_style, textposition="top center"))
    elif bit_depth == 3:
        bagua_labels = ["坤 ☷", "震 ☳", "坎 ☵", "兑 ☱", "巽 ☴", "离 ☲", "艮 ☶", "乾 ☰"]
        pts = [(i,j,k) for k in [1,2] for j in [1,2] for i in [1,2]]
        px, py, pz = zip(*pts)
        fig.add_trace(go.Scatter3d(x=px, y=py, z=pz, mode='markers+text',
                                   marker=dict(size=12, color=colors['cube']),
                                   text=bagua_labels, textfont=font_style, textposition="top center"))
        
        if show_l:
            adj_edges = [([1,2],[1,1],[1,1]), ([1,1],[1,2],[1,1]), ([1,1],[1,1],[1,2]),
                         ([2,2],[1,2],[1,1]), ([2,2],[1,1],[1,2]), ([1,2],[2,2],[1,1]),
                         ([1,1],[2,2],[1,2]), ([1,2],[1,1],[2,2]), ([1,1],[1,2],[2,2]),
                         ([2,2],[2,2],[1,2]), ([2,2],[1,2],[2,2]), ([1,2],[2,2],[2,2])]
            for lx, ly, lz in adj_edges:
                fig.add_trace(go.Scatter3d(x=lx, y=ly, z=lz, mode='lines', 
                                           line=dict(color='rgba(255,255,255,0.3)', width=2), showlegend=False))

    # 设置视角旋转逻辑
    x_eye = 2 * np.sin(np.deg2rad(angle_theta)) * np.cos(np.deg2rad(angle_phi))
    y_eye = 2 * np.sin(np.deg2rad(angle_theta)) * np.sin(np.deg2rad(angle_phi))
    z_eye = 2 * np.cos(np.deg2rad(angle_theta))

    fig.update_layout(
        template="plotly_dark",
        scene=dict(
            xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
            camera=dict(eye=dict(x=x_eye, y=y_eye, z=z_eye))
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=700
    )
    return fig

# --- 主界面 ---
st.title(f"🌌 576 Abyss Logic: {dimension}-Bit 观测态")
st.plotly_chart(get_plot(dimension, angle_phi, angle_theta, show_lines), use_container_width=True)

# --- 底部逻辑解释 ---
with st.expander("📝 逻辑深渊笔记：关于本维度的演化"):
    notes = [
        "**0-Bit (太极)**：逻辑的奇点。没有 0 或 1，只有一种‘存在’。所有的算法最终都要回归到这个单点。",
        "**1-Bit (两仪)**：一画开天。引入了比特的对立。左右、开关、阴阳。这是计算的最小单位。",
        "**2-Bit (四象)**：逻辑的循环。四象代表了逻辑状态的四种组合，形成了闭合回路。",
        "**3-Bit (八卦)**：三维矩阵的雏形。这是 576 逻辑阵列（24x24）的基础‘细胞’。"
    ]
    st.write(notes[dimension])