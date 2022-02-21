import './Search.css';

const Search = () => {
    return (
        <form id="search" className="searchContainer" action="/search" method="get">
            <input className="searchBoxText" name="q" size="40" type="text" placeholder="Search"/>
            <input className="searchBoxButton" value="Go" type="submit"/>
        </form>
    )
}

export default Search;