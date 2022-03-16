import React, { useState, useEffect } from 'react';
import Loading from '../components/Loading/Loading';
import Menu from '../components/Menu/Menu';
import './Results.css';

const RESULTS_API_URL = 'http://127.0.0.1:5000/results'

const Results = () => {
    const [state, setState] = useState({ loading: true });

    useEffect(() => {
        if (state.loading) {
            const fetchData = async () => {
                await fetch(RESULTS_API_URL)
                    .then(r => r.json())
                    .then(d => setState({ ...state, results: d, loading: false }))
            }
            fetchData();
        }
    })


    console.log(state);

    if (state.loading) {
        return <Loading loadType={1} />
    }


    return (
        <div className="section">
            <Menu />
            <h2>Results</h2>
            <div className="chartSelector">
                <h2>Sort By</h2>
                <div className="tabItem">Profit %</div>
                <div className="tabItem">Trades Won</div>
                <div className="tabItem">Trades Lost</div>
            </div>

            <div className="resultsContainer">
                <table>
                    <thead>
                        <tr>
                            <th scope="col">Strategy</th>
                            <th scope="col">Parameters</th>
                            <th scope="col">Profit %</th>
                            <th scope="col">Total Trades</th>
                            <th scope="col">Positive Trades</th>
                            <th scope="col">Negative Trades</th>
                            <th scope="col">Trade %</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>

                    <tbody>
                        { state.results.map(result => {
                            return (
                                <tr>
                                    <td scope="row" data-label="Strategy">RSI</td>
                                    <td data-label="Parameters">{ `${result.rsiWindow}/${result.rsiBuy}/${result.rsiSell}` }</td>
                                    <td data-label="Profit Percentage">{ result.profitPercentage }</td>
                                    <td data-label="Total Trades">{ result.totalTrades }</td>
                                    <td data-label="Total Trades">{ result.positiveTrades }</td>
                                    <td data-label="Total Trades">{ result.negativeTrades }</td>
                                    <td data-label="Total Trades">{ (result.totalTrades / result.positiveTrades).toFixed(2) }%</td>
                                    <td data-label="Update"><div className="tabItem">Update</div></td>
                                </tr>
                            )
                        })
                    }
                    </tbody>
                </table>     
            </div>
        </div>
    )
}

export default Results;