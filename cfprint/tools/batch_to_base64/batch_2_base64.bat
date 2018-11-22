@title 康虎云报表模板批量转换成base64
@echo off
@echo.
@echo.
@echo.
@echo #     正在把当前目录下的康虎云报表文件批量转成base64，请稍候
@echo.
@echo.
@echo.

set PYTHON_HOME=F:\Odoo\GreenPython_2.7_x64

set PATH=%PATH%;%PYTHON_HOME%

python.exe batch_b64.py

pause