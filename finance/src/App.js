import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChartPage from './Pages/ChartPage';
import Results from './Pages/Results';
import RSI from './Pages/RSI';
import EMA from './Pages/EMA';
import './App.css';


function App() {
  return (
    <div className="App">
       <BrowserRouter>
        <Routes>
            <Route exact path="/rsi" element={<RSI />} />
            <Route path='/ema' element={<EMA />} />
            <Route path='/results' element={<Results />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
