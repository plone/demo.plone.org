/**
 * Add your config changes here.
 * @module config
 * @example
 * export default function applyConfig(config) {
 *   config.settings = {
 *     ...config.settings,
 *     port: 4300,
 *     listBlockTypes: {
 *       ...config.settings.listBlockTypes,
 *       'my-list-item',
 *    }
 * }
 */

import { SystemBlockView, SystemBlockEdit } from '@package/components';
import systemSVG from '@plone/volto/icons/computer.svg';

// All your imports required for the config here BEFORE this line
import '@plone/volto/config';

export default function applyConfig(config) {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['en'],
    defaultLanguage: 'en',
  };

  config.blocks.blocksConfig.system = {
    id: 'system',
    title: 'System',
    icon: systemSVG,
    group: 'common',
    view: SystemBlockView,
    edit: SystemBlockEdit,
    restricted: false,
    mostUsed: true,
    sidebarTab: 1,
  };

  return config;
}
