import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const data = [
    {
      name: 'Page A',
      uv: 4000,
      pv: 2400,
      amt: 2400,
    },
    {
      name: 'Page B',
      uv: 3000,
      pv: 1398,
      amt: 2210,
    },
    {
      name: 'Page C',
      uv: 2000,
      pv: 9800,
      amt: 2290,
    },
    {
      name: 'Page D',
      uv: 2780,
      pv: 3908,
      amt: 2000,
    },
    {
      name: 'Page E',
      uv: 1890,
      pv: 4800,
      amt: 2181,
    },
    {
      name: 'Page F',
      uv: 2390,
      pv: 3800,
      amt: 2500,
    },
    {
      name: 'Page G',
      uv: 3490,
      pv: 4300,
      amt: 2100,
    },
];

const Stacked = (props) => {
  const { height, width } = props;

  const colourData = ["#0099ff", "#e8175d", "#fad30c", "#81ba4b"];

  return (
    <ResponsiveContainer className="justified" width="103%" height="25%">    
        <AreaChart
          width={500}
          height={400}
          data={data}
        >
          <XAxis tick={false} dataKey="name" stroke="white" />
          <YAxis tick={false} stroke="white" />
          <Tooltip />
          <Area type="monotone" dataKey="uv" stackId="1" stroke="#0099ff" fill="#0099ff" />
          <Area type="monotone" dataKey="pv" stackId="1" stroke="#e8175d" fill="#e8175d" />
          <Area type="monotone" dataKey="amt" stackId="1" stroke="#fad30c" fill="#fad30c" />
        </AreaChart>
      </ResponsiveContainer>
  );
}

export default Stacked;
