# volto-demo

You can develop an add-on in isolation using the boilerplate already provided by the add-on generator.
The project is configured to have the current add-on installed and ready to work with.
This is useful to bootstrap an isolated environment that can be used to quickly develop the add-on or for demo purposes.
It's also useful when testing an add-on in a CI environment.

Note: It's quite similar when you develop a Plone backend add-on in the Python side, and embed a ready-to-use Plone build (using buildout or pip), to develop and test the package.

## Development

The Dockerized approach performs all these actions in a custom built Docker environment:

1. Generates a vanilla project using the official Volto Yeoman generator (@plone/generator-volto)
2. Configures the project to use the add-on with the name stated in the `package.json`
3. Links the root of the add-on inside the created project

After that, you can use the inner Dockerized project, and run any standard Volto command for linting, acceptance tests, or unit tests using Makefile commands, provided for your convenience.

## Set up the environment

Run the following command only once.

```shell
make dev
```

This command builds and launches the backend and frontend containers.
There's no need to build them again after doing it the first time, unless something has changed from the container setup.

To make your local IDE play well with this setup, you must run `yarn` once to install the required packages.

```shell
yarn
```

## Build the containers manually

Run the following commands to build the containers.

```shell
make build-backend
make build-addon
```

## Run the containers

Run the following command to start both the frontend and backend containers.

```shell
make start-dev
```

## Stop backend (Docker)

After developing, to stop the running backend, run the following command.

```shell
make stop-backend
```

### Linting

Run the following command to lint your code.

```shell
make lint
```

### Formatting

Run the following command to format your code.

```shell
make format
```

### i18n

Run the following command to update internationalized language strings.

```shell
make i18n
```

### Unit tests

Run the following command to run unit tests.

```shell
make test
```

### Acceptance tests

Run the following command only once to install the acceptance test environment.

```shell
make install-acceptance
```

To start the servers, run the following command.

```shell
make start-test-acceptance-server
```

The frontend runs in development mode, so you can develop while writing tests.

Then run the following command to run Cypress tests.

```shell
make test-acceptance
```

When finished, shutdown the backend server with the following command.

```shell
make stop-test-acceptance-server
```

### Release

To make a release, run the following command.

```shell
make release
```

To release a release candidate version, run the following command.

```shell
make release-rc
```
