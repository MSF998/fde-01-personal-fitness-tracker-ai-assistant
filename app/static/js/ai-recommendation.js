function showAiRecoPanel(visiblePanelId) {
    ["ai-reco-request", "ai-reco-loading", "ai-reco-result", "ai-reco-error"].forEach((id) => {
        document.getElementById(id).hidden = id !== visiblePanelId;
    });
}

const aiRecoModal = document.getElementById("ai-recommendation-modal");
if (aiRecoModal) {
    const messageInput = document.getElementById("ai-message");

    async function requestRecommendation() {
        showAiRecoPanel("ai-reco-loading");

        let response;
        try {
            response = await fetch("/api/recommendation", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: messageInput.value || null }),
            });
        } catch (networkError) {
            showAiRecoPanel("ai-reco-error");
            return;
        }

        if (!response.ok) {
            showAiRecoPanel("ai-reco-error");
            return;
        }

        const body = await response.json();
        document.getElementById("ai-reco-text").textContent = body.recommendation;
        document.getElementById("ai-reco-guardrail-note").hidden = !body.guardrail_triggered;
        showAiRecoPanel("ai-reco-result");
    }

    document.getElementById("ai-reco-submit").addEventListener("click", requestRecommendation);
    document.getElementById("ai-reco-retry").addEventListener("click", requestRecommendation);

    document
        .querySelector('[data-modal-target="ai-recommendation-modal"]')
        .addEventListener("click", () => {
            messageInput.value = "";
            showAiRecoPanel("ai-reco-request");
        });
}
