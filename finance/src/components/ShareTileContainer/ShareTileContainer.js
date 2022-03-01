import './ShareTileContainer.css';

const ShareTileContainer = (props) => {
    const {
        data,
        name,
        type
    } = props;

    const {
        zip,
        city,
        state,
        country,
        shortName,
        website,
        industry,
        sector,
        fullTimeEmployees,
        longBusinessSummary,

        profitMargins,
        grossMargins,
        totalRevenue,
        totalDebt,
        totalCash,
        grossProfits,
        operatingCashflow,
        revenueGrowth,
        operatingMargins,
        targetLowPrice,
        targetMedianPrice,
        targetMeanPrice,
        targetHighPrice,
        recommendationKey,
        freeCashflow,
        returnOnAssets,
        numberOfAnalystOpinions,
        totalCashPerShare,
        revenuePerShare,
        bookValue,
        forwardPE,

        currentPrice,
        fiftyTwoWeekLow,
        fiftyTwoWeekHigh,
        fiftyDayAverage,
        twoHundredDayAverage,
        fiftyTwoWeekChange,

        marketCap,
        volume,
    } = data;

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    });

    const renderShareInfo = () => {
        return (
                <div className="shareInfoTile">
                    <h1>{ shortName }</h1>
                    <h2 className="colourWhite">{ industry } | { sector }</h2>

                    <div className="shareOuter">
                        <div className="shareInfoContainer">
                            <div className="shareDivider" style={{ marginRight: "20px" }}>
                                <h2 style={{ width: "200px" }}>Current Price:</h2>
                                <h2 className="colourWhite">{ formatter.format(currentPrice.toFixed(2)) }</h2>
                            </div>
                            <div className="shareDivider">
                                <h2 style={{ width: "200px" }}>Market Cap</h2>
                                <h2 className="colourWhite">{ formatter.format(marketCap.toFixed(2)) }</h2>
                            </div>
                            <div className="shareDivider">
                                <h2 style={{ width: "200px" }}>Revenue Per Share:</h2>
                                <h2 className="colourWhite">{ formatter.format(revenuePerShare.toFixed(2)) }</h2>
                            </div>
                            <div className="shareDivider">
                                <h2 style={{ width: "200px" }}>Forward PE</h2>
                                <h2 className="colourWhite">{ formatter.format(forwardPE.toFixed(2)) }</h2>
                            </div>
                        </div>

                        <div className="shareInfoContainer">
                            <div className="shareDivider" style={{ marginRight: "20px" }}>
                                <h2 style={{ width: "200px" }}>Target Low Price:</h2>
                                <h2 className="colourWhite">{ formatter.format(targetLowPrice.toFixed(2)) }</h2>
                            </div>
                            <div className="shareDivider">
                                <h2 style={{ width: "200px" }}>Target Median Price:</h2>
                                <h2 className="colourWhite">{ formatter.format(targetMedianPrice.toFixed(2)) }</h2>
                            </div>
                            <div className="shareDivider">
                                <h2 style={{ width: "200px" }}>Target High Price:</h2>
                                <h2 className="colourWhite">{ formatter.format(targetHighPrice.toFixed(2)) }</h2>
                            </div>
                            <div className="shareDivider">
                                <h2 style={{ width: "200px" }}>Target Mean Price:</h2>
                                <h2 className="colourWhite">{ formatter.format(targetMeanPrice.toFixed(2)) }</h2>
                            </div>
                        </div>

                        <div className="shareInfoContainer">
                            <div className="shareDivider" style={{ marginRight: "20px" }}>
                                <h2 style={{ width: "200px" }}>52 Week Low:</h2>
                                <h2 className="colourWhite">{ formatter.format(fiftyTwoWeekLow.toFixed(2)) }</h2>
                            </div>
                            <div className="shareDivider">
                                <h2 style={{ width: "200px" }}>52 Week High:</h2>
                                <h2 className="colourWhite">{ formatter.format(fiftyTwoWeekHigh.toFixed(2)) }</h2>
                            </div>
                            <div className="shareDivider">
                                <h2 style={{ width: "200px" }}>50 Day Average:</h2>
                                <h2 className="colourWhite">{ formatter.format(fiftyDayAverage.toFixed(2)) }</h2>
                            </div>
                            <div className="shareDivider">
                                <h2 style={{ width: "200px" }}>200 Day Average:</h2>
                                <h2 className="colourWhite">{ formatter.format(twoHundredDayAverage.toFixed(2)) }</h2>
                            </div>
                        </div>
                    </div>
                </div>
        )
    }

    const renderCryptoInfo = () => {
        return (
            <div className="shareInfoTile">
                <h1 className="shareTitle">{ name }</h1>
                <div className="shareSubtitle">${ currentPrice.toFixed(2) }</div>
                <div className="shareAddress">${ currentPrice } - %{ data['24hchange'] }</div>
                <div className="shareAddress">${ marketCap.toFixed(2) } ${ volume }</div>

                {/* <div className="shareAddress mt-8">SPY Correlation: { 0 }</div>
                <div className="shareAddress">BTC Correlation: { 0 }</div>
                <div className="shareAddress mt-8">BTC: { 0 }% vs { 0 }%</div> */}
            </div>
        )
    }

    console.log(data, type);
    if (type === "equities") return renderShareInfo();
    return renderCryptoInfo();
}

export default ShareTileContainer;