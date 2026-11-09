// Fills in the dashboard from the API.

let chartReadings = [];
let chartLevels = null;

function drawChart() {
    if (chartLevels) {
        drawMoistureChart(document.getElementById("chart"), chartReadings, chartLevels.dry_threshold, chartLevels.wet_threshold);
    }
}

function showCurrent(data) {
    const reading = data.reading;
    document.getElementById("moisture").textContent = reading.moisture;

    const status = document.getElementById("status");
    status.textContent = reading.status;
    status.className = statusClass(reading.status);

    document.getElementById("last-reading").textContent = formatDateTime(reading.timestamp);

    const levels = data.settings;
    document.getElementById("levels-note").textContent =
        `Dry is below ${levels.dry_threshold}%, wet is above ${levels.wet_threshold}%.`;
}

function showRecent(readings) {
    const body = document.getElementById("recent-readings");
    body.innerHTML = "";
    for (const reading of readings) {
        const row = body.insertRow();
        addCell(row, formatDateTime(reading.timestamp));
        addCell(row, reading.moisture + "%");
        addCell(row, reading.status, statusClass(reading.status));
    }
}

async function loadDashboard() {
    const message = document.getElementById("page-message");
    try {
        const data = await callApi("/api/status");
        const readings = await callApi("/api/readings?limit=10");
        chartReadings = await callApi("/api/readings?hours=24");
        chartLevels = data.settings;
        showCurrent(data);
        showRecent(readings);
        drawChart();
        showMessage(message, "");
    } catch (error) {
        showMessage(message, error.message, true);
    }
}

loadDashboard();

// Keep the page up to date without reloading it
setInterval(loadDashboard, 10000);
redrawOnResize(drawChart);
