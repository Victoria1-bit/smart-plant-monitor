// Draws the soil moisture line chart as an SVG.

const SVG_NS = "http://www.w3.org/2000/svg";

function svgElement(name, attributes, parent) {
    const element = document.createElementNS(SVG_NS, name);
    for (const key in attributes) {
        element.setAttribute(key, attributes[key]);
    }
    parent.appendChild(element);
    return element;
}

function formatTick(time, spanHours) {
    const options = spanHours <= 48
        ? { hour: "2-digit", minute: "2-digit" }
        : { day: "numeric", month: "short" };
    return new Date(time).toLocaleString("en-IE", options);
}

function drawMoistureChart(container, readings, dryLevel, wetLevel) {
    container.innerHTML = "";

    if (readings.length < 2) {
        container.textContent = "Not enough readings to draw a chart.";
        return;
    }

    // The API sends newest first but the chart runs oldest to newest
    const points = readings
        .map((r) => ({ time: new Date(r.timestamp).getTime(), moisture: r.moisture, status: r.status }))
        .sort((a, b) => a.time - b.time);

    const width = Math.max(container.clientWidth, 280);
    const height = 260;
    const margin = { top: 12, right: 16, bottom: 28, left: 44 };
    const plotWidth = width - margin.left - margin.right;
    const plotHeight = height - margin.top - margin.bottom;

    const firstTime = points[0].time;
    const lastTime = points[points.length - 1].time;
    const x = (time) => margin.left + ((time - firstTime) / (lastTime - firstTime)) * plotWidth;
    const y = (moisture) => margin.top + ((100 - moisture) / 100) * plotHeight;

    const latest = points[points.length - 1];
    const svg = svgElement("svg", {
        width: width,
        height: height,
        viewBox: `0 0 ${width} ${height}`,
        role: "img",
        "aria-label": `Soil moisture over time. The latest reading is ${latest.moisture} percent.`,
    }, container);

    // Shaded areas for dry and wet soil, always named so colour is not the only clue
    svgElement("rect", { x: margin.left, y: y(dryLevel), width: plotWidth, height: y(0) - y(dryLevel), class: "band-dry" }, svg);
    svgElement("rect", { x: margin.left, y: y(100), width: plotWidth, height: y(wetLevel) - y(100), class: "band-wet" }, svg);
    svgElement("text", { x: margin.left + 8, y: y(dryLevel) + 16, class: "band-label" }, svg).textContent = "Dry";
    svgElement("text", { x: margin.left + 8, y: y(100) + 16, class: "band-label" }, svg).textContent = "Wet";

    // Moisture axis
    for (const tick of [0, 25, 50, 75, 100]) {
        svgElement("line", { x1: margin.left, x2: width - margin.right, y1: y(tick), y2: y(tick), class: "grid" }, svg);
        svgElement("text", { x: margin.left - 8, y: y(tick) + 4, "text-anchor": "end", class: "axis" }, svg).textContent = tick + "%";
    }

    // Time axis, with fewer labels on narrow screens
    const tickCount = width < 480 ? 3 : 5;
    const spanHours = (lastTime - firstTime) / 3600000;
    for (let i = 0; i < tickCount; i++) {
        const time = firstTime + ((lastTime - firstTime) * i) / (tickCount - 1);
        const anchor = i === 0 ? "start" : i === tickCount - 1 ? "end" : "middle";
        svgElement("text", { x: x(time), y: height - 8, "text-anchor": anchor, class: "axis" }, svg).textContent = formatTick(time, spanHours);
    }

    // The line itself
    const path = points.map((p, i) => `${i === 0 ? "M" : "L"}${x(p.time).toFixed(1)},${y(p.moisture).toFixed(1)}`).join(" ");
    svgElement("path", { d: path, class: "moisture-line" }, svg);

    // Mark and label only the latest reading
    svgElement("circle", { cx: x(latest.time), cy: y(latest.moisture), r: 5, class: "latest-point" }, svg);
    const labelAbove = latest.moisture < 85;
    svgElement("text", {
        x: x(latest.time) - 10,
        y: y(latest.moisture) + (labelAbove ? -10 : 22),
        "text-anchor": "end",
        class: "latest-label",
    }, svg).textContent = latest.moisture + "%";

    addChartHover(container, svg, points, x, y, margin.top, height - margin.bottom);
}

// Show the exact value of the nearest reading under the pointer
function addChartHover(container, svg, points, x, y, top, bottom) {
    const crosshair = svgElement("line", { y1: top, y2: bottom, class: "crosshair", visibility: "hidden" }, svg);
    const dot = svgElement("circle", { r: 5, class: "latest-point", visibility: "hidden" }, svg);
    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    tooltip.hidden = true;
    container.appendChild(tooltip);

    svg.addEventListener("pointermove", (event) => {
        const pointerX = event.clientX - svg.getBoundingClientRect().left;
        let nearest = points[0];
        for (const point of points) {
            if (Math.abs(x(point.time) - pointerX) < Math.abs(x(nearest.time) - pointerX)) {
                nearest = point;
            }
        }

        const nearestX = x(nearest.time);
        crosshair.setAttribute("x1", nearestX);
        crosshair.setAttribute("x2", nearestX);
        crosshair.setAttribute("visibility", "visible");
        dot.setAttribute("cx", nearestX);
        dot.setAttribute("cy", y(nearest.moisture));
        dot.setAttribute("visibility", "visible");

        tooltip.textContent = `${formatDateTime(nearest.time)}: ${nearest.moisture}% (${nearest.status})`;
        tooltip.hidden = false;
        const left = Math.min(nearestX + 10, container.clientWidth - tooltip.offsetWidth);
        tooltip.style.left = Math.max(0, left) + "px";
    });

    svg.addEventListener("pointerleave", () => {
        crosshair.setAttribute("visibility", "hidden");
        dot.setAttribute("visibility", "hidden");
        tooltip.hidden = true;
    });
}

// Draw the chart again when the window changes size
function redrawOnResize(draw) {
    let timer;
    window.addEventListener("resize", () => {
        clearTimeout(timer);
        timer = setTimeout(draw, 150);
    });
}
