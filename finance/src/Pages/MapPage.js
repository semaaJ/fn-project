import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import Map from '../components/Map/Map';
import Loading from '../components/Loading/Loading';

const API_URL = 'http://127.0.0.1:5000/';

const MapPage = () => {
    const [loading, setLoading] = useState(true)
    const [mapData, setMapData] = useState(null);
    
    useEffect(() => {
        const fetchData = async () => {
            if (mapData === null) {
                await fetch(`${API_URL}map`)
                    .then(resp => resp.json())
                    .then(r => setMapData(r));
                setLoading(false);
            }
        }
        fetchData();
    });
    

    console.log("MAP". mapData);
    if (loading) {
        return <Loading />
    }
    return (
        <>
            <div className="navBar">
                <Menu 
                    symbol={""}
                    todaysData={[]}
                    data={{}} 
                />
            </div>
            <Map mapData={mapData}/>
        </>
    )
}

export default MapPage;