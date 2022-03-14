import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChartPage from './Pages/ChartPage';
import RSI from './Pages/RSI';
import './App.css';


function App() {
  return (
    <div className="App">
       <BrowserRouter>
        <Routes>
            <Route path="/" element={<RSI />}>
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
