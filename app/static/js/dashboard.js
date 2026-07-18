document.querySelectorAll("[data-modal-target]").forEach((trigger) => {
    trigger.addEventListener("click", () => {
        document.getElementById(trigger.dataset.modalTarget).showModal();
    });
});

document.querySelectorAll("[data-modal-close]").forEach((closeBtn) => {
    closeBtn.addEventListener("click", () => {
        closeBtn.closest("dialog").close();
    });
});

async function refreshRecentActivity() {
    const response = await fetch("/api/workouts");
    if (!response.ok) return;
    const body = await response.json();
    const recent = body.workouts.slice(0, 5);

    const container = document.getElementById("recent-activity");
    container.innerHTML = "";

    if (recent.length === 0) {
        const empty = document.createElement("p");
        empty.textContent = "No workouts logged yet.";
        container.appendChild(empty);
        return;
    }

    const list = document.createElement("ul");
    list.className = "activity-list";
    for (const workout of recent) {
        const item = document.createElement("li");
        item.textContent = `${workout.type} · ${workout.duration_minutes} min · felt ${workout.feeling}`;
        list.appendChild(item);
    }
    container.appendChild(list);
}

const logWorkoutForm = document.getElementById("log-workout-form");
if (logWorkoutForm) {
    logWorkoutForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        logWorkoutForm.querySelectorAll(".error").forEach((el) => {
            el.textContent = "";
        });

        const form = event.target;
        const payload = {
            type: form.type.value,
            duration_minutes: Number(form.duration_minutes.value),
            feeling: form.feeling.value,
        };

        let response;
        try {
            response = await fetch("/api/workouts", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
        } catch (networkError) {
            logWorkoutForm.querySelector('[data-error-for="_form"]').textContent =
                "Couldn't reach the server. Please try again.";
            return;
        }

        if (response.ok) {
            form.reset();
            document.getElementById("log-workout-modal").close();
            await refreshRecentActivity();
            return;
        }

        const body = await response.json();
        const fields = (body.error && body.error.fields) || {};
        if (Object.keys(fields).length === 0) {
            logWorkoutForm.querySelector('[data-error-for="_form"]').textContent =
                (body.error && body.error.message) || "Something went wrong. Please try again.";
            return;
        }
        for (const [field, message] of Object.entries(fields)) {
            const el = logWorkoutForm.querySelector(`[data-error-for="${field}"]`);
            if (el) el.textContent = message;
        }
    });
}
