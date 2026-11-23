// Sends the sign in form. The server does not accept logins yet.

document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = document.getElementById("login-message");

    try {
        await sendJson("/api/login", "POST", {
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
        });
    } catch (error) {
        showMessage(message, error.message, true);
    }
});
