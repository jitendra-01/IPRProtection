import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import "./PatentForm.css"; 

const PatentForm = () => {
    const [file, setFile] = useState(null);
    const [metadata, setMetadata] = useState({ title: '', keywords: '', abstract: '',email: ''});
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');

        // if (!token) {
        //     setMessage('You must be logged in to submit a patent.');
        //     navigate('/');
        //     return;
        // }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('title', metadata.title);
        formData.append('keywords', metadata.keywords);
        formData.append('abstract', metadata.abstract);
        formData.append('email', metadata.email);

        try {

            const response = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {});
            setMessage(response.data.message);
        } catch (error) {
            setMessage('Error submitting patent.');
        }
    };

    return (
        <div>
            <h1>Submit Patent</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Your Email"
                    value={metadata.email}
                    onChange={(e) => setMetadata({ ...metadata, email: e.target.value })}
                    required
                />
                <input
                    type="text"
                    placeholder="Title"
                    value={metadata.title}
                    onChange={(e) => setMetadata({ ...metadata, title: e.target.value })}
                    required
                />
                <input
                    type="text"
                    placeholder="Keywords (comma separated)"
                    value={metadata.keywords}
                    onChange={(e) => setMetadata({ ...metadata, keywords: e.target.value })}
                    required
                />
                <input
                    type="text"
                    placeholder="Abstract"
                    value={metadata.abstract}
                    onChange={(e) => setMetadata({ ...metadata, abstract: e.target.value })}
                    required
                />
                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files[0])}
                    required
                    style={{ color: "white" }}
                />

                <button type="submit">Submit</button>
            </form>
            <Link to="/home/review-dashboard" className="button">Review Dashboard</Link>
            {message && <p>{message}</p>}
        </div>
    );
};

export default PatentForm;
