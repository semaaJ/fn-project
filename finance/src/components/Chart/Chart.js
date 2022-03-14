import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

import './Chart.css';

const initialData = [
  {
    close: 4000,
    open: 2400,
  },
  {
    close: 3000,
    open: 1398,
  },
  {
    close: 2000,
    open: 9800,
  },
  {
    close: 2780,
    open: 3908,
  },
  {
    close: 1890,
    open: 4800,
  },
  {
    close: 2390,
    open: 3800,
  },
  {
    close: 3490,
    open: 4300,
  },
];

const initialLines = ['close', 'open']

const Chart = (props) => {
  const { lines, data, height, width } = props;

  const colourData = ["#0099ff", "#e8175d", "#fad30c", "#81ba4b"];

  return (
      <ResponsiveContainer width="100%" height={height}>
        <LineChart
          width={width}
          height={height}
          data={data || initialData}
        >
          <XAxis stroke="white" />
          <YAxis stroke="white" tickFormatter={(value) => new Intl.NumberFormat('en', { notation: "compact", compactDisplay: "short" }).format(value)} />
          <Tooltip />
          <Legend />
          {
            lines && lines.map((val, ind) => <Line dot={false} type="monotone" dataKey={val} stroke={colourData[ind]} strokeWidth={2} />)
          }
          {
            !lines && initialLines.map((val, ind) => <Line dot={false} type="monotone" dataKey={val} stroke={colourData[ind]} strokeWidth={2} />)
          }
        </LineChart>
      </ResponsiveContainer>
  );
}

export default Chart;
