import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import Loading from '../components/Loading/Loading';
import Chart from '../components/Chart/Chart';
import Input from '../components/Input/Input';
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
    "3Y": 365 * 3,
    "5Y": 365 * 5,
    "10Y": 365 * 10,
    "20Y": 365 * 20
}


const EMA  = () => {
    const [state, setState] = useState({ 
        loading: true,
        status: 'results',
        inputData: {
            graphPeriod: 365,
            lowEMA: 7,
            mediumEMA: 25,
            highEMA: 99,
        },
    });

    useEffect(() => {
        if (state.loading) {
            const fetchData = async () => {
                await fetch(`${API_URL}ema?` + new URLSearchParams({
                        lowEMA: state.inputData.lowEMA,
                        mediumEMA: state.inputData.mediumEMA,
                        highEMA: state.inputData.highEMA
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
            `${API_URL}ema?` + new URLSearchParams({
                lowEMA: state.inputData.lowEMA,
                mediumEMA: state.inputData.mediumEMA,
                highEMA: state.inputData.highEMA
            })
        )
        .then(resp => resp.json())
        .then(r => setState({ ...state, status: 'results', ...r }))
    }

    if (state.loading) {
        return <Loading loadType={1} />
    };

    console.log(state)

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
            acc.push({ 
                name: ind + 1,
                close: curr.toFixed(2),
                lowEMA: state.lowEMA[ind],
                mediumEMA: state.mediumEMA[ind],
                highEMA: state.highEMA[ind],
                signal: state.signals[ind],
                crossover: "mediumEMA"          
            })
        }
        return acc;
    }, []);

    const ema = state.lowEMA.reduce((acc, curr, ind) => {
        if (ind < state.inputData.graphPeriod) {
            acc.push({ 
                name: ind + 1,
                lowEMA: curr,
                mediumEMA: state.mediumEMA[ind],
                highEMA: state.highEMA[ind],    
            })
        }
        return acc;
    }, []);

    return (
        <>
            <div className="section">
                <Menu />
            
                <div style={{ width: "80%", display: "flex" }}>
                    <div className="chartInfo">
                        <h1 style={{ fontSize: "32px"}}><span className="colourWhite">EMA</span> Exponential Moving Average</h1>
                        <h2 style={{ textTransform: 'inherit'  }} className="colourWhite">A moving average that places a greater weight and significance on the most recent data points.</h2>                 

                        <h2>Parameters: { state.inputData.lowEMA } { state.inputData.mediumEMA } { state.inputData.highEMA }</h2>
                        <h2>Trades: { state.totalTrades } +{ state.positiveTrades } -{ state.negativeTrades } {((state.positiveTrades/ state.totalTrades) * 100).toFixed(2)}%</h2>
                    </div>

                    <div className="chartInfo">
                        <h1 style={{ fontSize: "32px"}}><span className="colourWhite">EMA</span> Parameters</h1>
                        <div className="parameters">
                            <Input 
                                label="Low EMA"
                                inputId="lowEMA"
                                onChange={onInputChange}
                                value={state.inputData.lowEMA} 
                            />
                            <Input 
                                label="Medium EMA"
                                inputId="mediumEMA"
                                onChange={onInputChange}
                                value={state.inputData.mediumEMA} 
                            />
                            <Input 
                            label="High EMA"
                            inputId="highEMA"
                            onChange={onInputChange}
                            value={state.inputData.highEMA} 
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
                            <h2 style={{ marginLeft: "70px"}}>EMA 9D / 25D / 99D</h2>
                            <Chart data={ema} width={"100%"} height={100} lines={["lowEMA", "mediumEMA", "highEMA"]} />
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

export default EMA;