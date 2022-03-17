import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Chart.css';


const Signal = (props) => {
  const { cx, cy, payload,  } = props;

  if (payload.signal === -1) {
    return (
      <svg x={cx - 10} y={cy - 10} width={150} height={150} fill="red" viewBox="0 0 1024 1024">
        <circle cx="50" cy="50" r="40" fill="red" />      
      </svg>
    );
  } else if (payload.signal == 1) {
    return (
      <svg x={cx - 10} y={cy - 10} width={150} height={150} fill="green" viewBox="0 0 1024 1024">
        <circle cx="50" cy="50" r="40" fill="green" /> 
      </svg>
    );
  }
  return <svg />
};


const Chart = (props) => {
  const { lines, data, height, width, max, min } = props;

  const colourData = ["#0099ff", "#e8175d", "#fad30c", "#81ba4b"];

  return (
      <ResponsiveContainer width="100%" height={height}>
        <LineChart
          width={width}
          height={height}
          data={data}
        >
          <XAxis stroke="white" />
          <YAxis 
            stroke="white" 
            domain={[min, max]} 
            tickFormatter={(value) => new Intl.NumberFormat('en', { notation: "compact", compactDisplay: "short" }).format(value)} 
          />
          <Tooltip />
          { lines.map((val, ind) => <Line dot={<Signal />} type="monotone" dataKey={val} stroke={colourData[ind]} strokeWidth={2} />) }
        </LineChart>
      </ResponsiveContainer>
  );
}

export default Chart;
