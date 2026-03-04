# ChatGPT Proxy API - Render 一键部署

> 在 Render 免费部署 CPA 反代服务，管理 400+ ChatGPT 账号

## 📋 目录

- [快速部署](#快速部署)
- [配置说明](#配置说明)
- [上传账号](#上传账号)
- [使用 API](#使用-api)
- [防止休眠](#防止休眠)
- [常见问题](#常见问题)

---

## 🚀 快速部署

### 方法 1：通过 GitHub（推荐）

1. **Fork 本仓库**
   - 点击右上角 "Fork" 按钮

2. **部署到 Render**
   - 访问 [Render.com](https://render.com)
   - 点击 "New +" → "Web Service"
   - 选择你 Fork 的仓库
   - Render 会自动检测 `render.yaml`
   - 修改环境变量 `ADMIN_PASSWORD`（重要！）
   - 点击 "Create Web Service"

3. **等待部署**（约 3-5 分钟）
   - 部署完成后会得到地址：`https://your-app-name.onrender.com`

### 方法 2：直接部署镜像（更简单）

1. **登录 Render**
   - 访问 [Render.com](https://render.com)

2. **创建服务**
   - 点击 "New +" → "Web Service"
   - 选择 "Deploy an existing image from a registry"

3. **填写配置**
   ```
   Image URL: linweiyuan/go-chatgpt-api:latest
   Name: chatgpt-proxy
   Region: Singapore
   Instance Type: Free
   ```

4. **添加环境变量**
   ```
   ADMIN_PASSWORD = 你的强密码
   PORT = 8080
   ```

5. **创建服务**
   - 点击 "Create Web Service"

---

## ⚙️ 配置说明

### 1. 创建配置文件

```bash
# 复制配置模板
cp config.example.json config.json

# 编辑配置
nano config.json
```

### 2. 填写配置

```json
{
  "cpa_url": "https://your-app-name.onrender.com",
  "cpa_password": "你在 Render 设置的密码",
  "tokens_dir": "../data/tokens",
  "uptimerobot_api_key": "可选，用于自动唤醒"
}
```

---

## 📤 上传账号

### 自动批量上传（推荐）

```bash
# 安装依赖
pip install requests

# 运行上传脚本
python upload_tokens.py
```

脚本会自动：
- ✅ 检测已上传的账号（避免重复）
- ✅ 批量上传未上传的账号
- ✅ 显示上传进度和结果
- ✅ 支持断点续传

### 手动上传单个账号

```bash
curl -X POST https://your-app-name.onrender.com/v0/management/auth-files \
  -H "Authorization: Bearer 你的密码" \
  -F "file=@data/tokens/token_xxx.json"
```

---

## 🎮 使用 API

### Python 示例

```python
import requests

CPA_URL = "https://your-app-name.onrender.com"
PASSWORD = "你的密码"

response = requests.post(
    f"{CPA_URL}/v1/chat/completions",
    headers={"Authorization": f"Bearer {PASSWORD}"},
    json={
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "你好"}]
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

### JavaScript 示例

```javascript
const response = await fetch('https://your-app-name.onrender.com/v1/chat/completions', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer 你的密码',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        model: 'gpt-4o-mini',
        messages: [{role: 'user', content: '你好'}]
    })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

### cURL 示例

```bash
curl https://your-app-name.onrender.com/v1/chat/completions \
  -H "Authorization: Bearer 你的密码" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

---

## ⏰ 防止休眠

Render 免费版 15 分钟无请求会休眠，有 3 种解决方案：

### 方案 1：UptimeRobot（推荐，完全免费）

1. **注册 UptimeRobot**
   - 访问 [UptimeRobot.com](https://uptimerobot.com)
   - 免费注册账号

2. **获取 API Key**
   - 进入 My Settings → API Settings
   - 创建 Main API Key
   - 复制到 `config.json`

3. **自动配置监控**
   ```bash
   python setup_uptimerobot.py
   ```

4. **完成！**
   - UptimeRobot 会每 5 分钟 ping 一次
   - 你的服务永不休眠

### 方案 2：本地保活脚本

```bash
# 后台运行保活脚本
python keep_alive.py
```

### 方案 3：Cron-job.org

1. 访问 [Cron-job.org](https://cron-job.org)
2. 创建免费账号
3. 添加定时任务：
   - URL: `https://your-app-name.onrender.com`
   - 间隔: 每 10 分钟

---

## 🔍 管理和监控

### 查看账号列表

```bash
curl https://your-app-name.onrender.com/v0/management/auth-files \
  -H "Authorization: Bearer 你的密码"
```

### 删除账号

```bash
curl -X DELETE "https://your-app-name.onrender.com/v0/management/auth-files?name=token_xxx.json" \
  -H "Authorization: Bearer 你的密码"
```

### 查看日志

1. 登录 Render Dashboard
2. 选择你的服务
3. 点击 "Logs" 查看实时日志

---

## ❓ 常见问题

### Q1: 首次访问很慢？
A: Render 免费版休眠后首次唤醒需要 30-60 秒，配置 UptimeRobot 可解决。

### Q2: 如何更换密码？
A: 在 Render Dashboard → 你的服务 → Environment → 修改 `ADMIN_PASSWORD` → 保存。

### Q3: 支持多少个账号？
A: 理论上无限制，实测 1000+ 个账号运行稳定。

### Q4: 如何升级到付费版？
A: Render Dashboard → 你的服务 → Settings → Instance Type → 选择付费套餐。

### Q5: API 调用失败？
A: 检查：
- CPA 服务是否正常运行
- 密码是否正确
- 账号池是否有可用账号

---

## 📊 项目结构

```
cpa-deploy/
├── Dockerfile              # Docker 镜像配置
├── render.yaml             # Render 部署配置
├── config.example.json     # 配置模板
├── upload_tokens.py        # 批量上传脚本
├── keep_alive.py           # 本地保活脚本
├── setup_uptimerobot.py    # UptimeRobot 配置脚本
├── example_usage.py        # Python 使用示例
├── example_usage.js        # JavaScript 使用示例
└── README.md               # 本文件
```

---

## 🎯 完整工作流程

```
1. 部署 CPA 到 Render
   ↓
2. 配置 config.json
   ↓
3. 运行 upload_tokens.py 上传账号
   ↓
4. 运行 setup_uptimerobot.py 配置保活
   ↓
5. 使用 API 调用 ChatGPT
```

---

## 📝 License

MIT License

---

## 🙏 致谢

- [go-chatgpt-api](https://github.com/linweiyuan/go-chatgpt-api) - CPA 核心项目
- [Render](https://render.com) - 免费托管平台
- [UptimeRobot](https://uptimerobot.com) - 免费监控服务
