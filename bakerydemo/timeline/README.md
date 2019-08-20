
## attempt 1 - create-react-app

* nvm ls - v10.15.3
* npx create-react-app client (in timeline app)
* cd client
* yarn start

## attempt 2 - neutrino

* nvm ls - v10.15.3
* npx @neutrinojs/create-project client
* First up, what would you like to create? Components
* Next, what kind of components would you like to create? React Components
* Would you like to add a test runner to your project? Jest
* Would you like to add linting to your project? Airbnb style rules
* cd client, yarn start
* add .gitignore manually



## Notes

* add `os.path.join(PROJECT_DIR, 'timeline/client/build'),` to STATICFILES_DIRS in settings.py
* Issue; requires a `require` in global, does not strip proptypes (nwb does)


nwb
* + adds gitignore, unlcear if it will add when we skip git initialisation
* + uses node, no yarn needed
* + easily build a UMD that 'just works'
* + removes proptypes in production build
* + no need for MyComponent.default in production build
* + focused library, mainly cares about deploying to web or npm
* + easily configure what is and is not available in global scope
* - requires a global install to use the CLI
* - default test suite is karma only
* - does not add linting by default


neutrino
* + no need for global install
* + testing, linting, multible variants just works, including various testing libraries
* + appears to have a lot of capacity to do many things, maybe too much
* + docs are huge
* - detailed docs for specific things is a bit hard to find
* - uses yarn, yet another package manager (but it is not too much overhead)
* - react-component by default will need `require` in global to work in prod
* - does not remove proptypes requirement in production build
