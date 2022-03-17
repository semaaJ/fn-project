import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import Loading from '../components/Loading/Loading';
import Chart from '../components/Chart/Chart';
import Input from '../components/Input/Input';
import { getProfitPercentage, getPercentageChange } from './helpers';
import './ChartPage.css';

const API_URL = 'http://127.0.0.1:5000/';

const dayMapping = {
    "1D": 1,
    "1W": 7,
    "2W": 14,
    "1M": 31,
    "3M": 93,
    "6M": 186,
    "1Y": 365,
    "5Y": 365 * 5,
    "10Y": 365 * 10,
    "20Y": 365 * 20
}


const RSI  = () => {
    const [state, setState] = useState({ 
        loading: true,
        status: 'results',
        inputData: {
            graphPeriod: 365,
            rsiWindow: 9,
            rsiBuy: 30,
            rsiSell: 70,
        },
    });

    useEffect(() => {
        if (state.loading) {
            const fetchData = async () => {
                await fetch(`${API_URL}rsi?` + new URLSearchParams({
                        rsiWindow: state.inputData.rsiWindow,
                        rsiSell: state.inputData.rsiSell,
                        rsiBuy: state.inputData.rsiBuy
                    })
                )
                .then(resp => resp.json())
                .then(r => setState({ ...state, loading: false, ...r }));
            }
            fetchData();
        }
    });

    const getCalculating = () => (
        <div className="calculatingResults">
            <h2 className="colourWhite" style={{ marginTop: "25px" }}>Calculating Results..</h2>
            <Loading loadType={2} />
        </div>
    )
    
    const getSubmit = () => (
        <div className="calculatingResults">
            <h2 className="colourWhite" style={{ marginTop: "25px" }}>Submit parameters to see results...</h2>
        </div>
    )

    const getResults = () => {
        const { portfolioValue, profitPercentage, trades, totalTrades, positiveTrades, negativeTrades } = state;

        return (
            <>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Starting Equity</h2>
                    <h2>${ portfolioValue[0] }</h2>
                </div>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Ending Equity</h2>
                    <h2>${ portfolioValue[portfolioValue.length - 1].toFixed(2) }</h2>
                </div>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Profit Percentage</h2>
                    <h2>{ profitPercentage }%</h2>
                </div>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Total Trades</h2>
                    <h2>{ totalTrades }</h2>
                </div>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Trade Win/Loss</h2>
                    <h2>{ positiveTrades }/{ negativeTrades } ({ (positiveTrades / totalTrades).toFixed(2) * 100 }%)</h2>
                </div>

                <h2 style={{ marginLeft: "25px", marginTop: "15px" }} className="colourWhite">Trades Made</h2>
                <div className="log">
                    { trades.map(val => {
                        const date = val.split(" ")[0]
                        return (
                        <h2 style={{ fontSize: "8px"  }}><span className="colourWhite">{ date }</span> { val.split(" ").splice(1).join(" ")}</h2>)
                    })
                }
                </div>
            </>
        )
    }

    const onDateChange = (graphPeriod) => {
        setState({ ...state, inputData: { ...state.inputData, graphPeriod: dayMapping[graphPeriod] }})
    }

    const onInputChange = (e, target) => {
        setState({ 
            ...state,
            inputData: {
                ...state.inputData,
                [target]: e.target.value
            }
        })
    }

    const onSubmit = async () => {
        setState({ ...state, status: 'calculating' })
        await fetch(
            `${API_URL}rsi?` + new URLSearchParams({
                rsiWindow: state.inputData.rsiWindow,
                rsiSell: state.inputData.rsiSell,
                rsiBuy: state.inputData.rsiBuy
            })
        )
        .then(resp => resp.json())
        .then(r => setState({ ...state, status: 'results', ...r.data }))
    }

    if (state.loading) {
        return <Loading loadType={1} />
    };

    const portfolioData = state.portfolioValue.reduce((acc, curr, ind) => {
        if (ind < state.inputData.graphPeriod) {
            acc.push({ name: ind + 1, portfolioValue: curr, portfolioCash: state.portfolioCash[ind]})
        }
        return acc;
    }, [])

    const max = Math.max(...state.close.slice(0, state.inputData.graphPeriod));
    const min = Math.min(...state.close.slice(0, state.inputData.graphPeriod));

    const mainData = state.close.reduce((acc, curr, ind) => {
        if (ind < state.inputData.graphPeriod) {
            acc.push({ name: ind + 1, close: curr.toFixed(2), signal: state.signals[ind] })
        }
        return acc;
    }, []);

    const rsi = state.rsi.reduce((acc, curr, ind) => {
        if (ind < state.inputData.graphPeriod) {
            acc.push({ name: ind + 1, rsi: curr.toFixed(2), rsiEMA: state.rsiEMA[ind] })
        }
        return acc;
    }, []);

    return (
        <>
            <div className="section">
                <Menu />
            
                <div style={{ width: "80%", display: "flex" }}>
                    <div className="chartInfo">
                        <h1 style={{ fontSize: "32px"}}><span className="colourWhite">RSI</span> Relative Strength Index</h1>
                        <h2 style={{ textTransform: 'inherit'  }} className="colourWhite">Evaluates overbought or oversold conditions in the price of a stock or other asset.</h2>                 

                        <h2>Parameters: { state.inputData.rsiWindow } { state.inputData.rsiBuy } { state.inputData.rsiSell }</h2>
                        <h2>Trades: { state.totalTrades } +{ state.positiveTrades } -{ state.negativeTrades } {((state.positiveTrades/ state.totalTrades) * 100).toFixed(2)}%</h2>
                    </div>

                    <div className="chartInfo">
                        <h1 style={{ fontSize: "32px"}}><span className="colourWhite">RSI</span> Parameters</h1>
                        <div className="parameters">
                            <Input 
                                label="RSI Window"
                                inputId="rsiWindow"
                                onChange={onInputChange}
                                value={state.inputData.rsiWindow} 
                            />
                            <Input 
                                label="RSI Buy Signal"
                                inputId="rsiBuy"
                                onChange={onInputChange}
                                value={state.inputData.rsiBuy} 
                            />
                            <Input 
                            label="RSI Sell Signal"
                            inputId="rsiSell"
                            onChange={onInputChange}
                            value={state.inputData.rsiSell} 
                        />
                        </div>
                        <div style={{ marginLeft: "0px", marginRight: "0px", marginTop: "8px"}} className="tabItem" onClick={() => onSubmit()}>Submit</div>
                    </div>
                </div>
               
                <div className="mainContainer">
                    <div className="chartOuter">
                        <div className="chartContainer">
                            <h2 style={{ marginLeft: "70px"}}>SPY Close</h2>
                            <Chart max={max} min={min} data={mainData} lines={["close"]} width={"100%"} height={320} />
                        </div>
                        <div className="chartContainer">
                            <h2 style={{ marginLeft: "70px"}}>Portfolio / Broker Value</h2>
                            <Chart data={portfolioData} lines={["portfolioValue", "portfolioCash"]} width={800} height={100} />
                        </div>
                        <div className="chartContainer">
                            <h2 style={{ marginLeft: "70px"}}>RSI Value / EMA</h2>
                            <Chart data={rsi} width={"100%"} height={100} lines={["rsi", "rsiEMA"]} />
                        </div>
                    </div>
                </div>

                <div className="chartSelector">
                    { Object.keys(dayMapping).map(date => <div style={{ width: "25px" }} onClick={() => onDateChange(date)} className="tabItem">{ date }</div>) }
                </div>
            </div>              
        </>
    )
}

export default RSI;