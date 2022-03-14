export function linearRegression(y, x) {
    var lr = {};
    var n = y.length;
    var sum_x = 0;
    var sum_y = 0;
    var sum_xy = 0;
    var sum_xx = 0;
    var sum_yy = 0;

    for (var i = 0; i < n; i++) {
        sum_x += x[i];
        sum_y += y[i];
        sum_xy += (x[i] * y[i]);
        sum_xx += (x[i] * x[i]);
        sum_yy += (y[i] * y[i]);
    } 

    const slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x);
    const intercept = (sum_y - slope * sum_x) / n;

    return x.map((val, i) => slope * i + intercept);
}

export function getPercentageChange(oldNumber, newNumber){
    const decreaseValue = oldNumber - newNumber;
    return -(decreaseValue / oldNumber) * 100;
}

export function getProfitPercentage(invesmentReturn, invemesntValue) {
    return (invesmentReturn / invemesntValue) * 100
}
