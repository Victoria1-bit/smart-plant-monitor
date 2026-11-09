// Helpers used by every page.

async function callApi(url, options) {
    let response;
    try {
        response = await fetch(url, options);
    } catch (error) {
        throw new Error("Could not reach the server.");
    }

    const data = await response.json().catch(() => null);
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
