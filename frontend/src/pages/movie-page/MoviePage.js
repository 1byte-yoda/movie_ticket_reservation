import React, { Fragment } from "react";
import {Link} from "react-router-dom";
import { Box } from '@material-ui/core';
import MovieCategoryList from "../../components/movie-category-list/MovieCategoryList";


export default function MoviePage(props) {
    const { pageSize, page, movies, setValue } = props;

    return (
        <Box bgcolor="common.grey" p={2}>
            <MovieCategoryList setValue={setValue} pageSize={pageSize} page={page} movies={movies}/>
        </Box>
    );
};
