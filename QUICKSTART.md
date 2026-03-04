# 🚀 5 分钟快速开始

## 第 1 步：部署到 Render（2 分钟）

### 最简单方式：

1. 访问 https://render.com 并登录
2. 点击 "New +" → "Web Service"
3. 选择 "Deploy an existing image from a registry"
4. 填写：
   ```
   Image URL: linweiyuan/go-chatgpt-api:latest
   Name: chatgpt-proxy
   ```
5. 添加环境变量：
   ```
   ADMIN_PASSWORD = 你的强密码（记住这个密码！）
   PORT = 8080
   ```
6. 点击 "Create Web Service"
7. 等待部署完成，记下你的地址：`https://chatgpt-proxy-xxxx.onrender.com`

---

## 第 2 步：配置本地工具（1 分钟）

1. **复制配置文件**
   ```bash
   cp config.example.json config.json
   ```

2. **编辑 config.json**
   ```json
   {
     "cpa_url": "https://chatgpt-proxy-xxxx.onrender.com",
     "cpa_password": "你在 Render 设置的密码"
   }
   ```

---

## 第 3 步：上传账号（1 分钟）

```bash
# 安装依赖
pip install requests

# 上传所有账号
python upload_tokens.py
```

等待上传完成，你会看到：
```
✅ 成功: 400 个
📊 CPA 服务器当前账号数: 400 个
```

---

## 第 4 步：配置保活（1 分钟）

### 方式 A：使用 UptimeRobot（推荐）

1. 访问 https://uptimerobot.com 注册
2. 进入 My Settings → API Settings
3. 创建 Main API Key
4. 复制 API Key 到 `config.json`：
   ```json
   {
     "uptimerobot_api_key": "你的API Key"
   }
   ```
5. 运行配置脚本：
   ```bash
   python setup_uptimerobot.py
   ```

### 方式 B：使用 Cron-job.org

1. 访问 https://cron-job.org 注册
2. 创建新任务：
   - URL: `https://chatgpt-proxy-xxxx.onrender.com`
   - 间隔: 每 10 分钟
3. 保存

---

## 第 5 步：开始使用！

### 测试 API

```bash
curl https://chatgpt-proxy-xxxx.onrender.com/v1/chat/completions \
  -H "Authorization: Bearer 你的密码" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### Python 示例

```python
import requests

response = requests.post(
    "https://chatgpt-proxy-xxxx.onrender.com/v1/chat/completions",
    headers={"Authorization": "Bearer 你的密码"},
    json={
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "你好"}]
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

---

## 🎉 完成！

你现在有：
- ✅ 一个运行在 Render 的 CPA 反代服务
- ✅ 400+ 个 ChatGPT 账号
- ✅ 统一的 API 接口
- ✅ 自动保活（永不休眠）

---

## 💡 下一步

- 在 ChatGPT-Next-Web 中使用你的 API
- 在 ChatBox 中配置自定义 API
- 编写自己的应用调用 API

---

## ❓ 遇到问题？

### 问题 1：上传失败
- 检查 CPA 服务是否正常运行
- 检查密码是否正确
- 查看 Render 日志

### 问题 2：API 调用失败
- 确认账号已上传成功
- 检查请求格式是否正确
- 查看 Render 日志

### 问题 3：服务休眠
- 配置 UptimeRobot 或 Cron-job.org
- 或运行本地保活脚本：`python keep_alive.py`

---

## 📖 更多文档

- [完整 README](README.md)
- [API 文档](https://github.com/linweiyuan/go-chatgpt-api)
