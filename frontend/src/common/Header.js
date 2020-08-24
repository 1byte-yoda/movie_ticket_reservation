import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import {useTheme} from "@material-ui/core/styles";
import MenuItem from "@material-ui/core/MenuItem";
import AppBar from "@material-ui/core/AppBar";  // Layout everything in appbar into horizontal
import Toolbar from "@material-ui/core/Toolbar";
import Slide from "@material-ui/core/Slide";  // Sliding effect
import Zoom from '@material-ui/core/Zoom';
import useScrollTrigger from "@material-ui/core/useScrollTrigger";  // If the user scrolls
import { makeStyles } from "@material-ui/styles";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import Button from "@material-ui/core/Button";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";
import Divider from "@material-ui/core/Divider";
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

import logo from "../assets/logo.svg";
import {isLoggedIn} from "../authentication/Auth";

import SwipeableDrawer from '@material-ui/core/SwipeableDrawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

import Paper from '@material-ui/core/Paper';
import InputBase from '@material-ui/core/InputBase';
import SearchIcon from '@material-ui/icons/Search';

import ClickAwayListener from '@material-ui/core/ClickAwayListener';
import Grow from '@material-ui/core/Grow';
import Popper from '@material-ui/core/Popper';
import MenuList from '@material-ui/core/MenuList';
import Dialog from "@material-ui/core/Dialog";
import DialogContent from "@material-ui/core/DialogContent";
import { Typography } from "@material-ui/core";

import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import VpnKeyIcon from '@material-ui/icons/VpnKey';

/* Hide the AppBar on scroll */
function HideOnScroll(props) {
    const { children } = props;
    const trigger = useScrollTrigger();
    return (
      <Slide appear={false} direction="down" in={!trigger}>
        {children}
      </Slide>
    );
  }


const  useStyle = makeStyles(theme => ({
    toolbarMargin: {
        ...theme.mixins.toolbar,  // Height of the Toolbar component to fix elements hiding behind the AppBar
        marginBottom: "2em",
        backgroundColor: theme.text.background.default,
        [theme.breakpoints.down("md")]: {
            marginBottom: "1.4em",
        },
        [theme.breakpoints.down("sm")]: {
            marginBottom: "1em",
        },
    },
    tabContainer: {
        marginLeft: "0.25em"
    },
    logo: {
        height: "7em",
        width: "24em",
        [theme.breakpoints.down("md")]: {
            height: "6.2em",
            width: "21.2em",
        },
        [theme.breakpoints.down("sm")]: {
            height: "5.8em",
            width: "19.2em",
        },
        [theme.breakpoints.down("xs")]: {
            height: "5.35em",
            width: "18.35em",
        },
    },
    logoContainer: {
        padding: 0,
        "&:hover": {
            backgroundColor: "transparent"
        }
    },
    drawerHeader: {
        ...theme.mixins.toolbar,
        padding: "1.3em",
        marginTop: "1.3em",
        marginButton: "1.3em",
        marginLeft: "1em"
    },
    tab: {
        ...theme.typography.tab,
        minWidth: 8,
        marginLeft: "0.5em"
    },
    signInButton: {
        ...theme.typography.signIn,
        marginLeft: "1.5rem",
        marginRight: "1.5rem",
        height: "45px",
    },
    signOutButton: {
        marginLeft: "1.5rem",
        marginRight: "1.5rem",
        height: "45px",
    },
    searchFieldContainer: {
        padding: '0px 4px',
        borderRadius: "50px",
        marginLeft: "auto",
        marginBottom: "1em",
        marginTop: "1em",
        display: 'flex',
        width: "21em",
        height: "2.5em",
        [theme.breakpoints.down("md")]: {
            marginTop: "1em",
            marginLeft: ".6em",
            marginRight: ".6em",
        },
        [theme.breakpoints.down("sm")]: {
            width: "15em",
        },
    },
    searchField: {
        marginLeft: "1em",
        flex: 1,
    },
    searchButton: {
        padding: 10,
        [theme.breakpoints.down("sm")]: {
            padding: 5,
        },
    },
    categoriesMenu: {
        backgroundColor: theme.palette.common.blue,
        color: theme.palette.common.white,
        borderRadius: "0px",
        zIndex: 1302
    },
    categoriesMenuItem: {
        ...theme.typography.tab,
        opacity: 0.7,
        "&:hover": {
            opacity: 1
        }
    },
    drawerIconContainer: {
        marginLeft: "auto",
        "&:hover": {
            backgroundColor: "transparent"
        }
    },
    drawerIcon: {
        height: "40px",
        width: "40px",
        color: theme.palette.common.white,
    },
    drawer: {
        backgroundColor: theme.palette.common.blue,
        
    },
    drawerItem: {
        ...theme.typography.tab,
        color: theme.palette.common.white,
        opacity: 0.7
    },
    drawerSignIn: {
        backgroundColor: theme.palette.common.orange
    },
    drawerItemSelected: {
        "& .MuiListItemText-root":{
            opacity: 1
        }
    },
    appBar: {
        zIndex: theme.zIndex.modal + 1
    },
}))


export default function Header(props) {
    const classes = useStyle();
    const theme = useTheme();
    const iOS = process.browser && /iPad|iPhone|iPod/.test(navigator.userAgent);
    const matchesMd = useMediaQuery(theme.breakpoints.down("md"));
    const matchesSm = useMediaQuery(theme.breakpoints.down("sm"))
    const matchesXs = useMediaQuery(theme.breakpoints.down("xs"))
    const [openDrawer, setOpenDrawer] = useState(false);
    const [loggedIn, setLoggedIn] = useState(isLoggedIn());
    const [anchorEl, setAnchorEl] = useState(null);
    const [openMenu, setOpenMenu] = useState(false);
    const [openSignIn, setOpenSignIn] = useState(false);
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
    const [barangayHelper, setBarangayHelper] = useState("");
    const [city, setCity] = useState("");
    const [cityHelper, setCityHelper] = useState("");
    const [province, setProvince] = useState("");
    const [provinceHelper, setProvinceHelper] = useState("");
    const [phone, setPhone] = useState("");
    const [phoneHelper, setPhoneHelper] = useState("");
    
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
            case "barangay":
                setBarangay(event.target.value);
                valid = event.target.value.length !== 0
                if (!valid) {
                    setBarangayHelper("This field is required.")
                } else {
                    setBarangayHelper("");
                }
                break;
            case "city":
                setCity(event.target.value);
                valid = event.target.value.length !== 0
                if (!valid) {
                    setCityHelper("This field is required.")
                } else {
                    setCityHelper("");
                }
                break;
            case "province":
                setProvince(event.target.value);
                valid = event.target.value.length !== 0
                if (!valid) {
                    setProvinceHelper("This field is required.")
                } else {
                    setProvinceHelper("");
                }
                break;
            default:
                break;
        }
    }
    
    const clearLogin = () => {
        setEmail("");
        setEmailHelper("");
        setPassword("");
        setPasswordHelper("");
    }

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
        setBarangay("");
        setBarangayHelper("");
        setCity("");
        setCityHelper("");
        setProvince("");
        setProvinceHelper("");
    }

    const clearToken = () => {
        localStorage.removeItem("user");
    }

    const handleUserLogout = () => {
        setLoggedIn(false);
        clearToken();
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
            if (!!localStorage.user) {
              setLoggedIn(true); 
              setOpenSignIn(false);
              clearLogin();
              if (data.claims_id) {
                axios.get(`/api/cinema/${data.claims_id}`)
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
            const data = response.data
            if (response.status === 201) {
              setOpenSignUp(false);
              clearSignUp();
            }
        })
        .catch(function (error) {
            console.log(error);
        })
        
    }

    const handleChange = (event, newValue) => {
        props.setValue(newValue);
    }

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
        setOpenMenu(true)
    }

    const handleCategoryMenuItemClick = (event, index) => {
        setAnchorEl(null);
        setOpenMenu(false);
        props.setSelectedIndex(index);
    }

    const handleClose = (event) => {
        setAnchorEl(null); 
        setOpenMenu(false);
    }

    const handleListKeyDown = (event) => {
        if (event.key === 'Tab') {
          event.preventDefault();
          setOpenMenu(false);
        }
    }

    const handleClickMenuItem = (index, route, props) => {
        if (!loggedIn && !route.text.includes("Sign Out")) {
            setOpenDrawer(false);
            props.setValue(index);
            setOpenSignIn(route.text.includes("Sign In") ? true : false);
        } 
        if (loggedIn) {
            setOpenDrawer(false);
            if (route.text.includes("Sign Out")) {
                props.setValue(index);
                handleUserLogout();
            }
        }
    }

    const menuOptions = [
        {name: "Action Movies", link: "/movies/action", activeIndex: 1, selectedIndex: 0},
        {name: "Drama Movies", link: "/movies/drama", activeIndex: 1, selectedIndex: 1},
        {name: "Comedy Movies", link: "/movies/comedy", activeIndex: 1, selectedIndex: 2},
        {name: "Sci-fi Movies", link: "/movies/scifi", activeIndex: 1, selectedIndex: 3}
     ]

    const routes = [
        {text: "Home", activeIndex: 0, link: "/"},
        {text: "Movies", activeIndex: 1, link: "/movies", ariaOwns: anchorEl ? "simple-menu" : undefined, ariaPopup: anchorEl ? "true" : undefined, mouseOver: event => handleClick(event), mouseLeave: () => setOpenMenu(false)},
        {text: "Cinemas", activeIndex: 2, link: "/cinemas"},
        loggedIn ? 
          {text: "Profile", activeIndex: 3, link: "/profile"} 
        : {text: "About Us", activeIndex: 3, link: "/about"},
        // matches ? 
          {text: "Contact Us", activeIndex: 4, link: "/contact"},
        // : null,
        loggedIn ? 
          {text: "Sign Out", activeIndex: 0, link: "/"} 
        : {text: "Sign In", activeIndex: 0, link: ""}
    ]

    useEffect(() => {
        return () => {
          console.log("MOUNTED");
        };
      }, []);

    useEffect(() => {
        [...menuOptions, ...routes].forEach(route => {
            switch (window.location.pathname) {
                case `${route.link}`:
                    if (props.value !== route.activeIndex) {
                        props.setValue(route.activeIndex)
                        if (route.selectedIndex && route.selectedIndex !== props.selectedIndex) {
                            props.setSelectedIndex(route.selectedIndex);
                        }
                    }
                    break;
                default:
                    break;
            }
        })
    }, [props.value, menuOptions, props.selectedIndex, routes, props])

    useEffect(() => {
        return () => {
          console.log("UNMOUNT");
        };
      }, []);

    const tabs = (
        <React.Fragment>
            <Paper
                component="form"
                className={classes.searchFieldContainer}
                >
                    <InputBase
                        className={classes.searchField}
                        onClick={() => setOpenDrawer(false)}
                        placeholder="Search for Movies"
                        inputProps={{ 'aria-label': 'search movies' }}
                    />
                    <IconButton
                    type="submit"
                    className={classes.searchButton}
                    aria-label="search"
                    >
                        <SearchIcon />
                    </IconButton>
                </Paper>
            <Tabs
            value={props.value}
            onChange={handleChange}
            className={classes.tabContainer}
            indicatorColor="primary"
            >
                {routes.filter(route => !route.text.startsWith("Sign")).map((route, index) => (
                    <Tab
                    key={`${routes}${index}`}
                    component={Link}
                    to={route.link}
                    label={route.text}
                    className={classes.tab}
                    aria-owns={route.ariaOwns}
                    aria-haspopup={route.ariaPopup}
                    onMouseOver={route.mouseOver}
                    onMouseLeave={route.mouseLeave}>
                    </Tab>
                ))}
                {
                loggedIn ? 
                    <Tab
                    className={[classes.tab, classes.signOutButton]}
                    component={Link}
                    to="/"
                    label="Sign Out"
                    onClick={handleUserLogout}
                    /> :
                    <Button 
                    variant="contained"
                    // onClick={() => setLoggedIn(!loggedIn)}
                    onClick={() => setOpenSignIn(true)}
                    color="secondary"
                    className={classes.signInButton}
                    >
                        Sign In
                    </Button>
                }
            </Tabs>
            
            <Popper
            open={openMenu}
            anchorEl={anchorEl}
            placement="bottom-start"
            role={undefined}
            transition
            disablePortal
            >
            {({ TransitionProps, placement }) => (
                <Grow
                {...TransitionProps}
                style={{ transformOrigin: "top left"}}
                >
                <Paper
                classes={{root: classes.categoriesMenu}}
                elevation={0}
                keepMounted
                >
                    <ClickAwayListener onClickAway={handleClose}>
                    <MenuList
                    onMouseOver={() => setOpenMenu(true)}
                    onMouseLeave={handleClose}
                    disablePadding
                    autoFocusItem={false}
                    id="simple-menu"
                    onKeyDown={handleListKeyDown}
                    >
                    {menuOptions.map((option, index) => (
                        <MenuItem 
                        key={`${option}${index}`}
                        component={Link} 
                        to={option.link}
                        classes={{root: classes.categoriesMenuItem}}
                        onClick={event => {handleCategoryMenuItemClick(event, index); props.setValue(1); handleClose()}}
                        selected={index === props.selectedIndex && props.value === 1 && window.location.pathname !== "/categories"}
                        >
                            {option.name}
                        </MenuItem>
                    ))}
                    </MenuList>
                    </ClickAwayListener>
                </Paper>
                </Grow>
            )}
            </Popper>
        </React.Fragment>
    )
    
    const drawer = (
        <React.Fragment>
            <SwipeableDrawer
            open={openDrawer}
            onClose={() => setOpenDrawer(false)}
            onOpen={() => setOpenDrawer(true)}
            disableBackdropTransition={!iOS}
            disableDiscovery={iOS}
            classes={{paper: classes.drawer}}
            >
                <div className={classes.toolbarMargin}/>
                <Paper
                component="form"
                className={classes.searchFieldContainer}
                >
                    <InputBase
                        className={classes.searchField}
                        onClick={() => setOpenDrawer(true)}
                        placeholder="Search for Movies"
                        inputProps={{ 'aria-label': 'search movies' }}
                    />
                    <IconButton
                    type="submit"
                    className={classes.searchButton}
                    aria-label="search"
                    >
                        <SearchIcon />
                    </IconButton>
                </Paper>
                <List disablePadding>
                    {routes.map((route, index) => (
                        <ListItem
                        key={`${routes}${index}`}
                        selected={props.value === index}
                        classes={{selected: classes.drawerItemSelected}}
                        className={route.text === "Sign In" ? classes.drawerSignIn : null}
                        onClick={() => handleClickMenuItem(index, route, props)}
                        divider
                        button
                        component={route.text === "Sign In" ? ListItem : Link}
                        to={route.text === "Sign In" ? null : route.text}
                        >
                            <ListItemText
                            className={classes.drawerItem}
                            disableTypography
                            >   {route.text}
                            </ListItemText>
                        </ListItem>
                    ))}
                </List>

            </SwipeableDrawer>
            <IconButton
            className={classes.drawerIconContainer}
            onClick={() => setOpenDrawer(!openDrawer)}
            disableRipple
            >
                <MenuIcon className={classes.drawerIcon}/>
            </IconButton>
        </React.Fragment>
    )
    const signInDialog = (
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

    return (
        <React.Fragment>
            <HideOnScroll {...props}>
                <AppBar position="fixed" color="primary" className={classes.appBar}>
                    <Toolbar disableGutters> 
                        <Button 
                        component={Link} to="/" 
                        onMouseEnter={() => props.setValue(0)} 
                        className={classes.logoContainer}
                        disableRipple
                        >
                            <img className={classes.logo} alt="company logo" src={logo}/>
                        </Button>
                        
                        {matchesMd ? drawer : tabs}
                    </Toolbar>
                </AppBar>
            </HideOnScroll>
            <div className={classes.toolbarMargin}/>
            {signInDialog}
        </React.Fragment>
    )
}