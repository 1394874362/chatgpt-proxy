#!/usr/bin/env python3
"""
CPA 服务保活脚本
定时 ping CPA 服务，防止 Render 免费版休眠
可以作为后台服务运行，或配置到 cron/任务计划
"""

import time
import json
import requests
from datetime import datetime
from pathlib import Path

CONFIG_FILE = "config.json"
PING_INTERVAL = 600  # 10 分钟 ping 一次

def load_config():
    """加载配置"""
    if not Path(CONFIG_FILE).exists():
        print(f"❌ 配置文件不存在: {CONFIG_FILE}")
        exit(1)
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def ping_service(url: str) -> bool:
    """Ping CPA 服务"""
    try:
        response = requests.get(url, timeout=30)
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ Ping 失败: {e}")
        return False

def main():
    """主循环"""
    print("=" * 60)
    print("  CPA 服务保活脚本")
    print("  每 10 分钟 ping 一次，防止休眠")
    print("=" * 60)
    print()
    
    config = load_config()
    cpa_url = config.get("cpa_url", "").rstrip("/")
    
    if not cpa_url:
        print("❌ 配置文件缺少 cpa_url")
        exit(1)
    
    print(f"🎯 目标服务: {cpa_url}")
    print(f"⏰ Ping 间隔: {PING_INTERVAL} 秒")
    print()
    print("按 Ctrl+C 停止")
    print()
    
    ping_count = 0
    success_count = 0
    
    try:
        while True:
            ping_count += 1
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"[{now}] Ping #{ping_count}...", end=" ")
            
            if ping_service(cpa_url):
                success_count += 1
                print(f"✅ 成功 (成功率: {success_count}/{ping_count})")
            else:
                print(f"❌ 失败 (成功率: {success_count}/{ping_count})")
            
            time.sleep(PING_INTERVAL)
    
    except KeyboardInterrupt:
        print()
        print()
        print("=" * 60)
        print("已停止")
        print(f"总 Ping 次数: {ping_count}")
        print(f"成功次数: {success_count}")
        print(f"成功率: {success_count/ping_count*100:.1f}%")
        print("=" * 60)

if __name__ == "__main__":
    main()
