import React, { useState } from 'react';
import './Menu.css';

const Menu = () => {
    const [open, setOpen] = useState(false);

    return (
        <div className="navContainer">
            <h1 style={{ fontSize: "32px" }}><span className="colourWhite">S&P</span>500</h1>
            <a id="menu-toggle" href="#" className={!open ? "burger" : 'burger toggled'} onClick={() => setOpen(!open)}>
                <span className="sr">Toggle Navigation</span>
                <span className="menu-bar bar1"></span>
                <span className="menu-bar bar2"></span>
                <span className="menu-bar bar3"></span>
            </a>
        </div>
    )
}

export default Menu;