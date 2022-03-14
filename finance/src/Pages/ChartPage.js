import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import Loading from '../components/Loading/Loading';
import Chart from '../components/Chart/Chart';
import Input from '../components/Input/Input';
import './ChartPage.css';

const API_URL = 'http://127.0.0.1:5000/';

const ChartPage  = () => {
    const [state, setState] = useState({ 
        loading: true,
        status: 'calculating',
        inputData: {
            graphPeriod: 100,
            lowEMA: 7,
            mediumEMA: 25,
            highEMA: 99     
        }
    });

    useEffect(() => {
        if (state.loading) {
            const fetchData = async () => {
                await fetch(`${API_URL}get`).then(resp => resp.json()).then(r => setState({ ...state, loading: false, ...r.data }));
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
            <h2 className="colourWhite" style={{ marginTop: "25px" }}>Calculating Results..</h2>
            <Loading loadType={2} />
        </div>
    )

    const getResults = () => {
        return (
            <>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Starting Equity</h2>
                    <h2>$100,000</h2>
                </div>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Ending Equity</h2>
                    <h2>$388,512.72</h2>
                </div>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Profit Percentage</h2>
                    <h2>388%</h2>
                </div>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Total Trades</h2>
                    <h2>1,348</h2>
                </div>
                <div className="chartSelectorSection">
                    <h2 className="colourWhite">Trade Win/Loss</h2>
                    <h2>789/592 (65%)</h2>
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
            `${API_URL}ema?` + new URLSearchParams({
                lowEMA: state.inputData.lowEMA,
                mediumEMA: state.inputData.mediumEMA,
                highEMA: state.inputData.highEMA
            })
        ).then(resp => resp.json())

    }

    if (state.loading) {
        return <Loading loadType={1} />
    };

    const mainData = state.close.reduce((acc, curr, ind) => {
        if (ind < state.inputData.graphPeriod) {
            acc.push({ 
                name: ind + 1, 
                close: curr.toFixed(2),
                lowEMA: state.lowEMA[ind].toFixed(2),
                mediumEMA: state.mediumEMA[ind].toFixed(2),
                highEMA: state.highEMA[ind].toFixed(2),
            })
        }
        return acc;
    }, []);

    const rsi = state.rsi.reduce((acc, curr, ind) => {
        if (ind < state.inputData.graphPeriod) {
            acc.push({ name: ind + 1, rsi: curr.toFixed(2) })
        }
        return acc;
    }, []);

    return (
        <>
            <div className="section">
                {/* <div className="chartSelector">
                    { ["1D", "1W", "2W", "1M", "3M", "6M", "1Y", "5Y", "10Y", "All"].map(date => <div style={{ width: "25px" }} className="tabItem">{ date }</div>) }
                </div>  */}
                <h2>Exponential Moving Average (EMA)</h2>  
                <Input    
                    label="Graph Period"
                    inputId="graphPeriod"
                    onChange={onInputChange}
                    value={state.inputData.graphPeriod} 
                />                            
                <div className="mainContainer">
                    <div className="chartOuter">
                        <div className="chartContainer">
                            <h2 style={{ marginLeft: "70px"}}>Portfolio / Broker Value</h2>
                            <Chart data={rsi} lines={["rsi"]} width={800} height={150} />
                        </div>
                        <div className="chartContainer">
                            <h2 style={{ marginLeft: "70px"}}>Close / 9 Day EMA / 25 Day EMA / 99 Day EMA</h2>
                            <Chart data={mainData} lines={["close", "lowEMA", "mediumEMA", "highEMA"]} width={800} height={300} />
                        </div>
                        <div className="chartContainer">
                            <h2 style={{ marginLeft: "70px"}}>RSI Value</h2>
                            <Chart data={rsi} width={800} height={150} lines={["rsi"]} />
                        </div>
                    </div>

                    <div className="chartSelectorContainer">
                        <div style={{ paddingTop: "25px" }} className="chartSelectorSection">
                            <h2 className="colourWhite">EMA Parameter</h2>
                            <Input 
                                label="EMA Low Period"
                                inputId="lowEMA"
                                onChange={onInputChange}
                                value={state.inputData.lowEMA} 
                            />
                        </div>
                        <div style={{ paddingTop: "25px" }} className="chartSelectorSection">
                            <h2 className="colourWhite">EMA Parameter</h2>
                            <Input 
                                inputId="mediumEMA"
                                label="EMA Medium Period"
                                onChange={onInputChange}
                                value={state.inputData.mediumEMA}
                            />
                        </div>
                        <div style={{ paddingTop: "25px" }} className="chartSelectorSection">
                            <h2 className="colourWhite">EMA Parameter</h2>
                            <Input 
                                label="EMA High Period" 
                                inputId="highEMA"
                                onChange={onInputChange} 
                                value={state.inputData.highEMA}
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

export default ChartPage;