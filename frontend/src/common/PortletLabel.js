import React from 'react';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core';
import { Typography } from '@material-ui/core';

const styles = theme => ({
  root: {
    display: 'flex',
    alignItems: 'center'
  },
  icon: {
    fontSize: '1.3rem',
    marginRight: theme.spacing(1),
    color: theme.palette.text.secondary,
    alignItems: 'center',
    display: 'flex'
  },
  title: {
    fontWeight: 500
  },
  body1: {
    fontWeight: 400,
    color: theme.palette.text.secondary
  }
});

const PortletLabel = props => {
  const { classes, className, icon, title, body1, ...rest } = props;

  const rootClassName = classNames(classes.root, className);

  return (
    <div {...rest} className={rootClassName}>
      {icon && <span className={classes.icon}>{icon}</span>}
      {title && (
        <Typography className={classes.title} variant="h5">
          {title}
        </Typography>
      )}
      {body1 && (
        <Typography className={classes.body1} variant="body1">
          {body1}
        </Typography>
      )}
    </div>
  );
};

PortletLabel.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string,
  classes: PropTypes.object.isRequired,
  icon: PropTypes.node,
  subtitle: PropTypes.string,
  title: PropTypes.string
};

export default withStyles(styles)(PortletLabel);
