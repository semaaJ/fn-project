import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import Loading from '../components/Loading/Loading';
import Chart from '../components/Chart/Chart';
import Bar from '../components/Chart/Bar';
import './ChartPage.css';

const API_URL = 'http://127.0.0.1:5000/';

const ChartPage  = () => {
    const [state, setState] = useState({ loading: true });

    useEffect(() => {
        const fetchData = async () => {
            if (state.loading) {
                await fetch(`${API_URL}cache`)
                .then(resp => resp.json())
                .then(r => setState({ loading: false, ...r }));
            } else {
                await fetch(`${API_URL}current`)
                .then(resp => resp.json())
                .then(r => setState({ ...state, current: r }));
            }
        }

        const timer = setInterval(() => {
            fetchData();
        }, 300);    
        return () => clearTimeout(timer);
    }, [state.loading]);


    const formatData = (items, len) => {
        return state.history.date.reduce((acc, curr, ind) => {
            if (ind < len) {
                acc.push(Object.assign({ date: curr } , ...items.map(val => ({ [val]: state.history[val][ind] }))))
            }
            return acc;
        }, []);
    }

    if (state.loading) {
        return <Loading loadType={1} />
    };


    const len = 100;
    const min = Math.min(...state.history.close.slice(0, len)) - 25;
    const max = Math.max(...state.history.close.slice(0, len)) + 25;

    const volMin = Math.min(...state.history.volume.slice(0, len));
    const volMax = Math.max(...state.history.volume.slice(0, len));

    const history = formatData(['close', 'ema7', 'ema25', 'ema99'], len);
    const rsi = formatData(['rsi14'], len);
    const vol = formatData(['volume'], len);
    const mfi = formatData(['mfi'], len);

    return (
        <>
            <div className="section">
                <Menu 
                    current={state.current ? parseFloat(state.current.price).toFixed(2) : 0}
                    portfolio={state.portfolio}
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