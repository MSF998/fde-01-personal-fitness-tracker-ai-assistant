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
