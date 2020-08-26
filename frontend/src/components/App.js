import React, { useState, useEffect } from 'react';

import { ThemeProvider } from "@material-ui/styles";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import axios from "axios";

import { isLoggedIn } from "../authentication/Auth";
import Header from "../common/Header";
import Footer from "../common/Footer";
import theme from "../common/Theme";
import HomePage from "../pages/home-page/HomePage";
import MoviePage from "../pages/movie-page/MoviePage";
import ContactPage from "../pages/contact-page/Contact";
import MovieDetailedPage from "../pages/movie-detailed-page/MovieDetailedPage"


function App() {
  const PAGINATION_SIZE = 20;
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [value, setValue] = useState(null);
  const [movies, setMovies] = useState([])
  const [pageSize, setPageSize] = useState(20);
  const [openSignIn, setOpenSignIn] = useState(false);


  useEffect(() => {
    let _pageSize = 20;
    axios.all([
        axios.get("/api/movies"),
    ])
    .then(axios.spread((_movies) => {
      
      if (_movies.status === 200) {
        setMovies(_movies.data)
        _pageSize = _movies.data.length / PAGINATION_SIZE
        setPageSize(_pageSize % 1 >= 0.5 ? Math.ceil(_pageSize) : Math.floor(_pageSize))
      }
      
    }))
    .catch(function (error) {
        console.log(error);
    })
  }, [setMovies])

  const getMovies = (page) => {
    let endIndex = PAGINATION_SIZE * page;
    let startIndex = endIndex - PAGINATION_SIZE
    return movies.slice(startIndex, endIndex)
  }

  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Header
        value={value}
        setValue={setValue}
        selectedIndex={selectedIndex}
        setSelectedIndex={setSelectedIndex}
        isLoggedIn={isLoggedIn()}
        openSignIn={openSignIn}
        setOpenSignIn={setOpenSignIn}
        />
        <Switch>
          <Route
            exact
            path="/"
            render={props => (
            <HomePage
              {...props}
              // nowShowing={movies}
            />
            )}
          />
          {[...Array(pageSize + 1)].map((x, index) =>
            <Route exact path={
                index === 1 ? "/movies" : `/movies/page/${index}`
              }
              component={()=> 
                <MoviePage
                pageSize={pageSize}
                page={index}
                movies={getMovies(index)}
                setValue={setValue}
                setSelectedIndex={setSelectedIndex}
                />
              }
            />
          )}
          <Route exact path="/movies/now-showing" component={()=> <div style={{height: "300px"}}>Now Showing</div>}/>
          <Route exact path="/movies/coming-soon" component={()=> <div style={{height: "300px"}}>Coming Soon</div>}/>
          <Route exact path="/movies/recommended" component={()=> <div style={{height: "300px"}}>Recommended Movies</div>}/>
          {movies.map((movie, index) => (
              <Route exact path={`/movie/${movie.id}`} component={()=><MovieDetailedPage 
                isLoggedIn={isLoggedIn()}
                openSignIn={openSignIn}
                setOpenSignIn={setOpenSignIn}
                setValue={setValue} movie={movie}/>}/>
          ))}
          <Route exact path="/cinemas" component={()=> <div style={{height: "300px"}}>Cinemas</div>}/>
          <Route exact path="/about" component={()=> <div style={{height: "300px"}}>About Us</div>}/>
          <Route exact path="/profile" component={()=> <div style={{height: "300px"}}>Profile</div>}/>
          <Route exact path="/ticket-seller" component={()=> <div style={{height: "300px"}}>Ticket Seller</div>}/>
          <Route
            exact
            path="/contact"
            render={props => (
            <ContactPage
              {...props}
            />
            )}
          />
        </Switch>
        <Footer
        value={value}
        setValue={setValue}
        selectedIndex={selectedIndex}
        setSelectedIndex={setSelectedIndex}
        />
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
