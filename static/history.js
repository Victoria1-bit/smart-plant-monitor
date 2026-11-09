// Shows past readings as a chart and a table.

let readings = [];
let levels = null;

function drawChart() {
    if (levels) {
        drawMoistureChart(document.getElementById("chart"), readings, levels.dry_threshold, levels.wet_threshold);
    }
}

function showTable(rows) {
    const body = document.getElementById("history-table");
    body.innerHTML = "";
    for (const reading of rows) {
        const row = body.insertRow();
        addCell(row, formatDateTime(reading.timestamp));
        addCell(row, reading.moisture + "%");
        addCell(row, reading.status, statusClass(reading.status));
    }
}

function showSummary() {
    const values = readings.map((r) => r.moisture);
    const summary = document.getElementById("summary");
    if (values.length === 0) {
        summary.textContent = "No readings in this time range.";
        return;
    }
    const average = Math.round(values.reduce((total, value) => total + value, 0) / values.length);
    summary.textContent = `Lowest ${Math.min(...values)}%, highest ${Math.max(...values)}%, average ${average}%.`;
}

function filteredReadings() {
    const status = document.getElementById("status-filter").value;
    return status ? readings.filter((r) => r.status === status) : readings;
}

async function loadHistory() {
    const message = document.getElementById("page-message");
    try {
        levels = await callApi("/api/settings");
        const hours = document.getElementById("range").value;
        readings = await callApi(`/api/readings?hours=${hours}`);
        drawChart();
        showSummary();
        showTable(filteredReadings());
        showMessage(message, "");
    } catch (error) {
        showMessage(message, error.message, true);
    }
}

document.getElementById("range").addEventListener("change", loadHistory);
document.getElementById("status-filter").addEventListener("change", () => showTable(filteredReadings()));

loadHistory();
redrawOnResize(drawChart);
