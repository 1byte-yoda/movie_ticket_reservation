import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import PaginationItem from "@material-ui/lab/PaginationItem"
import Pagination from '@material-ui/lab/Pagination';
import { makeStyles, Grid, Typography, Container, useTheme } from '@material-ui/core';
import MovieCategoryCard from '../movie-category-card/MovieCategoryCard';
import _ from 'lodash';
import useMediaQuery from "@material-ui/core/useMediaQuery";


const useStyles = makeStyles(theme => ({
  title: {
    fontSize: '2.5rem',
    fontWeight: 500,
    fontFamily: "Raleway",
    color: theme.palette.text.primary,
    textAlign: 'center',
    marginTop: "1em"
  },
  dateButton: {
    margin: 1
  },
  toggleButton: {
    fontSize: 13,
    padding: 7,
    [theme.breakpoints.down("md")]: {
      fontSize: 12,
      padding: 5,
    },
    [theme.breakpoints.down("xs")]: {
      fontSize: 11,
      padding: 4,
    },
  },
  container: {
    paddingBottom: "1.5rem",
    paddingLeft: "2.5rem"
  }
}));

function MovieCategoryList(props) {
  const classes = useStyles(props);
  const theme = useTheme();
  const matches = useMediaQuery(theme.breakpoints.down("xs"));
  const { pageSize, page, movies, setValue } = props;
  // const [selectedYear, setSeletedYear] = useState(() => [movieDates[0].year])
  // const [selectedMonth, setSeletedMonth] = useState(() => ["Aug"])
  // const [monthsToDisable, setmonthsToDisable] = useState(() => movieDates[0].months)
  // const MONTHS = [
  //   "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  // ]
  // const handleSelectYear = (event, year) => {
  //   if (year) {
  //     let _tempMonths = null;
  //     setSeletedYear(year);
  //     _tempMonths = movieDates.filter(date => year.includes(date.year)).map(date => date.months).flat()
  //     setmonthsToDisable(_tempMonths)
  //     setSeletedMonth([MONTHS.filter(month => _tempMonths.includes(month))[0]]);
  //   }
  // };
  // const handleSelectMonth = (event, months) => {
  //   if (months.length !== 0) {
  //     setSeletedMonth(months.filter(month => monthsToDisable.includes(month)));
  //   }
  // };
  return (
    <Container className={classes.container} maxWidth="xl">
      <Grid container direction="column" spacing={3}>
        <Grid item >
          <Typography className={classes.title} variant="h2" color="inherit">
            Movies
          </Typography>
        </Grid>
        {/* <Grid item>
          <Grid container spacing={1}>
            <ToggleButtonGroup
              exclusive
              value={selectedYear}
              onChange={handleSelectYear}
              aria-label="year"
            >
              {movieDates.map((item, index) => (
                <ToggleButton
                  key={index}
                  className={classes.toggleButton}
                  value={item.year}
                  aria-label={item.year}
                >
                  {item.year}
                </ToggleButton>
              ))}
            </ToggleButtonGroup>
          </Grid>
        </Grid> */}
        {/* <Grid item>
          <Grid container spacing={1}>
            <Grid item>
              <ToggleButtonGroup
                value={selectedMonth}
                // orientation={matches ? "vertical" : "horizontal"}
                onChange={handleSelectMonth}
                aria-label="month">
                {MONTHS.map((month, index) =>
                  <ToggleButton 
                    key={index}
                    disabled={!monthsToDisable.includes(month)}
                    className={classes.toggleButton}
                    value={month}
                    aria-label={month}
                  >
                    {month}
                  </ToggleButton>
                )}
              </ToggleButtonGroup>
            </Grid>
          </Grid>
        </Grid> */}
        <Grid
          container
          item
          xs={12}
          alignItems="center"
          justify="flex-start"
          spacing={2}>
          {movies.map(movie => (
            <Grid 
              key={movie.id}
              item
              xs={12}
              md={4}
              lg={3}
            >
              <Link to={`/movie/${movie.id}`} style={{textDecoration: "none"}}>
                <MovieCategoryCard movie={movie} />
              </Link>
            </Grid>
          ))}
        </Grid>
        {(movies.length > 0) ?
        <Grid container item style={{marginTop: "1rem"}} justify="flex-end">
            <Pagination
            page={page}
            count={pageSize}
            size="large"
            renderItem={(item) => (
                <PaginationItem
                component={Link}
                to={`/movies${item.page === 1 ? '' : `/page/${item.page}`}`}
                onClick={() => setValue(1)}
                {...item}
                />
            )}
        />
        </Grid>
        : null
        }
      </Grid>
    </Container>
  );
}

export default MovieCategoryList;
