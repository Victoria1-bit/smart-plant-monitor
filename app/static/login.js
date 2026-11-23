// Sends the sign in form and opens the dashboard when it works.

document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = document.getElementById("login-message");

    try {
        await sendJson("/api/auth/login", "POST", {
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
        });
        window.location.href = "/";
    } catch (error) {
        showMessage(message, error.message, true);
    }
});
