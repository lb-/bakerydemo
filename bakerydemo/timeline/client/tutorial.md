# Tutorial

**Goal:** Integrate a single npm react component to leverage it inside an existing Wagtail admin project.

## Problems to work through

- Quick Development / prod deployment
- Understanding the 'build' vs dev env
- Connecting to the API (method 1 to get data)
- Passing data down to component from view (method 2 to get data)
- Installing/bundling external react dependency
- Bundling css _maybe even scss_
- Must leverage existing Wagtail view, sidebar, header etc
- Set up prettier

## Understanding

- yarn build & refresh to see changes in admin
- hot reloading to see changes in dev

## Assumptions

- Wagtail project set up
- Wagtail API set up
- Basic knowledge of React, NPM, Yarn and JS ecosystem

## Steps

### 1. Django App `timeline`

- add app to settings
- views.py
- templates/timeline.html (include basic dom based react component and styles)

```django
{% block extra_js %}
  {{ block.super }}
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      ReactDOM.render(
        React.createElement(
          'div',
          {
            children: 'component here',
            className: 'content'
          }
        ), document.getElementById('timeline'));
    });
  </script>
{% endblock %}
```

- wagtail_hooks.py
- test it all & commit changes

### 2. Add client app within Django app

- cd ./timeline
- nvm ls - v10.15.3
- npx @neutrinojs/create-project client
- First up, what would you like to create? Components
- Next, what kind of components would you like to create? React Components
- Would you like to add a test runner to your project? Jest
- Would you like to add linting to your project? Airbnb style rules
- add .gitignore manually
- commit changes here
- configure editor, prettier and format files created by the template
- add style.css, className + classNames package & import
- test it all & commit changes (yarn start, dev only)

### 3. Get build output loading in template

- configure neutrino to work with global React in Wagtail admin
- configure for static file approach
- setting up static files - this is the result of 'yarn build', we can either set `STATICFILES_DIRS` to point to the default build directory or update neturinorc.js options to move to the static, we will assume the later for now
- add the build HelloWorld imports into the template + css file import
- yarn build & check
- test it all & commit changes

### 4. Add external js dependencies and timeline component

- https://github.com/namespace-ee/react-calendar-timeline#getting-started
- `yarn add react-calendar-timeline`
- `yarn add moment`
- `yarn add interactjs`
- Copy in the basic getting started data for rendering & then yarn build to update in admin (check it works)
- yarn build and refresh

### 6. Add Wagtail admin header & search form

- Use Wagtail header template snippet syntax
- add a search form to the template response
- add the request query to the template response
- pass the search form id and the query value into the react component
- add event listener to the search form and add react component value if searching + filter data
- Test works on pressing enter (submitting) the search form
- test it all & commit changes

### 7. Add API calls & transform data in the react component

- bit of refactoring, renaming (rename to Timeline.jsx)
- add API calls (ensure Wagtail API is configured)
- transform data and pass in to the react timeline component
- remember to keep the 'mocked' value in the index.jsx file for quick hot loading development
- filter based on search value
- yarn build
- test it all & commit changes

### 8. Stretch: get more complex data from custom API endpoint

- important: must have a way to secure the response to signed in only

## Attempts

### attempt 1 - create-react-app

- nvm ls - v10.15.3
- npx create-react-app client (in timeline app)
- cd client
- yarn start
- Too heavy handed for what we need, good if we were not trying to integrate with an existing Django view template (eg. extend admin)

### attempt 2 - neutrino

- nvm ls - v10.15.3
- npx @neutrinojs/create-project client
- First up, what would you like to create? Components
- Next, what kind of components would you like to create? React Components
- Would you like to add a test runner to your project? Jest
- Would you like to add linting to your project? Airbnb style rules
- cd client, yarn start
- add .gitignore manually

### attempt 3 - nwb

- nvm ls - v10.15.3
- nwb new react-component client --no-git
- UMD module
- Builds to multiple folders, lib & umd
- Added import of umd to timeline.html
- Major issues after checking out a different branch and attempting npm install again, could not get it working at all
- Pros & cons below

### attempt 4 - neutrino (again)

- this time started on a clean project and focused only on the neutrino configuration
  - https://github.com/neutrinojs/neutrino/issues/1425
  - https://github.com/neutrinojs/neutrino/issues/1457
  - https://github.com/neutrinojs/neutrino/blob/master/packages/react-components/index.js#L63
  - https://www.npmjs.com/package/webpack-node-externals
  - https://webpack.js.org/configuration/externals/#externals
- found a way to avoid the need for require and ended up with a much simpler set up on the html side

## Notes

- add `os.path.join(PROJECT_DIR, 'timeline/client/build'),` to STATICFILES_DIRS in settings.py
- Issue; requires a `require` in global, does not strip proptypes (nwb does)

### nwb

- ✓ adds gitignore, unlcear if it will add when we skip git initialisation
- ✓ uses node, no yarn needed
- ✓ easily build a UMD that 'just works'
- ✓ removes proptypes in production build
- ✓ no need for MyComponent.default in production build
- ✓ focused library, mainly cares about deploying to web or npm
- ✓ easily configure what is and is not available in global scope
- ✘ requires a global install to use the CLI
- ✘ default test suite is karma only
- ✘ does not add linting by default
- ✘ could not get back into it after npm install (when checking out a different branch, removing node_modules and starting again)

### neutrino

- ✓ no need for global install
- ✓ testing, linting, multible variants just works, including various testing libraries
- ✓ appears to have a lot of capacity to do many things, maybe too much
- ✓ docs are huge
- ✓ yarn seems to be better at recovering after a clean install / new branch
- ✘ detailed docs for specific things is a bit hard to find
- ✘ uses yarn, yet another package manager (but it is not too much overhead)
- ✘ react-component by default will need `require` in global to work in prod
- ✘ does not remove proptypes requirement in production build
