async function fetchJSON(url, options={}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
}

async function loadTasks() {
  try {
    const data = await fetchJSON(`${API_BASE}/tasks`);
    renderTasks(data);
  } catch (e) {
    console.error(e);
    alert("加载任务失败: " + e.message);
  }
}

function renderTasks(tasks) {
  const ul = document.getElementById("taskList");
  ul.innerHTML = "";
  tasks.forEach(t => {
    const li = document.createElement("li");
    li.className = "task" + (t.done ? " done" : "");
    li.innerHTML = `
      <div class="left">
        <input type="checkbox" ${t.done ? "checked" : ""} data-id="${t.id}" class="toggle">
        <span class="content">${escapeHtml(t.content)}</span>
      </div>
      <div class="actions">
        <button class="del" data-id="${t.id}">删除</button>
      </div>
    `;
    ul.appendChild(li);
  });
}

function escapeHtml(str) {
  return str.replace(/[&<>"']/g, s => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[s]));
}

async function addTask() {
  const input = document.getElementById("taskInput");
  const content = input.value.trim();
  if (!content) return;
  try {
    await fetchJSON(`${API_BASE}/tasks`, {
      method: "POST",
      body: JSON.stringify({ content })
    });
    input.value = "";
    await loadTasks();
  } catch (e) {
    alert("添加失败: " + e.message);
  }
}

async function delTask(id) {
  try {
    await fetch(`${API_BASE}/tasks/${id}`, { method: "DELETE" });
    await loadTasks();
  } catch (e) {
    alert("删除失败: " + e.message);
  }
}

async function toggleTask(id, checked) {
  try {
    await fetchJSON(`${API_BASE}/tasks/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ done: checked })
    });
    await loadTasks();
  } catch (e) {
    alert("更新失败: " + e.message);
  }
}

document.addEventListener("click", (e) => {
  if (e.target.id === "addBtn") {
    addTask();
  } else if (e.target.classList.contains("del")) {
    delTask(e.target.dataset.id);
  } else if (e.target.classList.contains("toggle")) {
    toggleTask(e.target.dataset.id, e.target.checked);
  }
});

window.addEventListener("DOMContentLoaded", () => {
  loadTasks();
});
