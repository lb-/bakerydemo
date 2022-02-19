window.addEventListener("stimulus:init", ({ detail }) => {
  const Stimulus = detail.Stimulus;
  const Controller = detail.Controller;

  class SchematicEditHandler extends Controller {
    static targets = ["imageInput"];

    connect() {
      this.setupImageInputObserver();
    }

    /**
     * Once connected, use DOMMutationObserver to 'listen' to the image chooser's input.
     * We are unable to use 'change' event as it is updated by JS programmatically
     * and we cannot easily listen to the Bootstrap modal close as it uses jQuery events.
     */
    setupImageInputObserver() {
      const imageInput = this.imageInputTarget;

      const observer = new MutationObserver((mutations) => {
        const { oldValue = "" } = mutations[0] || {};
        const newValue = imageInput.value;
        if (newValue && oldValue !== newValue)
          this.updateImage(newValue, oldValue);
      });

      observer.observe(imageInput, {
        attributeFilter: ["value"],
        attributeOldValue: true,
        attributes: true,
      });
    }

    /**
     * Once we know the image has changed to a new one (not just cleared)
     * we use the Wagtail API to find the original image URL so that a more
     * accurate preview image can be updated.
     *
     * @param {String} newValue
     */
    updateImage(newValue) {
      const image = this.imageInputTarget
        .closest(".field-content")
        .querySelector(".preview-image img");

      fetch(`/api/v2/images/${newValue}/`)
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`HTTP error! Status: ${response.status}`);
        })
        .then(({ meta }) => {
          image.setAttribute("src", meta.download_url);
        })
        .catch((e) => {
          throw e;
        });
    }
  }

  // register the above controller
  Stimulus.register("schematic-edit-handler", SchematicEditHandler);
});
