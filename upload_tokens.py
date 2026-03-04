#!/usr/bin/env python3
"""
自动上传 Token 到 CPA 服务器
支持批量上传、断点续传、进度显示
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Any

# 配置文件路径
CONFIG_FILE = "config.json"

def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ 配置文件不存在: {CONFIG_FILE}")
        print(f"请复制 config.example.json 为 config.json 并填写配置")
        exit(1)
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_uploaded_tokens(cpa_url: str, password: str) -> List[str]:
    """获取已上传的 Token 列表"""
    try:
        response = requests.get(
            f"{cpa_url}/v0/management/auth-files",
            headers={"Authorization": f"Bearer {password}"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            files = data.get("files", [])
            return [f.get("name", "") for f in files]
        else:
            print(f"⚠️  获取已上传列表失败: {response.status_code}")
            return []
    except Exception as e:
        print(f"⚠️  获取已上传列表异常: {e}")
        return []

def upload_token(cpa_url: str, password: str, token_file: Path) -> bool:
    """上传单个 Token 文件"""
    try:
        with open(token_file, 'rb') as f:
            files = {'file': (token_file.name, f, 'application/json')}
            response = requests.post(
                f"{cpa_url}/v0/management/auth-files",
                headers={"Authorization": f"Bearer {password}"},
                files=files,
                timeout=30
            )
        
        if response.status_code in (200, 201, 204):
            return True
        else:
            print(f"  ❌ 上传失败 ({response.status_code}): {response.text[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ 上传异常: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("  CPA Token 自动上传工具")
    print("=" * 60)
    print()
    
    # 加载配置
    config = load_config()
    cpa_url = config.get("cpa_url", "").rstrip("/")
    password = config.get("cpa_password", "")
    tokens_dir = Path(config.get("tokens_dir", "../data/tokens"))
    
    if not cpa_url or not password:
        print("❌ 配置文件缺少 cpa_url 或 cpa_password")
        exit(1)
    
    if not tokens_dir.exists():
        print(f"❌ Token 目录不存在: {tokens_dir}")
        exit(1)
    
    # 测试连接
    print(f"🔗 测试连接: {cpa_url}")
    try:
        response = requests.get(f"{cpa_url}/", timeout=10)
        print(f"✅ 连接成功 (HTTP {response.status_code})")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("请检查 CPA 服务是否正常运行")
        exit(1)
    
    print()
    
    # 获取本地 Token 文件
    token_files = list(tokens_dir.glob("token_*.json"))
    print(f"📁 本地 Token 文件: {len(token_files)} 个")
    
    if not token_files:
        print("⚠️  没有找到 Token 文件")
        exit(0)
    
    # 获取已上传列表
    print(f"🔍 检查已上传的 Token...")
    uploaded = set(get_uploaded_tokens(cpa_url, password))
    print(f"✅ 已上传: {len(uploaded)} 个")
    print()
    
    # 过滤未上传的文件
    to_upload = [f for f in token_files if f.name not in uploaded]
    
    if not to_upload:
        print("🎉 所有 Token 已上传，无需操作")
        exit(0)
    
    print(f"📤 待上传: {len(to_upload)} 个")
    print()
    
    # 确认上传
    confirm = input(f"是否开始上传 {len(to_upload)} 个 Token? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 已取消")
        exit(0)
    
    print()
    print("=" * 60)
    print("开始上传...")
    print("=" * 60)
    print()
    
    # 批量上传
    success_count = 0
    fail_count = 0
    
    for i, token_file in enumerate(to_upload, 1):
        print(f"[{i}/{len(to_upload)}] {token_file.name}")
        
        if upload_token(cpa_url, password, token_file):
            print(f"  ✅ 上传成功")
            success_count += 1
        else:
            fail_count += 1
        
        # 避免请求过快
        if i < len(to_upload):
            time.sleep(0.5)
    
    # 统计结果
    print()
    print("=" * 60)
    print("上传完成")
    print("=" * 60)
    print(f"✅ 成功: {success_count} 个")
    print(f"❌ 失败: {fail_count} 个")
    print(f"📊 总计: {len(to_upload)} 个")
    print()
    
    # 验证最终状态
    print("🔍 验证上传结果...")
    final_uploaded = get_uploaded_tokens(cpa_url, password)
    print(f"✅ CPA 服务器当前账号数: {len(final_uploaded)} 个")

if __name__ == "__main__":
    main()
