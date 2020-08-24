import React from "react";
import { Box } from '@material-ui/core';
import MovieCarousel from "../../components/movie-carousel/MovieCarousel";

export default function HomePage(props) {
    const {
        nowShowing,
        comingSoon,
        suggested
    } = props;

    return (
        <Box bgcolor="common.grey" p={2} style={{height: "130em",}}>
            <Box height={30}/>
                <MovieCarousel movies={nowShowing} title="Now Showing" to="/"/>
            <Box height={30}/>
                <MovieCarousel movies={nowShowing} title="Trending in Cinemas" to="/"/>
            <Box height={30}/>
                <MovieCarousel movies={nowShowing} title="Recommended for you" to="/"/>
        </Box>
    );
};
