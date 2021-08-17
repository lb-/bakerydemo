(() => {
  /* 1. set up buttons for each possible state (first, last, only) of a step */

  const nextButton = {
    action() {
      return this.next();
    },
    classes: "button",
    text: "Next",
  };

  const backButton = {
    action() {
      return this.back();
    },
    classes: "button button-secondary",
    secondary: true,
    text: "Back",
  };

  const doneButton = {
    action() {
      return this.next();
    },
    classes: "button",
    text: "Done",
  };

  /* 2. create a function that will maybe return an object with the buttons */

  const getButtons = ({ index, length }) => {
    if (length <= 1) return { buttons: [doneButton] }; // only a single step, no back needed
    if (index === 0) return { buttons: [nextButton] }; // first
    if (index === length - 1) return { buttons: [backButton, doneButton] }; // last
    return {};
  };

  /* 3. prepare the default step options */

  const defaultButtons = [backButton, nextButton];

  const defaultStepOptions = {
    arrow: false,
    buttons: defaultButtons,
    cancelIcon: { enabled: true },
    canClickTarget: false,
    scrollTo: { behavior: "smooth", block: "center" },
  };

  /* 4. once the DOM is loaded, find all the elements with the data-help attribute
     - for each of these elements attempt to parse the JSON into steps and title
     - if we find steps then initiate a `Shepherd` tour with those steps
     - finally, attach a click listener to the link so that the link will trigger the tour
   */

  window.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".help-available[data-help]");

    // if no links found with data-help - return
    if (!links || links.length === 0) return;

    links.forEach((link) => {
      const data = link.dataset.help;

      // if data on data-help attribute is empty or missing, do not attempt to parse
      if (!data) return;

      const { steps = [], title } = JSON.parse(data);

      const tour = new Shepherd.Tour({
        defaultStepOptions,
        steps: steps.map(({ element, ...step }, index) => ({
          ...step,
          ...(element ? { attachTo: { element } } : {}),
          ...getButtons({ index, length: steps.length }),
        })),
        tourName: title,
        useModalOverlay: true,
      });

      link &&
        link.addEventListener("click", (event) => {
          event.preventDefault();
          tour.start();
        });
    });
  });
})();
