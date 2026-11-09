// Loads and saves the watering settings.

const NUMBER_FIELDS = ["dry_threshold", "wet_threshold", "water_seconds", "cooldown_minutes"];
const form = document.getElementById("settings-form");
const message = document.getElementById("settings-message");

async function loadSettings() {
    try {
        const settings = await callApi("/api/settings");
        for (const field of NUMBER_FIELDS) {
            document.getElementById(field).value = settings[field];
        }
        document.getElementById("auto_water").checked = settings.auto_water;
    } catch (error) {
        showMessage(message, error.message, true);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const values = { auto_water: document.getElementById("auto_water").checked };
    for (const field of NUMBER_FIELDS) {
        values[field] = Number(document.getElementById(field).value);
    }

    if (values.dry_threshold >= values.wet_threshold) {
        showMessage(message, "The dry level must be lower than the wet level.", true);
        return;
    }

    try {
        await sendJson("/api/settings", "PUT", values);
        showMessage(message, "Settings saved.");
    } catch (error) {
        showMessage(message, error.message, true);
    }
});

loadSettings();
