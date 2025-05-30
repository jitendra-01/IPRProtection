import React, { useState } from "react";
import axios from "axios";

const TransferOwnership = () => {
  const [patentId, setPatentId] = useState("");
  const [newOwner, setNewOwner] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleTransfer = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post("http://localhost:8000/api/transfer_ownership/", {
        patent_id: patentId,
        new_owner: newOwner,
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-xl shadow-md space-y-4">
      <h2 className="text-2xl font-bold">Transfer Patent Ownership</h2>
      <form onSubmit={handleTransfer} className="space-y-4">
        <div>
          <label className="block font-medium">Patent ID:</label>
          <input
            type="text"
            value={patentId}
            onChange={(e) => setPatentId(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
        </div>
        <div>
          <label className="block font-medium">New Owner Address:</label>
          <input
            type="text"
            value={newOwner}
            onChange={(e) => setNewOwner(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? "Transferring..." : "Transfer Ownership"}
        </button>
      </form>

      {result && (
        <div className="p-4 mt-4 bg-green-100 border border-green-300 rounded">
          <p>✅ {result.message}</p>
          <p>🔗 Transaction Hash: <code>{result.transaction_hash}</code></p>
        </div>
      )}

      {error && (
        <div className="p-4 mt-4 bg-red-100 border border-red-300 rounded text-red-700">
          ❌ {error}
        </div>
      )}
    </div>
  );
};

export default TransferOwnership;
