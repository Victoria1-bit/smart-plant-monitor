// Lists every time the plant was watered.

async function loadWatering() {
    const message = document.getElementById("page-message");
    try {
        const events = await callApi("/api/watering");
        const body = document.getElementById("watering-table");
        body.innerHTML = "";

        for (const item of events) {
            const row = body.insertRow();
            addCell(row, formatDateTime(item.timestamp));
            addCell(row, item.trigger);
            addCell(row, item.seconds + " s");
            addCell(row, `${item.before}% to ${item.after}%`);
        }

        document.getElementById("watering-summary").textContent =
            events.length === 0 ? "The plant has not been watered yet." : `${events.length} waterings recorded.`;
    } catch (error) {
        showMessage(message, error.message, true);
    }
}

loadWatering();
