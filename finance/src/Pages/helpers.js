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

export function correlationCoefficient(X, Y) {
    const n = X.length;
    let sum_X = 0, sum_Y = 0, sum_XY = 0;
    let squareSum_X = 0, squareSum_Y = 0;
    
    for(let i = 0; i < n; i++) {  
        sum_X = sum_X + X[i];
        sum_Y = sum_Y + Y[i];
        sum_XY = sum_XY + X[i] * Y[i];
        squareSum_X = squareSum_X + X[i] * X[i];
        squareSum_Y = squareSum_Y + Y[i] * Y[i];
    }

    let corr = (n * sum_XY - sum_X * sum_Y)/
            (Math.sqrt((n * squareSum_X -
                    sum_X * sum_X) * 
                        (n * squareSum_Y - 
                    sum_Y * sum_Y)));
    
    return corr;
}

export function getPercentageChange(oldNumber, newNumber){
    const decreaseValue = oldNumber - newNumber;
    return -(decreaseValue / oldNumber) * 100;
}

export function sliceArr(data, index) {
    const new_arr = data.slice(data.length - 1 - index);
    return new_arr;
}