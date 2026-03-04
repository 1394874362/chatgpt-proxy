#!/usr/bin/env python3
"""
CPA 反代 API 使用示例
"""

import requests

# 你的 CPA 反代地址
CPA_BASE_URL = "https://chatgpt-proxy-xxxx.onrender.com"
CPA_PASSWORD = "你的密码"

def chat_with_gpt(message: str) -> str:
    """
    通过 CPA 反代调用 ChatGPT
    """
    url = f"{CPA_BASE_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {CPA_PASSWORD}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",  # 或 gpt-4
        "messages": [
            {"role": "user", "content": message}
        ],
        "stream": False
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"错误: {response.status_code} - {response.text}"

# 使用示例
if __name__ == "__main__":
    # 测试对话
    answer = chat_with_gpt("你好，请介绍一下你自己")
    print(f"ChatGPT: {answer}")
    
    # 多轮对话
    questions = [
        "1+1等于几？",
        "用 Python 写一个冒泡排序",
        "解释一下什么是递归"
    ]
    
    for q in questions:
        print(f"\n问: {q}")
        answer = chat_with_gpt(q)
        print(f"答: {answer}")
