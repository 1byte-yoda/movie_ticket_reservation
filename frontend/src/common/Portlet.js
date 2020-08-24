import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core';
import CustomPaper from './CustomPaper';
// Component styles
const styles = () => ({
  root: {
    display: 'flex',
    flexDirection: 'column'
  }
});

const Portlet = props => {
  const { classes, className, children, ...rest } = props;
  const rootClassName = classNames(classes.root, className);

  return (
    <CustomPaper
      {...rest}
      className={rootClassName}
      elevation={0}
      outlined
      squared={false}>
      {children}
    </CustomPaper>
  );
};
Portlet.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string,
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Portlet);
