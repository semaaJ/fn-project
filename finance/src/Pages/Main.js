import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import Search from '../components/Search/Search';
import { Chart } from "react-google-charts";
import Loading from '../components/Loading/Loading';

const API_URL = 'http://127.0.0.1:5000/'

const Main  = () => {
    const [loading, setLoading] = useState(true);
    const [tickerData, setTickerData] = useState({ selected: null, data: {} });

    useEffect(() => {
        const fetchData = async () => {
            if (tickerData.selected === null) {
                await fetch(`${API_URL}/cache`)
                .then(resp => resp.json())
                .then(r => setTickerData({ 
                    selected: Object.keys(r.data)[0],
                    data: r.data
                }));
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    const setSelected = (val) => {
        setTickerData({ data: tickerData.data, selected: val})
    }

    return (
        loading ? (
            <Loading />
        ) :
        (
            <>
                <Menu 
                    symbol={tickerData.selected}
                    todaysData={tickerData.data[tickerData.selected].historicalData[tickerData.data[tickerData.selected].historicalData.length - 1]}
                    data={tickerData.data[tickerData.selected]} 
                />

                {/* <div className="shareTitle">{ shortName }</div>
                <div className="shareSubtitle">${ close }</div>
                */}

                <Chart
                    chartType="LineChart"
                    data={[["Date", "Close"], ...tickerData.data[tickerData.selected].historicalData.map(val => [val.date.split("-")[0], val.close])]}
                    width="100%"
                    height="450px"
                    options={{
                        colors: ["white"],
                        backgroundColor: {
                            fill: '#11182f',
                        },
                        legend: {
                            textStyle: { color: '#FFF' },
                        },
                        hAxis: {
                            title: "Date",
                            titleTextStyle: { color: '#FFF' },
                            textStyle: { color: '#FFFFFF' },
                        },
                        vAxis: {
                            title: "Price $",
                            titleTextStyle: { color: '#FFF' },
                            textStyle:{ color: '#FFFFFF' }
                        },
                    }}
                />

                <div className="tabContainer">
                    {
                        tickerData.data[tickerData.selected].historicalData.map(name => <div onClick={() => setSelected(name)} className="tabItem">{ name }</div>)
                    }
                </div>   
                <Search />
            </>
        )
    )
}

export default Main;