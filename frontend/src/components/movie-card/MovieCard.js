import React from "react";
import { Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";


const useStyles = makeStyles(theme => ({
    card: {
        maxWidth: 400,
        marginLeft: "1.7em",
        backgroundColor: "transparent",
        borderRadius: 0,
        color: theme.palette.common.white,
        boxShadow: "unset",
    },
    media: {
        height: 300,
    },
    h5: {
        ...theme.typography.movie,
        textTransform: "capitalize",
        [theme.breakpoints.down("md")]: {
            fontSize: "1.4rem"
        }
        
    },
    movieDate: {
        fontSize: "1.3em",
        fontWeight: 450,
        fontFamily: "Raleway",
        textTransform: "uppercase"
    },
    movieOnwards: {
        fontSize: "0.7em",
        fontWeight: 450,
        fontFamily: "Raleway",
        textTransform: "uppercase"
    },
    moviePrice: {
        fontSize: "1.3em",
        fontWeight: 450,
        fontFamily: "Raleway",
        textTransform: "uppercase"
    }
}));


const MovieCard = props => {
    const classes = useStyles();
    const { movie } = props;

    return (
        <Card className={classes.card}>
            <CardActionArea>
                <CardMedia
                className={classes.media}
                image={movie.image}
                title={movie.title}
                />
            <CardContent>
                <Grid container justify="space-between">
                    <Grid item>
                        <Grid container direction="column" alignItems="center">
                            <Grid item>
                                <Typography
                                className={classes.movieDate}
                                color="inherit"
                                >
                                    <Box letterSpacing={3}>
                                        {movie.launch_date.split(" ")[1]}
                                    </Box>
                                </Typography>
                            </Grid>
                            <Grid item>
                                <Typography
                                className={classes.movieDate}
                                color="inherit"
                                >
                                    <Box letterSpacing={3}>
                                        {movie.launch_date.split(" ")[0].substring(0, 3)}
                                    </Box>
                                </Typography>
                            </Grid>
                            <Grid item>
                                <Typography
                                className={classes.movieOnwards}
                                gutterBottom
                                color="inherit"
                                >
                                    <Box letterSpacing={1}>
                                        onwards
                                    </Box>
                                </Typography>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item>
                        <Grid container direction="column" alignItems="flex-end" spacing={0.75}>
                            <Grid item>
                                <Typography
                                className={classes.h5}
                                variant="h5"
                                component="h2"
                                color="inherit"
                                >
                                    {movie.title}
                                </Typography>
                            </Grid>
                            <Grid item>
                                <Typography
                                className={classes.moviePrice}
                                gutterBottom
                                color="inherit"
                                >
                                    <Box letterSpacing={1}>
                                        {"php " + movie.price}
                                    </Box>
                                </Typography>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </CardContent>
            </CardActionArea>
        </Card>
    );
};


export default MovieCard;