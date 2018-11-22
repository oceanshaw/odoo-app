@echo off

echo.
echo.
echo.
echo.

echo 正在编译py文件
echo.
echo.

..\..\..\runtime\python\python.exe pyc_modifier.py --path=. --compile=Y

echo.
echo.
echo 已经编译完毕，稍后会自动关闭窗口。
echo.
echo.

ping 127.0.0.1 > NUL
ping 127.0.0.1 > NUL
