export const API_BASE_URL =
  localStorage.getItem("API_BASE_URL") || window.location.origin;

const TOKEN_KEY = "todo_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request(path, { method = "GET", token, json, form } = {}) {
  const headers = { "ngrok-skip-browser-warning": "1" };
  if (token) headers.Authorization = `Bearer ${token}`;
  if (json) headers["Content-Type"] = "application/json";
  if (form) headers["Content-Type"] = "application/x-www-form-urlencoded";

  const res = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: json ? JSON.stringify(json) : form ? new URLSearchParams(form) : undefined,
  });

  const contentType = res.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await res.json().catch(() => null)
    : await res.text().catch(() => "");

  if (!res.ok) {
    const msg =
      payload?.detail ||
      (typeof payload === "string" && payload) ||
      `Erro ${res.status}`;
    const err = new Error(msg);
    err.status = res.status;
    err.payload = payload;
    throw err;
  }

  return payload;
}

export async function login(username, password) {
  const data = await request("/auth/token", {
    method: "POST",
    form: { username, password },
  });
  setToken(data.access_token);
  return data;
}

export async function getMe() {
  return request("/auth/me", { token: getToken() });
}

export async function listTasks() {
  return request("/tasks/", { token: getToken() });
}

export async function createTask(task) {
  return request("/tasks/", { method: "POST", token: getToken(), json: task });
}

export async function updateTask(id, task) {
  return request(`/tasks/${id}`, { method: "PUT", token: getToken(), json: task });
}

export async function deleteTask(id) {
  return request(`/tasks/${id}`, { method: "DELETE", token: getToken() });
}
