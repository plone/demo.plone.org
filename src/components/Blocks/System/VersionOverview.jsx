/**
 * Version Overview component.
 * @module components/manage/Controlpanels/VersionOverview
 */

import React from 'react';
import { List } from 'semantic-ui-react';

import packageJSON from '@plone/volto/../package.json';

const VersionOverview = ({
  cmf_version,
  pil_version,
  plone_version,
  python_version,
  plone_restapi_version,
  zope_version,
}) => {
  const voltoVersion = packageJSON.version;

  return (
    <>
      <List bulleted size="large">
        {voltoVersion && (
          <List.Item key="volto">Volto {voltoVersion}</List.Item>
        )}
        <List.Item key="volto">Plone {plone_version}</List.Item>
        <List.Item key="volto">plone.restapi {plone_restapi_version}</List.Item>
        <List.Item key="volto">Zope {zope_version}</List.Item>
        <List.Item key="volto">Python {python_version}</List.Item>
        <List.Item key="volto">PIL {pil_version}</List.Item>
      </List>
    </>
  );
};

export default VersionOverview;
