import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const formatDate = (date) => {
  // 2016-02-09
  const split = date.split("-");
  return `${ split[1] }/${ split[0].slice(0, 2) }`;
}


const ChartBar = (props) => {
  const { data, height, width, min, max } = props;


  return (
    <ResponsiveContainer width="100%" height={height}>
        <BarChart width={width} height={height} data={data}>
            <Tooltip />
            <XAxis 
              stroke="white"
              tick={false}
              dataKey="date" 
              domain={[min, max]}
              tickFormatter={(value) => formatDate(value)} 
            />
            <YAxis stroke="white" tick={false} />
            <Bar dataKey="volume" fill="#0099ff" />
        </BarChart>
    </ResponsiveContainer>
  );
}

export default ChartBar;
