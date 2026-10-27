# Playwright acceptance tests

End-to-end acceptance tests run against a Plone acceptance backend and the
Aurora frontend. The backend uses RobotRemote so the suite can reset it between
tests.

Tests live in `tests/` and use the configuration in `../playwright.config.ts`.
Run `make install-acceptance` once to install Chromium, then start the backend
and frontend and run `make acceptance-test` for the Playwright UI or
`make ci-acceptance-test` for a headless run.

The helpers read `BACKEND_HOST` (default `127.0.0.1`), `SITE_ID` (default
`plone`), `API_PATH` (default `http://127.0.0.1:55001/plone`), and `FRONTEND_URL`
(default `http://localhost:3000`).
