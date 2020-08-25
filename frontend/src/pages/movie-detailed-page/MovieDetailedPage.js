import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardMedia from "@material-ui/core/CardMedia";
import Typography from "@material-ui/core/Typography";
import ReactPlayer from 'react-player';
import Modal from '@material-ui/core/Modal';
import Dialog from "@material-ui/core/Dialog";
import DialogContent from "@material-ui/core/DialogContent";
import PlayArrowIcon from '@material-ui/icons/PlayArrow';
import IconButton from "@material-ui/core/IconButton";
import Fade from '@material-ui/core/Fade';
import Rating from '@material-ui/lab/Rating';
import DateRange from "@material-ui/icons/DateRange";
import Avatar from '@material-ui/core/Avatar';
import Button from "@material-ui/core/Button";
import Select from '@material-ui/core/Select';
import MenuItem from "@material-ui/core/MenuItem";
import InputLabel from "@material-ui/core/InputLabel";
import FormControl from '@material-ui/core/FormControl';

import BookingSeats from "../../components/booking-seats/BookingSeats"
import BookingCheckout from "../../components/booking-checkout/BookingCheckout";

const useStyles = makeStyles(theme => ({
    root: {
      width: 340,
      maxWidth: 340,
      marginBottom: "0",
      display: "inline-block",
      position: "relative",
      cursor: "pointer",
    },
    media: {
      minHeight: 470,
      maxHeight: 470,
      
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
        backgroundColor: theme.palette.common.light_grey,
        padding: "0.5em"
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
        marginLeft: "0"
    },
    large: {
        width: theme.spacing(8),
        height: theme.spacing(8),
        color: "white"
    },
    reserveButton: {
        ...theme.typography.signIn,
        height: "50px",
    },
    reserveButtonContainer: {
        
        paddingBottom: "1em"
    },
    formControl: {
        marginBottom: theme.spacing(2),
        minWidth: 220,
    },
    title: {
        color: "white"
    },
    subtitle: {
        color: "white"
    },
    calendar: {
        color: "white"
    }
  }));


export default function MovieDetailedPage(props) {
    const { movie } = props;
    const theme = useTheme();
    const matchesMd = useMediaQuery(theme.breakpoints.down("md"));
    const matchesSm = useMediaQuery(theme.breakpoints.down("sm"))
    const matchesXs = useMediaQuery(theme.breakpoints.down("xs"))
    const classes = useStyles();
    const [openYoutubeModal, setOpenYoutubeModal] = useState(false);
    const [openReserveModal, setOpenReserveModal] = useState(false);
    const [schedule, setSchedule] = useState(10);

    const handlePlayButtonClick = () => {
        setOpenYoutubeModal(true);
    }

    const handleReserveButtonClick = () => {
        setOpenReserveModal(true);
    }
    
    const handleScheduleChange = (event) => {
        setSchedule(event.target.value);
    }

    console.log(movie)
    return (
        <Box bgcolor="common.grey" pb={2} pt={2} pr={8} pl={8}>
            <Grid container>
                <Grid item container className={classes.cardWrapper} lg={3}>
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
                    <Grid item container justify="center" className={classes.reserveButtonContainer}>
                        <Button onClick={handleReserveButtonClick}
                                color="secondary"
                                variant="contained"
                                className={classes.reserveButton}
                                fullWidth
                        >
                            Reserve a Ticket
                        </Button>
                    </Grid>
                    <Grid item container justify="center" className={classes.reserveButtonContainer}>
                        <Button onClick={handlePlayButtonClick}
                                color="secondary"
                                variant="contained"
                                className={classes.reserveButton}
                                fullWidth
                                
                        >
                            Watch Trailer
                        </Button>
                    </Grid>
                </Grid>
                
                <Grid item container direction="column" lg={9}>
                    <Box ml={2} mb={3} style={{padding: "0.5em", backgroundColor: "#424242"}}>
                        <Grid item container>
                            <Grid item>
                                <Typography className={classes.title} variant="h3">{movie.name}</Typography>
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
                                <DateRange className={classes.calendar}/> 
                            </Grid>
                            <Grid item>
                                <Typography >{movie.release_date} onwards</Typography>
                            </Grid>
                        </Grid>
                    </Box>
                    <Box ml={2} mt={1} style={{minHeight: "430px", padding: "0.5em", backgroundColor: "#424242"}}>
                        <Grid item style={{marginBottom: "0.25em"}}>
                            <Typography className={classes.subtitle} variant="h6">Synopsis</Typography>
                        </Grid>
                        <Grid item>
                            <Typography variant="body1">{movie.description}</Typography>
                        </Grid>
                        <Grid item container direction="column" style={{marginTop: "3.25em"}}>
                            <Grid item>
                                <Typography className={classes.subtitle} variant="h6">Cast</Typography>
                            </Grid>
                            <Grid item>
                                <Grid item container>
                                    {movie.casts.slice(0, 5).map((name, index) => (
                                        <Grid key={index} style={{marginRight: "1em"}} item>
                                            <Grid item container direction="column"> 
                                                <Grid item>
                                                    <Avatar className={classes.large}>{name[0]}</Avatar>
                                                </Grid>
                                                <Grid key={index} style={{marginTop: "0.25em", color: "white"}} item component={Link}>
                                                    <Box 
                                                        textAlign="center"
                                                        className={classes.large}
                                                        component="div"
                                                        whiteSpace="normal"
                                                    >
                                                        {name}
                                                    </Box>
                                                </Grid>
                                            </Grid>
                                        </Grid>
                                    ))}
                                </Grid>
                            </Grid>
                        </Grid>
                        <Grid item container direction="column" style={{marginTop: "3em"}}>
                            <Grid item style={{marginBottom: "0.25em"}}>
                                <Typography className={classes.subtitle} variant="h6">Created by</Typography>
                            </Grid>
                            <Grid item>
                                <Typography component={Link} variant="body1" >{movie.company}</Typography>
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
                    <ReactPlayer url={`https://www.youtube.com/watch?v=${JSON.parse(movie.youtube).length ? JSON.parse(movie.youtube)[0].key : "#"}`} playing/>
                </Fade>
            </Modal>
            <Dialog
            PaperProps={{style:
            {
                paddingTop: "2em",
                paddingBottom: "2em",
                paddingLeft: matchesXs ? 0 : matchesSm ? "5em" : matchesMd ? "10em" : "15em",
                paddingRight: matchesXs ? 0 : matchesSm ? "5em" : matchesMd ? "10em" : "15em"
            }}}
            style={{zIndex: 1302}}
            fullScreen={matchesXs}
            open={openReserveModal}
            onClose={(event) => setOpenReserveModal(false)}
            >
                <Fade in={openReserveModal}>
                    <DialogContent style={{overflow: "visible"}}>
                        <Grid container item direction="column" spacing={2} >
                            <Grid item container justify="space-between">
                                <Grid item>
                                        <FormControl className={classes.formControl}>
                                            <InputLabel id="demo-simple-select-label">Theatre</InputLabel>
                                            <Select
                                                labelId="demo-simple-select-label"
                                                id="demo-simple-select"
                                                fullWidth
                                                value={schedule}
                                                onChange={handleScheduleChange}
                                                MenuProps={{style: {zIndex: 2000}}}
                                            >
                                                <MenuItem value={10}>Ten</MenuItem>
                                                <MenuItem value={20}>Twenty</MenuItem>
                                                <MenuItem value={30}>Thirty</MenuItem>
                                            </Select>
                                        </FormControl>
                                    </Grid>
                                    <Grid item>
                                        <FormControl className={classes.formControl}>
                                            <InputLabel id="demo-simple-select-label">Schedule</InputLabel>
                                            <Select
                                                labelId="demo-simple-select-label"
                                                id="demo-simple-select"
                                                value={schedule}
                                                fullWidth
                                                onChange={handleScheduleChange}
                                                MenuProps={{style: {zIndex: 2000}}}
                                            >
                                                <MenuItem value={10}>Ten</MenuItem>
                                                <MenuItem value={20}>Twenty</MenuItem>
                                                <MenuItem value={30}>Thirty</MenuItem>
                                            </Select>
                                        </FormControl>
                                    </Grid>
                            </Grid>
                            <Grid item>
                                <BookingSeats
                                seats={[[4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                    ]}
                                />
                            </Grid>
                            <Grid item>
                                <BookingCheckout
                                    />
                            </Grid>
                        </Grid>
                    </DialogContent>
                </Fade>
            </Dialog>
        </Box>
        
    )
}