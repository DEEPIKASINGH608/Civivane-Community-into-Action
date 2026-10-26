import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Component to fix grey tile rendering issues on load
function MapResizer() {
  const map = useMap();
  useEffect(() => {
    setTimeout(() => {
      map.invalidateSize();
    }, 100);
  }, [map]);
  return null;
}

export default function CivicMap({ requests = [], center = [24.5854, 83.0567] }) {
  return (
    <div className="h-[450px] w-full rounded-xl overflow-hidden shadow-lg border border-slate-200 relative z-0">
      <MapContainer center={center} zoom={13} scrollWheelZoom={false} style={{ height: '100%', width: '100%' }}>
        <MapResizer />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {requests.map((req) => (
          req.latitude && req.longitude && (
            <Marker key={req.id} position={[req.latitude, req.longitude]}>
              <Popup>
                <div className="p-1">
                  <span className="text-xs font-bold px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full">
                    {req.category}
                  </span>
                  <h4 className="font-semibold text-slate-800 mt-1">{req.title}</h4>
                  <p className="text-xs text-slate-600 mt-0.5">{req.description}</p>
                  <p className="text-[10px] text-red-500 font-medium mt-1">Urgency: {req.urgency}</p>
                </div>
              </Popup>
            </Marker>
          )
        ))}
      </MapContainer>
    </div>
  );
}