import React from 'react';
import { Link } from 'react-router-dom';

const Connected = () => {
    return (
        <>
            <Link to="/home/patent-form">Create Patent</Link>
            <br/>
            <Link to="/home/review-dashboard">Review Dashboard</Link>
        </>
    );
};

export default Connected;