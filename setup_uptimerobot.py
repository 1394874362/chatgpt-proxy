#!/usr/bin/env python3
"""
自动配置 UptimeRobot 监控
免费版支持 50 个监控，每 5 分钟检查一次
"""

import json
import requests
from pathlib import Path

CONFIG_FILE = "config.json"

def load_config():
    """加载配置"""
    if not Path(CONFIG_FILE).exists():
        print(f"❌ 配置文件不存在: {CONFIG_FILE}")
        exit(1)
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_monitor(api_key: str, url: str, name: str) -> bool:
    """创建 UptimeRobot 监控"""
    try:
        response = requests.post(
            "https://api.uptimerobot.com/v2/newMonitor",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "api_key": api_key,
                "format": "json",
                "type": 1,  # HTTP(s)
                "url": url,
                "friendly_name": name,
                "interval": 300  # 5 分钟
            }
        )
        
        result = response.json()
        if result.get("stat") == "ok":
            print(f"✅ 监控创建成功")
            return True
        else:
            print(f"❌ 创建失败: {result.get('error', {}).get('message', 'Unknown error')}")
            return False
    
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("  UptimeRobot 监控配置工具")
    print("=" * 60)
    print()
    
    config = load_config()
    cpa_url = config.get("cpa_url", "").rstrip("/")
    api_key = config.get("uptimerobot_api_key", "")
    
    if not cpa_url:
        print("❌ 配置文件缺少 cpa_url")
        exit(1)
    
    if not api_key:
        print("⚠️  配置文件缺少 uptimerobot_api_key")
        print()
        print("请按以下步骤获取 API Key:")
        print("1. 访问 https://uptimerobot.com")
        print("2. 注册/登录账号（免费）")
        print("3. 进入 My Settings → API Settings")
        print("4. 创建 Main API Key")
        print("5. 复制 API Key 到 config.json 的 uptimerobot_api_key 字段")
        print()
        exit(1)
    
    print(f"🎯 目标服务: {cpa_url}")
    print(f"🔑 API Key: {api_key[:10]}...")
    print()
    
    monitor_name = f"CPA-{cpa_url.split('//')[1].split('.')[0]}"
    
    print(f"📝 创建监控: {monitor_name}")
    create_monitor(api_key, cpa_url, monitor_name)
    
    print()
    print("=" * 60)
    print("配置完成！")
    print("=" * 60)
    print()
    print("UptimeRobot 将每 5 分钟访问一次你的服务")
    print("这样可以防止 Render 免费版休眠")
    print()
    print("你可以在 https://uptimerobot.com/dashboard 查看监控状态")

if __name__ == "__main__":
    main()
