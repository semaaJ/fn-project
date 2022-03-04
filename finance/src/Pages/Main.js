import React, { useState, useEffect } from 'react';
import Menu from '../components/Menu/Menu';
import { Chart } from "react-google-charts";
import Map from '../components/Map/Map';
import Loading from '../components/Loading/Loading';
import ShareTileContainer from '../components/ShareTileContainer/ShareTileContainer';
import Table from '../components/Table/Table';
import { linearRegression } from './helpers';
import './Main.css';

const API_URL = 'http://127.0.0.1:5000/';
const LIVE_CRYPTO_URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=1h%2C24h%2C7d';
const COUNTRIES = {
    "AF": "Afghanistan",
    "AX": "Aland Islands",
    "AL": "Albania",
    "DZ": "Algeria",
    "AS": "American Samoa",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AQ": "Antarctica",
    "AG": "Antigua and Barbuda",
    "AR": "Argentina",
    "AM": "Armenia",
    "AW": "Aruba",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BS": "Bahamas",
    "BH": "Bahrain",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Belarus",
    "BE": "Belgium",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BT": "Bhutan",
    "BO": "Bolivia",
    "BQ": "Bonaire, Sint Eustatius and Saba",
    "BA": "Bosnia and Herzegovina",
    "BW": "Botswana",
    "BV": "Bouvet Island",
    "BR": "Brazil",
    "IO": "British Indian Ocean Territory",
    "BN": "Brunei Darussalam",
    "BG": "Bulgaria",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "KH": "Cambodia",
    "CM": "Cameroon",
    "CA": "Canada",
    "CV": "Cape Verde",
    "KY": "Cayman Islands",
    "CF": "Central African Republic",
    "TD": "Chad",
    "CL": "Chile",
    "CN": "China",
    "CX": "Christmas Island",
    "CC": "Cocos (Keeling) Islands",
    "CO": "Colombia",
    "KM": "Comoros",
    "CG": "Congo",
    "CD": "Congo, the Democratic Republic of the",
    "CK": "Cook Islands",
    "CR": "Costa Rica",
    "CI": "Cote D'Ivoire",
    "HR": "Croatia",
    "CU": "Cuba",
    "CW": "Curacao",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "EC": "Ecuador",
    "EG": "Egypt",
    "SV": "El Salvador",
    "GQ": "Equatorial Guinea",
    "ER": "Eritrea",
    "EE": "Estonia",
    "ET": "Ethiopia",
    "FK": "Falkland Islands (Malvinas)",
    "FO": "Faroe Islands",
    "FJ": "Fiji",
    "FI": "Finland",
    "FR": "France",
    "GF": "French Guiana",
    "PF": "French Polynesia",
    "TF": "French Southern Territories",
    "GA": "Gabon",
    "GM": "Gambia",
    "GE": "Georgia",
    "DE": "Germany",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GR": "Greece",
    "GL": "Greenland",
    "GD": "Grenada",
    "GP": "Guadeloupe",
    "GU": "Guam",
    "GT": "Guatemala",
    "GG": "Guernsey",
    "GN": "Guinea",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HT": "Haiti",
    "HM": "Heard Island and Mcdonald Islands",
    "VA": "Holy See (Vatican City State)",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IS": "Iceland",
    "IN": "India",
    "ID": "Indonesia",
    "IR": "Iran, Islamic Republic of",
    "IQ": "Iraq",
    "IE": "Ireland",
    "IM": "Isle of Man",
    "IL": "Israel",
    "IT": "Italy",
    "JM": "Jamaica",
    "JP": "Japan",
    "JE": "Jersey",
    "JO": "Jordan",
    "KZ": "Kazakhstan",
    "KE": "Kenya",
    "KI": "Kiribati",
    "KP": "Korea, Democratic People's Republic of",
    "KR": "Korea, Republic of",
    "XK": "Kosovo",
    "KW": "Kuwait",
    "KG": "Kyrgyzstan",
    "LA": "Lao People's Democratic Republic",
    "LV": "Latvia",
    "LB": "Lebanon",
    "LS": "Lesotho",
    "LR": "Liberia",
    "LY": "Libyan Arab Jamahiriya",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MO": "Macao",
    "MK": "Macedonia, the Former Yugoslav Republic of",
    "MG": "Madagascar",
    "MW": "Malawi",
    "MY": "Malaysia",
    "MV": "Maldives",
    "ML": "Mali",
    "MT": "Malta",
    "MH": "Marshall Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MU": "Mauritius",
    "YT": "Mayotte",
    "MX": "Mexico",
    "FM": "Micronesia, Federated States of",
    "MD": "Moldova, Republic of",
    "MC": "Monaco",
    "MN": "Mongolia",
    "ME": "Montenegro",
    "MS": "Montserrat",
    "MA": "Morocco",
    "MZ": "Mozambique",
    "MM": "Myanmar",
    "NA": "Namibia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Netherlands",
    "AN": "Netherlands Antilles",
    "NC": "New Caledonia",
    "NZ": "New Zealand",
    "NI": "Nicaragua",
    "NE": "Niger",
    "NG": "Nigeria",
    "NU": "Niue",
    "NF": "Norfolk Island",
    "MP": "Northern Mariana Islands",
    "NO": "Norway",
    "OM": "Oman",
    "PK": "Pakistan",
    "PW": "Palau",
    "PS": "Palestinian Territory, Occupied",
    "PA": "Panama",
    "PG": "Papua New Guinea",
    "PY": "Paraguay",
    "PE": "Peru",
    "PH": "Philippines",
    "PN": "Pitcairn",
    "PL": "Poland",
    "PT": "Portugal",
    "PR": "Puerto Rico",
    "QA": "Qatar",
    "RE": "Reunion",
    "RO": "Romania",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "BL": "Saint Barthelemy",
    "SH": "Saint Helena",
    "KN": "Saint Kitts and Nevis",
    "LC": "Saint Lucia",
    "MF": "Saint Martin",
    "PM": "Saint Pierre and Miquelon",
    "VC": "Saint Vincent and the Grenadines",
    "WS": "Samoa",
    "SM": "San Marino",
    "ST": "Sao Tome and Principe",
    "SA": "Saudi Arabia",
    "SN": "Senegal",
    "RS": "Serbia",
    "CS": "Serbia and Montenegro",
    "SC": "Seychelles",
    "SL": "Sierra Leone",
    "SG": "Singapore",
    "SX": "Sint Maarten",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "SB": "Solomon Islands",
    "SO": "Somalia",
    "ZA": "South Africa",
    "GS": "South Georgia and the South Sandwich Islands",
    "SS": "South Sudan",
    "ES": "Spain",
    "LK": "Sri Lanka",
    "SD": "Sudan",
    "SR": "Suriname",
    "SJ": "Svalbard and Jan Mayen",
    "SZ": "Swaziland",
    "SE": "Sweden",
    "CH": "Switzerland",
    "SY": "Syrian Arab Republic",
    "TW": "Taiwan, Province of China",
    "TJ": "Tajikistan",
    "TZ": "Tanzania, United Republic of",
    "TH": "Thailand",
    "TL": "Timor-Leste",
    "TG": "Togo",
    "TK": "Tokelau",
    "TO": "Tonga",
    "TT": "Trinidad and Tobago",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TM": "Turkmenistan",
    "TC": "Turks and Caicos Islands",
    "TV": "Tuvalu",
    "UG": "Uganda",
    "UA": "Ukraine",
    "AE": "United Arab Emirates",
    "GB": "United Kingdom",
    "US": "United States",
    "UM": "United States Minor Outlying Islands",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VU": "Vanuatu",
    "VE": "Venezuela",
    "VN": "Viet Nam",
    "VG": "Virgin Islands, British",
    "VI": "Virgin Islands, U.s.",
    "WF": "Wallis and Futuna",
    "EH": "Western Sahara",
    "YE": "Yemen",
    "ZM": "Zambia",
    "ZW": "Zimbabwe"
};

const Main  = () => {
    const [state, setState] = useState({ 
        selected: null, 
        selectedType: "equities", 
        dateRange: "10Y",
        data: { crypto: {}, equities: {} },
        loading: true,
        selectedCountry: 'RU',
        cryptoTable: null,
    });

    useEffect(() => {
        const fetchData = async () => {
            if (state.selected === null) return await fetch(`${API_URL}cache`).then(resp => resp.json());
        }

        const fetchLiveCrypto = async () => {
            if (state.selected == null) return await fetch(LIVE_CRYPTO_URL)
                .then(resp => resp.json())
                .then(res => res.map(r => { return { 
                    name: r.id,
                    symbol: r.symbol,
                    // ath: r.ath,
                    // athChangePercentage: r.ath_change_percentage,
                    // atl: r.atl,
                    // atlChangePercentage: r.atl_change_percentage,
                    "Current Price": r.current_price,
                    "24h Low": r.low_24h,
                    "24h High": r.high_24h,
                    "Market cap": r.market_cap,
                    // marketCap24hChange: r.market_cap_change_percentage_24h,
                    "24h Change": r.price_change_24h.toFixed(2),
                    "7D %": r.price_change_percentage_7d_in_currency.toFixed(2)
                }})
            )
        }

        Promise.all([fetchData(), fetchLiveCrypto()]).then(results => setState({ 
            ...state,
            selected: Object.keys(results[0].equities)[0],
            data: {
                crypto: results[0].crypto,
                equities: results[0].equities
            },
            cryptoTable: results[1],
            loading: false
        }));
    });

    const setSelected = (val, type) => setState({ ...state, selectedType: type, selected: val});
    const setDateRange = (val) => setState({ ...state, dateRange: val });

    const renderHistoricalTrendData = () => {
        const data = [...state.data[state.selectedType][state.selected].googleTrends.historicalTrendData]
        return (
            <Chart
                chartType="LineChart"
                data={[["Date", state.selected,], ...data]}
                height="230px"
                width="100%"
                options={{
                    colors: ['#0099ff', '#ffc107', '#ff0099'],
                    backgroundColor: {
                        fill: '#11182f',
                    },
                    legend: "none",
                    hAxis: {
                        titleTextStyle: { color: '#FFF' },
                        textStyle: { color: '#FFFFFF' },
                    },
                    vAxis: {
                        titleTextStyle: { color: '#FFF' },
                        textStyle:{ color: '#FFFFFF' }
                    },
                }}
            /> 
        )
    }

    const renderEquityChart = (selected, historical, spyHistorical) => {         
        let adjustedSelectedData = selected;
        if (spyHistorical.length - selected.length < 0) {
            adjustedSelectedData = selected.slice(Math.abs(spyHistorical.length - selected.length));
        }

        const lineOfBestFit = linearRegression(historical, Array.from(Array(selected.length).keys()));
        const mainChart = [...adjustedSelectedData.map((val, i) => [val.date.split(" ")[0], val.close, lineOfBestFit[i], spyHistorical[i]])];
        const volumeChart = [...selected.map(val => [val.date.split(" ")[0], val.volume])];

        return (
            <>
                <Chart
                    chartType="LineChart"
                    data={[["Date", "Close", "LOBF", "S&P"], ...mainChart]}
                    width="100%"
                    height="350px"
                    loading={<Loading />}
                    options={{
                        colors: ['#0099ff', '#ffc107', '#ff0099'],
                        backgroundColor: {
                            fill: '#11182f',
                        },
                        legend: "none",
                        hAxis: {
                            title: "Date",
                            titleTextStyle: { color: '#FFF' },
                            textStyle: { color: '#FFFFFF' },
                        },
                        vAxis: {
                            titleTextStyle: { color: '#FFF' },
                            textStyle:{ color: '#FFFFFF' }
                        },
                    }}
                /> 
                <Chart
                    chartType="LineChart"
                    data={[["Date", "Vol"], ...volumeChart]}
                    width="1390px"
                    height="120px"
                    options={{
                        colors: ["#FFFFFF", '#0099ff'],
                        backgroundColor: {
                            fill: '#11182f',
                        },
                        legend: "none",
                        hAxis: {
                            titleTextStyle: { color: '#FFF' },
                            textStyle: { color: '#FFFFFF' },
                        },
                        vAxis: {
                            titleTextStyle: { color: '#FFF' },
                            textStyle:{ color: '#FFFFFF' },
                        },
                    }}
                /> 
            </>
        )
    }

    const renderCryptoChart = (selected, historical) => {
            const lineOfBestFit = linearRegression(historical, Array.from(Array(selected.length).keys()));
            const mainChart = [...selected.map((val, i) => [val.date.split(" ")[0], val.price, lineOfBestFit[i]])];
            const volumeChart = [...selected.map(val => [val.date.split(" ")[0], val.volume])];

            return (
               <>
                    <Chart
                        chartType="LineChart"
                        data={[["Date", state.selected, "LOBF"], ...mainChart]}
                        width="100%"
                        height="350px"
                        options={{
                            colors: ['#0099ff', '#ffc107', '#ff0099'],
                            backgroundColor: {
                                fill: '#11182f',
                            },
                            legend: "none",
                            hAxis: {
                                title: "Date",
                                titleTextStyle: { color: '#FFF' },
                                textStyle: { color: '#FFFFFF' },
                            },
                            vAxis: {
                                titleTextStyle: { color: '#FFF' },
                                textStyle:{ color: '#FFFFFF' }
                            },
                        }}
                    /> 
                    <Chart
                        chartType="LineChart"
                        data={[["Date", "Vol"], ...volumeChart]}
                        width="1390px"
                        height="120px"
                        options={{
                            colors: ["#FFFFFF", '#0099ff'],
                            backgroundColor: {
                                fill: '#11182f',
                            },
                            legend: "none",
                            hAxis: {
                                titleTextStyle: { color: '#FFF' },
                                textStyle: { color: '#FFFFFF' },
                            },
                            vAxis: {
                                titleTextStyle: { color: '#FFF' },
                                textStyle:{ color: '#FFFFFF' },
                            },
                        }}
                    /> 
                </>
            )
    }

    if (state.loading) {
        return <Loading />
    };

    let historicalPrice = [];
    const selected = state.data[state.selectedType][state.selected].historicalData;
    const spyData = state.data["equities"]["SPY"].historicalData.map(val => val.close);

    if (state.selectedType === "equities") {
        historicalPrice = selected.map(val => val.close);
    } else if (state.selectedType === "crypto") {
        historicalPrice = selected.map(val => val.price);
    }

    console.log(state);
    return (
        <>
            <div className="section">
                <Menu 
                    symbol={state.selected}
                    todaysData={state.data[state.selectedType][state.selected].historicalData[state.data[state.selectedType][state.selected].historicalData.length - 1]}
                    data={state.data[state.selectedType][state.selected]} 
                />

                <ShareTileContainer
                    name={state.selected}
                    type={state.selectedType}
                    data={state.data[state.selectedType][state.selected]}
                    menu={ <Menu 
                        symbol={state.selected}
                        todaysData={state.data[state.selectedType][state.selected].historicalData[state.data[state.selectedType][state.selected].historicalData.length - 1]}
                        data={state.data[state.selectedType][state.selected]} 
                    />}
                />

                <div className="chartSelector">
                    { ["1D", "1W", "2W", "1M", "3M", "6M", "1Y", "5Y", "10Y", "All"].map(date => <div style={{ width: "25px" }} onClick={() => setDateRange(date)} className={`tabItem ${state.dateRange === date ? 'selected' : ''}`}>{ date }</div>) }
                </div>
                
                { 
                    state.selectedType === "equities" ?
                        renderEquityChart(selected, historicalPrice, spyData) : 
                        renderCryptoChart(selected, historicalPrice) 
                }



                <div className="tabContainer">
                    <div className="tabItemContainer">
                        <h2 style={{ width: "85px" }}>Equities</h2>
                        {
                            Object.keys(state.data.equities).map(name => <div style={{ width: "50px "}} onClick={() => setSelected(name, 'equities')} className={`tabItem ${state.selected === name ? 'selected' : ''}`}>{ name }</div>)
                        }
                    </div>
                    <div className="tabItemContainer">
                        <h2 style={{ width: "85px" }}>Crypto</h2>
                        {
                            Object.keys(state.data.crypto).map(name => <div style={{ width: "50px "}} onClick={() => setSelected(name, 'crypto')} className={`tabItem ${state.selected === name ? 'selected' : ''}`}>{ name }</div>)
                        }
                    </div>
                </div>                 
            </div>
           
           <div className="section" stlye={{ "justify-content": 'center' }}>
               <div className="mapContainer">
                    <Map trendByCountry={state.data[state.selectedType][state.selected].googleTrends.trendByCountry} />

                    <div>
                        <h1 className="pt-20">Trends</h1>
                        <div className="tabCntainer">
                            <div className="related">
                                <h2 style={{ width: "150px" }}>Related Queries</h2>
                                <h2 className="colourWhite">{ state.data[state.selectedType][state.selected].googleTrends.relatedQueries.map(val => `${val}, `) }</h2>
                            </div>
                            <div className="related">
                                <h2 style={{ width: "150px" }}>Related Topics</h2>
                                <h2 className="colourWhite">{ state.data[state.selectedType][state.selected].googleTrends.relatedTopics.map(val => `${val}, `) }</h2>
                            </div>
                        </div>       
                    </div>
               </div>

               
                { renderHistoricalTrendData() }                     
           </div>

           <div className="section">
               <div className="tableContainer">
                    <Table 
                        columnNames={Object.keys(state.cryptoTable[0])}
                        rowData={state.cryptoTable}
                    />
               </div>
           </div>
        </>
    )
}

export default Main;