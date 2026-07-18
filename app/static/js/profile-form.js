document.getElementById("profile-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    document.querySelectorAll(".error").forEach((el) => {
        el.textContent = "";
    });

    const form = event.target;
    const payload = {
        name: form.name.value,
        age: Number(form.age.value),
        fitness_goal: form.fitness_goal.value,
        height_cm: Number(form.height_cm.value),
        weight_kg: Number(form.weight_kg.value),
    };

    let response;
    try {
        response = await fetch("/api/profile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
    } catch (networkError) {
        document.querySelector('[data-error-for="_form"]').textContent =
            "Couldn't reach the server. Please try again.";
        return;
    }

    if (response.ok) {
        window.location.href = "/";
        return;
    }

    const body = await response.json();
    const fields = (body.error && body.error.fields) || {};
    if (Object.keys(fields).length === 0) {
        document.querySelector('[data-error-for="_form"]').textContent =
            (body.error && body.error.message) || "Something went wrong. Please try again.";
        return;
    }
    for (const [field, message] of Object.entries(fields)) {
        const el = document.querySelector(`[data-error-for="${field}"]`);
        if (el) el.textContent = message;
    }
});
