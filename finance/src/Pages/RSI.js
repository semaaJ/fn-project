import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import Loading from '../components/Loading/Loading';
import Chart from '../components/Chart/Chart';
import Input from '../components/Input/Input';
import { getProfitPercentage, getPercentageChange } from './helpers';
import './ChartPage.css';

const API_URL = 'http://127.0.0.1:5000/';

const RSI  = () => {
    const [state, setState] = useState({ 
        loading: true,
        status: 'results',
        inputData: {
            graphPeriod: 100,
            rsiWindow: 14,
            rsiSell: 30,
            rsiBuy: 70,
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
                .then(r => setState({ ...state, loading: false, ...r.data }));
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
        const { portfolioValue, profitPercentage, trades } = state;

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
                    <h2>1,348</h2>
                </div>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Trade Win/Loss</h2>
                    <h2>789/592 (65%)</h2>
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
        .then(() => setState({ ...state, status: 'results'}))
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

    const mainData = state.close.reduce((acc, curr, ind) => {
        if (ind < state.inputData.graphPeriod) {
            acc.push({ name: ind + 1, close: curr.toFixed(2) })
        }
        return acc;
    }, []);

    const rsi = state.rsi.reduce((acc, curr, ind) => {
        if (ind < state.inputData.graphPeriod) {
            acc.push({ name: ind + 1, rsi: curr.toFixed(2), rsiEMA: state.rsiEMA[ind] })
        }
        return acc;
    }, []);


    console.log(state)
    return (
        <>
            <div className="section">
                {/* <div className="chartSelector">
                    { ["1D", "1W", "2W", "1M", "3M", "6M", "1Y", "5Y", "10Y", "All"].map(date => <div style={{ width: "25px" }} className="tabItem">{ date }</div>) }
                </div>  */}
                <h2>Relative Strength Index (RSI)</h2>  
                <Input    
                    label="Graph Period"
                    inputId="graphPeriod"
                    onChange={e => onInputChange(e, "graphPeriod")}
                    value={state.inputData.graphPeriod} 
                />                            
                <div className="mainContainer">
                    <div className="chartOuter">
                        <div className="chartContainer">
                            <h2 style={{ marginLeft: "70px"}}>Portfolio / Broker Value</h2>
                            <Chart data={portfolioData} lines={["portfolioValue", "portfolioCash"]} width={800} height={150} />
                        </div>
                        <div className="chartContainer">
                            <h2 style={{ marginLeft: "70px"}}>RSI EMA</h2>
                            <Chart data={mainData} lines={["close"]} width={800} height={300} />
                        </div>
                        <div className="chartContainer">
                            <h2 style={{ marginLeft: "70px"}}>RSI Value</h2>
                            <Chart data={rsi} width={800} height={150} lines={["rsi", "rsiEMA"]} />
                        </div>
                    </div>

                    <div className="chartSelectorContainer">
                        <div style={{ paddingTop: "25px" }} className="chartSelectorSection">
                            <h2 className="colourWhite">RSI Parameter</h2>
                            <Input 
                                label="RSI Buy Signal"
                                inputId="rsiBuy"
                                onChange={onInputChange}
                                value={state.inputData.rsiBuy} 
                            />
                        </div>
                        <div style={{ paddingTop: "25px" }} className="chartSelectorSection">
                            <h2 className="colourWhite">RSI Parameter</h2>
                            <Input 
                                label="RSI Sell Signal"
                                inputId="rsiSell"
                                onChange={onInputChange}
                                value={state.inputData.rsiSell}
                            />
                        </div>
                        <div style={{ paddingTop: "25px" }} className="chartSelectorSection">
                            <h2 className="colourWhite">RSI Parameter</h2>
                            <Input 
                                label="RSI Window" 
                                inputId="rsiWindow"
                                onChange={onInputChange} 
                                value={state.inputData.rsiWindow}
                            />
                        </div>

                        <div style={{ margin: "25px" }} onClick={() => onSubmit()} className="tabItem">Submit</div>

                        { state.status === 'submit' ? getSubmit() : state.status === "calculating" ? getCalculating() : getResults() }
                    </div>
                </div>              
            </div>
        </>
    )
}

export default RSI;