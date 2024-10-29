FROM pytorch/pytorch:2.5.0-cuda11.8-cudnn9-runtime

WORKDIR /app
COPY Visionary_T.py main.py
COPY train.py train.py
COPY fonts.py fonts.py
COPY runs/detect/train29 /app/runs/detect/train29
COPY sick1.png /app/sick1.png
COPY cautao_vst.png /app/cautao_vst.png
COPY contruotnhua.STL /app/contruotnhua.STL
COPY miengvuongg4lo.STL /app/miengvuongg4lo.STL
COPY vithinhthang.STL /app/vithinhthang.STL
RUN apt-get update && apt-get install -y vim \
    libgl1-mesa-glx \
    libglib2.0-0
RUN pip install streamlit streamlit_option_menu trimesh plotly ultralytics mss
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

