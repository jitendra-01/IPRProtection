import React from 'react';
import { Link } from 'react-router-dom';
import './Connected.css';

const Connected = () => {
    return (
        <div className="container">
            <h1>Choose the next step!</h1>
            <Link to="/home/patent-form" className="button">Upload document for patent consideration</Link>
            <Link to="/home/review-dashboard" className="button">Review Dashboard</Link>
        </div>
    );
};

export default Connected;
