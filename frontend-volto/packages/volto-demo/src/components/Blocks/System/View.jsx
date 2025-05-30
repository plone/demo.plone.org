import React from 'react';
import { getSystemInformation } from '@plone/volto/actions';
import { useDispatch, useSelector } from 'react-redux';
import { VersionOverview } from '@plone/volto/components';

const SystemView = (props) => {
  const dispatch = useDispatch();
  const systemInfo = useSelector((state) => state.controlpanels.systeminformation);

  React.useEffect(() => {
    dispatch(getSystemInformation());
    /* eslint-disable react-hooks/exhaustive-deps */
  }, []);

  return <VersionOverview {...systemInfo} />;
};

export default SystemView;
