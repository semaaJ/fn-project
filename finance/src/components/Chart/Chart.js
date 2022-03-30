import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ReferenceLine, ResponsiveContainer } from 'recharts';

const Signal = (props) => {
  const { cx, cy, payload,  } = props;

  if (payload.signal === -1) {
    return (
      <svg x={cx - 10} y={cy - 10} width={150} height={150} fill="red" viewBox="0 0 1024 1024">
        <circle cx="50" cy="50" r="20" fill="red" />      
      </svg>
    );
  } else if (payload.signal === 1) {
    return (
      <svg x={cx - 10} y={cy - 10} width={150} height={150} fill="green" viewBox="0 0 1024 1024">
        <circle cx="50" cy="50" r="20" fill="green" /> 
      </svg>
    );
  }
  return <svg />
};

const Chart = (props) => {
  const { 
    lines,
    data, 
    height, 
    width, 
    max, 
    min, 
    referenceLines 
  } = props;

  const colourData = ["#0099ff", "#e8175d", "#fad30c", "#81ba4b"];

  return (
      <ResponsiveContainer width="100%" height={height}>
        <LineChart
          width={width}
          height={height}
          data={data}
          onClick={e => console.log(e)}
        >
          <XAxis 
            stroke="white"
            dataKey="date" 
            tick={false}
            // tickFormatter={(value) => formatDate(data[value].date)}
          />
          <YAxis 
            stroke="white" 
            domain={[min, max]} 
            tickFormatter={(value) => new Intl.NumberFormat('en', { notation: "compact", compactDisplay: "short" }).format(value)} 
          />
          <Tooltip />
          { referenceLines && referenceLines.map(val => <ReferenceLine y={val} stroke="white" strokeDasharray="3 3" />)}
          { lines.map((val, ind) => <Line isAnimationActive={false} dot={<Signal />} type="monotone" dataKey={val} stroke={colourData[ind]} strokeWidth={1} />) }
        </LineChart>
      </ResponsiveContainer>
  );
}

export default Chart;
