document.getElementById("logout-btn").addEventListener("click", async () => {
    const response = await fetch("/api/logout", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
        },
    });
    const data = await response.json().catch(() => ({}));
    window.location.href = data.redirect || "/login";
});
