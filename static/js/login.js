const passwordStep = document.querySelector('.field-step[data-step="password"]');
const nextBtn = document.getElementById("next-btn");
const submitBtn = document.getElementById("submit-btn");
const loginErrorsEl = document.getElementById("login-errors");

nextBtn.addEventListener("click", () => {
    const username = document.getElementById("username").value;
    if (!validateUsername(username)) {
        showErrors(loginErrorsEl, ["El usuario debe tener al menos 3 caracteres."]);
        return;
    }
    showErrors(loginErrorsEl, []);
    passwordStep.hidden = false;
    nextBtn.hidden = true;
    submitBtn.hidden = false;
    document.getElementById("password").focus();
});

document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const errors = [];
    if (!validateUsername(username)) {
        errors.push("El usuario debe tener al menos 3 caracteres.");
    }
    if (!validatePassword(password)) {
        errors.push("La contraseña debe tener al menos 8 caracteres.");
    }
    if (errors.length) {
        showErrors(loginErrorsEl, errors);
        return;
    }

    const { ok, data } = await postJson("/api/login", { username, password });
    if (!ok) {
        showErrors(loginErrorsEl, data.errors || ["Ocurrió un error al iniciar sesión."]);
        return;
    }
    window.location.href = data.redirect || "/dashboard";
});
