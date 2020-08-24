import React from "react";
import { Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import Hidden from "@material-ui/core/Hidden";

import footerAdornment from "../assets/Footer Adornment.svg";
import facebook from "../assets/facebook.svg";
import twitter from "../assets/twitter.svg";
import instagram from "../assets/instagram.svg";


const useStyles = makeStyles(theme => ({
    footer: {
        backgroundColor: theme.palette.common.blue,
        width: "100%",
        zIndex: 1302,
        position: "relative"
    },
    adornment: {
        width: "20em",
        verticalAlign: "bottom",
        [theme.breakpoints.down("md")]: {
            width: "18em"
        },
        [theme.breakpoints.down("xs")]: {
            width: "12.22em"
        }
    },
    mainContainer: {
        position: "absolute"
    },
    link: {
        color: theme.palette.common.white,
        fontFamily: "Arial",
        fontSize: "0.75rem",
        fontWeight: "bold",
        textDecoration: "none"
    },
    gridItem: {
        margin: "2em"
    },
    icon: {
        height: "4em",
        width: "4em",
        [theme.breakpoints.down("xs")]: {
            marginTop: "0.5em",
            height: "2.25em",
            width: "2.25em",
        }
    },
    socialContainer: {
        position: "absolute",
        marginTop: "-6em",
        right: "1.5em",
        [theme.breakpoints.down("xs")]: {
            right: "1em"
        }
    }
}))


export default function Footer(props) {
    const classes = useStyles();

    return (
        <footer className={classes.footer}>
            <Hidden mdDown>
                <Grid
                justify="center"
                container
                className={classes.mainContainer}
                >
                    <Grid item className={classes.gridItem}>
                        <Grid container direction="column" spacing={2}>
                            <Grid
                            item
                            component={Link}
                            to="/"
                            onClick={() => props.setValue(0)}
                            className={classes.link}
                            >
                                Home
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item className={classes.gridItem}>
                        <Grid container direction="column" spacing={2}>
                            <Grid
                            item
                            component={Link}
                            to="/categories"
                            onClick={() => props.setValue(1)}
                            className={classes.link}
                            >
                                Categories
                            </Grid>
                            <Grid
                            item
                            component={Link}
                            to="/categories/action"
                            onClick={() => {props.setValue(1); props.setSelectedIndex(0); }}
                            className={classes.link}
                            >
                                Action Movies
                            </Grid>
                            <Grid
                            item
                            component={Link}
                            to="/categories/drama"
                            onClick={() => {props.setValue(1); props.setSelectedIndex(1); }}
                            className={classes.link}
                            >
                                Drama Movies
                            </Grid>
                            <Grid
                            item
                            component={Link}
                            to="/categories/comedy"
                            onClick={() => {props.setValue(1); props.setSelectedIndex(2); }}
                            className={classes.link}>
                                Comedy Movies
                            </Grid>
                            <Grid
                            item
                            component={Link}
                            to="/categories/scifi"
                            onClick={() => {props.setValue(1); props.setSelectedIndex(3); }}
                            className={classes.link}
                            >
                                Sci-fi Movies
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item className={classes.gridItem}>
                        <Grid container direction="column" spacing={2}>
                            <Grid
                            item
                            component={Link}
                            to="/cinemas"
                            onClick={() => props.setValue(2)}
                            className={classes.link}
                            >
                                Cinemas
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item className={classes.gridItem}>
                        <Grid container direction="column" spacing={2}>
                            <Grid
                            item
                            component={Link}
                            to="/about"
                            onClick={() => props.setValue(3)}
                            className={classes.link}
                            >
                                About Us
                            </Grid>
                            <Grid
                            item
                            component={Link}
                            to="/ticket-seller"
                            onClick={() => props.setValue(3)}
                            className={classes.link}
                            >
                                Be a Ticket Seller
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item className={classes.gridItem}>
                        <Grid container direction="column" spacing={2}>
                            <Grid
                            item
                            component={Link}
                            to="/contact"
                            onClick={() => props.setValue(4)}
                            className={classes.link}
                            >
                                Contact Us
                            </Grid>
                            <Grid
                            item
                            component={Link}
                            to="/careers"
                            onClick={() => props.setValue(4)}
                            className={classes.link}
                            >
                                Careers
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Hidden>
            <img
            alt="black footer"
            src={footerAdornment} 
            className={classes.adornment}/>
            <Grid spacing={2} justify="flex-end" className={classes.socialContainer} container>
                <Grid item component={"a"} href="https://www.facebook.com" rel="noopener noreferer" target="_blank">
                    <img alt="facebook-logo" src={facebook} className={classes.icon}/>
                </Grid>
                <Grid item component={"a"} href="https://www.twitter.com" rel="noopener noreferer" target="_blank">
                    <img alt="twitter-logo" src={twitter} className={classes.icon}/>
                </Grid>
                <Grid item component={"a"} href="https://www.instagram.com" rel="noopener noreferer" target="_blank">
                    <img alt="instagram-logo" src={instagram} className={classes.icon}/>
                </Grid>
            </Grid>
        </footer>
    )
}