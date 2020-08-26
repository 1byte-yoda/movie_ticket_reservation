import React from 'react';
import classNames from 'classnames';
import { makeStyles } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import CustomPaper from '../../common/CustomPaper';
import { Payment, DateRange } from '@material-ui/icons';

const useStyles = makeStyles(theme => ({
  root: {
    maxWidth: '100%',
    height: "550px",
    paddingBottom: theme.spacing(2),
    cursor: 'pointer',
    backgroundColor: "rgba(41, 41, 41, 0.4)",
    borderRadius: 0,
    color: theme.palette.common.white,
    boxShadow: "unset",
    "&:hover": {
      transform: "scale(1.015)",
      backgroundColor: "rgba(41, 41, 41, 1)",
    },
    textDecoration: "none"
  },
  detailsContainer: {
    // "&:hover": {
    //   transform: "scale(1.01)"
    // }
  },
  imageWrapper: {
    height: '320px',
    margin: '0 auto',
    overflow: 'hidden',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    width: '100%',
    height: '100%',
    'object-fit': 'cover'
  },
  details: { padding: theme.spacing(3) },
  name: {
    fontSize: '18px',
    lineHeight: '21px',
    marginTop: theme.spacing(2),
    textTransform: 'capitalize'
  },
  city: {
    lineHeight: '16px',
    height: theme.spacing(4),
    overflow: 'hidden',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis',
    color: theme.palette.text.secondary,
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(2)
  },
  stats: {
    display: 'flex',
    alignItems: 'center',
    paddingTop: theme.spacing(1),
    paddingLeft: theme.spacing(3),
    opacity: 0.6,
  },
  eventIcon: {
    color: theme.palette.text.secondary
  },
  eventText: {
    marginLeft: theme.spacing(1),
    color: theme.palette.text.secondary
  },

}));

function MovieCategoryCard(props) {
  const classes = useStyles(props);
  const { movie } = props;
  const dateTimeFormat = new Intl.DateTimeFormat(
    'en', { year: 'numeric', month: 'long', day: '2-digit' }
  ) 
  const _date = new Date(movie.release_date)
  const [{ value: month },,{ value: day },,{ value: year }] = dateTimeFormat.formatToParts(_date)
  const rootClassName = classNames(classes.root);
  return (
    <CustomPaper className={rootClassName}>
        <div className={classes.imageWrapper}>
          <img alt={`${movie.name}`} className={classes.image} src={`/api/image/${movie.id}.jpg`} />
        </div>
        <div className={classes.details}>
          <Typography className={classes.name} variant="h4">
            {movie.name}
          </Typography>
          <Typography className={classes.city} variant="body1">
              {movie.cinema.name}
          </Typography>
        </div>
        <div className={classes.stats}>
          <DateRange className={classes.eventIcon}/> 
          <Typography className={classes.eventText} variant="body2">
            {`${day} - ${month} - ${year }`} onwards
          </Typography>
        </div>
        <div className={classes.stats}>
          <Payment className={classes.eventIcon} />
          <Typography className={classes.eventText} variant="body2">
          <span>&#8369;</span> {movie.price} 
          </Typography>
        </div>
    </CustomPaper>
  );
}

export default MovieCategoryCard;
