# Lightweight JavaScript Framework

The Wagtail core team are investigating other frontend frameworks as part of the work to resolve the [UI Technical Debt](https://github.com/wagtail/wagtail/discussions/7689), and with the upcoming [Page Editor enhancements](https://github.com/wagtail/wagtail/discussions/7739).

## Goals

The purpose of this document is to investigate what existing lightweight frontend frameworks could be used in Wagtail.

We want to to see what may suitable for the middle ground of interactivity where React may not be an ideal option. We want to make it easy for those building Wagtail and building with Wagtail to think in HTML first (leveraging Django) but make a great experience for those editing width Wagtail.

A look at where our goals for this library align with our Wagtail vision pillars.

- First thirty minutes of Wagtail
  - It should be easier to find out how to implement a custom thing
- Editors, get your best work done
  - Interactive content - interaction (reactivity) should be easy to build and reason about.
  - Less bugs - the library should make it hard to break other 'parts' (e.g. when React errors, the whole component tree errors).
  - Accessibility - it should be easy to use existing accessibility approaches or add them to components.
- Sophistication without compromising simplicity
  - HTML first - Where possible, Django land first and JavaScript land second, it should be easy to to basic things (use, modify initial data, change some behaviour/classes) in templates alone. Ideally we want to avoid ALL JS code when it is just 'init something' type code and not rely on hard-coded classes for visible functionality.
  - Extend all the things - Let Wagtail developers enhance/extend as much as possible (even if not documented).
- Wagtail as a platform
  - Namespaced - Wagtail implementations should be namespaced or somehow isolated from other potential duplicate usage of the same libraries
  - Building blocks - Provide the right building blocks at the right abstractions, remembering there is a spectrum between rendering a submit button through to the Draftail editor.
  - Development - It should be super productive for developers to work on and contribute to Wagtail core (including writing unit tests).
- Multi-channel experiences
  - i18n/l10n - It should be easy to provide translated / localised content to the elements without additional thought.
  - Can we use these 'components' outside the Wagtail admin easily?
  - CSP compliance, remember not all instances of Wagtail activate this but we aim to support it.

## Additional context

- Throughout 2022, Wagtail will be releasing a major UI overhaul of the user interface and features in Wagtail’s page editor.
- React is an incredible library but better serves situations where the full control of the DOM branch is given to React, DOM rendering is 'given over' to JavaScript and Django templates cannot be leveraged (easily) to change what is inside those DOM elements.
- jQuery has served a great purpose, providing easy DOM traversal and manipulation, however it is becoming a bottleneck for new features and modern DOM APIs are sufficient and jQuery does not solve the problem of making it easy to write consistent code (component state). Additional to this we end up having to a lot of 'initialising' of elements whenever added to the DOM by other means (other JS or maybe async HTML).

### Assumptions

- **Not in scope** - Component library (e.g. modals/tooltips etc), it is assumed that discussion will be separate. Components will be implemented or adopted using whatever framework is selected.
- Modern JS (non-IE11), support for ES6 classes, custom events can be assumed (with some polyfills required).

## Why not React all the things?

### Where React fits

- React is a different paradigm to HTML with JS, instead it reverses the world as JS first and foremost (JSX is just JS under the hood).
- React is an incredible solution high complexity, large state, components with a high level of interactivity (e.g. Draftail editor).
- React components are great for a self-contained component, owning its own state where the DOM structure is contained 100% in React.
- React provides a consistent approach to one way data flow that helps for testing and development.

### Why React is not a catch all solution

- React elements need to be initialised for any DOM to be added to the browser, the HTML it produces does not exist until React builds it.
- Harder to 'replace' an implementation with an extended one, while some React components may be class based components that could be extended there is no central and consistent way to provide this 'API'.
- Not possible to 'dig in' and modify some data (props) that is used.
- Not possible to use HTML provided by the server in any meaningful way, if you wanted to leverage any of the existing Django ecosystem like templating, custom form widgets, template includes for somewhere 'inside' the React component it is just not possible.
- A specific API must be exposed to customise behaviour, and if you want this data from the server we need to reach for something like Telepath to do it.
- React takes over the whole tree it controls, so everything down the tree must also be React which means reimplementing everything in React and non-React. While it is possible to add a DOM element and attach something to it (like a jQuery initialisation) it is not idea.
- It is not practical to output Django server rendered HTML inside a React element, Telepath provides a nice abstraction for data though.
- A good example of the current situation is the new Wagtail admin sidebar, the code was written in 2021 and will become the default in Wagtail 2.16. This has been built in React which means the support to provide [HTML and any additional JavaScript on the menu items has had to be deprecated](https://github.com/wagtail/wagtail/blob/main/docs/releases/2.16.md#deprecated-sidebar-capabilities). The Wagtail team are forced to decide between writing new UI components in jQuery, ad-hoc JS or React and React makes sense in those options but we lose so much flexibility that pure HTML with 'sprinkles of JS provides. This also leads to a situation where the main editor is no longer part of the HTML provided, it is not in the DOM until JS loads and adds it creating a less than ideal experience for our editors on slower browsers. See Use Case 9 for more details.

### A guide of when to use React or not

- The [rule of least power](https://www.w3.org/2001/tag/doc/leastPower.html) is a nice way to think of this, solve the solution in the simplest tool first.
- It would be good for Wagtail to decide and document this, but it could be 'use the lightweight approach until you cannot'.
- Alternatively few|complex vs many|simple, if there is likely to be FEW instances of the component (or one) and it is also quite complex it should be React, if there going to be many of the thing and the behaviour is simple it should be the lightweight approach.

## Leverage existing abstractions

We want to ensure that anything we adopt, not only works with the existing abstractions but does not replace them and ideally makes the existing approaches work better.

- [Wagtail Template Components](https://docs.wagtail.io/en/stable/extending/template_components.html)
  - Mostly HTML, but `media` can be added, provides a Wagtail wide abstraction for 'things that output html', similar to Django Widgets.
  - Note: Maybe we should call this something else one way (Gadget?) as the term Component is quite overloaded.
- [Telepath](https://wagtail.github.io/telepath/)
  - Provides a way to compile server side logic/data and send to the client as JSON and then provides a JS registration of how to 'render' the output.
  - Note: This is the area that could the conflict most with any lightweight framework, however there could be a consistent approach built.
- [Exposed React components](https://docs.wagtail.io/en/stable/advanced_topics/customisation/admin_templates.html#extending-clientside-components)
  - Mostly Draftail parts, includes Icon
  - Probably will not conflict with a new lightweight framework decision but good to be aware of.
- StructBlock & StreamField
  - https://docs.wagtail.io/en/stable/reference/streamfield/widget_api.html
  - https://docs.wagtail.io/en/stable/advanced_topics/customisation/streamfield_blocks.html#additional-javascript-on-structblock-forms
  - This is really an extension of the Telepath approach but should also be considered.

## Comparison of lightweight frameworks / libraries

- **[jQuery](https://jquery.com/)** (in use - deprecation planned)
  - CSP - Needs to be written correctly to compatible.
  - Composing & Extending - Hard to make one 'element' do two things, not possible to extend existing jQuery logic, most often must be copied/pasted or add duplicate event listeners to add logic.
  - Development - Simple,
  - Initialisation - Each jQuery instance needs to be initialised manually.
  - State & Reactivity - ad-hoc, normally not accessible outside the element, sometimes state is stored on data attributes, needs to be managed individually.
- **[Alpine.js](https://alpinejs.dev/)** 19.6k stars
  - Composing & Extending - Not simple to [register additional components outside of the initialisation](https://alpinejs.dev/globals/alpine-data#registering-from-a-bundle), components can be composed but cannot do more than one 'thing', not really possible to extend existing registered components without specific APIs built.
  - CSP - Not compatible, there is away to 'ignore' a branch of a DOM tree to not allow Alpine to read those elements. There is a planned [CSP compatible build](https://alpinejs.dev/advanced/csp), however this is [not yet released and no timeline available](https://github.com/alpinejs/alpine/issues/237#issuecomment-999692410), the CSP build lacks all the functionality of the `x-` attributes though and 100% relies on classes.
  - Development - Mostly uses functions, not classes.
  - Initialisation - Initialises when added to the DOM, either on first render or after, however does not 'disconnect' when `x-data` is removed from the DOM element.
  - Links - [When to use Alpine](https://lightit.io/blog/when-to-use-alpine-js/), [HTMX & Alpine in Django](https://www.saaspegasus.com/guides/modern-javascript-for-django-developers/htmx-alpine/), [Alpine speed issues](https://github.com/alpinejs/alpine/issues/566)
  - Platform - No way to namespace the HTML attributes but the data name can be prefixed by convention, potential for accidental conflicts with external libraries using Alpine.
  - State & Reactivity - `data` object that is initialised and then self-contained in the component, not accessible outside, uses vue's reactivity model under the hood.
- **[Stimulus](stimulus.hotwired.dev/)** 11.1k stars
  - Composing & Extending - Global object can be used to add additional registered items, even replace and extend existing behaviour with class inheritance, behaviour can be composed and also multiple controllers can be put on the one element (e.g. a modal trigger that also has a keyboard shortcut behaviour).
  - CSP - Compatible, although not explicitly stated in the documentation, See discussion [Security, CSP, and Stimulus](https://discuss.hotwired.dev/t/security-csp-and-stimulus/171).
  - Development - Uses [ES6 classes](https://caniuse.com/es6-class), although in theory it could work with function expressions, has a debug mode for local development.
  - Initialisation - Initialises when added to the DOM, either on first render or after, does 'disconnect' when `data-controller` is removed from the DOM element.
  - Links - [Alpine vs Stimulus JS](https://brianschiller.com/blog/2021/11/05/alpine-stimulus-js) - recommends Stimulus but does not address CSP concern, + see Stimulus Resources below.
  - Platform - Allows for a [custom namespaced set of data attributes](https://stimulus.hotwired.dev/handbook/installing#overriding-attribute-defaults) (e.g. `data-controller` could become `data-wg-controller`) creating zero conflicts with any other additional usage of Stimulus, which means the controller names can be simple. For example, we can use `data-wg-controller='modal'` instead of `data-controller='wg-modal'` everywhere, we may not need to namespace the action/target attributes.
  - State/Reactivity - Data attributes, uses DOM mutation observer for reactivity, controller class methods available for each 'value' when changed (including previous value).
- **[Web Components (Catalyst)](https://github.github.io/catalyst/)** ~1k stars
  - Composing & Extending - Components can be composed with non-web element ones and with other web elements, dev tooling likely required to 'extend' an existing component, behaviour cannot be composed together in the one element at the HTML level. Inspired by Stimulus so very similar in goals and API, except that it is a web components approach, although not as much adoption.
  - CSP - Unclear, but cannot see anything that would indicate this being an issue.
  - Initialisation - As the components are just DOM components, no initialisation required for each element.
  - Links - [Anti-patterns - great guide for naming things even if we go with Stimulus](https://github.github.io/catalyst/guide/anti-patterns/)
  - Platform - Compiled components get added to a registry of web components available in the UI and should not conflict if a suitable naming convention is used.
  - State/Reactivity - Recommends that state be stored on the DOM as attributes, this means that just HTML can be used for the initial state, can be changed by external code and `attributeChangedCallback` can be used to listen to these changes.
- **[Web Components (Lit)](https://lit.dev/)** 10.1k stars
  - Composing & Extending - Components can be composed with non-web element ones and with other web elements, dev tooling likely required to 'extend' an existing component, behaviour cannot be composed together in the one element.
  - CSP - Unclear, there is an ongoing discussion about the [ShadowDOM and usage of `innerHTML`](https://github.com/google/WebFundamentals/issues/8817)
  - Development - Web components, Shadow DOM, Typescript (in docs but not required), Decorators, build tool recommended.
  - Initialisation - As the components are just DOM components, no initialisation required for each element.
  - Links - [The problem with web components](https://adamsilver.io/blog/the-problem-with-web-components/)
  - Platform - Compiled web components should be isolated and can be prefixed (e.g wg-modal), so it should not conflict if others also use their own web components.
  - State/Reactivity - [Reactive properties](https://lit.dev/docs/components/properties/) approach, contained within the Class and not accessible outside, can be 'synced' with attributes on the component though.
- **Excluded**
  - [HTMX](https://htmx.org/) - This library provides a way to patch in server side provided HTML to parts of the DOM, useful but does not serve the purpose of the lightweight frontend framework. Also, this library is very hard to google. It is more of a compliment to lightweight frameworks instead of a replacement.
  - [min.js](https://github.com/remy/min.js) - DOM traversal and manipulation library, akin to jQuery, nice but we may end up with the same ad-hoc approach as the current jQuery code, not really maintained.
  - [Trimmings](https://postlight.github.io/trimmings/) - Looks promising, kind of a mix between Alpine and HTMX, however it is still quite new and does not seem to provide much extensibility.
  - [UmbrellaJS](https://umbrellajs.com/) - DOM traversal and manipulation library, akin to jQuery, maintained but not what we are looking for.
  - [Unpoly](https://unpoly.com/) - This looks interesting but it seems to be a whole solution for managing server side and client data interaction/rendering, we already have Telepath.

### The case for Stimulus JS

- No matter what, we still need to write some JS to get the behaviour working, even with Alpine.js (due to the CSP build approach), so the focus should be on providing a consistent approach to building this that makes it easy for HTML to still be the first class citizen.
- Classses can be abstracted so that it is easy to separate the behaviour of an element from the classes that get added/removed (e.g. collapse element could be used but with `.my-custom-collapsed-class` defined), default classes can be set up if not provided also.
- Allows for default variables, so that data can be supplied as needed.
- Allows for the target elements to be changed (e.g. you could write the expanded formset in a way that the 'add' button is elsewhere in the DOM, or maybe there are two add buttons, with HTML only).
- Stimulus Controllers are not really components but more a 'chunk of behaviour' and as such it is a pretty powerful way to split out JS behaviour.
- Everything is based on data attributes, which we already use for many of our existing components such as finding nodes for sidebar/draftail and finding nodes for dropdown, plus some values are already read from data attributes (e.g. chooser modal), the exact attributes will change but it is not a stretch for all of these usages to be used by Stimulus.
- This means that if some customised version wants to opt-out of some behaviour, all they need to do is either remove the `data-controller` attribute (e.g. maybe on an Django field widget OR just one line of JavaScript) and that element will be disconnected (or never connect) from Stimulus and not do anything. Remember - it is not easy to remove event listeners with JS, but it is easy to change a data attribute.
- Even the mounting of React components could leverage Stimulus, providing a simple way to initialise various DOM elements with their React injection, with some of the props being supplied to the component as data attributes... which can even trigger a re-render if the data-attributes change from some other JS.
- Stimulus JS is modest, it does not try to solve everything (no animations), DOM manipulations still need to be written in JS for example.
- As the state is stored on the data attributes, any other code can modify these attributes to change the behaviour (for example, want to close all collapsibles, just change `data-collapsible-collapsed-value` to false with any JS and it will work), this means that Django templates can be used extensively for 'initial' data without having to write any init JS functions.
- This library is a core part of the Rails ecosystem and built by the team at Basecamp, it is unlikely to go anywhere anytime soon.

#### Further notes

- We can avoid a lot of global functions populating Window (e.g. `window.LockUnlockAction`) by adopting Stimulus.
- We may want to implement something similar to [Alpine.js `x-cloak` directive](https://alpinejs.dev/directives/cloak), this is quite useful when you want to wait for the JS to trigger before showing some content.
- We may want to move to `template` elements instead of `script` for template content (e.g. expanding formset), not critical but a nicer modern approach.

#### Case against Stimulus JS

- **Risk** Telepath integration needs to be considered, we want to avoid having both a Telepath adapter and a Controller, we need to see how these can work together nicely.
  - Ideally the Telepath adapter keeps minimal and the 'work' is kept in the Controller and all the Telepath JS code does it convert the provided args to their relevant data attribute values and just puts something in the DOM for Stimulus to work with.
  - Worst case - this is no different to now, we still init some elements in pure JS, however we need to review approaches we can take.
  - Maybe the Telepath 'render' method can just output the HTML with the spread data attributes and the work is always done in the Controller. Maybe one class can serve both purposes (`render` is not used by Stimulus), we would have to be careful with `this` as there would be the Telepath instance AND the Stimulus instance I guess.
- Relies ES6 classes, may not able to be compiled down to ES5, so our bundle will need to move to ES6 (2015) - https://stimulus.hotwired.dev/handbook/installing#browser-support. https://caniuse.com/?search=es6
- Using with Typescript will work but it is a bit verbose, see resources section, maybe we can somehow create a WagtailBaseController that is smart about this?
- There is no official approach to testing in the documentation, however there are resources online and it appears to be possible to set up in Jest without too many issues.
- Web components may be the way to go, but this moves us more away from a light touch approach and it will be harder to tell where the lines stop between this and React, maybe if we were scrapping React?
- It is still just JavaScript and buggy or inconsistent code can be written, but we will have a base of a consistent class based approach for everything, instead of ad-hoc approaches.
- There are solutions for writing Jest test online but none are part of the official docs (note: Alpine js also has no testing guidelines), but it is possible to write tests for.
- [Recent 3.0](https://world.hey.com/hotwired/stimulus-3-c438d432) did have some breaking changes so some online docs are out of date (however, this is similar for Alpine js v1/v2 and lit.dev vs Polymer), welcome to the JavaScript ecosystem.

#### Resources

- [Stimulus 2.0 - HN comments](https://news.ycombinator.com/item?id=25305467) - the good, bad and ugly feedback
- [Official Stimulus discussion board](https://discuss.hotwired.dev/)
- [Blog - Intro to Stimulus](https://www.smashingmagazine.com/2020/07/introduction-stimulusjs/)
- [Awesome Stimulus JS](https://github.com/skatkov/awesome-stimulusjs)
- [Full Library of Stimulus controllers](https://sub-xaero.github.io/stimulus-library/docs) - great example of a BaseController / Typescript usage but no unit tests it seems, We may not want to use this library but it is a good reference.
- [Better Stimulus](https://www.betterstimulus.com/) - a set of resources (similar to awesome list) + best practices/recommendations.
- [Podcast - Changelog - Stimulus JS](https://changelog.com/podcast/286)
- **Testing**
  - https://github.com/hotwired/stimulus/issues/130
  - https://discuss.hotwired.dev/t/testing-stimulus/90/8
  - https://shime.sh/til/testing-stimulus
- **Typescript**
  - https://dieterlunn.ca/stimulus-and-typescript/
  - https://github.com/hotwired/stimulus/issues/221
  - [targets and typescript · Issue #121 · hotwired/stimulus](https://github.com/hotwired/stimulus/issues/121)
  - https://www.sourlemon.co.za/blog/rails-typescript-and-stimulus/

#### Potential architecture

- Wagtail core code would likely use the recommended [Webpack build system approach](https://stimulus.hotwired.dev/handbook/installing#using-webpack-helpers) and controller file naming conventions so that we do not need to manually load each new controller added to the Wagtail admin. This assumes we want all controllers on all page, I think this is a good assumption to make but it does add to the base JS load.
- On every admin page, the Stimulus code is loaded with the default controllers added and an event `wagtail:stimulus-init` would be fired that other code could hook into. See https://github.com/lb-/bakerydemo/blob/ui-experiments/bakerydemo/ui/wagtail_hooks.py
- We could also add handling of the [debug flag](https://stimulus.hotwired.dev/handbook/installing#debugging) to be true when Django is in local dev mode, this will aid those customising Wagtail and also those working on Wagtail core.
- If custom controllers are added (or overriding existing ones), they can leverage this event and also know that when this event fires the `Stimulus` and `Controller` global will be available.
- We may want to put these behind a global object like `wagtail.stimulus.Stimulus` for example - so we do not populate the global object AND it allows other customisations where another Stimulus application exists in isolation of the Wagtail one.
- We may want to actually define a prefix for all controllers (e.g. wg-loading-button) instead of a prefix for the data attributes as the controller name is used by default for prefixing the events on dispatch. Further investigation needed to see if this behaviour can be changed. Alternatively if we have a `WagtailBaseController` it could extend this method and modify this behaviour to prefix all events with `wagtail:` so an event dispatched from a collapsible controller would be something like `wagtail:collapsible:close`.
- We can even render Stimulus controlled elements via React, there are some edge cases we need to be aware of, and I doubt this will work when the controller also renders a new React element on the inner controlled one but it may open an avenue to avoid re-doing all the same components in React and non-React. Note: When react modifies the inner content of an element and the Stimulus controller also does this, the next re-render will take priority but the first render (with the adding of the controlled element) will be handled by Stimulus, this can be avoided if needed by putting a unique key on the controlled element when we know we want Stimulus to 'take over' again.

## Stimulus use cases

### Use Case 1 - Collapsible

- client/src/entrypoints/admin/collapsible.js
- It may be preferred we provide a styled variant of the [`details`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details) element instead of coding this at all.
- However, our existing collapsible code has some custom event firing (for comments) and this would still require some kind of JS code written and initialised.

## Use Case 2 - Upgrade Notification

- client/src/components/UpgradeNotification/index.js
- See working on Wagtail code example here https://github.com/wagtail/wagtail/compare/385a0aee67a6730553be6581fdf3898f132f2d6d...lb-:ui-experiments?expand=1
- Note: IE 11 support dropped in the commit & tsconfig to ES2015 required to run (which produces some Webpack errors to work through)
- This is a great example of a simple component that requires some basic initial data from the rendered HTML and does something from it on page load
- The HTML was already using data attributes to identify the element, target the 'values' to replace with teh resolved content and provide the initial 'current version'
- Stimulus really shines here as it provides a consistent approach to this very common behaviour, and porting over to Stimulus actually makes the functionality easier to follow
- Along with this we do not have to keep 'initing' this with additional manual code here client/src/entrypoints/admin/wagtailadmin.js - as Stimulus does this for us

### Use Case 3 - Long Running Button

- client/src/entrypoints/admin/core.js (see button.button-longrunning usage)
- Some modifications would be needed initially so there is less reliance on classes by default (to hide the spinner)
- But this would be a great candidate for Stimulus
- Something like `- <button data-controller="loading-button" data-action="loading-button#start">label</button>` would cover most cases, with the ability to define the fallback re-enable after as a data value, along with the loading text label etc.
- Also the 'stop' or 'cancel' could be handled with lots of flexibility by the HTML to implement.
- In the below HTML you can see we are using the same button with multiple controllers, start a new request, reset the existing data from the previous request AND start the loading indicator - all on click.
- Then there is an extra action that will stop the loading state when the document receives an event `request:response`
- We can further scope the trigger of the stop via the 'stop-selector-value' (just an idea, might be a nicer way).
- This shows off the power of the multiple controllers, we do not need to duplicate the 'disable a button and add a spinner' in each and every case, and we get a lot of power out of the data attributes.
- Note: The actual implementation may be a bit more abstracted into a generic 'container loading thing' and then have one that extends that for buttons.

```
        <button
            class="button button-small"
            data-action="request#fetch activity#reset loading-button#start request:response@document->loading-button#stop"
            data-controller="loading-button"
            data-loading-button-clicked-text-value="Loading..."
            data-loading-button-stop-after-value="30000"
            data-loading-button-stop-selector-value=".find-an-activity"
            type="button"
        >
            Find something to do
        </button>
```

### Use Case 4 - Locking Action Button

- client/src/entrypoints/admin/lock-unlock-action.js
- Current approach is to provide a global `LockUnlockAction` that accepts a `csrfToken` and a `next`, when called it will traverse the DOM for any `data-locking-action` to set up event listeners.
- This creates an issue where the csrf token needs to be provided to the JS somehow, which means it must be templated JS and this has caused Wagtail bugs where it has been missed or not correctly escaped.
- Could be replaced with `<button data-controller='page-lock' data-page-lock-csrf-value="{% csrf_token %}" data-page-lock-action-value="{% url 'wagtailadmin_pages:unlock' page.id %}" data-page-lock-next-url-value="{% some_url %}" class="button button-small button-secondary">{% trans "Unlock" %}</button>`
- The Controller would almost be a cut & paste of the existing lock-unlock-action.js, creating a form element and posting to it but with a consistent approach.
- As noted above, if we wanted this button to do two things e.g. lock the page and also be able to be triggered by a keyboard shortcut, we could do this with two discrete controllers and then `<button data-controller='page-lock keyboard-shortcut' ...`.

### Use Case 5 - Dropdown

- client/src/entrypoints/admin/core.js (see `DropDown` function).
- Current approach is to init this on load if there is a `data-dropdown`, there is code to throw an error if there is also not a `DropDownController` provided. Stimulus handles this scenario out of the box, when you attempt to access a target that does not exist you get a nicely formatted error.
- Outside click would need to be implemented, but it would be possible to abstract these behaviours with shared base classes.
- The nice thing that Stimulus would provide here is that the state of (open/closed) would be on the element in the data attributes, which means you can render a 'default open' dropdown by just changing HTML.
- Aria attributes can be added/removed easily as per existing code.
- It would be quite easy to provide the option to customise what classes are used for the open/closed state by HTML alone (handled by extra data attributes).

### Use Case 6 - Expanding Formset / InlinePanel

- client/src/entrypoints/admin/expanding-formset.js
- client/src/entrypoints/admin/page-editor.js - see InlinePanel
- `window.buildExpandingFormset` is made available that is basically an init function that provides the ability to define a prefix value and some additional handlers.
- This would need to be built slightly differently with Stimulus, as functions cannot be provided as DOM attributes, so there would need to be a base controller with some class methods for `onAdd` and `onInit`.
- The default behaviour of these methods (just `onInit`) would be the abstracted version of the same code used in the following (negating the need for JS init in these).
  - wagtail/admin/templates/wagtailadmin/permissions/includes/collection_member_permissions_formset.html
  - wagtail/users/static_src/wagtailusers/js/group-form.js
  - wagtail/admin/templates/wagtailadmin/workflows/includes/workflow_pages_formset.html
- However, the more complex case (InlinePanel) would need to use a different controller, let's say we call this `InlinePanelExpandingFormsetController` and it extends `ExpandingFormsetController`.
- This extended class would have an override of `onInit` to do nothing, and then an override of `onAdd` to handle the additional behaviour (note: formCount would need to be resolved in isolation by reading the DOM).
- The awesome thing though is once we start doing this it becomes easy to rewrite InlinePanel into a controller that accepts its init params as data attribute values (e.g. canOrder, maxForms etc).
- Another approach to get the 'onInit' and 'onAdd' behaviour working well is to put these in different controllers and use the dispatch event system (see async content driven modals for info).
- The behaviour of `initControls` may not be needed to be called in isolation as this would all happen based on the controller's `connect` method, meaning we could remove wagtail/contrib/search_promotions/templates/wagtailsearchpromotions/includes/searchpromotions_formset.js & wagtail/admin/templates/wagtailadmin/edit_handlers/inline_panel.js and just have the attributes passed into the HTML.

### Use Case 7 - Async content driven modals

- client/src/entrypoints/admin/modal-workflow.js
- ModalWorkflow is quite a beast but basically it gets a URL (to call for the async HTML response) and then two sets of callbacks.
- This behaviour could be built out into two discrete controllers where the behaviour of 'get some HTML from some URL and put it in a modal' is isolated from 'do something when it loads / errors / responds'.
- There is a powerful feature in Stimulus that let's you find the other Controllers also on the element and pass a message to them https://stimulus.hotwired.dev/reference/controllers#cross-controller-coordination-with-events
- So the Workflow action modal trigger could look something like `<button class="button" data-controller="modal-action workflow-modal" data-modal-action-url-value="{% url 'wagtailadmin_pages:workflow_action' revision.page.id action_name task_state.id %}" data-action="modal-workflow:open->workflow-modal#onload">{{ action_label }}</button>`
- The controller `ModalActionController` would read the URL value, make the request, render the modal in the DOM, then fires off an event to the other controller once the HTML has responded.
- Note: There are two ways to communicate between controllers, one is the syntax above the other is 'finding' the controller on the element and calling it's method directly.
- The ideal case is via the event system though, as this is just the JavaScript custom events with an easy way to trigger and some built in assumptions (prefixed event name, event dispatched from the controlled element). The great thing about this is the framework kind of forces us to use JS events, which other JS can listen for (whether in Stimulus or not) making the 'platform' of Wagtail even more useful.
- There is a fair bit glossed over here obviously, but one critical thing to note is that ANY elements that load from the async HTML will automatically be initialised (if they are Stimulus ones). This means that the bulk of the work in `DOCUMENT_CHOOSER_MODAL_ONLOAD_HANDLERS` will not be needed, adding event listeners, doing an initial search etc.

### Use Case 8 - React driven components (Draftail)

- client/src/components/Draftail/index.js
- Note: There is no need or even any reason to move Draftail to Stimulus, it should stay as a React component - we are not crazy.
- **Recommendation** We should give this a go with some test code and see how this could be written.
- Instead we need to think about the JS we write and how easy it is to just 'add' an editor somewhere.
- The main entry point is client/src/entrypoints/admin/telepath/widgets.js (Telepath) and wagtail/admin/templates/wagtailadmin/widgets/draftail_rich_text_area.html (HTML widget)
- These can leverage the same Stimulus controller that will read the data attributes as initial options and then attach the React rendered component to it.
- For example the Telepath variant will need a bit more work but should be able to read in the initialState as a JSON object on an attribute, render the input field and also call init editor while self-containing the other opts/getValue etc handling itself.

### Use Case 9 - FUTURE: Keyboard shortcuts

- This is something that will become much easier to implement globally across Wagtail.
- We would implement two controller types, one to say 'this button can be triggered by a keyboard shortcut' and another to show a modal of the available shortcuts on the page.
- We may still want to leverage a library like [Hotkeys](https://wangchujiang.com/hotkeys/) or [Mousetrap](https://craig.is/killing/mice) and leverage the syntax they use `ctrl+a`.
- The `HotkeyController` would be used like this `<button data-controller='other-controller hotkey' data-hotkey-shortcut-value='o' data-hotkey-label-value'Optional Label'>Some label</button>` on an element and would use the shortcut library to register a shortcut that will trigger onClick on the button that has the controller.
- The other part is the modal that shows the info, this would also be a controller but when rendered it would 'find' all the other shortcuts on the page (either by accessing the controllers directly globally OR just DOM traversal), and show them all on the modal.
- We now have two discrete functions, one is a behaviour to make something a shortcut and the other is the modal, the great thing is that the modal can be implemented multiple ways (simple bootstrap modal or a full React component), either reading the DOM directly or via the Stimulus js API.
- This also means that 'registering a shortcut key' for a button is as simple as adding a few data attributes via HTML, no additional JS at all!

### Use Case 10 - FUTURE: Mini-map aka page navigator

- Anything that should appear on the mini-map just needs the `data-controller='minimap-item'` added and also should have an `id` on that element. Additional value attributes could be used for things like 'label', 'icon' or even 'priority'.
- Then when 'connect' is run, it passes a message (either via the Stimulus js system or a custom event) and the mini-map component listens to it, keeping a record if the id and its 'depth' and visual 'relative height' in the DOM structure (not pixel height but Tree height).
- The actual minimap component could be a React component but it itself could be initialised by having its own controller, we could even have a convention where some React components have their own controller on them that is registered, to keep the code together. Scroll listeners and alignment to the minimap items would be handled by this component.
- Some nuance would be needed for things that are not actually visible (e.g. behind tabs or collapsed content).
- The whole thing would be reactive quite easily, add a new minimap item (no JS init) via any process, including React driven, and it will connect to it's controller, fire off the event for the minimap to read and add to its list. Same when removed from the DOM.
- The huge benefit of this is we get decoupled behaviour for registering an item and the showing of the items in the side. The complex bit (showing the items on the side) can be done in React if we want, but the registering is just adding some HTML data attributes for the others, completely opt in and easy to be added by external libraries.
- This means adding a minimap to any page (e.g. modeladmin edit) is as simple as adding some data attributes to the 'fields' you want to track (can be done by changing the attributes on the widget) and putting in one div with `data-controller='minimap'`, no JS init scripts needed.
