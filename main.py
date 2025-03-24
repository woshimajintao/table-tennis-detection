import streamlit as st
import cv2
import tempfile  # 用于临时保存上传的视频文件

# ==================== 正确位置：set_page_config 必须是第一个 Streamlit 命令 ====================
st.set_page_config(layout="wide")

# ==================== 自定义 CSS ====================
st.markdown("""
<style>
    html {
        font-size: 14px;
        font-family: 'Inter', sans-serif;
    }
    h1 {
        font-size: 2.5em;
    }
    body {
        color: #fff;
        background-color: #00FF00;
    }
    .stApp {
        padding-top: -200px;
    }        

    /* Long & Close 按钮 */
    .btn-long {
        background-color: #005f73;  /* 深青蓝色 */
        color: white;
        width: 100px;
        border-radius: 8px;
        border: none;
        padding: 8px 15px;
        cursor: pointer;
        font-weight: bold;
    }
    .btn-close {
        background-color: #0a9396;  /* 浅青蓝色 */
        color: white;
        width: 100px;
        border-radius: 8px;
        border: none;
        padding: 8px 15px;
        cursor: pointer;
        font-weight: bold;
    }

    /* High & Low 按钮 */
    .btn-high {
        background-color: #3a0ca3;  /* 深紫色 */
        color: white;
        width: 100px;
        border-radius: 8px;
        border: none;
        padding: 8px 15px;
        cursor: pointer;
        font-weight: bold;
    }
    .btn-low {
        background-color: #7209b7;  /* 浅紫色 */
        color: white;
        width: 100px;
        border-radius: 8px;
        border: none;
        padding: 8px 15px;
        cursor: pointer;
        font-weight: bold;
    }

    /* Wide & Narrow 按钮 */
    .btn-wide {
        background-color: #588157;  /* 深黄绿色 */
        color: white;
        width: 100px;
        border-radius: 8px;
        border: none;
        padding: 8px 15px;
        cursor: pointer;
        font-weight: bold;
    }
    .btn-narrow {
        background-color: #a3b18a;  /* 浅黄绿色 */
        color: white;
        width: 100px;
        border-radius: 8px;
        border: none;
        padding: 8px 15px;
        cursor: pointer;
        font-weight: bold;
    }

</style>
""", unsafe_allow_html=True)

# ==================== 视频片段时间点 (每个片段的起始和结束时间) ====================
video_segments = [
    {"label": "Long", "start": 21, "end": 28},
    {"label": "Close", "start": 41, "end": 48},
    {"label": "High", "start": 108, "end": 113},
    {"label": "Low", "start": 114.5, "end": 118},
    {"label": "Wide", "start": 31, "end": 33},
    {"label": "Narrow", "start": 119, "end": 121},
]

# ==================== 左侧侧边栏 (添加片段选择) ====================
st.sidebar.title("✂️ Cut Detection")

# ========== 上传视频 ========== 
uploaded_file = st.sidebar.file_uploader("📂 Upload a video file", type=["mp4", "avi", "mov", "mkv"])

# ==================== 视频初始化控制 ====================
video_file = None

# 如果上传了视频，保存到临时文件
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(uploaded_file.read())
        video_file = tmp_file.name

# 初始化选定时间
selected_segment = None

# 只有上传了视频后，按钮才可用
if video_file:
    # =========== Shot 类别 ===========
    st.sidebar.markdown("### 🎯 Shot")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.sidebar.button("Long", key="btn_long", help="Long Shot", args=('btn-long',)):
            selected_segment = {"start": 21, "end": 28}
    with col2:
        if st.sidebar.button("Close", key="btn_close", help="Close Shot", args=('btn-close',)):
            selected_segment = {"start": 41, "end": 48}

    # =========== Angles 类别 ===========
    st.sidebar.markdown("### 📐 Angles")
    col3, col4 = st.sidebar.columns(2)
    with col3:
        if st.sidebar.button("High", key="btn_high", help="High Angle", args=('btn-high',)):
            selected_segment = {"start": 108, "end": 113}
    with col4:
        if st.sidebar.button("Low", key="btn_low", help="Low Angle", args=('btn-low',)):
            selected_segment = {"start": 114.5, "end": 118}

    # =========== Lens 类别 ===========
    st.sidebar.markdown("### 🔍 Lens")
    col5, col6 = st.sidebar.columns(2)
    with col5:
        if st.sidebar.button("Wide", key="btn_wide", help="Wide Lens", args=('btn-wide',)):
            selected_segment = {"start": 31, "end": 33}
    with col6:
        if st.sidebar.button("Narrow", key="btn_narrow", help="Narrow Lens", args=('btn-narrow',)):
            selected_segment = {"start": 119, "end": 121}

# ==================== 视频播放功能 ====================
def play_video_segment(video_file, start_time, end_time):
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # 显示视频
    video_placeholder = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or cap.get(cv2.CAP_PROP_POS_FRAMES) >= end_frame:
            break
        video_placeholder.image(frame, channels="BGR")

    cap.release()

# ==================== 视频片段播放控制 ====================
st.markdown("## 🎥 Table Tennis Match Video Clip Search🏓")  # 新增标题
video_placeholder = st.empty()

# 初始状态：未上传视频时，显示提示信息
if not video_file:
    st.warning("Please upload your video")

# 如果上传新视频，则更新并播放新视频
if video_file:
    video_placeholder.video(video_file)

# 点击按钮后播放指定片段（原视频消失）
if selected_segment is not None and video_file:
    video_placeholder.empty()  # 清空原视频
    start_time = selected_segment["start"]
    end_time = selected_segment["end"]
    play_video_segment(video_file, start_time, end_time)
