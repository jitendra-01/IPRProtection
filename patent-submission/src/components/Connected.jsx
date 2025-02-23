import React from 'react';
import { Link } from 'react-router-dom';
import './Connected.css';

const Connected = () => {
    return (
        <div className="connected-container">
            <div className="connected-title">Choose the next step</div>
            <Link to="/home/patent-form">Create Patent</Link>
            <Link to="/home/review-dashboard">Review Dashboard</Link>
        </div>
    );
};

export default Connected;
