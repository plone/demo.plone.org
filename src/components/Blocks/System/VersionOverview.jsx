/**
 * Version Overview component.
 * @module components/manage/Controlpanels/VersionOverview
 */

import React from 'react';
import { isEmpty } from 'lodash';
import { version as voltoVersion } from '@plone/volto/../package.json';
import { defineMessages, useIntl } from 'react-intl';
import config from '@plone/volto/registry';

const messages = defineMessages({
  no_addons: {
    id: 'No addons found',
    defaultMessage: 'No addons found',
  },
});

const VersionOverview = ({
  cmf_version,
  pil_version,
  plone_version,
  python_version,
  plone_restapi_version,
  zope_version,
}) => {
  const intl = useIntl();
  const { addonsInfo } = config.settings;

  return (
    <>
      <ul
        style={{
          fontSize: '16px',
          fontFamily: 'Monospace',
        }}
      >
        {voltoVersion && <li>Volto {voltoVersion}</li>}
        <li>Plone {plone_version}</li>
        <li>plone.restapi {plone_restapi_version}</li>
        <li>CMF {cmf_version}</li>
        <li>Zope {zope_version}</li>
        <li>Python {python_version}</li>
        <li>PIL {pil_version}</li>
      </ul>
      <h3>Add-ons</h3>
      {isEmpty(addonsInfo) ? (
        <p>{intl.formatMessage(messages.no_addons)}</p>
      ) : (
        <ul style={{ fontSize: '16px', fontFamily: 'Monospace' }}>
          {addonsInfo.map((addon) => (
            <li key={addon.name}>{`${addon.name} ${addon.version || ''}`}</li>
          ))}
        </ul>
      )}
    </>
  );
};

export default VersionOverview;
