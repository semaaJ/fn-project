import './ShareTileContainer.css';

const ShareTileContainer = (props) => {
    const {
        data,
        e1,
        e2,
        corr
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

    return (
        <div className="shareInfoContainer">
            <div className="shareInfoTile">
                <div className="shareTitle">{ shortName }</div>
                <div className="">{ industry }</div>
                <div className="shareAddress">{ city }, { state }, { country }, { zip }</div>
                <div className="shareAddress mt-8">Correlation: { corr }</div>
                <div className="shareAddress">SPY: { e1 }% vs { e2 }%</div>
            </div>
        </div>
    )
}

export default ShareTileContainer;