// Sends the create account form and opens the dashboard when it works.

document.getElementById("register-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = document.getElementById("register-message");

    try {
        await sendJson("/api/auth/register", "POST", {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
        });
        window.location.href = "/";
    } catch (error) {
        showMessage(message, error.message, true);
    }
});
