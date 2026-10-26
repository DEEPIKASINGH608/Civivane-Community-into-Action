import React, { useEffect, useState } from 'react';
import apiClient from '../services/api';
import CivicMap from '../components/CivicMap';

export default function Dashboard() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      const response = await apiClient.get('/requests/');
      setRequests(response.data);
    } catch (err) {
      console.error("Failed to load community requests:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Civivane Command Center</h1>
            <p className="text-sm text-slate-500">Real-time disaster relief & community request intelligence</p>
          </div>
          <button
            onClick={fetchRequests}
            className="px-4 py-2 bg-indigo-600 text-white font-medium text-sm rounded-xl hover:bg-indigo-700 transition"
          >
            Refresh Data
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white p-4 rounded-2xl shadow-sm border border-slate-100">
            <h2 className="text-lg font-semibold text-slate-800 mb-3">Live Incident Map</h2>
            <CivicMap requests={requests} />
          </div>

          <div className="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 flex flex-col h-[520px]">
            <h2 className="text-lg font-semibold text-slate-800 mb-3">Active Requests</h2>
            <div className="overflow-y-auto space-y-3 pr-1 flex-1">
              {loading ? (
                <p className="text-sm text-slate-400 text-center py-10">Loading requests...</p>
              ) : requests.length === 0 ? (
                <p className="text-sm text-slate-400 text-center py-10">No requests found.</p>
              ) : (
                requests.map((r) => (
                  <div key={r.id} className="p-3.5 rounded-xl border border-slate-100 bg-slate-50/50 hover:bg-slate-50 transition">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-[11px] font-semibold px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded-md">
                        {r.category}
                      </span>
                      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                        r.urgency === 'CRITICAL' ? 'bg-red-100 text-red-600' : 'bg-amber-100 text-amber-600'
                      }`}>
                        {r.urgency}
                      </span>
                    </div>
                    <h3 className="font-semibold text-slate-800 text-sm">{r.title}</h3>
                    <p className="text-xs text-slate-500 mt-1 line-clamp-2">{r.description}</p>
                    <div className="flex justify-between items-center mt-2 pt-2 border-t border-slate-200/60 text-[11px] text-slate-400">
                      <span>📍 {r.location_name || 'Location N/A'}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}