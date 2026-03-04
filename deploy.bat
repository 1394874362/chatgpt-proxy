@echo off
chcp 65001 >nul
REM CPA 一键部署脚本（Windows）

echo ==========================================
echo   CPA 反代一键部署脚本
echo ==========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装 Python，请先安装
    pause
    exit /b 1
)

REM 创建配置文件
if not exist "config.json" (
    echo 📝 创建配置文件...
    copy config.example.json config.json
    echo ✅ 已创建 config.json，请编辑填写你的配置
    echo.
    echo 需要填写：
    echo   - cpa_url: 你的 Render 服务地址
    echo   - cpa_password: 你设置的密码
    echo.
    pause
)

REM 安装依赖
echo.
echo 📦 安装 Python 依赖...
pip install requests

REM 上传 Token
echo.
echo 📤 开始上传 Token...
python upload_tokens.py

REM 配置保活
echo.
set /p setup_uptime="是否配置 UptimeRobot 自动唤醒? (y/n): "
if /i "%setup_uptime%"=="y" (
    python setup_uptimerobot.py
)

echo.
echo ==========================================
echo   部署完成！
echo ==========================================
echo.
echo 使用示例：
echo   python example_usage.py
echo.
pause
