// 全局变量
let accountsData = [];
let currentFilter = 'all';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 初始化应用
function initializeApp() {
    setupNavigation();
    setupFilters();
    refreshData();
    
    // 每30秒自动刷新数据
    setInterval(refreshData, 30000);
}

// 设置导航
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 移除所有活跃状态
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // 添加当前活跃状态
            this.classList.add('active');
            
            // 显示对应页面
            const page = this.dataset.page;
            showPage(page);
            
            // 更新页面标题
            updatePageTitle(page);
        });
    });
}

// 显示页面
function showPage(pageId) {
    const pages = document.querySelectorAll('.page-content');
    pages.forEach(page => page.classList.add('hidden'));
    
    const targetPage = document.getElementById(`${pageId}-page`);
    if (targetPage) {
        targetPage.classList.remove('hidden');
    }
    
    // 如果是账号页面，加载账号数据
    if (pageId === 'accounts') {
        loadAccountsPage();
    }
}

// 更新页面标题
function updatePageTitle(page) {
    const titles = {
        'dashboard': '仪表板',
        'accounts': '账号管理',
        'api': 'API 文档'
    };
    
    const subtitles = {
        'dashboard': '实时监控您的 ChatGPT 账号池',
        'accounts': '管理和查看所有账号信息',
        'api': '查看 API 接口使用说明'
    };
    
    document.querySelector('.page-title').textContent = titles[page] || '仪表板';
    document.querySelector('.page-subtitle').textContent = subtitles[page] || '';
}

// 设置过滤器
function setupFilters() {
    const filterTabs = document.querySelectorAll('.filter-tab');
    filterTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // 移除所有活跃状态
            filterTabs.forEach(t => t.classList.remove('active'));
            
            // 添加当前活跃状态
            this.classList.add('active');
            
            // 更新过滤器
            currentFilter = this.dataset.filter;
            filterAccounts();
        });
    });
    
    // 搜索功能
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            filterAccounts();
        });
    }
}

// 刷新数据
async function refreshData() {
    try {
        // 显示加载状态
        showLoadingState();
        
        // 获取统计数据
        const statsResponse = await fetch('/api/stats');
        const stats = await statsResponse.json();
        
        // 更新统计显示
        updateStats(stats);
        
        // 获取账号数据（如果在账号页面）
        const currentPage = document.querySelector('.nav-item.active').dataset.page;
        if (currentPage === 'accounts') {
            await loadAccountsData();
        }
        
        // 更新活动记录
        updateRecentActivity();
        
        // 隐藏加载状态
        hideLoadingState();
        
    } catch (error) {
        console.error('刷新数据失败:', error);
        showError('数据加载失败，请检查网络连接');
    }
}

// 更新统计数据
function updateStats(stats) {
    document.getElementById('total-accounts').textContent = stats.total || 0;
    document.getElementById('active-accounts').textContent = stats.active || 0;
    document.getElementById('inactive-accounts').textContent = stats.inactive || 0;
    document.getElementById('expired-accounts').textContent = stats.expired || 0;
}

// 加载账号数据
async function loadAccountsData() {
    try {
        const response = await fetch('/api/accounts', {
            headers: {
                'Authorization': '1394874362.ljw'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            accountsData = data.accounts || [];
            filterAccounts();
        } else {
            console.error('获取账号数据失败:', response.status);
        }
    } catch (error) {
        console.error('加载账号数据失败:', error);
    }
}

// 加载账号管理页面
function loadAccountsPage() {
    if (accountsData.length === 0) {
        loadAccountsData();
    } else {
        filterAccounts();
    }
}

// 过滤账号
function filterAccounts() {
    let filteredAccounts = accountsData;
    
    // 按状态过滤
    if (currentFilter !== 'all') {
        filteredAccounts = accountsData.filter(account => account.status === currentFilter);
    }
    
    // 按搜索词过滤
    const searchInput = document.getElementById('search-input');
    if (searchInput && searchInput.value.trim()) {
        const searchTerm = searchInput.value.trim().toLowerCase();
        filteredAccounts = filteredAccounts.filter(account => 
            account.email.toLowerCase().includes(searchTerm)
        );
    }
    
    // 渲染账号列表
    renderAccounts(filteredAccounts);
}

// 渲染账号列表
function renderAccounts(accounts) {
    const grid = document.getElementById('accounts-grid');
    if (!grid) return;
    
    if (accounts.length === 0) {
        grid.innerHTML = `
            <div class="no-accounts">
                <div class="no-accounts-icon">📭</div>
                <h3>暂无账号</h3>
                <p>没有找到符合条件的账号</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = accounts.map(account => `
        <div class="account-card" onclick="showAccountDetails('${account.email}')">
            <div class="account-header">
                <div class="account-email">${account.email}</div>
                <div class="account-status ${account.status}">${getStatusText(account.status)}</div>
            </div>
            <div class="account-info">
                <div class="account-field">
                    <span class="label">创建时间</span>
                    <span class="value">${formatDate(account.created_at)}</span>
                </div>
                <div class="account-field">
                    <span class="label">最后更新</span>
                    <span class="value">${formatDate(account.updated_at)}</span>
                </div>
                <div class="account-field">
                    <span class="label">Token 状态</span>
                    <span class="value">${account.access_token ? '有效' : '无效'}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// 获取状态文本
function getStatusText(status) {
    const statusMap = {
        'active': '活跃',
        'inactive': '暂停',
        'expired': '过期'
    };
    return statusMap[status] || status;
}

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '未知';
    
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    if (days < 30) return `${days}天前`;
    
    return date.toLocaleDateString('zh-CN');
}

// 显示账号详情
function showAccountDetails(email) {
    const account = accountsData.find(acc => acc.email === email);
    if (!account) return;
    
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <div class="account-details">
            <div class="detail-row">
                <strong>邮箱地址：</strong>
                <span>${account.email}</span>
            </div>
            <div class="detail-row">
                <strong>状态：</strong>
                <span class="account-status ${account.status}">${getStatusText(account.status)}</span>
            </div>
            <div class="detail-row">
                <strong>Access Token：</strong>
                <textarea readonly class="token-field">${account.access_token || '无'}</textarea>
            </div>
            <div class="detail-row">
                <strong>Refresh Token：</strong>
                <textarea readonly class="token-field">${account.refresh_token || '无'}</textarea>
            </div>
            <div class="detail-row">
                <strong>Session Token：</strong>
                <textarea readonly class="token-field">${account.session_token || '无'}</textarea>
            </div>
            <div class="detail-row">
                <strong>创建时间：</strong>
                <span>${formatDate(account.created_at)}</span>
            </div>
            <div class="detail-row">
                <strong>最后更新：</strong>
                <span>${formatDate(account.updated_at)}</span>
            </div>
        </div>
        
        <style>
            .account-details {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }
            
            .detail-row {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .detail-row strong {
                color: #333;
                font-weight: 600;
            }
            
            .token-field {
                width: 100%;
                min-height: 80px;
                padding: 0.75rem;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-family: 'Monaco', 'Menlo', monospace;
                font-size: 0.8rem;
                background: #f8f9fa;
                resize: vertical;
            }
            
            .no-accounts {
                grid-column: 1 / -1;
                text-align: center;
                padding: 4rem 2rem;
                color: #666;
            }
            
            .no-accounts-icon {
                font-size: 4rem;
                margin-bottom: 1rem;
            }
        </style>
    `;
    
    document.getElementById('account-modal').classList.remove('hidden');
}

// 关闭模态框
function closeModal() {
    document.getElementById('account-modal').classList.add('hidden');
}

// 获取随机账号
async function getRandomAccount() {
    try {
        const response = await fetch('/api/account');
        const account = await response.json();
        
        if (account) {
            showAccountDetails(account.email);
        } else {
            showError('没有可用的账号');
        }
    } catch (error) {
        console.error('获取随机账号失败:', error);
        showError('获取账号失败');
    }
}

// 测试连接
async function testConnection() {
    try {
        const startTime = Date.now();
        const response = await fetch('/');
        const endTime = Date.now();
        
        if (response.ok) {
            const latency = endTime - startTime;
            showSuccess(`连接正常，延迟 ${latency}ms`);
        } else {
            showError('连接测试失败');
        }
    } catch (error) {
        console.error('连接测试失败:', error);
        showError('连接测试失败');
    }
}

// 导出数据
function exportData() {
    if (accountsData.length === 0) {
        showError('没有数据可导出');
        return;
    }
    
    const dataStr = JSON.stringify(accountsData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `chatgpt-accounts-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    
    showSuccess('数据导出成功');
}

// 更新最近活动
function updateRecentActivity() {
    const activityList = document.getElementById('activity-list');
    if (!activityList) return;
    
    const activities = [
        {
            icon: '✅',
            title: '系统状态检查完成',
            time: '2分钟前'
        },
        {
            icon: '🔄',
            title: '账号池数据已刷新',
            time: '5分钟前'
        },
        {
            icon: '📊',
            title: '统计数据已更新',
            time: '10分钟前'
        },
        {
            icon: '🚀',
            title: '服务启动成功',
            time: '1小时前'
        }
    ];
    
    activityList.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-icon">${activity.icon}</div>
            <div class="activity-content">
                <div class="activity-title">${activity.title}</div>
                <div class="activity-time">${activity.time}</div>
            </div>
        </div>
    `).join('');
}

// 显示加载状态
function showLoadingState() {
    // 可以在这里添加加载动画
}

// 隐藏加载状态
function hideLoadingState() {
    // 隐藏加载动画
}

// 显示成功消息
function showSuccess(message) {
    showNotification(message, 'success');
}

// 显示错误消息
function showError(message) {
    showNotification(message, 'error');
}

// 显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // 添加样式
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 300px;
        word-wrap: break-word;
    `;
    
    // 根据类型设置背景色
    if (type === 'success') {
        notification.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
    } else if (type === 'error') {
        notification.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
    } else {
        notification.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
    }
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 3秒后自动移除
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);