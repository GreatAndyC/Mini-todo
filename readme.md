
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



## 8.部署后端到Render
注意：根目录选择mini-todo-backend
当本地代码更新并Push到Github时，render会自动重新部署代码

## 9.部署前端到Vercel
根目录选择mini-todo-frontend
部署好后端后，将config.json里面的link改为Render提供的链接
在后端没有释放的时候访问
https://mini-todo-cyan.vercel.app/
即可测试使用

## 10.本地测试
在backend目录下
创建虚拟环境
```
python -m venv .venv
```
激活虚拟环境git bash
```
source .venv/Scripts/activate
```
安装依赖
```
pip install -r requirements.txt
```

好嘞 👍 我帮你整理成一份可以直接放到 `README.md` 里的 Markdown 内容，复制即可。

---


## 11.部署踩坑总结（Vercel + Render）

### 1. Live Server 缓存问题
- **现象**：本地调试前端时，改了 `config.js` 或 `app.js`，刷新后还是旧数据。  
- **原因**：浏览器缓存静态资源，Live Server 不会自动禁用缓存。  
- **解决**：  
  - 强制刷新：`Ctrl+Shift+R`（Mac: `Cmd+Shift+R`）  
  - Chrome DevTools → Network → 勾选 **Disable cache**  
  - 上线后 Vercel 会自动给文件加 hash，不会有这个问题。  

---

### 2. `.gitignore` 配置不当
- **现象**：第一次 push 时，把 `.venv/` 和 `database.db` 传上去了，push 巨慢。  
- **解决**：  
  - `.gitignore` 示例：  
    ```gitignore
    .venv/
    __pycache__/
    *.pyc
    *.db
    node_modules/
    dist/
    ```
  - 清理并重新提交：  
    ```bash
    git rm -r --cached .
    git add .
    git commit -m "chore: clean repo with .gitignore"
    git push
    ```

---

### 3. SSH Push 失败
- **现象**：
````

Connection closed by UNKNOWN port 65535
fatal: Could not read from remote repository.

````
- **原因**：SSH Key 没配置好，或者网络阻断了 22 端口。  
- **解决**：  
- 配置 SSH Key → GitHub → Settings → SSH and GPG keys  
- 或者切换成 HTTPS：  
  ```bash
  git remote set-url origin https://github.com/<用户名>/<仓库名>.git
  ```

---

### 4. Flask CORS 错误
- **现象**：前端请求后端时报 CORS policy 错误。  
- **解决**：  
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
````

---

### 5. Render 上数据库未创建 (`db_exists=false`)

* **现象**：

  ```json
  {"db_exists": false, "ok": true, "service": "todo-backend"}
  ```
* **原因**：Render 用 `gunicorn app:app` 启动，不会执行 `if __name__ == "__main__"` 里的 `init_db()`。
* **解决**：
  把 `init_db()` 放到 `app = Flask(__name__)` 后面：

  ```python
  app = Flask(__name__)
  CORS(app)
  init_db()
  ```

---

### 6. Python 模块缺失

* **现象**：

  ```
  ModuleNotFoundError: No module named 'flask_cors'
  ```
* **原因**：虚拟环境没激活，或 `requirements.txt` 里缺少依赖。
* **解决**：

  * 激活虚拟环境：

    ```powershell
    .venv\Scripts\Activate.ps1   # PowerShell
    ```
  * 安装依赖：

    ```bash
    pip install -r requirements.txt
    ```

---

### 7. Git 换行符警告

* **现象**：

  ```
  warning: in the working copy of 'app.py', LF will be replaced by CRLF
  ```
* **原因**：Windows 和 Linux 换行符不一致。
* **解决**：

  ```bash
  git config --global core.autocrlf true
  ```

---

## ✅ 小结

* **前端**：静态站点（Vercel 部署）
* **后端**：Flask + SQLite（Render 部署）
* **功能**：任务的增删改查完整闭环
* **数据库**：自动初始化，数据持久化到 `database.db`

## 11.下一步优化
* 🟢 第一层：功能优化（最小可用增强）

任务状态更新：目前只能新增和删除，可以加上“修改任务内容”“标记已完成/未完成”。  

前端交互优化：加 loading 动画、错误提示（比如后端挂了时提醒）。  

样式优化：加一点 CSS 美化，任务列表更好看（勾选框、删除按钮、hover 效果）。  

更好的数据库操作：把 database.db 的逻辑封装到单独的文件，代码更清晰。  

* 🟡 第二层：工程优化（更专业）

分层结构：后端把 app.py 拆成 routes.py、models.py、db.py，形成更规范的结构。  

环境配置：用 .env 文件管理 API 地址、密钥，不写死在代码里。  

日志系统：Flask 打印请求日志，方便调试。  

错误处理：API 出错时返回标准 JSON（比如 {error: "db not found"}）。  

前端构建：把原生 JS 替换成 React / Vue（可选，面试加分）。  

* 🔵 第三层：部署优化（上线可用）

持久化数据库：Render 的 SQLite 是临时的，可以换成：  

Render + PostgreSQL（官方支持）  

PlanetScale / Railway 提供的免费 MySQL/Postgres  

容器化：用 Docker 打包后端 → 部署到自己服务器/VPS（学习 DevOps 技能）。  

CI/CD：配置 GitHub Actions，让 push → 自动测试 + 部署到 Vercel/Render。  

* 🔴 第四层：产品化（对外展示）

加登录功能：用户体系（注册、登录、JWT 鉴权），每个人有独立的任务列表。  

部署域名：绑定你自己的域名（比如 todo.caoyueyang.org）。  

写文档：把 README.md 完整化，包括架构图、API 文档、踩坑记录。  

Demo 视频：录一个 1 分钟的操作视频，放到 GitHub README 或简历里。  



