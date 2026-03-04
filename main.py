"""
ChatGPT Account Pool API - Render Compatible Version
基于 FastAPI 的 ChatGPT 账号池管理系统
"""
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="ChatGPT Account Pool API")

# 配置
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1394874362.ljw")
DATA_FILE = "/tmp/accounts.json"

# 数据模型
class Account(BaseModel):
    email: str
    access_token: str
    refresh_token: Optional[str] = None
    session_token: Optional[str] = None
    expires_at: Optional[int] = None
    status: str = "active"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class AccountPool:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.load_accounts()
    
    def load_accounts(self):
        """从文件加载账号"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.accounts = {k: Account(**v) for k, v in data.items()}
            except Exception as e:
                print(f"加载账号失败: {e}")
    
    def save_accounts(self):
        """保存账号到文件"""
        try:
            data = {k: v.dict() for k, v in self.accounts.items()}
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存账号失败: {e}")
    
    def add_account(self, account: Account) -> bool:
        """添加账号"""
        account_id = hashlib.md5(account.email.encode()).hexdigest()[:16]
        account.created_at = datetime.now().isoformat()
        account.updated_at = account.created_at
        self.accounts[account_id] = account
        self.save_accounts()
        return True
    
    def get_account(self) -> Optional[Account]:
        """获取一个可用账号"""
        for account in self.accounts.values():
            if account.status == "active":
                return account
        return None
    
    def get_all_accounts(self) -> List[Account]:
        """获取所有账号"""
        return list(self.accounts.values())
    
    def update_account_status(self, email: str, status: str) -> bool:
        """更新账号状态"""
        for account_id, account in self.accounts.items():
            if account.email == email:
                account.status = status
                account.updated_at = datetime.now().isoformat()
                self.save_accounts()
                return True
        return False

# 全局账号池
pool = AccountPool()

# 认证中间件
def verify_password(password: str) -> bool:
    """验证密码"""
    return password == ADMIN_PASSWORD

# API 路由
@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "ok",
        "service": "ChatGPT Account Pool API",
        "accounts": len(pool.accounts),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/accounts")
async def list_accounts(authorization: Optional[str] = Header(None)):
    """列出所有账号"""
    if not authorization or not verify_password(authorization.replace("Bearer ", "")):
        raise HTTPException(status_code=401, detail="未授权")
    
    accounts = pool.get_all_accounts()
    return {
        "total": len(accounts),
        "accounts": [acc.dict() for acc in accounts]
    }

@app.post("/api/accounts")
async def add_account(account: Account, authorization: Optional[str] = Header(None)):
    """添加账号"""
    if not authorization or not verify_password(authorization.replace("Bearer ", "")):
        raise HTTPException(status_code=401, detail="未授权")
    
    success = pool.add_account(account)
    if success:
        return {"status": "success", "message": "账号添加成功"}
    else:
        raise HTTPException(status_code=500, detail="添加失败")

@app.post("/api/accounts/batch")
async def add_accounts_batch(accounts: List[Account], authorization: Optional[str] = Header(None)):
    """批量添加账号"""
    if not authorization or not verify_password(authorization.replace("Bearer ", "")):
        raise HTTPException(status_code=401, detail="未授权")
    
    success_count = 0
    for account in accounts:
        if pool.add_account(account):
            success_count += 1
    
    return {
        "status": "success",
        "total": len(accounts),
        "success": success_count,
        "failed": len(accounts) - success_count
    }

@app.get("/api/account")
async def get_account():
    """获取一个可用账号（公开接口）"""
    account = pool.get_account()
    if account:
        return account.dict()
    else:
        raise HTTPException(status_code=404, detail="没有可用账号")

@app.put("/api/accounts/{email}/status")
async def update_status(email: str, status: str, authorization: Optional[str] = Header(None)):
    """更新账号状态"""
    if not authorization or not verify_password(authorization.replace("Bearer ", "")):
        raise HTTPException(status_code=401, detail="未授权")
    
    if status not in ["active", "inactive", "expired"]:
        raise HTTPException(status_code=400, detail="无效的状态")
    
    success = pool.update_account_status(email, status)
    if success:
        return {"status": "success", "message": "状态更新成功"}
    else:
        raise HTTPException(status_code=404, detail="账号不存在")

@app.get("/api/stats")
async def get_stats():
    """获取统计信息（公开接口）"""
    accounts = pool.get_all_accounts()
    active = sum(1 for acc in accounts if acc.status == "active")
    inactive = sum(1 for acc in accounts if acc.status == "inactive")
    expired = sum(1 for acc in accounts if acc.status == "expired")
    
    return {
        "total": len(accounts),
        "active": active,
        "inactive": inactive,
        "expired": expired,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
