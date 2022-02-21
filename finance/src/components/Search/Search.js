import React, { useState } from 'react';
import './Search.css';

const Search = () => {
    const [searchState, setSearchState] = useState({ message: 'Go', value: '', status: '' });

    const handleChange = (e) => setSearchState({ ...searchState, value: e.target.value });
    const onSubmit = () => {
        const fetchData = async () => {
            await fetch(`http://127.0.0.1:5000/${searchState.value}`)
            .then(resp => resp.json())
            .then(r => console.log(r))
        }

        fetchData();
    }

    return (
        <form id="search" className="searchContainer" action="/search" method="get">
            <input 
                className="searchBoxText"
                name="symbol"
                size="40"
                type="text"
                placeholder="Search"
                value={searchState.value} onChange={e => handleChange(e)}
            />
            <input className="searchBoxButton" value="Go" type="submit" onClick={() => onSubmit()}/>
        </form>
    )
}

export default Search;