@echo off
REM 设置pip的镜像源为清华大学镜像源
set PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

REM 安装opencv-python库
pip install opencv-python

REM 安装numpy库
pip install numpy

REM 安装matplotlib库
pip install matplotlib

REM 安装PyQt5库
pip install PyQt5

REM 安装rich库
pip install rich

REM 恢复pip的默认镜像源
set PIP_INDEX_URL=