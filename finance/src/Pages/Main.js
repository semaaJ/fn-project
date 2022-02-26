import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import Search from '../components/Search/Search';
import { Chart } from "react-google-charts";
import Loading from '../components/Loading/Loading';
import ShareTileContainer from '../components/ShareTileContainer/ShareTileContainer';
import { linearRegression } from './helpers';

const API_URL = 'http://127.0.0.1:5000/';

const Main  = () => {
    const [loading, setLoading] = useState(true);
    const [pageData, setPageData] = useState({ 
        selected: null, 
        selectedType: "equities", 
        dateRange: "10Y",
        data: { crypto: {}, equities: {} },
    });

    useEffect(() => {
        const fetchData = async () => {
            if (pageData.selected === null) {
                await fetch(`${API_URL}cache`)
                    .then(resp => resp.json())
                    .then(r => setPageData({ ...pageData, selected: Object.keys(r.equities)[0], data: { crypto: r.crypto, equities: r.equities }}));
                setLoading(false);
            }
        }
        fetchData();
    });

    const setSelected = (val, type) => setPageData({ ...pageData, selectedType: type, selected: val});
    const setDateRange = (val) => setPageData({ ...pageData, dateRange: val });

    const renderEquityChart = (selected, historical, spyHistorical) => {         
        let adjustedSelectedData = selected;
        if (spyHistorical.length - selected.length < 0) {
            adjustedSelectedData = selected.slice(Math.abs(spyHistorical.length - selected.length));
        }

        const lineOfBestFit = linearRegression(historical, Array.from(Array(selected.length).keys()));
        const mainChart = [...adjustedSelectedData.map((val, i) => [val.date.split(" ")[0], val.close, lineOfBestFit[i], spyHistorical[i]])];
        const volumeChart = [selected.map(val => [val.date.split(" ")[0], val.volume])];

        return (
            <>
                <Chart
                    chartType="LineChart"
                    data={[["Date", "Close", "LOBF", "S&P"], ...mainChart]}
                    width="100%"
                    height="350px"
                    options={{
                        colors: ['#0099ff', '#ffc107', '#ff0099'],
                        backgroundColor: {
                            fill: '#11182f',
                        },
                        legend: "none",
                        hAxis: {
                            title: "Date",
                            titleTextStyle: { color: '#FFF' },
                            textStyle: { color: '#FFFFFF' },
                        },
                        vAxis: {
                            titleTextStyle: { color: '#FFF' },
                            textStyle:{ color: '#FFFFFF' }
                        },
                    }}
                /> 
                <Chart
                    chartType="LineChart"
                    data={[["Date", "Vol"], ...volumeChart]}
                    width="1390px"
                    height="120px"
                    options={{
                        colors: ["#FFFFFF", '#0099ff'],
                        backgroundColor: {
                            fill: '#11182f',
                        },
                        legend: "none",
                        hAxis: {
                            titleTextStyle: { color: '#FFF' },
                            textStyle: { color: '#FFFFFF' },
                        },
                        vAxis: {
                            titleTextStyle: { color: '#FFF' },
                            textStyle:{ color: '#FFFFFF' },
                        },
                    }}
                /> 
            </>
        )
    }

    const renderCryptoChart = (selected, historical) => {
            const lineOfBestFit = linearRegression(historical, Array.from(Array(selected.length).keys()));
            const mainChart = [...selected.map((val, i) => [val.date.split(" ")[0], val.price, lineOfBestFit[i]])];
            const volumeChart = [...selected.map(val => [val.date.split(" ")[0], val.volume])];

            return (
               <>
                    <Chart
                        chartType="LineChart"
                        data={[["Date", pageData.selected, "LOBF"], ...mainChart]}
                        width="100%"
                        height="350px"
                        options={{
                            colors: ['#0099ff', '#ffc107', '#ff0099'],
                            backgroundColor: {
                                fill: '#11182f',
                            },
                            legend: "none",
                            hAxis: {
                                title: "Date",
                                titleTextStyle: { color: '#FFF' },
                                textStyle: { color: '#FFFFFF' },
                            },
                            vAxis: {
                                titleTextStyle: { color: '#FFF' },
                                textStyle:{ color: '#FFFFFF' }
                            },
                        }}
                    /> 
                    <Chart
                        chartType="LineChart"
                        data={[["Date", "Vol"], ...volumeChart]}
                        width="1390px"
                        height="120px"
                        options={{
                            colors: ["#FFFFFF", '#0099ff'],
                            backgroundColor: {
                                fill: '#11182f',
                            },
                            legend: "none",
                            hAxis: {
                                titleTextStyle: { color: '#FFF' },
                                textStyle: { color: '#FFFFFF' },
                            },
                            vAxis: {
                                titleTextStyle: { color: '#FFF' },
                                textStyle:{ color: '#FFFFFF' },
                            },
                        }}
                    /> 
                </>
            )
    }

    const refresh = () => {
        return 0;
    }

    if (loading) {
        return <Loading />
    };

    let historicalPrice = [];
    const selected = pageData.data[pageData.selectedType][pageData.selected].historicalData;
    const spyData = pageData.data["equities"]["SPY"].historicalData.map(val => val.close);

    if (pageData.selectedType === "equities") {
        historicalPrice = selected.map(val => val.close);
    } else if (pageData.selectedType === "crypto") {
        historicalPrice = selected.map(val => val.price);
    }

    return (
        <>
            <div className="navBar">
                <Menu 
                    symbol={pageData.selected}
                    todaysData={pageData.data[pageData.selectedType][pageData.selected].historicalData[pageData.data[pageData.selectedType][pageData.selected].historicalData.length - 1]}
                    data={pageData.data[pageData.selectedType][pageData.selected]} 
                />
            </div>

            <ShareTileContainer
                name={pageData.selected}
                type={pageData.selectedType}
                data={pageData.data[pageData.selectedType][pageData.selected]}
            />

            {/* 
            <div className="chartSelector">
                { chartSelections.map(date => <div onClick={() => setDateRange(date)} className={`tabItem ${pageData.dateRange === date ? 'selected' : ''}`}>{ date }</div>) }
            </div> 
            */}
            <div className="chartSelector">
                { ["1D", "1W", "2W", "1M", "3M", "6M", "1Y", "5Y", "10Y", "All"].map(date => <div onClick={() => setDateRange(date)} className={`tabItem ${pageData.dateRange === date ? 'selected' : ''}`}>{ date }</div>) }
            </div>

            { 
                pageData.selectedType === "equities" ?
                    renderEquityChart(selected, historicalPrice, spyData) : 
                    renderCryptoChart(selected, historicalPrice) 
            }

            <div className="tabContainer">
                    {
                        Object.keys(pageData.data.equities).map(name => <div onClick={() => setSelected(name, 'equities')} className={`tabItem ${pageData.selected === name ? 'selected' : ''}`}>{ name }</div>)
                    }
                </div>
                <div className="tabContainer">
                    {
                        Object.keys(pageData.data.crypto).map(name => <div onClick={() => setSelected(name, 'crypto')} className={`tabItem ${pageData.selected === name ? 'selected' : ''}`}>{ name }</div>)
                    }
                </div> 
            
            <Search />
        </>
    )
}

export default Main;