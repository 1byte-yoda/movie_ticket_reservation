import { createMuiTheme } from "@material-ui/core/styles";

// 831010 292929 564d4d
const RED = "#292929";
const ORANGE = "#831010";
const WHITE = "	#ffffff";
const GREY = "#221f1f"

export default createMuiTheme({
    /* Centralized Color System */
    palette: {
        type: 'dark',
        common: {
            blue: `${RED}`,
            orange: `${ORANGE}`,
            white: `${WHITE}`,
            grey: `${GREY}`
        },
        primary: {
            main: `${RED}`
        },
        secondary: {
            main: `${ORANGE}`
        }
    },
    typography: {
        fontSize: 14,
        tab: {
            fontFamily: "Raleway",
            textTransform: "none",
            fontWeight: 700,
            fontSize: "1rem",
        },
        signIn: {
            fontFamily: "Pacifico",
            fontSize: "1rem",
            color: `${WHITE}`,
            textTransform: "none",
        },
        movie: {
            fontFamily: "Raleway",
            textTransform: "none",
            fontWeight: 550,
            fontSize: "1.5rem",
        },
        body1: {
            fontFamily: "Raleway",
            fontWeight: 500,
            lineHeight: 1.5,
            letterSpacing: "0.00938em",
            color: `${WHITE}`,
        },
        
    },
    text: {
        background: {
            default: `${GREY}`
        }
    },
    overrides: {
        MuiInputLabel: {
            root: {
                color: `${WHITE}`,
                fontSize: "1rem"
            },
        },
        MuiButton: {
            outlined: {
                border: `1.5px solid ${WHITE}`,
                opacity: 0.6,
                "&:hover": {
                    opacity: 1
                },
            }
            
        },
        MuiFormLabel: {
            root: {
                "&.Mui-focused": {
                    color: `${WHITE}`
                }
            }
        },
        MuiToggleButton: {
            sizeSmall: {
                padding: 7,
            }
        }
    }
});