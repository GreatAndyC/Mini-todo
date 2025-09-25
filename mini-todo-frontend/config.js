// 替换为你的后端地址（部署上线后粘贴 Render/Railway 的域名）
const API_BASE = localStorage.getItem("API_BASE") || "http://127.0.0.1:5000";
document.getElementById("apiUrl").textContent = API_BASE;
