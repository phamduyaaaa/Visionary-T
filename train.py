import plotly.graph_objects as go
import trimesh
import psutil
import shutil
import os
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import mss
import torch

def load_screen():
    sct = mss.mss()
    monitor = {
        "top": 188,
        "left": 187,
        "width": 640,
        "height": 640
    }
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
    image_resized = cv2.resize(frame, (640, 640))
    return image_resized

def load_stl(file):
    stl_mesh = trimesh.load(file, file_type='stl')
    vertices = stl_mesh.vertices
    faces = stl_mesh.faces
    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=x, y=y, z=z,
                i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
                color='lightblue', opacity=0.5
            )
        ]
    )
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig
def preprocess_image(uploaded_file):
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    image_resized = cv2.resize(image_np, (640, 640))
    return image_resized
def test_image_model(image_tensor):
    # device = torch.device("cuda")
    model_path = 'runs/detect/train29/weights/best.pt'
    model = YOLO(model_path)
    results = model.predict(image_tensor)
    output_image = image_tensor
    for result in results:
        boxes = result.boxes
        conf_list = []
        label_list = []
        cnt = 0
        ht = 0
        hcn = 0
        for box in boxes:
            if len(box.xyxy[0]) >= 4:
                x1, y1, x2, y2 = box.xyxy[0][:4]
                conf = box.conf[0] if len(box.conf) > 0 else None
                cls = box.cls[0] if len(box.cls) > 0 else None
                if conf is not None and cls is not None:
                    cnt += 1
                    if model.names[int(cls)] == "ht":
                        ht += 1
                        label = f'{model.names[int(cls)]}{ht}'
                    else:
                        hcn += 1
                        label = f'{model.names[int(cls)]}{hcn}'
                    conf_list.append(conf)
                    label_list.append(label)
                    cv2.rectangle(output_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 128, 0), 3)
                    cv2.putText(output_image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 128, 0),
                                2)

    return output_image,conf_list,label_list,cnt
def train_model(epochs=10,batch=16):
    model = YOLO("yolo11s.pt")
    model.train(
        data="datasets/roboflow/data.yaml",
        epochs=epochs,
        batch=batch,
        imgsz=640,
        plots=True
    )
def laptop_info():
    gib = 1 << 30  # bytes per GiB
    ram = psutil.virtual_memory().total
    total, used, free = shutil.disk_usage("/")
    s = f"ultralytic 8.3.2🚀({os.cpu_count()} CPUs, {ram / gib:.1f} GB RAM, {(total - free) / gib:.1f}/{total / gib:.1f} GB disk).✅"
    return s