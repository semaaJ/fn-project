import React, { useState } from 'react';
import { Chart } from "react-google-charts";
import { FaRegArrowAltCircleUp } from "react-icons/fa";
import data from './data.json';
import './App.css';

function App() {
  const chartItems = Object.keys(data);
  const [chartSymbol, setChartSymbol] = useState(chartItems[0]);
  const setChart = (name) => setChartSymbol(name);
    
  const {
    shortName,
    industry,
    historicalData,
    fiftyTwoWeekLow,
    fiftyTwoWeekHigh,
    fiftyDayAverage,
    twoHundredDayAverage,
    totalRevenue,
    totalDebt,
    totalCash,
    grossProfits,
    marketCap
  } = data[chartSymbol];

  console.log(historicalData)

  const open = historicalData[historicalData.length - 1].open.toFixed(2);
  const close = historicalData[historicalData.length - 1].close.toFixed(2);
  const low = historicalData[historicalData.length - 1].low.toFixed(2);
  const high = historicalData[historicalData.length - 1].high.toFixed(2);

  const dayDifference = (open - close).toFixed(2);
  
  return (
      <div className="App">

        <form id="searchthis" action="/search" method="get">
          <input id="namanyay-search-box" name="q" size="40" type="text" placeholder="Search"/>
          <input id="namanyay-search-btn" value="Go" type="submit"/>
        </form>
        
        <nav id="menu">
            <div class="menu-item">
                <div class="menu-text">
                    <a href="#">Products</a>
                </div>
                <div class="sub-menu">
                    <div class="icon-box">
                    <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="icon-box">
                    <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="icon-box">
                    <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="sub-menu-holder"></div>
                </div>
            </div>
            <div class="menu-item highlight">
                <div class="menu-text">
                    <a href="#">Models</a>
                </div>
                <div class="sub-menu double">
                    <div class="icon-box gb a">
                        <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="icon-box gb b">
                      <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="icon-box gb c">
                      <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="icon-box gb d">
                        <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="icon-box gb e">
                      <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="icon-box gb f">
                      <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="bottom-container">
                        Model Code <a href="#">View</a>
                    </div>
                    <div class="sub-menu-holder"></div>
                </div>
            </div>
            <div class="menu-item highlight">
                <div class="menu-text">
                    <a href="#">Info</a>
                </div>
                <div class="sub-menu triple">
                    <div class="top-container gb c icon-box">
                        <div class="text">
                            <div class="title">{ chartSymbol } | { industry }</div>
                            <div class="sub-text">{ shortName }</div>
                            <div class="sub-text">Market Cap: ${ marketCap.toLocaleString('en-US') }</div>
                        </div>
                    </div>
                    <div class="box">
                        <h3>Today</h3>
                        <a href="#">Open: { open }</a>
                        <a href="#">Close: { close }</a>
                        <a href="#">Low: { low }</a>
                        <a href="#">High: { high }</a>
                    </div>
                    <div class="box">
                        <h3>Historical</h3>
                        <a href="#">50 Day Average: { fiftyDayAverage }</a>
                        <a href="#">200 Day Average: { twoHundredDayAverage}</a>
                        <a href="#">52 Week Low: { fiftyTwoWeekLow}</a>
                        <a href="#">52 Week High: { fiftyTwoWeekHigh}</a>
                    </div>
                    <div class="icon-box flat">
                        <div class="text">
                            <div class="title">Total Revenue: ${ totalRevenue.toLocaleString('en-US') } <i class="far fa-arrow-right"></i></div>
                        </div>
                    </div>
                    <div class="icon-box flat">
                        <div class="text">
                            <div class="title">Total Cash: ${ totalCash.toLocaleString('en-US')  }  <i class="far fa-arrow-right"></i></div>
                        </div>
                    </div>
                    <div class="icon-box flat">
                        <div class="text">
                            <div class="title">Total Debt: ${totalDebt.toLocaleString('en-US') } <i class="far fa-arrow-right"></i></div>
                        </div>
                    </div>
                    <div class="icon-box flat">
                        <div class="text">
                            <div class="title">Gross Profits: ${ grossProfits.toLocaleString('en-US') } <i class="far fa-arrow-right"></i></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="menu-item">
                <div class="menu-text">
                    <a href="#">Lorem</a>
                </div>
                <div class="sub-menu">
                    <div class="icon-box">
                    <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="icon-box">
                    <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="icon-box">
                    <div class="text">
                            <div class="title">Lorem Ipsum</div>
                            <div class="sub-text">Lorem ipsum dolor sit amet</div>
                        </div>
                    </div>
                    <div class="sub-menu-holder"></div>
                </div>
            </div>

            <div id="sub-menu-container">
                <div id="sub-menu-holder">
                    <div id="sub-menu-bottom">

                    </div>
                </div>
            </div>
        </nav>

        <Chart
          chartType="LineChart"
          data={[["Date", "Close"], ...historicalData.map(val => [val.date.split("-")[0], val.close])]}
          width="100%"
          height="450px"
          legendToggle
          options={{
            colors: ["white"],
            backgroundColor: {
                fill: '#11182f',
            },
            legend: {
                textStyle: { color: '#FFF' },
            },
            hAxis: {
                title: "Date",
                titleTextStyle: { color: '#FFF' },
                textStyle: { color: '#FFFFFF' },
            },
            vAxis: {
                title: "Price $",
                titleTextStyle: { color: '#FFF' },
                textStyle:{ color: '#FFFFFF' }
            },
        }}
        />

        <div className="tabContainer">
          {
            chartItems.map(name => <div onClick={() => setChart(name)} className="tabItem">{ name }</div>)
          }
        </div>  
      </div>

      
  );
}

export default App;
