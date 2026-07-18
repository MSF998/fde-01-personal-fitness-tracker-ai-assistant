function formatDuration(totalMinutes) {
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    if (hours && minutes) return `${hours}h ${minutes}m`;
    if (hours) return `${hours}h`;
    return `${minutes}m`;
}

let frequencyChart = null;
let durationChart = null;

function renderCharts(stats) {
    if (frequencyChart) frequencyChart.destroy();
    if (durationChart) durationChart.destroy();

    frequencyChart = new Chart(document.getElementById("frequency-chart"), {
        type: "bar",
        data: {
            labels: stats.workout_frequency.map((p) => p.period),
            datasets: [{ label: "Workouts", data: stats.workout_frequency.map((p) => p.count) }],
        },
    });

    durationChart = new Chart(document.getElementById("duration-chart"), {
        type: "line",
        data: {
            labels: stats.duration_trend.map((p) => p.period),
            datasets: [{ label: "Minutes", data: stats.duration_trend.map((p) => p.minutes) }],
        },
    });
}

const progressDataEl = document.getElementById("progress-data");
if (progressDataEl) {
    renderCharts(JSON.parse(progressDataEl.textContent));

    document.getElementById("range").addEventListener("change", async (event) => {
        const response = await fetch(`/api/progress?range=${event.target.value}`);
        if (!response.ok) return;
        const stats = await response.json();
        document.getElementById("total-workouts").textContent = stats.total_workouts;
        document.getElementById("total-duration").textContent = formatDuration(
            stats.total_duration_minutes
        );
        renderCharts(stats);
    });
}
