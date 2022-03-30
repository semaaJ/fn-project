import React from 'react';
import { Helmet } from 'react-helmet';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChartPage from './Pages/ChartPage';
import './App.css';


function App() {
  return (
    <div className="App">
       <Helmet>
        <title>Paper Trader</title>
        <meta name="description" content="Paper Trader" />
      </Helmet>

       <BrowserRouter>
        <Routes>
            <Route path='/' element={<ChartPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
