import React, { useState } from "react";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import {useTheme} from "@material-ui/core/styles";
import axios from "axios";
import Dialog from "@material-ui/core/Dialog";
import DialogContent from "@material-ui/core/DialogContent";
import { Typography } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import Divider from "@material-ui/core/Divider";
import Zoom from '@material-ui/core/Zoom';
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import VpnKeyIcon from '@material-ui/icons/VpnKey';


export default function SignInDialog(props) {
    const { isLoggedIn, openSignIn, setOpenSignIn } = props;
    const theme = useTheme();
    const matchesMd = useMediaQuery(theme.breakpoints.down("md"));
    const matchesSm = useMediaQuery(theme.breakpoints.down("sm"));
    const matchesXs = useMediaQuery(theme.breakpoints.down("xs"));
    const [openSignUp, setOpenSignUp] = useState(false);
    const [email, setEmail] = useState("");
    const [emailHelper, setEmailHelper] = useState("");
    const [password, setPassword] = useState("");
    const [passwordHelper, setPasswordHelper] = useState("");
    const [confirm_password, setConfirmPassword] = useState("");
    const [confirmPasswordHelper, setConfirmPasswordHelper] = useState("");
    const [first_name, setFirstName] = useState("");
    const [firstNameHelper, setFirstNameHelper] = useState("");
    const [last_name, setLastName] = useState("");
    const [lastNameHelper, setLastNameHelper] = useState("");
    const [barangay, setBarangay] = useState("");
    const [city, setCity] = useState("");
    const [province, setProvince] = useState("");
    const [phone, setPhone] = useState("");
    const [phoneHelper, setPhoneHelper] = useState("");


    const clearSignUp = () => {
        setFirstName("");
        setFirstNameHelper("");
        setLastName("");
        setLastNameHelper("");
        setEmail("");
        setEmailHelper("")
        setPhone("");
        setPhoneHelper("")
        setPassword("");
        setPasswordHelper("");
        setConfirmPassword("");
        setConfirmPasswordHelper("");
    }
    
    
    const clearLogin = () => {
        setEmail("");
        setEmailHelper("");
        setPassword("");
        setPasswordHelper("");
    }


    const handleUserLogin = () => {
        axios({
            method: "post",
            url: "/api/auth/login",
            data: {
                "email": email,
                "password": password
            }
        })
        .then(function (response) {
            const data = response.data
            localStorage.setItem('user', JSON.stringify(data))
            setOpenSignIn(false);
            clearLogin();
            if (isLoggedIn) {
                if (!!data.claims_id) {
                    axios.get(
                        `/api/cinema/${data.claims_id}`,
                        { headers: {"Authorization" : `Bearer ${JSON.parse(localStorage.getItem("user")).access_token}`} }
                    )
                }
            }
        })
        .catch(function (error) {
            console.log(error);
        })
    }


    const handleUserSignUp = () => {
        axios({
            method: "post",
            url: "/api/user/register",
            data: {
                "first_name": first_name,
                "last_name": last_name,
                "contact_no": phone,
                "account": {
                    "email": email,
                    "password": password,
                    "type": "regular"
                },
                "location": {
                    "barangay": {
                        "name": barangay,
                        "city": {
                            "name": city,
                            "province": {
                                "name": province
                            }
                        }
                    },
                    "longitude": "121.001",
                    "latitude": "14.28"
                }
            }
        })
        .then(function (response) {
            if (response.status === 201) {
            setOpenSignUp(false);
            clearSignUp();
            }
        })
        .catch(function (error) {
            console.log(error);
        })
        
    }


    const onChange = event => {
        let valid;

        switch (event.target.id) {
            case "first_name":
                setFirstName(event.target.value)
                valid = event.target.value.length !== 0
                if (!valid) {
                    setFirstNameHelper("This field is required.")
                } else {
                    setFirstNameHelper("");
                }
                break;
            case "last_name":
                setLastName(event.target.value)
                valid = event.target.value.length !== 0
                if (!valid) {
                    setLastNameHelper("This field is required.")
                } else {
                    setLastNameHelper("");
                }
                break;
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
            case "password":
                setPassword(event.target.value);
                valid = event.target.value.length > 8
                if (!valid) {
                    setPasswordHelper("Password must be 8 characters long.")
                } else {
                    setPasswordHelper("");
                }
                break;
            case "confirm_password":
                setConfirmPassword(event.target.value);
                valid = event.target.value === password
                if (!valid) {
                    setConfirmPasswordHelper("Password did not match.")
                } else {
                    setConfirmPasswordHelper("");
                }
                break;
            default:
                break;
        }
    }


    return (
        <React.Fragment>
            <Dialog
                onExit={() => {clearLogin(); clearSignUp();}}
                PaperProps={{style:
                {
                    paddingTop: matchesXs ? "2em" : "5em",
                    paddingBottom: matchesXs ? "2em" : "5em",
                    paddingLeft: matchesXs ? 0 : matchesSm ? "5em" : matchesMd ? "10em" : "15em",
                    paddingRight: matchesXs ? 0 : matchesSm ? "5em" : matchesMd ? "10em" : "15em"
                }}}
                style={{zIndex: 1302}}
                fullScreen={matchesXs}
                open={openSignIn} 
                onClose={() => {setOpenSignIn(false); setOpenSignUp(false);}}
            >
                <Zoom in={!openSignUp} style={{ transitionDelay: openSignUp ? '500ms': "0ms"}} mountOnEnter unmountOnExit>
                    <DialogContent hidden={openSignUp}>
                        <Grid container direction="column" spacing={1}>
                            <Grid item>
                                <Typography align="center" variant="h4" gutterBottom>
                                    Sign In
                                </Typography>
                            </Grid>
                            <Grid item style={{width: matchesXs ? "100%" : "20em"}}>
                                <TextField
                                    fullWidth
                                    autoComplete={false}
                                    error={emailHelper.length !== 0}
                                    helperText={emailHelper}
                                    label="Email"
                                    id="email"
                                    value={email}
                                    onChange={onChange}
                                />
                            </Grid>
                            <Grid item style={{width: matchesXs ? "100%" : "20em"}}>
                                <TextField
                                    fullWidth
                                    label="Password"
                                    id="password"
                                    value={password}
                                    type="password"
                                    onChange={onChange}
                                />
                            </Grid>
                            <Grid item container justify="space-between" alignItems="center" style={{marginTop: "2em"}}>
                                <Grid item>
                                    <Button
                                    variant="outlined"
                                    style={{width: "120px"}}
                                    onClick={() => setOpenSignIn(false)}
                                    >
                                        Cancel
                                    </Button>
                                </Grid>
                                <Grid item>
                                    <Button
                                        disabled={
                                            email.length === 0 ||
                                            password.length === 0 ||
                                            emailHelper.length !== 0
                                        }
                                        onClick={handleUserLogin}
                                        variant="outlined"
                                        style={{width: "120px"}}
                                        endIcon={<VpnKeyIcon/>}
                                    >Sign In
                                    
                                    </Button>
                                </Grid>
                            </Grid>
                            <Divider style={{marginTop: "3em", backgroundColor: "white", height: 1}}/>
                            <Grid item container justify="center" style={{marginTop: "1em"}}>
                                
                                <Grid item>
                                    <Button
                                        style={{width: "170px"}}
                                        variant="outlined"
                                        onClick={() => {setOpenSignUp(true); clearLogin();}}
                                    >
                                        Sign Up
                                    </Button>
                                </Grid>
                            </Grid>
                        </Grid>
                    </DialogContent>
                </Zoom>
                <Zoom in={openSignUp} style={{ transitionDelay: !openSignUp ? '500ms': "0ms"}} mountOnEnter unmountOnExit>
                    <DialogContent hidden={!openSignUp}>
                        <Grid container direction="column" alignItems="center" spacing={1}>
                            <Grid item>
                                <Typography align="center" variant="h4" gutterBottom>
                                    Sign Up
                                </Typography>
                            </Grid>
                            <Grid item style={{width: matchesXs ? "100%" : "20em"}}>
                                <TextField
                                    fullWidth
                                    autoComplete={false}
                                    required
                                    error={firstNameHelper.length !== 0}
                                    helperText={firstNameHelper}
                                    label="First Name"
                                    id="first_name"
                                    value={first_name}
                                    onChange={onChange}
                                />
                            </Grid>
                            <Grid item style={{width: matchesXs ? "100%" : "20em"}}>
                                <TextField
                                    fullWidth
                                    autoComplete={false}
                                    required
                                    error={lastNameHelper.length !== 0}
                                    helperText={lastNameHelper}
                                    label="Last Name"
                                    id="last_name"
                                    value={last_name}
                                    onChange={onChange}
                                />
                            </Grid>
                            <Grid item style={{width: matchesXs ? "100%" : "20em"}}>
                                <TextField
                                    fullWidth
                                    required
                                    autoComplete={false}
                                    error={emailHelper.length !== 0}
                                    helperText={emailHelper}
                                    label="Email"
                                    id="email"
                                    value={email}
                                    onChange={onChange}
                                />
                            </Grid>
                            <Grid item style={{width: matchesXs ? "100%" : "20em"}}>
                                <TextField
                                    fullWidth
                                    autoComplete={false}
                                    required
                                    error={phoneHelper.length !== 0}
                                    helperText={phoneHelper}
                                    label="Phone"
                                    id="phone"
                                    value={phone}
                                    onChange={onChange}
                                />
                            </Grid>
                            <Grid item style={{width: matchesXs ? "100%" : "20em"}}>
                                <TextField
                                    fullWidth
                                    required
                                    error={passwordHelper.length !== 0}
                                    helperText={passwordHelper}
                                    label="Password"
                                    id="password"
                                    value={password}
                                    type="password"
                                    onChange={onChange}
                                />
                            </Grid>
                            <Grid item style={{width: matchesXs ? "100%" : "20em"}}>
                                <TextField
                                    fullWidth
                                    required
                                    error={confirmPasswordHelper.length !== 0}
                                    helperText={confirmPasswordHelper}
                                    label="Confirm Password"
                                    id="confirm_password"
                                    value={confirm_password}
                                    type="password"
                                    onChange={onChange}
                                />
                            </Grid>
                            <Grid item container justify="space-between" alignItems="center" style={{marginTop: "2em"}}>
                                <Grid item>
                                    <Button
                                    variant="outlined"
                                    style={{width: "120px"}}
                                    onClick={() => {setOpenSignUp(false); clearSignUp();}}
                                    >
                                        Cancel
                                    </Button>
                                </Grid>
                                <Grid item>
                                    <Button
                                        disabled={
                                            email.length === 0 ||
                                            phone.length === 0 ||
                                            first_name.length === 0 ||
                                            last_name.length === 0 ||
                                            password.length < 8 ||
                                            confirm_password.length === 0 ||
                                            // barangay.length === 0 ||
                                            // city.length === 0 ||
                                            // province.length === 0 ||
                                            password.length === 0 ||
                                            emailHelper.length !== 0 ||
                                            phoneHelper.length !== 0 ||
                                            passwordHelper.length !== 0 ||
                                            confirmPasswordHelper.length !== 0
                                        }
                                        onClick={handleUserSignUp}
                                        variant="outlined"
                                        style={{width: "120px"}}
                                    >Sign Up
                                    </Button>
                                </Grid>
                            </Grid>
                        </Grid>
                    </DialogContent>
                </Zoom>
            </Dialog>
        </React.Fragment>
    )
}