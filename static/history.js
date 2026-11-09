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

async function loadHistory() {
    const message = document.getElementById("page-message");
    try {
        levels = await callApi("/api/settings");
        readings = await callApi("/api/readings?hours=168");
        drawChart();
        showTable(readings);
        showMessage(message, "");
    } catch (error) {
        showMessage(message, error.message, true);
    }
}

loadHistory();
redrawOnResize(drawChart);
