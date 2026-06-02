import { login, getToken } from "./api.js";

function $(id) {
  return document.getElementById(id);
}

function redirectToAdmin() {
  window.location.href = "./admin.html";
}

if (getToken()) {
  redirectToAdmin();
}

const form = $("loginForm");
const error = $("error");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  error.hidden = true;

  const username = $("username").value.trim();
  const password = $("password").value;

  try {
    await login(username, password);
    redirectToAdmin();
  } catch (err) {
    error.textContent = err?.message || "Falha no login";
    error.hidden = false;
  }
});

