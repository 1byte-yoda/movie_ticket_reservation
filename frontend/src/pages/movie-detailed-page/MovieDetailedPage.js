import React, { useEffect, useState } from "react"
import { Link } from "react-router-dom";
import {makeStyles} from "@material-ui/core/styles";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardMedia from "@material-ui/core/CardMedia";
import Typography from "@material-ui/core/Typography";
import ReactPlayer from 'react-player';
import Modal from '@material-ui/core/Modal';
import PlayArrowIcon from '@material-ui/icons/PlayArrow';
import IconButton from "@material-ui/core/IconButton";
import Fade from '@material-ui/core/Fade';
import Rating from '@material-ui/lab/Rating';
import DateRange from "@material-ui/icons/DateRange";
import Avatar from '@material-ui/core/Avatar';
import Button from "@material-ui/core/Button";

import BookingSeats from "../../components/booking-seats/BookingSeats"
import BookingCheckout from "../../components/booking-checkout/BookingCheckout";

const useStyles = makeStyles(theme => ({
    root: {
      maxWidth: 450,
    },
    media: {
      height: 650,
    },
    modal: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    playIconContainer: {
        "&:hover": {
            backgroundColor: "transparent"
        }
    },
    playIcon: {
        height: "80px",
        width: "80px",
    },
    cardWrapper: {
        display: "inline-block",
        position: "relative",
        cursor: "pointer"
    }, 
    layer: {
        position: "absolute",
        top: 0,
        bottom: 0,
        left: 0,
        right: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    hideLayer: {
        position: "absolute",
        top: 0,
        bottom: 0,
        left: 0,
        right: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        visibility: "hidden"
    },
    bookingSeats: {
        marginLeft: "18em"
    },
    large: {
        width: theme.spacing(8),
        height: theme.spacing(8),
    },
    reserveButton: {
        ...theme.typography.signIn,
        height: "50px",
    }
  }));


export default function MovieDetailedPage(props) {
    const { movie } = props
    const classes = useStyles();
    const [openYoutubeModal, setOpenYoutubeModal] = useState(false);
    const [openReserveModal, setOpenReserveModal] = useState(false);

    const handlePlayButtonClick = () => {
        setOpenYoutubeModal(true);
    }

    const handleReserveButtonClick = () => {
        setOpenReserveModal(true);
    }
    
    console.log(movie)
    return (
        <Box bgcolor="common.grey" pb={2} pt={2} pr={8} pl={8}>
            <Grid container>
                <Grid item className={classes.cardWrapper} lg={4}>
                    <Card className={classes.root}>
                        <CardMedia
                        className={classes.media}
                        component="img"
                        src={`/api/image/${movie.id}.jpg`}
                        title={`${movie.name}`}
                        />
                        <div className={openYoutubeModal ? classes.hideLayer : classes.layer} onClick={handlePlayButtonClick}>
                            <IconButton className={classes.playIconContainer}>
                                <PlayArrowIcon className={classes.playIcon}/>
                            </IconButton>
                        </div>
                    </Card>
                </Grid>
                
                <Grid item container direction="column" lg={8}>
                    <Box ml={2} mb={3} style={{padding: "0.5em", backgroundColor: "#424242"}}>
                        <Grid item container>
                            <Grid item>
                                <Typography variant="h3">{movie.name}</Typography>
                            </Grid>
                        </Grid>
                        <Grid item container style={{marginTop: "0.25em"}}>
                            <Grid item>
                                <Typography style={{marginRight: "0.7em", fontWeight: "bold", color: "#ffb400"}} component="body2">{movie.rating/10*5}</Typography>
                            </Grid>
                            <Grid item>
                                <Rating name="half-rating-read" defaultValue={0.0} precision={0.1} readOnly value={movie.rating/10*5} readOnly />
                            </Grid>
                        </Grid>
                        <Grid item container style={{marginTop: "0.5em"}}>
                            <Grid item style={{marginRight: "0.5em"}}>
                                <Typography variant="body1">Genre:</Typography>
                            </Grid>
                            <Grid item>
                                <Box color="#221f1f">
                                    <Typography component={Link} variant="body1">{movie.genre}</Typography>
                                </Box>
                            </Grid>
                        </Grid>
                        <Grid item container style={{marginTop: "1.25em"}}>
                            <Grid item style={{marginRight: "0.25em"}}>
                                <DateRange/> 
                            </Grid>
                            <Grid item>
                                <Typography >{movie.release_date}</Typography>
                            </Grid>
                        </Grid>
                    </Box>
                    <Box ml={2} mt={1} style={{height: "415px", padding: "0.5em", backgroundColor: "#424242"}}>
                        <Grid item style={{marginBottom: "0.25em"}}>
                            <Typography variant="h6">Synopsis</Typography>
                        </Grid>
                        <Grid item>
                            <Typography variant="body1">{movie.description}</Typography>
                        </Grid>
                        <Grid item container direction="column" style={{marginTop: "3.25em"}}>
                            <Grid item>
                                <Typography variant="h6">Casts</Typography>
                            </Grid>
                            <Grid item container>
                                {movie.casts.slice(0, 5).map((name, index) => (
                                    <Grid key={index} style={{marginRight: "0.5em"}} item>
                                        <Avatar className={classes.large}>{name[0]}</Avatar>
                                    </Grid>
                                ))}
                            </Grid>
                        </Grid>
                        <Grid item container direction="column" style={{marginTop: "3.25em"}}>
                            <Grid item style={{marginBottom: "0.25em"}}>
                                <Typography variant="h6">Created by</Typography>
                            </Grid>
                            <Grid item>
                                <Typography component={Link} variant="body1" >{movie.company}</Typography>
                            </Grid>
                        </Grid>
                        <Grid item container style={{marginTop: "1em"}} justify="flex-end">
                            <Grid item>
                                <Button onClick={handleReserveButtonClick}
                                        color="secondary"
                                        variant="contained"
                                        className={classes.reserveButton}
                                >
                                    Reserve a Ticket
                                </Button>
                            </Grid>
                        </Grid>
                    </Box>
                </Grid>
            </Grid>
            <Modal
            className={classes.modal}
            open={openYoutubeModal}
            disableEnforceFocus
            onClose={(event) => setOpenYoutubeModal(false)}
            >
                <Fade in={openYoutubeModal}>
                    <ReactPlayer url={`https://www.youtube.com/watch?v=${JSON.parse(movie.youtube)[0].key}`} playing/>
                </Fade>
            </Modal>
            <Modal
            className={classes.modal}
            open={openReserveModal}
            disableEnforceFocus
            onClose={(event) => setOpenYoutubeModal(false)}
            >
                <Fade in={openReserveModal}>
                    <Grid container item lg={8}>
                        <Grid item className={classes.bookingSeats}>
                            <BookingSeats
                            seats={[[4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                ]}
                            />
                            <BookingCheckout
                            />
                        </Grid>
                    </Grid>
                </Fade>
            </Modal>
        </Box>
        
    )
}