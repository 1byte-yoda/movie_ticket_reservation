import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import {useTheme} from "@material-ui/core/styles";
import MenuItem from "@material-ui/core/MenuItem";
import AppBar from "@material-ui/core/AppBar";  // Layout everything in appbar into horizontal
import Toolbar from "@material-ui/core/Toolbar";
import Slide from "@material-ui/core/Slide";  // Sliding effect
import useScrollTrigger from "@material-ui/core/useScrollTrigger";  // If the user scrolls
import { makeStyles } from "@material-ui/styles";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import Button from "@material-ui/core/Button";
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

import logo from "../assets/logo.svg";
import SignInDialog from "../components/sign-in/SigninForm";

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
    const [openDrawer, setOpenDrawer] = useState(false);
    const [anchorEl, setAnchorEl] = useState(null);
    const [openMenu, setOpenMenu] = useState(false);

    const clearToken = () => {
        localStorage.removeItem("user");
    }

    const handleUserLogout = () => {
        clearToken();
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
        if (!props.isLoggedIn && !route.text.includes("Sign Out")) {
            setOpenDrawer(false);
            props.setValue(index);
            props.setOpenSignIn(route.text.includes("Sign In") ? true : false);
        } 
        if (props.isLoggedIn) {
            setOpenDrawer(false);
            if (route.text.includes("Sign Out")) {
                props.setValue(index);
                handleUserLogout();
            }
        }
    }

    const menuOptions = [
        {name: "Now Showing", link: "/movies/now-showing", activeIndex: 1, selectedIndex: 0},
        {name: "Coming Soon", link: "/movies/coming-soon", activeIndex: 1, selectedIndex: 1},
        {name: "Recommended Movies", link: "/movies/recommended", activeIndex: 1, selectedIndex: 2}
     ]

    const routes = [
        {text: "Home", activeIndex: 0, link: "/"},
        {text: "Movies", activeIndex: 1, link: "/movies", ariaOwns: anchorEl ? "simple-menu" : undefined, ariaPopup: anchorEl ? "true" : undefined, mouseOver: event => handleClick(event), mouseLeave: () => setOpenMenu(false)},
        props.isLoggedIn ? 
          {text: "Profile", activeIndex: 2, link: "/profile"} 
        : {text: "About Us", activeIndex: 2, link: "/about"},
          {text: "Contact Us", activeIndex: 3, link: "/contact"},
        props.isLoggedIn ? 
          {text: "Sign Out", activeIndex: 0, link: "/"} 
        : {text: "Sign In", activeIndex: 0, link: ""}
    ]

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
                props.isLoggedIn ? 
                    <Tab
                    className={[classes.tab, classes.signOutButton]}
                    component={Link}
                    to="/"
                    label="Sign Out"
                    onClick={handleUserLogout}
                    /> :
                    <Button 
                    variant="contained"
                    // onClick={() => props.setLoggedIn(!props.isLoggedIn)}
                    onClick={() => props.setOpenSignIn(true)}
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
                        to={route.text === "Sign In" ? null : route.link}
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
            <SignInDialog
                isLoggedIn={props.isLoggedIn}
                openSignIn={props.openSignIn}
                setOpenSignIn={props.setOpenSignIn}/>
        </React.Fragment>
    )
}