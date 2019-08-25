# client

[![Travis][build-badge]][build]
[![npm package][npm-badge]][npm]
[![Coveralls][coveralls-badge]][coveralls]

Describe client here.

[build-badge]: https://img.shields.io/travis/user/repo/master.png?style=flat-square
[build]: https://travis-ci.org/user/repo
[npm-badge]: https://img.shields.io/npm/v/npm-package.png?style=flat-square
[npm]: https://www.npmjs.org/package/npm-package
[coveralls-badge]: https://img.shields.io/coveralls/user/repo/master.png?style=flat-square
[coveralls]: https://coveralls.io/github/user/repo

## Tutorial

**Goal:** Integrate a single npm react component to leverage it inside an existing Wagtail admin project.

### Problems to work through

- Quick Development / prod deployment
- Understanding the 'build' vs dev env
- Connecting to the API (method 1 to get data)
- Passing data down to component from view (method 2 to get data)
- Installing/bundling external react dependency
- Bundling css _maybe even scss_
- Must leverage existing Wagtail view, sidebar, header etc
- Set up prettier

### Understanding

- yarn build & refresh to see changes in admin
- hot reloading to see changes in dev

### Assumptions

- Wagtail project set up
- Wagtail API set up
- Basic knowledge of React, NPM, Yarn and JS ecosystem

### Steps

cd ./timeline
nwb new react-component client --no-git

es - no
UMD yes
UMD name Timeline

cd ./client

npm run start start

npm run build

add static dir OR pass param into build script

add css file & update nwb.config.js to remove hash from production build css

- `npm install --save react-calendar-timeline`
- `npm install --save moment`
- `npm install --save interactjs`
- Save & commit the package-lock
- https://github.com/namespace-ee/react-calendar-timeline#usage

WAGTAILAPI_LIMIT_MAX = 200

### Useful links

- https://reactjs.org/community/starter-kits.html
- https://www.npmtrends.com/neutrino-vs-nwb-vs-kyt-vs-razzle-vs-rekit-vs-react-static
- https://github.com/namespace-ee/react-calendar-timeline#usage
- http://docs.wagtail.io/en/latest/advanced_topics/api/v2/usage.html
- Using React 16.4 currently - https://github.com/wagtail/wagtail/blob/master/package.json#L94

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

### attempt 4 - nwb (again)

- better luck this time
- it appears that package.json does not get correctly used initially so runnin npm install first helps

## Notes

- add `os.path.join(PROJECT_DIR, 'timeline/client/build'),` to STATICFILES_DIRS in settings.py
- Issue; requires a `require` in global, does not strip proptypes (nwb does)

### nwb

- - adds gitignore, unlcear if it will add when we skip git initialisation
- - uses node, no yarn needed
- - easily build a UMD that 'just works'
- - removes proptypes in production build
- - no need for MyComponent.default in production build
- - focused library, mainly cares about deploying to web or npm
- - easily configure what is and is not available in global scope
- - requires a global install to use the CLI
- - default test suite is karma only
- - does not add linting by default
- - could not get back into it after npm install (when checking out a different branch, removing node_modules and starting again)

### neutrino

- - no need for global install
- - testing, linting, multible variants just works, including various testing libraries
- - appears to have a lot of capacity to do many things, maybe too much
- - docs are huge
- - yarn seems to be better at recovering after a clean install / new branch
- - detailed docs for specific things is a bit hard to find
- - uses yarn, yet another package manager (but it is not too much overhead)
- - react-component by default will need `require` in global to work in prod
- - does not remove proptypes requirement in production build
