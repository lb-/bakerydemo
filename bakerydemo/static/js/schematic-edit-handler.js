window.addEventListener("stimulus:init", ({ detail }) => {
  const Stimulus = detail.Stimulus;
  const Controller = detail.Controller;

  class SchematicEditHandler extends Controller {
    static targets = [
      "imageInput",
      "imagePoint",
      "imagePoints",
      "imagePointTemplate",
      "point",
    ];

    connect() {
      this.setupImageInputObserver();
      this.setupImageDropHandlers();
      this.updatePoints();
    }

    /**
     * Once a new point target (for each point within the inline panel) is connected
     * add an event listener to the delete button so we know when to re-update the points.
     *
     * @param {HTMLElement} element
     */
    pointTargetConnected(element) {
      const deletePointButton = element
        .closest("[data-inline-panel-child]")
        .querySelector('[id*="DELETE-button"]');

      deletePointButton.addEventListener("click", (event) => {
        this.updatePoints(event);
      });
    }

    /**
     * Allow the point to be dragged using the 'move' effect and set its data.
     *
     * @param {DragEvent} event
     */
    pointDragStart(event) {
      event.dataTransfer.dropEffect = "move";
      event.dataTransfer.setData("text/plain", event.target.dataset.id);
      event.target.style.opacity = "0.5";
    }

    /**
     * When dragging finishes on a point, reset its opacity.
     *
     * @param {DragEvent} event
     */
    pointDragEnd({ target }) {
      target.style.opacity = "1";
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
     * Once connected, set up the dragover and drop events on the preview image container.
     * We are unable to easily do this with `data-action` attributes in the template.
     */
    setupImageDropHandlers() {
      const previewImageContainer = this.imageInputTarget
        .closest(".field-content")
        .querySelector(".preview-image");

      previewImageContainer.addEventListener("dragover", (event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = "move";
      });

      previewImageContainer.addEventListener("drop", (event) => {
        event.preventDefault();

        const inputId = event.dataTransfer.getData("text/plain");
        const { height, width } = previewImageContainer.getBoundingClientRect();

        const xNumber = event.offsetX / width + Number.EPSILON;
        const x = Math.round(xNumber * 10000) / 100;
        const yNumber = 1 - event.offsetY / height + Number.EPSILON;
        const y = Math.round(yNumber * 10000) / 100;

        const inlinePanel = document
          .getElementById(inputId)
          .closest("[data-inline-panel-child]");

        inlinePanel.querySelector("[data-point-x]").value = x;
        inlinePanel.querySelector("[data-point-y]").value = y;

        this.updatePoints(event);
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

    /**
     * Removes the existing points shown and builds up a new list,
     * ensuring we do not add a point visually for any inline panel
     * items that have been deleted.
     */
    updatePoints() {
      if (this.hasImagePointsTarget) this.imagePointsTarget.remove();

      const template = this.imagePointTemplateTarget.content.firstElementChild;

      const points = this.pointTargets
        .reduce((points, element) => {
          const inlinePanel = element.closest("[data-inline-panel-child]");
          const isDeleted = inlinePanel.matches(".deleted");

          if (isDeleted) return points;

          return points.concat({
            id: inlinePanel.querySelector("[id$='-id']").id,
            label: element.querySelector("[data-point-label]").value,
            x: Number(element.querySelector("[data-point-x]").value),
            y: Number(element.querySelector("[data-point-y]").value),
          });
        }, [])
        .map(({ id, x, y, label }) => {
          const point = template.cloneNode(true);
          point.dataset.id = id;
          point.querySelector(".label").innerText = label;
          point.style.bottom = `${y}%`;
          point.style.left = `${x}%`;
          return point;
        });

      const newPoints = document.createElement("ol");
      newPoints.classList.add("points");
      newPoints.dataset.schematicEditHandlerTarget = "imagePoints";

      points.forEach((point) => {
        newPoints.appendChild(point);
      });

      this.imageInputTarget
        .closest(".field-content")
        .querySelector(".preview-image")
        .appendChild(newPoints);
    }
  }

  // register the above controller
  Stimulus.register("schematic-edit-handler", SchematicEditHandler);
});
