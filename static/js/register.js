document.getElementById("register-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorsEl = document.getElementById("register-errors");

    const errors = [];
    if (!validateUsername(username)) {
        errors.push("El usuario debe tener al menos 3 caracteres.");
    }
    if (!validateEmail(email)) {
        errors.push("El correo electrónico no es válido.");
    }
    if (!validatePassword(password)) {
        errors.push("La contraseña debe tener al menos 8 caracteres.");
    }
    if (errors.length) {
        showErrors(errorsEl, errors);
        return;
    }

    const { ok, data } = await postJson("/api/register", { username, email, password });
    if (!ok) {
        showErrors(errorsEl, data.errors || ["Ocurrió un error al registrarte."]);
        return;
    }
    window.location.href = "/login";
});
