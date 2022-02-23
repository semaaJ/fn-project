import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import Search from '../components/Search/Search';
import { Chart } from "react-google-charts";
import Loading from '../components/Loading/Loading';
import ShareTileContainer from '../components/ShareTileContainer/ShareTileContainer';
import { linearRegression, correlationCoefficient, getPercentageChange, sliceArr } from './helpers';

const API_URL = 'http://127.0.0.1:5000/';
const COIN_GECKO_API = 'https://api.coingecko.com/api/v3/';

const chartSelections = ["S&P", "LOBF"];

const Main  = () => {
    const [loading, setLoading] = useState(true);
    const [pageData, setPageData] = useState({ 
        selected: null, 
        selectedType: "equities", 
        dateRange: "All",
        data: { btc: {}, equities: {} },
    });

    const dateRangeMapping = {
        "1W": 7,
        "2W": 14,
        "1M": 31,
        "3M": 93,
        "6M": 186,
        "1Y": 280,
        "5Y": 1400,
        "10Y": 2400,
        "All": pageData.selected ? pageData.data[pageData.selectedType][pageData.selected].length : 100000
    }

    const sortCryptoData = (data) => {
        const formattedPrices = data.prices.map(val => val[0]);
        const formattedVolumes = data.total_volumes.map(val => val[1]);
        const formattedMarketCap = data.market_caps.map(val => val[1]);
        const date = data.prices.map(val => val[0]);

        return date.map((val, i) => { return { date: val, price: formattedPrices[i], volume: formattedVolumes[i], marketCap: formattedMarketCap[1]}})
    }

    useEffect(() => {
        const fetchEquityData = async () => {
            if (pageData.selected === null) {
                const [equities, btc] = await Promise.all([
                    await fetch(`${API_URL}cache`).then(resp => resp.json()),
                    await fetch(`${COIN_GECKO_API}coins/bitcoin/market_chart?vs_currency=usd&days=max&interval=daily`).then(resp => resp.json().then(r => sortCryptoData(r)))
                ]);

                setPageData({ ...pageData, selected: Object.keys(equities)[0], data: { crypto: { bitcoin: { historicalData: btc} }, equities }})
                setLoading(false);
            }
        }
        fetchEquityData();
    }, []);

    const setSelected = (val, type) => setPageData({ ...pageData, selectedType: type, selected: val});
    const setDateRange = (val) => setPageData({ ...pageData, dateRange: val });

    const renderPage = () => {        
        if (pageData.selected !== null) {
            const selected = pageData.data[pageData.selectedType][pageData.selected];
            const spyHistorical = pageData.data["equities"]["SPY"].historicalData;
            const historical = selected.historicalData;

            const spyData = spyHistorical.map(val => val.close).slice(spyHistorical.length - 1 - dateRangeMapping[pageData.dateRange]);
            const historicalClose = selected.historicalData.map(val => val.close).slice(historical.length - 1 - dateRangeMapping[pageData.dateRange]);
            
            const lineOfBestFit = spliceChart(linearRegression(historicalClose, Array.from(Array(historical.length).keys())), dateRangeMapping[pageData.dateRange]);
            const e1 = getPercentageChange(spyData[0], spyData[spyData.length - 1]);
            const e2 = getPercentageChange(historicalClose[0], historicalClose[historicalClose.length - 1]);
            const corr = correlationCoefficient(historicalClose, spyData);

            const mainChart = [...sliceArr(historical, dateRangeMapping[pageData.dateRange]).map((val, i) => 
                [val.date.split(" ")[0], val.close, lineOfBestFit[i], spyData[i]]
            )];

            const volumeChart = [...sliceArr(historical, dateRangeMapping[pageData.dateRange]).map(val => [val.date.split("-")[0], val.volume])];

            return (
                <>
                    <div className="navBar">
                        <Menu 
                            symbol={pageData.selected}
                            todaysData={historical[historical.length - 1]}
                            data={selected} 
                        />
                    </div>

                    <ShareTileContainer 
                        data={selected}
                        e1={e1.toFixed(2)}
                        e2={e2.toFixed(2)}
                        corr={corr.toFixed(2)}
                    />

                    {/* 
                    <div className="chartSelector">
                        { chartSelections.map(date => <div onClick={() => setDateRange(date)} className={`tabItem ${pageData.dateRange === date ? 'selected' : ''}`}>{ date }</div>) }
                    </div> 
                    */}
                    <div className="chartSelector">
                        { Object.keys(dateRangeMapping).map(date => <div onClick={() => setDateRange(date)} className={`tabItem ${pageData.dateRange === date ? 'selected' : ''}`}>{ date }</div>) }
                    </div>

                    <Chart
                        chartType="LineChart"
                        data={[["Date", "Close", "LOBF", "S&P"], mainChart]}
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
                        data={[["Date", "Vol"], volumeChart]}
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
    }

    return (
        loading ? <Loading /> : renderPage()
    )
}

export default Main;