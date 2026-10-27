import type { APIRequestContext, Page } from '@playwright/test';

export type CreateContentParams = {
  contentType: string;
  contentId: string;
  contentTitle: string;
  path?: string;
  transition?: string;
};

function getRequest(input: APIRequestContext | Page) {
  return 'request' in input ? input.request : input;
}

function apiURL() {
  const hostname = process.env.BACKEND_HOST || '127.0.0.1';
  const siteId = process.env.SITE_ID || 'plone';
  return process.env.API_PATH || `http://${hostname}:55001/${siteId}`;
}

function basicAuth() {
  const credentials = Buffer.from('admin:secret', 'utf8').toString('base64');
  return `Basic ${credentials}`;
}

export async function createContent(
  input: APIRequestContext | Page,
  { contentType, contentId, contentTitle, path = '', transition = '' }: CreateContentParams,
) {
  const request = getRequest(input);
  const normalizedPath = path.replace(/^\/+|\/+$/g, '');
  const container = `${apiURL()}/${normalizedPath}`;
  const body: Record<string, unknown> = {
    '@type': contentType,
    id: contentId,
    title: contentTitle,
    description: '',
    allow_discussion: false,
  };
  if (['Document', 'News Item', 'Folder'].includes(contentType)) {
    body.blocks = {
      'd3f1c443-583f-4e8e-a682-3bf25752a300': { '@type': 'title' },
      '7624cf59-05d0-4055-8f55-5fd6597d84b0': { '@type': 'slate' },
    };
    body.blocks_layout = {
      items: [
        'd3f1c443-583f-4e8e-a682-3bf25752a300',
        '7624cf59-05d0-4055-8f55-5fd6597d84b0',
      ],
    };
  }
  const headers = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    Authorization: basicAuth(),
  };
  const response = await request.post(container, { headers, data: body });
  if (!response.ok()) {
    throw new Error(`Create content failed: ${response.status()} ${response.statusText()}`);
  }
  if (transition) {
    const url = `${container}/${contentId}/@workflow/${transition}`;
    const transitionResponse = await request.post(url, {
      headers: { Accept: 'application/json', Authorization: basicAuth() },
    });
    if (!transitionResponse.ok()) {
      throw new Error(`Workflow transition failed: ${transitionResponse.status()} ${transitionResponse.statusText()}`);
    }
  }
  return response;
}
