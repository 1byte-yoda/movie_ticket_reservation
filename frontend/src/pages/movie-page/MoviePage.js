import React from "react";
import { Box } from '@material-ui/core';
import MovieCategoryList from "../../components/movie-category-list/MovieCategoryList";


export default function MoviePage(props) {
    const { pageSize, page, movies, setValue, setSelectedIndex } = props;

    return (
        <Box bgcolor="common.grey" p={2}>
            <MovieCategoryList
                setValue={setValue}
                pageSize={pageSize}
                page={page}
                movies={movies}
                setSelectedIndex={setSelectedIndex}
            />
        </Box>
    );
};
