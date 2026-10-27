import React, { useEffect, useState } from 'react';
import apiClient from '../services/api';
import CivicMap from '../components/CivicMap';

export default function Dashboard() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Form state for creating a new request
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'Water & Sanitation',
    urgency: 'HIGH',
    latitude: '24.5854',
    longitude: '83.0567',
    location_name: 'Robertsganj Town Center'
  });
  const [submitting, setSubmitting] = useState(false);

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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await apiClient.post('/requests/', {
        ...formData,
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude)
      });
      setIsModalOpen(false);
      // Reset form
      setFormData({
        title: '',
        description: '',
        category: 'Water & Sanitation',
        urgency: 'HIGH',
        latitude: '24.5854',
        longitude: '83.0567',
        location_name: 'Robertsganj Town Center'
      });
      fetchRequests();
    } catch (err) {
      console.error("Failed to create request:", err);
      alert("Failed to submit request. Make sure you are authorized or logged in via backend.");
    } finally {
      setSubmitting(false);
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
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsModalOpen(true)}
              className="px-4 py-2 bg-emerald-600 text-white font-medium text-sm rounded-xl hover:bg-emerald-700 transition shadow-sm"
            >
              + Report Need
            </button>
            <button
              onClick={fetchRequests}
              className="px-4 py-2 bg-indigo-600 text-white font-medium text-sm rounded-xl hover:bg-indigo-700 transition shadow-sm"
            >
              Refresh Data
            </button>
          </div>
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

      {/* Modal for Reporting a New Request */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-xl border border-slate-100">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-bold text-slate-900">Report Emergency / Community Need</h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 text-sm font-bold px-2 py-1"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Title</label>
                <input
                  type="text"
                  name="title"
                  required
                  value={formData.title}
                  onChange={handleInputChange}
                  placeholder="e.g. Clean Water Required"
                  className="w-full text-sm px-3 py-2 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Description</label>
                <textarea
                  name="description"
                  rows="3"
                  required
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Provide specific details about the need..."
                  className="w-full text-sm px-3 py-2 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Category</label>
                  <select
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                    className="w-full text-sm px-3 py-2 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                  >
                    <option value="Water & Sanitation">Water & Sanitation</option>
                    <option value="Medical Aid">Medical Aid</option>
                    <option value="Food & Ration">Food & Ration</option>
                    <option value="Shelter">Shelter</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Urgency</label>
                  <select
                    name="urgency"
                    value={formData.urgency}
                    onChange={handleInputChange}
                    className="w-full text-sm px-3 py-2 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                  >
                    <option value="CRITICAL">CRITICAL</option>
                    <option value="HIGH">HIGH</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="LOW">LOW</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Latitude</label>
                  <input
                    type="number"
                    step="any"
                    name="latitude"
                    required
                    value={formData.latitude}
                    onChange={handleInputChange}
                    className="w-full text-sm px-3 py-2 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Longitude</label>
                  <input
                    type="number"
                    step="any"
                    name="longitude"
                    required
                    value={formData.longitude}
                    onChange={handleInputChange}
                    className="w-full text-sm px-3 py-2 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Location Name</label>
                <input
                  type="text"
                  name="location_name"
                  value={formData.location_name}
                  onChange={handleInputChange}
                  placeholder="e.g. Salkhan Sector"
                  className="w-full text-sm px-3 py-2 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-xl font-medium transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 text-sm bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-medium transition shadow-sm disabled:opacity-50"
                >
                  {submitting ? 'Submitting...' : 'Submit Request'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}