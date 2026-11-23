// Helpers used by every page.

async function callApi(url, options) {
    let response;
    try {
        response = await fetch(url, options);
    } catch (error) {
        throw new Error("Could not reach the server.");
    }

    const data = await response.json().catch(() => null);

    // Signed out (or the session ran out): go to the sign in page
    const onSignInPage = ["/login", "/register"].includes(window.location.pathname);
    if (response.status === 401 && !onSignInPage) {
        window.location.href = "/login";
        throw new Error("Please sign in.");
    }

    if (!response.ok) {
        // FastAPI puts the reason in "detail"
        const reason = data && typeof data.detail === "string" ? data.detail : "Please check the values and try again.";
        throw new Error(reason);
    }
    return data;
}

function sendJson(url, method, body) {
    return callApi(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
}

function formatDateTime(timestamp) {
    return new Date(timestamp).toLocaleString("en-IE", {
        day: "numeric",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function showMessage(element, text, isError) {
    element.textContent = text;
    element.classList.toggle("error", Boolean(isError));
}

function addCell(row, text, className) {
    const cell = row.insertCell();
    cell.textContent = text;
    if (className) {
        cell.className = className;
    }
}

function statusClass(status) {
    return "status " + status.toLowerCase();
}

// The "Sign out" link is only on the page when someone is signed in
const logoutLink = document.getElementById("logout-link");
if (logoutLink) {
    logoutLink.addEventListener("click", async (event) => {
        event.preventDefault();
        try {
            await sendJson("/api/auth/logout", "POST", {});
        } finally {
            window.location.href = "/login";
        }
    });
}
