import type { APIRequestContext, Page } from '@playwright/test';

function getRequestContext(input: APIRequestContext | Page) {
  return 'request' in input ? input.request : input;
}

function getApiURL() {
  const hostname = process.env.BACKEND_HOST || '127.0.0.1';
  const siteId = process.env.SITE_ID || 'plone';
  return process.env.API_PATH || `http://${hostname}:55001/${siteId}`;
}

const headers = { Accept: 'text/xml', 'content-type': 'text/xml' };
const testingLayer = 'plone.app.robotframework.testing.VOLTO_ROBOT_TESTING';
const setupBody = `<?xml version="1.0"?><methodCall><methodName>run_keyword</methodName><params><param><value><string>remote_zodb_setup</string></value></param><param><value><array><data><value><string>${testingLayer}</string></value></data></array></value></param></params></methodCall>`;
const teardownBody = `<?xml version="1.0"?><methodCall><methodName>run_keyword</methodName><params><param><value><string>remote_zodb_teardown</string></value></param><param><value><array><data><value><string>${testingLayer}</string></value></data></array></value></param></params></methodCall>`;

async function callRobotRemote(
  input: APIRequestContext | Page,
  body: string,
) {
  const request = getRequestContext(input);
  const url = `${getApiURL()}/RobotRemote`;
  const response = await request.post(url, { headers, data: body });
  if (!response.ok()) {
    throw new Error(`RobotRemote ${url} returned ${response.status()} ${response.statusText()}`);
  }
  return response;
}

export const setup = (input: APIRequestContext | Page) =>
  callRobotRemote(input, setupBody);
export const teardown = (input: APIRequestContext | Page) =>
  callRobotRemote(input, teardownBody);
