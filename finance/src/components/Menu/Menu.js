import React, { useState } from 'react';
import Input from '../Input/Input';
import './Menu.css';

const API_URL = 'http://127.0.0.1:5000/';

const Side = (props) => {
    const { current, portfolio } = props;
    const [state, setState] = useState({ "orderType": null, "amount": null, "buyPrice": null });

    const onInputChange = (e, target) => setState({ ...state, [target]: e.target.value })

    const onCreateOrder = async () => {
        const { orderType, amount, buyPrice } = state;
        await fetch(
            `${API_URL}order?` + new URLSearchParams({
                orderType,
                amount,
                buyPrice
            })
        ).then(resp => resp.json())
    }

    const onCloseOrder = async (tradeId) => {
        await fetch(`${API_URL}close?` + new URLSearchParams({ tradeId, current }))
        .then(resp => resp.json())
    }

    return (
        <div className="d-f-c sidemenu">
            <div className="pd-25">
                <div className="d-f al-c jc-sb">
                    <h1 className="fs-32"><span className="fc-w">BTC</span>USD</h1>
                    <h1 className="fs-32">${ current || 0 }</h1>
                </div>

                <div className="d-f al-c jc-sb">
                    <h2 className="fc-w">${ portfolio.equity.toFixed(2) } / ${ portfolio.value.toFixed(2) } </h2>
                </div>
                
                {/* 
                    <div className="chartSelector">
                        { ["1D", "1W", "2W", "1M", "3M", "6M", "1Y", "5Y", "10Y", "All"].map(date => <div style={{ width: "25px" }} className="tabItem">{ date }</div>) }
                    </div>                           
                */}
                
                <h2 className="ta-c m-b-0 m-t-12">Make Order</h2>
                <div className="d-f jc-sb">
                    <Input onChange={onInputChange} inputId="orderType" value={state.orderType} label="Order Type" />
                    <Input onChange={onInputChange} inputId="amount" value={state.amount} label="Amount" />
                    <Input onChange={onInputChange} inputId="buyPrice" value={state.buyPrice} label="Buy Price" />
                </div>      
                <div onClick={() => onCreateOrder()} className="tabItem m-t-12" style={{ width: "98%"}}>Create Order</div>
                
                <h2 className="ta-c m-t-30 m-b-18">Open Trades</h2>
                <table id="trades">
                    <tr>
                        <th>ID</th>
                        <th>Type</th>
                        <th>Buy Price</th>
                        <th>Amount</th>
                        <th>$</th>
                        <th>%</th>
                        <th></th>
                    </tr>
                    
                    {
                        Object.keys(portfolio.openTrades).map(tradeId => {
                            const { openTrades } = portfolio;

                            let profitLoss = 0;
                            let profitPercentage = 0;
                            if (openTrades[tradeId].orderType === 'buy') {
                                profitLoss = (current * openTrades[tradeId].amount) - (openTrades[tradeId].buyPrice * openTrades[tradeId].amount)
                                profitPercentage = (profitLoss / current) * 100 
                            } else {
                                profitLoss = (openTrades[tradeId].buyPrice * openTrades[tradeId].amount) - (current * openTrades[tradeId].amount)
                                profitPercentage = (profitLoss / current) * 100
                            }

                            return (
                                <tr>
                                    <td>{ tradeId }</td>
                                    <td style={{ textTransform: "uppercase" }}>{ openTrades[tradeId].orderType }</td>
                                    <td>${ openTrades[tradeId].buyPrice }</td>
                                    <td>{ openTrades[tradeId].amount }</td>
                                    <td>${ profitLoss.toFixed(2) }</td>
                                    <td>{ profitPercentage.toFixed(2) }%</td>
                                    <td onClick={() => onCloseOrder(tradeId)}>X</td>
                                </tr>
                            )
                        })
                    }
                </table>

                <h2 className="ta-c m-t-30 m-b-18">Closed Trades</h2>
                <table id="trades">
                    <tr>
                        <th>ID</th>
                        <th>Type</th>
                        <th>Buy Price</th>
                        <th>Sell Price</th>
                        <th>Amount</th>
                        <th>$</th>
                    </tr>
                    
                    {
                        Object.keys(portfolio.closedTrades).map(tradeId => {
                            const { closedTrades } = portfolio;
                            const tradeColour = closedTrades[tradeId].profitLoss > 0 ? 'green' : 'red'; 
                            return (
                                <tr>
                                    <td>{ tradeId }</td>
                                    <td style={{ textTransform: "uppercase" }}>{ closedTrades[tradeId].orderType }</td>
                                    <td>${ closedTrades[tradeId].buyPrice }</td>
                                    <td>${ closedTrades[tradeId].sellPrice }</td>
                                    <td>{ closedTrades[tradeId].amount }</td>
                                    <td className={tradeColour}>${ closedTrades[tradeId].profitLoss.toFixed(2)  }</td>
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