import React from 'react';
import './Menu.css';

const Menu = (props) => {
    const {
        symbol, 
        todaysData,
        data
    } = props;

    const { 
        currentPrice,
        fiftyDayAverage,
        fiftyTwoWeekHigh,
        fiftyTwoWeekLow,
        fiftyTwoWeekChange,
        twoHundredDayAverage,
        grossProfits,
        industry,
        shortName,
        totalCash,
        totalDebt,
        totalRevenue,
        marketCap,
    } = data;

    const { open, close, low, high } = todaysData;

    return (
        <nav id="menu">
            <div className="menu-item">
                <div className="menu-text">
                    <a href="#">Back Test</a>
                </div>
                <div className="sub-menu">
                    <div className="icon-box">
                    <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="icon-box">
                    <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="icon-box">
                    <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="sub-menu-holder"></div>
                </div>
            </div>
            <div className="menu-item highlight">
                <div className="menu-text">
                    <a href="#">Models</a>
                </div>
                <div className="sub-menu double">
                    <div className="icon-box gb a">
                        <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="icon-box gb b">
                      <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="icon-box gb c">
                      <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="icon-box gb d">
                        <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="icon-box gb e">
                      <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="icon-box gb f">
                      <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="bottom-container">
                        Model Code <a href="#">View</a>
                    </div>
                    <div className="sub-menu-holder"></div>
                </div>
            </div>
            <div className="menu-item highlight">
                <div className="menu-text">
                    <a href="#">Info</a>
                </div>
                <div className="sub-menu triple">
                    <div className="top-container gb c icon-box">
                        <div className="text">
                            <div className="title colourMain">{ symbol } | { industry }</div>
                            <div className="sub-text">{ shortName }</div>
                            { marketCap && <div className="sub-text ">Market Cap: ${ marketCap.toLocaleString('en-US') }</div> }
                        </div>
                    </div>
                    <div className="box">
                        <h3 className="colourMain">Today</h3>
                        <a href="#">Open: { (open || 0).toFixed(2) }</a>
                        <a href="#">Close: { (close || 0).toFixed(2) }</a>
                        <a href="#">Low: { (low || 0).toFixed(2) }</a>
                        <a href="#">High: { (high || 0).toFixed(2) }</a>
                    </div>
                    <div className="box">
                        <h3 className="colourMain">Historical</h3>
                        <a href="#">50 Day Average: { fiftyDayAverage }</a>
                        <a href="#">200 Day Average: { twoHundredDayAverage }</a>
                        <a href="#">52 Week Low: { fiftyTwoWeekLow }</a>
                        <a href="#">52 Week High: { fiftyTwoWeekHigh }</a>
                    </div>
                    
                    { totalRevenue &&
                        <div className="icon-box flat">
                            <div className="text">
                                <div className="title">Total Revenue: ${ totalRevenue.toLocaleString('en-US') }</div>
                            </div>
                        </div>
                    }
                    { totalCash && 
                        <div className="icon-box flat">
                            <div className="text">
                                <div className="title">Total Cash: ${ totalCash.toLocaleString('en-US')  } </div>
                            </div>
                        </div>
                    }
                    { totalDebt &&
                        <div className="icon-box flat">
                            <div className="text">
                                <div className="title">Total Debt: ${ totalDebt.toLocaleString('en-US') }</div>
                            </div>
                        </div>
                    }
                    {
                        grossProfits && 
                            <div className="icon-box flat">
                                <div className="text">
                                    <div className="title">Gross Profits: ${ grossProfits.toLocaleString('en-US') }</div>
                                </div>
                            </div>
                    }
                </div>
            </div>
            <div className="menu-item">
                <div className="menu-text">
                    <a href="#">Lorem</a>
                </div>
                <div className="sub-menu">
                    <div className="icon-box">
                    <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="icon-box">
                    <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="icon-box">
                    <div className="text">
                            <div className="title">Lorem Ipsum</div>
                            <div className="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div className="sub-menu-holder"></div>
                </div>
            </div>

            <div id="sub-menu-container">
                <div id="sub-menu-holder">
                    <div id="sub-menu-bottom"></div>
                </div>
            </div>
        </nav>
    )
}

export default Menu;