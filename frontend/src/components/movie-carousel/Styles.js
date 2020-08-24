export default theme => ({
    container: {
      display: 'flex',
      alignItems: 'baseline'
    },
    h2: {
      fontSize: '2.5rem',
      fontWeight: 500,
      fontFamily: "Raleway",
      color:  theme.palette.text.primary,
      margin: theme.spacing(2.5, 1.5),
      textTransform: 'capitalize',
      [theme.breakpoints.down("md")]: {
        fontSize: '1.7rem',
        margin: theme.spacing(2, 1),
      }
    },
    button: {
      fontFamily: "Raleway",
      fontSize: "0.7em",
      color: theme.palette.info.main,
      [theme.breakpoints.down("md")]: {
        fontSize: '0.6rem',
      }
    },
    carousel: {
      marginBottom: theme.spacing(5),
      width: '100%',
      height: '35em',
    },
    arrow: {
      cursor: 'pointer',
      position: 'absolute',
      top: 0,
      bottom: 0,
      width: '10%',
      height: "50%",
      display: 'flex',
      alignItems: 'center',
      background: 'rgba(0,0,0,.5)',
      color:  theme.palette.common.white,
      opacity: 0.6,
      "&:hover": {
        opacity: 1
      },
      zIndex: 1,
      '&.prevArrow': {
        left: 0,
        justifyContent: 'flex-start',
        background:
          ' linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(0,0,37,0) 100%)',        
      },
      '&.nextArrow': {
        right: 0,
        justifyContent: 'flex-end',
        background:
          ' linear-gradient(90deg, rgba(0,0,37,0) 0%, rgba(0,0,0,1) 100%)',
      }
    },
  
    slider: {
      '& .slick-slide': {
        padding: theme.spacing(0.1)
      },
      "& .slick-center": { 
          img: {
            transform: "scale(1.1)"
        }
      }
    }
  });