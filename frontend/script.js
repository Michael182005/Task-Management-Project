const BASE_URL = "http://127.0.0.1:8000/api";

// ---- AUTH ----

async function loginUser() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorMsg = document.getElementById("error-msg");
    const loginBtn = document.getElementById("loginBtn");

    errorMsg.textContent = "";
    loginBtn.innerText = "Loading...";
    loginBtn.disabled = true;

    try {
        const response = await fetch(BASE_URL + "/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("token", data.access_token);
            window.location.href = "dashboard.html";
        } else {
            errorMsg.textContent = data.detail || "Login failed. Please try again.";
        }
    } catch (error) {
        errorMsg.textContent = "Something went wrong";
    } finally {
        loginBtn.innerText = "Login";
        loginBtn.disabled = false;
    }
}

async function registerUser() {
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorMsg = document.getElementById("error-msg");

    errorMsg.textContent = "";

    try {
        const response = await fetch(BASE_URL + "/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Registration successful! Please login.");
            window.location.href = "index.html";
        } else {
            errorMsg.textContent = data.detail || "Registration failed. Try again.";
        }
    } catch (error) {
        errorMsg.textContent = "Something went wrong";
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

// ---- HELPERS ----

function getToken() {
    return localStorage.getItem("token");
}

function authHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + getToken()
    };
}

// ---- TASKS ----

async function fetchTasks() {
    const token = getToken();

    if (!token) {
        window.location.href = "index.html";
        return;
    }

    try {
        const response = await fetch(BASE_URL + "/tasks", {
            headers: authHeaders()
        });

        if (response.status === 401) {
            alert("Session expired. Please login again.");
            logout();
            return;
        }

        if (!response.ok) {
            alert("Something went wrong");
            return;
        }

        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        alert("Something went wrong");
    }
}

function renderTasks(tasks) {
    const taskContainer = document.getElementById("task-list");
    taskContainer.innerHTML = "";

    if (tasks.length === 0) {
        taskContainer.innerHTML = "<p>No tasks yet. Add one!</p>";
        return;
    }

    tasks.forEach(task => {
        const item = document.createElement("li");
        item.className = "task task-card";
        item.innerHTML = `
            <div class="task-info">
                <h4>${task.title}</h4>
                <p>${task.description || "No description provided."}</p>
            </div>
            <button class="btn-delete" onclick="deleteTask(${task.id})">Delete</button>
        `;
        taskContainer.appendChild(item);
    });
}

async function createTask() {
    const title = document.getElementById("task-title").value.trim();
    const description = document.getElementById("task-desc").value.trim();
    const addBtn = document.getElementById("addTaskBtn");

    if (!title) {
        alert("Please enter a task title.");
        return;
    }

    addBtn.innerText = "Adding...";
    addBtn.disabled = true;

    try {
        const response = await fetch(BASE_URL + "/tasks", {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({ title, description })
        });

        if (response.ok) {
            document.getElementById("task-title").value = "";
            document.getElementById("task-desc").value = "";
            fetchTasks();
        } else {
            const data = await response.json();
            alert(data.detail || "Something went wrong");
        }
    } catch (error) {
        alert("Something went wrong");
    } finally {
        addBtn.innerText = "Add Task";
        addBtn.disabled = false;
    }
}

async function deleteTask(id) {
    if (!confirm("Are you sure you want to delete this task?")) {
        return;
    }

    try {
        const response = await fetch(BASE_URL + "/tasks/" + id, {
            method: "DELETE",
            headers: authHeaders()
        });

        if (response.ok) {
            fetchTasks();
        } else {
            alert("Something went wrong");
        }
    } catch (error) {
        alert("Something went wrong");
    }
}
