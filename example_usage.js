/**
 * CPA 反代 API 使用示例 (Node.js)
 */

const CPA_BASE_URL = "https://chatgpt-proxy-xxxx.onrender.com";
const CPA_PASSWORD = "你的密码";

async function chatWithGPT(message) {
    const response = await fetch(`${CPA_BASE_URL}/v1/chat/completions`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${CPA_PASSWORD}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'gpt-4o-mini',
            messages: [
                { role: 'user', content: message }
            ],
            stream: false
        })
    });
    
    if (response.ok) {
        const data = await response.json();
        return data.choices[0].message.content;
    } else {
        throw new Error(`错误: ${response.status} - ${await response.text()}`);
    }
}

// 使用示例
(async () => {
    try {
        const answer = await chatWithGPT("你好，请介绍一下你自己");
        console.log(`ChatGPT: ${answer}`);
    } catch (error) {
        console.error(error);
    }
})();
