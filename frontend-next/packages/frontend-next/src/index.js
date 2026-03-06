import { SystemBlockView, SystemBlockEdit } from './components';
import systemSVG from '@plone/volto/icons/computer.svg';

const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['en'],
    defaultLanguage: 'en',
  };

  config.blocks.requiredBlocks = [];

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
};

export default applyConfig;
