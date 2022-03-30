import React, { useState } from 'react';
import Input from '../Input/Input';
import { Select } from 'evergreen-ui';
import './Menu.css';

const API_URL = 'http://127.0.0.1:5000/';
const colourData = ["#fad30c", "#81ba4b"];

const Side = (props) => {
    const { symbol, currentPrices, setSelectedSymbol, results } = props;

    const [state, setState] = useState({ "orderType": null, "symbol": null, "amount": null, "buyPrice": null });

    const onInputChange = (e, target) => setState({ ...state, [target]: e.target.value })

    const onCreateOrder = async () => {
        const { orderType, symbol, amount, buyPrice } = state;
        await fetch(
            `${API_URL}order?` + new URLSearchParams({
                orderType,
                symbol,
                amount,
                buyPrice
            })
        )
        .then(resp => resp.json())
    }

    const onCloseOrder = async (tradeId) => {
        await fetch(`${API_URL}close?` + new URLSearchParams({ tradeId, price: currentPrices[symbol] }))
        .then(resp => resp.json())
    }

    const openTradeTotals = Object.keys(results.open).reduce((acc, tradeId) => {
        if (results.open[tradeId].orderType === 'buy') {
            acc += (currentPrices['BTCUSDT'] * results.open[tradeId].amount) - (results.open[tradeId].buyPrice * results.open[tradeId].amount)
        } else {
            acc += (results.open[tradeId].buyPrice * results.open[tradeId].amount) - (currentPrices['BTCUSDT'] * results.open[tradeId].amount)
        }
        return acc;
    }, 0);
    

    return (
        <div className="d-f-c sidemenu">
            <div className="pd-25">
                <div className="d-f al-c jc-sb">
                    <h1 className="fs-32"><span className="fc-w">{symbol.slice(0, 3)}</span>{symbol.slice(3)}</h1>
                    <div className="d-f al-c">
                        <h1 className="fs-32">${ currentPrices ? currentPrices[symbol].toFixed(2) : 0 }</h1>
                        <Select marginLeft={22} width="100px" value={symbol} onChange={e => setSelectedSymbol(e.target.value)}>
                            <option onClick={e => setSelectedSymbol(e, 'BTCUSDT')} value="BTCUSDT" selected>BTCUSDT</option>
                            <option onClick={e => setSelectedSymbol(e, 'LTCUSDT')} value="LTCUSDT">LTCUSDT</option>
                        </Select>
                    </div>
                </div>

                {/* <div className="d-f al-c jc-sb">
                    <h2 className="fc-w">${ portfolio.equity.toFixed(2) } / ${ portfolio.value.toFixed(2) } </h2>
                </div> */}
                
                {/* 
                    <div className="chartSelector">
                        { ["1D", "1W", "2W", "1M", "3M", "6M", "1Y", "5Y", "10Y", "All"].map(date => <div style={{ width: "25px" }} className="tabItem">{ date }</div>) }
                    </div>                           
                */}
                
                <h2 className="ta-c m-b-0 m-t-12 m-b-12">Make Order</h2>

                <div className="d-f jc-sb">
                    <Input onChange={onInputChange} inputId="orderType" value={state.orderType} label="Order Type" />
                    <Input onChange={onInputChange} inputId="symbol" value={state.symbol} label="Symbol" />
                    <Input onChange={onInputChange} inputId="amount" value={state.amount} label="Amount" />
                    <Input onChange={onInputChange} inputId="buyPrice" value={state.buyPrice} label="Buy Price" />
                </div>      
                <div onClick={() => onCreateOrder()} className="tabItem m-t-12">Create Order</div>
                
                <h2 className="ta-c m-t-30 m-b-18">Open Trades</h2>
                <table id="trades">
                    <tr>
                        <th>ID</th>
                        <th>Date</th>
                        <th>Type</th>
                        <th>Buy Price</th>
                        <th>Amount</th>
                        <th>$</th>
                        <th>%</th>
                        <th></th>
                    </tr>

                    {
                        Object.keys(results.open).map(tradeId => {
                            const trade = results.open[tradeId];

                            let profitLoss = 0;
                            let profitPercentage = 0;
                            if (trade.tradeType === 'buy') {
                                profitLoss = (currentPrices["BTCUSDT"] * trade.amount) - (trade.close * trade.amount)
                                profitPercentage = (currentPrices["BTCUSDT"] / trade.close)
                            } else if (trade.tradeType === 'sell') {
                                profitLoss = (trade.close * trade.amount) - (currentPrices["BTCUSDT"] * trade.amount)
                                profitPercentage = (trade.close / currentPrices["BTCUSDT"])
                            }
                            const tradeColour = profitLoss > 0 ? 'green' : 'red'; 

                            return (
                                <tr>
                                    <td>{ tradeId }</td>
                                    <td style={{ textTransform: "uppercase" }}>{ results.open[tradeId].date }</td>
                                    <td>{  results.open[tradeId].tradeType }</td>
                                    <td>${ results.open[tradeId].close.toFixed(2) }</td>
                                    <td>{ results.open[tradeId].amount }</td>
                                    <td className={tradeColour}>${ profitLoss.toFixed(2) }</td>
                                    <td className={tradeColour}>{ profitPercentage.toFixed(2) }%</td>
                                    <td className="menuDelete" onClick={() => onCloseOrder(tradeId)}>X</td>
                                </tr>
                            )
                        })
                    }
                    
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td className={openTradeTotals > 0 ? 'green' : 'red'}>${ openTradeTotals.toFixed(2) }</td>
                        <td></td>
                    </tr>
                </table>

                <h2 className="ta-c m-t-30 m-b-18">Closed Trades</h2>
                <table id="trades">
                    <tr>
                        <th>ID</th>
                        <th>Date</th>
                        <th>Buy Price</th>
                        <th>Sell Price</th>
                        <th>Amount</th>
                        <th>$</th>
                        <th>%</th>
                    </tr>
                    
                    {
                        Object.keys(results.closed).map(tradeId => {
                            const trade = results.closed[tradeId];

                            let profitPercentage = 0;
                            if (trade.tradeType === 'buy') {
                                profitPercentage = trade.buyPrice/ trade.sellPrice
                            } else if (trade.tradeType === 'sell') {
                                profitPercentage = trade.sellPrice / trade.buyPrice
                            }

                            const tradeColour = results.closed[tradeId].profit > 0 ? 'green' : 'red'; 
                            return (
                                <tr>
                                    <td>{ tradeId }</td>
                                    <td>{ results.closed[tradeId].date }</td>
                                    <td>${ results.closed[tradeId].buyPrice }</td>
                                    <td>${ results.closed[tradeId].sellPrice }</td>
                                    <td>{ results.closed[tradeId].amount }</td>
                                    <td className={tradeColour}>${ results.closed[tradeId].profit.toFixed(2)  }</td>
                                    <td className={tradeColour}>{ profitPercentage.toFixed(2) }%</td>
                                </tr>
                            )
                        })
                    }
                </table>
            </div>
        </div>
    )
}

export default Side;