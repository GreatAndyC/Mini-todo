// 替换为你的后端地址（部署上线后粘贴 Render/Railway 的域名）
const API_BASE = localStorage.getItem("API_BASE") || "https://mini-todo-u668.onrender.com";
document.getElementById("apiUrl").textContent = API_BASE;
