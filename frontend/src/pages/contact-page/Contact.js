import React, { useState } from "react";
import {Link} from "react-router-dom";
import {makeStyles, useTheme} from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Box from "@material-ui/core/Box";
import PhoneIcon from '@material-ui/icons/Phone';
import EmailIcon from '@material-ui/icons/Email';
import SendIcon from '@material-ui/icons/Send';

import background from "../../assets/contact_us_.jpg";


const useStyles = makeStyles(theme => ({
    root: {
        flexGrow: 1,
    },
    title: {
        fontSize: '2.5rem',
        fontWeight: 500,
        fontFamily: "Raleway",
        color: theme.palette.text.primary,
        textAlign: 'center',
    },
    background: {
        backgroundImage: `url(${background})`,
        backgroundPosition: "center",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        height: "80em",
    },
    body1: {
        color: theme.palette.text.primary,
        fontWeight: 400,
    },
    body2: {
        color: theme.palette.text.primary,
        fontWeight: 400,
        fontSize: "1rem"
    },
    body: {
        background: "rgba(0, 0, 0, 0.7)",
    },
    message: {
        border: "1.5px solid rgba(255, 255, 255, 0.7)",
        marginTop: "4em",
        borderRadius: 5,
        "&:hover": {
            border: "1.5px solid rgba(255, 255, 255, 1)",
        },
        "&:focus-within": {
            border: "1.5px solid rgba(255, 255, 255, 1)",
        }
    },
    sendButton: {
        borderRadius: 10,
        height: 45,
        width: 280,
        fontSize: "1rem"
    },

}))


export default function Contact(){
    const classes = useStyles();
    const theme = useTheme();

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [emailHelper, setEmailHelper] = useState("");
    const [phone, setPhone] = useState("");
    const [phoneHelper, setPhoneHelper] = useState("");
    const [message, setMessage] = useState("");
    
    const onChange = event => {
        let valid;

        switch (event.target.id) {
            case "email":
                setEmail(event.target.value)
                valid = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(
                    event.target.value
                )

                if (!valid) {
                    setEmailHelper("Invalid Email")
                } else {
                    setEmailHelper("");
                }
                break;
            case "phone":
                setPhone(event.target.value);
                valid = /^\(?([0-9]{4})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/.test(
                    event.target.value
                )

                if (!valid) {
                    setPhoneHelper("Invalid Phone")
                } else {
                    setPhoneHelper("");
                }
                break;
            default:
                break;
        }
    }
    
    return (
        <Box bgcolor="common.grey" className={classes.root}>
            <Grid container className={classes.background} justify="center">
                <Grid item container direction="column" alignItems="center" className={classes.body}>
                    <Grid item xs={3} style={{maxWidth: "100%"}}>
                        <Typography 
                            className={classes.title}
                            variant="h2"
                            style={{lineHeight: 0, marginTop: "2em"}}
                        >
                            Contact Us
                        </Typography>
                    </Grid>
                    <Grid item xs={9}>
                        <Grid container direction="column" justify="center" alignItems="center">
                            <Grid item>
                                <Typography
                                    variant="h5"
                                    className={classes.body1}
                                >
                                    Let's talk about anything.
                                </Typography>
                            </Grid>
                            <Grid item container justify="center" >
                                <Grid item>
                                    <PhoneIcon style={{color: "white", marginRight: "0.5em"}}/>
                                </Grid>
                                <Grid item>
                                    <Typography 
                                        className={classes.body2} 
                                        variant="h6"
                                    >
                                        <a href="tel:0995555777" style={{textDecoration: "none", color: "inherit"}}>099-5555-777</a>
                                    </Typography>
                                </Grid>
                            </Grid>
                            <Grid item container justify="center" style={{marginBottom: "2em"}}>
                                <Grid item>
                                    <EmailIcon style={{color: "white", marginRight: "0.5em"}}/>
                                </Grid>
                                <Grid item>
                                    <Typography 
                                        className={classes.body2} 
                                        variant="h6"
                                    >
                                        <a href="mailto:dmc.markr@gmail.com" style={{textDecoration: "none", color: "inherit"}}>dmc.markr@gmail.com</a>
                                    </Typography>
                                </Grid>
                            </Grid>
                            <Grid item container style={{maxWidth: "20em"}} spacing={2} direction="column" justify="center">
                                <Grid item>
                                    <TextField
                                        fullWidth
                                        label="Name"
                                        id="name"
                                        value={name}
                                        onChange={event => 
                                            setName(event.target.value)
                                        }
                                    />
                                </Grid>
                                <Grid item>
                                    <TextField
                                        fullWidth
                                        error={emailHelper.length !== 0}
                                        helperText={emailHelper}
                                        label="Email"
                                        id="email"
                                        value={email}
                                        onChange={onChange}
                                    />
                                </Grid>
                                <Grid item >
                                    <TextField
                                        fullWidth
                                        error={phoneHelper.length !== 0}
                                        helperText={phoneHelper}
                                        label="Phone"
                                        id="phone"
                                        value={phone}
                                        onChange={onChange}
                                    />
                                </Grid>
                                <Grid item >
                                <TextField
                                    fullWidth
                                    label="Message"
                                    InputProps={{disableUnderline: true}}
                                    value={message} 
                                    className={classes.message}
                                    multiline
                                    rows={10}
                                    onChange={event => 
                                        setMessage(event.target.value)
                                    }
                                    id="message"
                                />
                            </Grid>
                            <Grid item>
                                <Button
                                    disabled={
                                        name.length === 0 ||
                                        message.length === 0 ||
                                        email.length === 0 ||
                                        phone.length === 0 ||
                                        phoneHelper.length !== 0 ||
                                        emailHelper.length !== 0
                                    }
                                    className={classes.sendButton}
                                    variant="outlined"
                                    endIcon={<SendIcon/>}
                                >Send Message
                                
                                </Button>
                            </Grid>
                            </Grid>
                            
                        </Grid>
                    </Grid>
                </Grid>
                {/* <Grid item container direction="column" lg={6} className={classes.half}>
                            
                </Grid> */}
            </Grid>
        </Box>
    )
}