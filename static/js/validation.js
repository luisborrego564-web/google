// Validación de entrada compartida por los formularios (cliente).
const EMAIL_PATTERN = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').content;
}

function validateUsername(username) {
    return typeof username === "string" && username.trim().length >= 3;
}

function validateEmail(email) {
    return typeof email === "string" && EMAIL_PATTERN.test(email.trim());
}

function validatePassword(password) {
    return typeof password === "string" && password.length >= 8;
}

function showErrors(listEl, errors) {
    listEl.innerHTML = "";
    if (!errors.length) {
        listEl.hidden = true;
        return;
    }
    errors.forEach((error) => {
        const li = document.createElement("li");
        li.textContent = error;
        listEl.appendChild(li);
    });
    listEl.hidden = false;
}

async function postJson(endpoint, payload) {
    const response = await fetch(endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(payload),
    });
    const data = await response.json().catch(() => ({}));
    return { ok: response.ok, data };
}
