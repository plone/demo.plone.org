# volto-frontend

`volto-frontend` is the frontend of `volto.demo.plone.org`, a demo of Volto core without add-ons.
This site is useful for demonstrating observed behavior of Volto core.
It is pre-populated with Volto block content.

A training on how to create your own website using Volto is available as part of the Plone training at [https://training.plone.org/voltohandson/index.html](https://training.plone.org/voltohandson/index.html).

## Quick start

You can use the following commands while working with the project.

```shell
make install
```

Installs and checks out the `mrs-developer` directives (via `make develop`), creates a shortcut to the Volto source code (`omelette` folder), then triggers the install of the frontend environment.

```shell
yarn start
```

Runs the project in development mode.
You can view your application at `http://localhost:3000`.

The page will reload when you edit it.

```shell
yarn build
```

Builds the app for production in the build folder.

The build is minified, and the file names include the hashes.
Your app is ready to be deployed!

```shell
yarn start:prod
```

Runs the compiled app in production.

You can view your application at `http://localhost:3000`

```shell
yarn test
```

Runs the test watcher (Jest) in interactive mode.
By default, the command runs tests related to files changed since the last commit.

```shell
yarn i18n
```

Runs the test i18n runner, which extracts all the translation strings and generates the needed files.

## mrs-developer

[mrs-developer](https://github.com/collective/mrs-developer) is a great tool for developing multiple packages at the same time.

mrs-developer should work with this project by running the configured shortcut script:

```shell
make develop
```

Volto's latest Razzle configuration will pay attention to your `tsconfig.json` (or `jsconfig.json`) file for any customizations.

In case you don't want (or can't) install mrs-developer globally, you can install it in this project by running the following command:

```shell
yarn add -W mrs-developer
```

## Acceptance tests

To run your app locally while developing the project acceptance tests (Cypress), there are some `Makefile` commands in place (in the repo root). Run them in order:

```shell
start-test-acceptance-server
```

Start the server fixture in Docker.
This command requires that you first build your app.

```shell
start-test-acceptance-frontend
```

Start the core Acceptance frontend fixture in development mode.

```shell
test-acceptance
```

Start core Cypress acceptance tests in development mode.

```shell
full-test-acceptance
```
Start the whole Cypress acceptance test suite (backend, frontend, and headless tests) in headless (CI) mode.
