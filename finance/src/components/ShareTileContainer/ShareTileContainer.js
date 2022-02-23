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
    } = data;

    const renderShareInfo = () => {
        return (
            <div className="shareInfoContainer">
                <div className="shareInfoTile">
                    <div className="shareTitle">{ shortName }</div>
                    <div className="">{ industry }</div>
                    <div className="shareAddress">{ city }, { state }, { country }, { zip }</div>
                    {/* <div className="shareAddress mt-8">SPY Correlation: { 0 }</div>
                    <div className="shareAddress">BTC Correlation: { 0 }</div>
                    <div className="shareAddress mt-8">SPY: { 0 }% vs { 0 }%</div> */}
                </div>
            </div>
        )
    }

    const renderCryptoInfo = () => {
        return (
            <div className="shareInfoContainer">
                <div className="shareInfoTile">
                    <div className="shareTitle">{ name }</div>
                    {/* <div className="shareAddress mt-8">SPY Correlation: { 0 }</div>
                    <div className="shareAddress">BTC Correlation: { 0 }</div>
                    <div className="shareAddress mt-8">BTC: { 0 }% vs { 0 }%</div> */}
                </div>
            </div>
        )
    }

    console.log(data, type);
    if (type === "equities") return renderShareInfo();
    return renderCryptoInfo();
}

export default ShareTileContainer;