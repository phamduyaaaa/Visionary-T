import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
from io import BytesIO
import trimesh
import pandas as pd
from fonts import get_multiple_fonts_css
from train import test_image_model, train_model, load_stl, laptop_info, preprocess_image, load_screen

import cv2
import serial
import time
# CSS
st.markdown(get_multiple_fonts_css(), unsafe_allow_html=True)
st.markdown(
    """
    <style>
    /* Căn giữa các tab */
    [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
    }

    [data-baseweb="tab"] {
        color: #2D32501;
    }

    /* Căn giữa caption */
    .caption {
        text-align: center;
        font-size: 16px;
        color: #5D6D7E;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
sidebar_1 = "Validation Results"
sidebar_2 = "Visionary-T"
sidebar_3 = "Test Model"
sidebar_4 = "STL file"
sidebar_5 = "Train Model"
sidebar_6 = "Other Device"
with st.sidebar:
    selected = option_menu(
        "Menu",
        [sidebar_2, sidebar_4, sidebar_5, sidebar_1, sidebar_3, sidebar_6],
        icons=['1-circle-fill', '2-circle-fill', "3-circle-fill", '4-circle-fill', '5-circle-fill', '6-circle-fill'],
        menu_icon="app", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#2D3250"},
            "icon": {"color": "#D4BDAC", "font-size": "16px"},
            "nav-link": {
                "font-size": "18px",
                "font-family": "Pacifico, cursive",
                "color": "#758694",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#424769"
            },
            "nav-link-selected": {
                "background-color": "#7077A1",
                "color": "#F5E8C7",
                "font-weight": "bold"
            },
            "menu-title": {
                "font-size": "20px",
                "font-family": "Roboto, sans-serif",
                "color": "#F5E8C7",
                "text-align": "left",
                "font-weight": "bold",
                "padding": "8px",
            }
        }
    )

# Results Tab
if selected == sidebar_1:
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(50):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()
    st.header("Results")
    val_img = "runs/detect/train29/predicts.jpg"
    conf_matrix = "runs/detect/train29/conf_matrix.jpg"
    loss_img = "runs/detect/train29/loss_plot.png"

    tab1, tab2, tab3 = st.tabs(["Predicts", "Loss", "Confusion Matrix"])
    with tab1:
        st.image(val_img, width=800)
        st.markdown('<p class="caption">Kết quả thu được</p>', unsafe_allow_html=True)
    with tab2:
        st.image(loss_img, width=1000)
        st.markdown('<p class="caption">Biểu đồ Loss sau mỗi epoch</p>', unsafe_allow_html=True)
    with tab3:
        st.image(conf_matrix, width=1000)
        st.markdown('<p class="caption">Confusion Matrix</p>', unsafe_allow_html=True)
    char_data = pd.DataFrame(np.random.rand(20, 3), columns=["A", "B", "C"])

# Visionary-T Tab
if selected == sidebar_2:
    st.header("Visionary-T")
    st.image("sick1.png")
    st.text("Là 1 máy ảnh 3D hoạt động dựa trên nguyên tắc time-of-flight (ToF)")
    st.text("Cung cấp dữ liệu 3D thời gian thực với tốc độ 50 fps (frames per second)")
    st.text("Cấu tạo")
    st.image("cautao_vst.png")
  
# Test Model Tab
if selected == sidebar_3:
    ser = serial.Serial('COM6', 9600)  # Windows: COM6, Linux: /dev/ttyUSB0
    time.sleep(2)  # Đợi 2 giây để Arduino reset
    st.header("Test Model")
    uploaded_file = st.file_uploader("Tải lên ảnh của bạn", type=["jpg", "png", "jpeg"])
    col1, col2 = st.columns(2)
    with col1:
        button = st.button("Live")
    if button:
        with col2:
            button = st.button("Stop")
        frame_placeholder = st.empty()
        while True:
            frame = load_screen()
            start = time.time()
            results, conf, label, cnt = test_image_model(frame)
            end = time.time()
            totalTime = end - start
            fps = 1 / totalTime
            fps_disp = f"FPS: {fps:.2f}"
            results_fps = cv2.putText(frame, fps_disp, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            frame_placeholder.image(results_fps, use_column_width=True)
            if 'ht' in label:
                ser.write(b'1')
            elif 'hcn' in label:
                ser.write(b'0')
            if button:
                break

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        image = preprocess_image(uploaded_file)
        with col1:
            st.image(image, caption="Ảnh gốc", use_column_width=True)
        results, conf, label, cnt = test_image_model(image)
        st.text("Predicts:")
        with col2:
            st.image(results, caption="Ảnh dự đoán", use_column_width=True)
        for i in range(cnt):
            st.text(f"{label[i]}: {(conf[i]*100):.2f}%")
        st.toast("Done!", icon='😍')

# STL File Tab
if selected == sidebar_4:
    st.header("3D STL Model Viewer")
    tab_stl1, tab_stl2, tab_stl3 = st.tabs(["Khung", "Băng chuyền", "Hoàn thiện sản phẩm"])
    with tab_stl1:
        stl_mesh1 = trimesh.load('khung.STL', file_type='stl')
        fig1 = load_stl(stl_mesh1)
        st.plotly_chart(fig1, use_container_width=True, key='1')
    with tab_stl2:
        stl_mesh2 = trimesh.load('bangchuyen.STL', file_type='stl')
        fig2 = load_stl(stl_mesh2)
        st.plotly_chart(fig2, use_container_width=True, key='2')
    with tab_stl3:
        stl_mesh3 = trimesh.load('laprapbangchuyen.STL', file_type='stl')
        fig3 = load_stl(stl_mesh3)
        st.plotly_chart(fig3, use_container_width=True, key='3')
    uploaded_file = st.file_uploader("Tải file STL của bạn", type=["stl"])
    if uploaded_file is not None:
        stl_mesh = trimesh.load(BytesIO(uploaded_file.read()), file_type='stl')
        fig = load_stl(stl_mesh)
        st.plotly_chart(fig, use_container_width=True)
# Train Model Tab
if selected == sidebar_5:
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(50):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()
    st.toast(f'Cấu hình sử dụng: {laptop_info()}', icon='😍')
    # st.markdown('<p class="handwriting">Trainning Model</p>', unsafe_allow_html=True)
    st.header("Trainning Model")
    epochs = st.text_input("Nhập Epochs:", placeholder="Số lần duyệt qua toàn bộ dữ liệu")
    batch_size = st.text_input("Nhập Batch size:",
                               placeholder=" Số mẫu được truyền qua mạng trong mỗi lần cập nhật tham số ")

    if st.button("Xác nhận"):
        if epochs.strip() and batch_size.strip():
            try:
                epochs = int(epochs)
                batch_size = int(batch_size)
                if epochs > 0 and batch_size > 0:
                    train_model(epochs=epochs, batch=batch_size)
                    st.success(f"T: {batch_size}")
                else:
                    st.error("Giá trị Epochs và Batch size phải lớn hơn 0.")
            except ValueError:
                st.error("Vui lòng nhập một số nguyên hợp lệ. VD: Epochs = 10; Batch size = 16")
        else:
            st.warning("Vui lòng nhập giá trị!")
    # Live in Other Device
if selected == sidebar_6:
    st.header("Other Device")
    uploaded_file = st.file_uploader("Tải lên ảnh của bạn", type=["jpg", "png", "jpeg"])
    col1, col2 = st.columns(2)
    with col1:
        button = st.button("Live")
    if button:
        with col2:
            button = st.button("Stop")
        frame_placeholder = st.empty()
        while True:
            frame = load_screen()
            start = time.time()
            results, conf, label, cnt = test_image_model(frame)
            end = time.time()
            totalTime = end - start
            fps = 1 / totalTime
            fps_disp = f"FPS: {fps:.2f}"
            results_fps = cv2.putText(frame, fps_disp, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            frame_placeholder.image(results_fps, use_column_width=True)
            if button:
                break

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        image = preprocess_image(uploaded_file)
        with col1:
            st.image(image, caption="Ảnh gốc", use_column_width=True)
        results, conf, label, cnt = test_image_model(image)
        st.text("Predicts:")
        with col2:
            st.image(results, caption="Ảnh dự đoán", use_column_width=True)
        for i in range(cnt):
            st.text(f"{label[i]}: {(conf[i] * 100):.2f}%")
        st.toast("Done!", icon='😍')

# Sidebar footer
st.sidebar.text("@author: phamduyaaaa")
