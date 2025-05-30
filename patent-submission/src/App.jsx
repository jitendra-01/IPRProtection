import { useState, useEffect } from 'react';
import {ethers} from 'ethers';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
// import {contractAbi, contractAddress} from './constants/constant';
import Connected from './components/Connected';
import PatentForm from './components/PatentForm';
import ReviewDashboard from './components/ReviewDashboard';
import TransferOwnership from './components/transfer_ownership'
import OwnershipHistoryViewer from './components/CheckHistory'

function App() {
    // useEffect( () => {
    //     if (window.ethereum) {
    //       window.ethereum.on('accountsChanged', handleAccountsChanged);
    //     }
    
    //     return() => {
    //       if (window.ethereum) {
    //         window.ethereum.removeListener('accountsChanged', handleAccountsChanged);
    //       }
    //     }
    // });
    
    // function handleAccountsChanged(accounts) {
    // if (accounts.length > 0 && account !== accounts[0]) {
    //     setAccount(accounts[0]);
    // } else {
    //     setIsConnected(false);
    //     setAccount(null);
    // }
    // }
    const [account, setAccount] = useState(null);
    const [isConnected, setIsConnected] = useState(false);


    async function connectToMetamask() {
        if (window.ethereum) {
        try {
            const provider = new ethers.BrowserProvider(window.ethereum);
            await provider.send("eth_requestAccounts", []);
            const signer =await provider.getSigner();
            const address = signer.address;
            setAccount(address);
            console.log("Metamask Connected : " + address);
            setIsConnected(true);
            // const token = jwt.sign({ wallet: address }, 'your_secret_key', { expiresIn: '1h' });
            // localStorage.setItem('token', token);
            // console.log("Generated Token:", token);
        } catch (err) {
            console.error(err);
        }
        } else {
        console.error("Metamask is not detected in the browser")
        }
    }

    return (
    <Router>
      <Routes>
        <Route 
          path="/" 
          element={isConnected ? <Navigate to="/home" /> : <Login connectWallet={connectToMetamask} />} 
        />
        <Route 
          path="/home" 
          element={isConnected ? <Connected /> : <Navigate to="/" />} 
        />
        <Route 
            path="/home/patent-form" 
            element={isConnected ? <PatentForm /> : <Navigate to="/" />} 
        />
        <Route 
            path="/home/review-dashboard" 
            element={isConnected ? <ReviewDashboard ownerAddress={account}/> : <Navigate to="/" />} 
        />
        <Route 
          path="/home/transfer-ownership" 
          element={isConnected ? <TransferOwnership /> : <Navigate to="/" />}  
        />
        <Route 
          path="/home/check-history" 
          element={isConnected  ? <OwnershipHistoryViewer /> : <Navigate to="/" />} 
        />
      </Routes>
    </Router>
    );
}
export default App;
