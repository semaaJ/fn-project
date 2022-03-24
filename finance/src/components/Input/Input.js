import React from 'react';
import './Input.css';

const Input = (props) => {
    const { label, value, inputId, width, onChange } = props;
    return (
        <div className="group mt-16">      
            <input type="text" onChange={e => onChange(e, inputId)} value={value} required />
            <span class="highlight"></span>
            <span class="bar"></span>
            <label>{ label }</label>
        </div>
    )
}

export default Input;