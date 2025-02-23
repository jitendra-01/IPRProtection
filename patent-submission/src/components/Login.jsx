import React from "react";
import "./Login.css"; 

const Login = (props) => {
    return (
        <div className="login-container">
            <h1 className="welcome-message">Welcome to Patent Registration</h1>
            <p>Secure, decentralized, and efficient patent registration at your fingertips.</p>
            <button className="login-button" onClick={props.connectWallet}>
                Login with MetaMask.
            </button>
        </div>
    );
}

export default Login;
