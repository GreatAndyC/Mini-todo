
# 25.9.25 Mini Todo 全栈项目

## 1. 项目简介
这是一个极简的全栈 Todo 应用，用于练习 **前端 + 后端 + 数据库 + 部署** 的完整流程。

## 2. 功能
- 添加任务  
- 查看任务列表  
- 勾选任务完成/未完成  
- 删除任务  

## 3. 技术栈
- **Frontend**: HTML / CSS / JavaScript （部署在 Vercel）  
- **Backend**: Flask + SQLite （部署在 Render）  
- **架构**: 前端静态站点调用后端 REST API  

## 4. 快速开始 (本地运行)

### 后端
```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate   # Windows PowerShell
pip install -r requirements.txt
python app.py
# 打开 http://127.0.0.1:5000/health
````

### 前端

```bash
cd ../frontend
# 修改 config.js 的 API_BASE 为 http://127.0.0.1:5000
# 然后用 VSCode Live Server 打开 index.html
```

## 5. 部署

* **Frontend (Vercel)**: [https://your-frontend.vercel.app](https://your-frontend.vercel.app)
* **Backend (Render)**: [https://your-backend.onrender.com/health](https://your-backend.onrender.com/health)

## 6. Pros / Cons

✅ Pros: 超轻量、结构清晰、覆盖完整技术栈、可快速演示
❌ Cons: SQLite 在 Render 免费实例上是临时存储（数据可能重置），不适合生产环境

## 7. 文件结构

```text
minitodo/
├─ README.md               # 项目说明
├─ backend/                # 后端 (Flask + SQLite)
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ Procfile
│  ├─ database.db          # SQLite 数据库
│  └─ README.md
│
└─ frontend/               # 前端 (HTML/CSS/JS)
   ├─ index.html
   ├─ config.js
   ├─ app.js
   ├─ styles.css
   └─ README.md
```



