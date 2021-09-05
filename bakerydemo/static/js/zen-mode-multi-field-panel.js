window.addEventListener("DOMContentLoaded", () => {
  const FULLSCREEN_ACTIVE = "fullscreen-active";
  const HIDDEN = "hidden";

  document.querySelectorAll(".zen-mode-panel").forEach((panel) => {
    const activateButton = panel.querySelector(".zen-mode.activate");
    const exitButton = panel.querySelector(".zen-mode.exit");

    // ---- Hide button & return early if fullscreen is not supported ---- //

    if (!panel.requestFullscreen) {
      return activateButton.classList.toggle(HIDDEN);
    }

    // ---- Add button event listeners ---- //

    activateButton.onclick = (event) => {
      event.preventDefault(); // ensure the button does not submit the form
      panel.requestFullscreen();
    };

    exitButton.onclick = (event) => {
      event.preventDefault(); // ensure the button does not submit the form
      document.exitFullscreen();
    };

    // ---- Add fullscreen event listener ---- //

    panel.onfullscreenchange = (event) => {
      panel.classList.toggle(FULLSCREEN_ACTIVE);
      activateButton.classList.toggle(HIDDEN);
      exitButton.classList.toggle(HIDDEN);
    };
  });
});
