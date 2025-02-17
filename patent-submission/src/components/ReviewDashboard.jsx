import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ReviewDashboard = (props) => {
    const [patents, setPatents] = useState([]);
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchPatents = async () => {
            const token = localStorage.getItem('token');

            if (!token) {
                setMessage('You must be logged in to access the dashboard.');
                navigate('/');
                return;
            }

            try {
                const response = await axios.get('http://localhost:5000/review', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setPatents(response.data);
            } catch (error) {
                setMessage('Error fetching patents.');
            }
        };

        fetchPatents();
    }, [navigate]);

    const handleAction = async (id, action) => {
        const token = localStorage.getItem('token');

        try {
            const response = await axios.post(
                `http://localhost:5000/review/${id}`,
                { action },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setMessage(response.data.message);
            setPatents((prev) => prev.filter((patent) => patent.id !== id));
        } catch (error) {
            setMessage('Error performing action.');
        }
    };

    return (
        <div>
            <h1>Review Patents</h1>
            {message && <p>{message}</p>}
            <ul>
                {patents.map((patent) => (
                    <li key={patent.id}>
                        <h3>{patent.title}</h3>
                        <p>Similarity Score: {patent.similarity}%</p>
                        <button onClick={() => handleAction(patent.id, 'approve')}>Approve</button>
                        <button onClick={() => handleAction(patent.id, 'reject')}>Reject</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ReviewDashboard;
