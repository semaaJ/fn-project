import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import Menu from '../components/Menu/Menu';
import Loading from '../components/Loading/Loading';
import Chart from '../components/Chart/Chart';
import Bar from '../components/Chart/Bar';
import './ChartPage.css';

const API_URL = 'http://127.0.0.1:5000/';
const len = 250;


const ChartPage  = () => {
    const [state, setState] = useState({ loading: true, current: undefined, selectedSymbol: 'BTCUSDT' });

    const setSelectedSymbol = (symbol) => setState({ ...state, selectedSymbol: symbol });

    useEffect(() => {
        const fetchData = async () => {
            if (state.loading) {
                await fetch(`${API_URL}cache`)
                .then(resp => resp.json())
                .then(r => setState({ ...state, loading: false, ...r }));
            } else {
                await fetch(`${API_URL}current`)
                .then(resp => resp.json())
                .then(r => setState({  ...state, current: r }));
            }
        }

        const timer = setInterval(() => {
            fetchData();
        }, 600);
        return () => clearTimeout(timer);
    }, [state.loading, state.selectedSymbol]);


    const formatData = (items, len) => {
        const date = state.history[state.selectedSymbol].date.slice(state.history[state.selectedSymbol].date.length - len);

        return date.reduce((acc, curr, ind) => {
            if (ind < len) {
                acc.push(Object.assign({ date: curr } , ...items.map(val => ({ [val]: state.history[state.selectedSymbol][val][len + ind] }))))
            }
            return acc;
        }, []);
    }

    if (state.loading || state.current === undefined) {
        return <Loading loadType={1} />
    };

    const min = Math.min(...state.history[state.selectedSymbol].close.slice(0, len));
    const max = Math.max(...state.history[state.selectedSymbol].close.slice(0, len));

    const volMin = Math.min(...state.history[state.selectedSymbol].volume.slice(0, len));
    const volMax = Math.max(...state.history[state.selectedSymbol].volume.slice(0, len));

    const history = formatData(['close', 'ema7', 'ema25', 'ema99'], len);
    const vol = formatData(['volume'], len);

    const rsi = formatData(['rsi14', 'rsiSignal'], len).map(val => { return { date: val.date, rsi14: val.rsi14, signal: val.rsiSignal }});
    const mfi = formatData(['mfi', 'mfiSignal'], len).map(val => { return { date: val.date, mfi: val.mfi, signal: val.mfiSignal }});

    return (
        <>
            <Helmet>
                <title>{state.current ? `${state.selectedSymbol} - $${ parseFloat(state.current[state.selectedSymbol]).toFixed(2) }` : 'PaperTrader - Loading..'}</title>
            </Helmet>
            
            <div className="section">
                <Menu 
                    symbol={state.selectedSymbol}
                    currentPrices={state.current || {}}
                    setSelectedSymbol={setSelectedSymbol}
                    results={state.results}
                />


                <div className="d-f-c chartContainer">
                    <h2 className="ml-70">Close / 7D EMA / 25D EMA / 99D EMA</h2>
                    <Chart 
                        data={history} 
                        lines={["close", "ema7", "ema25", "ema99"]} 
                        width="100%" 
                        height={400} 
                        min={min} 
                        max={max} 
                    />
                    
                    <h2 className="ml-70">Volume</h2>
                    <Bar 
                        data={vol} 
                        width="100%" 
                        height={115}
                        min={volMin}
                        max={volMax}
                    />

                    <h2 className="ml-70">Relative Strength Index</h2>
                    <Chart 
                        data={rsi} 
                        lines={["rsi14"]} 
                        width="100%" 
                        height={115} 
                        min={0} 
                        max={100}
                        referenceLines={[30, 70]} 
                    />

                    <h2 className="ml-70">Money Flow Index</h2>
                    <Chart 
                        data={mfi} 
                        lines={["mfi"]} 
                        width="100%" 
                        height={115} 
                        min={0} 
                        max={100}
                        referenceLines={[20, 80]} 
                    />
                </div>
            </div>
        </>
    )
}

export default ChartPage;