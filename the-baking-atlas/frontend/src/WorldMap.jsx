import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Country code to coordinates mapping (approximate centers)
const COUNTRY_COORDINATES = {
  'JP': [36.2048, 138.2529],   // Japan
  'IT': [41.8719, 12.5674],    // Italy
  'CA': [56.1304, -106.3468],  // Canada
  'FR': [46.2276, 2.2137],     // France
  'MX': [23.6345, -102.5528],  // Mexico
  'IN': [20.5937, 78.9629],    // India
  'BR': [-14.2350, -51.9253],  // Brazil
  'EG': [26.8206, 30.8025],    // Egypt
};

function WorldMap({ countries, onCountryClick }) {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersRef = useRef({});
  const [hoveredCountry, setHoveredCountry] = useState(null);

  useEffect(() => {
    // Initialize map only once
    if (!mapInstanceRef.current) {
      const map = L.map(mapRef.current, {
        center: [20, 0],
        zoom: 2,
        minZoom: 2,
        maxZoom: 10,
        worldCopyJump: true,
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(map);

      mapInstanceRef.current = map;
    }

    // Clear existing markers
    Object.values(markersRef.current).forEach(marker => marker.remove());
    markersRef.current = {};

    // Add markers for each country
    countries.forEach(country => {
      const coords = COUNTRY_COORDINATES[country.code];
      
      if (coords) {
        const icon = L.divIcon({
          className: 'country-marker',
          html: `
            <div class="marker-pin">
              <span class="marker-flag">🥐</span>
            </div>
            <div class="marker-label">${country.name}</div>
          `,
          iconSize: [40, 40],
          iconAnchor: [20, 40],
        });

        const marker = L.marker(coords, { icon })
          .addTo(mapInstanceRef.current);

        marker.on('click', () => {
          onCountryClick(country);
        });

        marker.on('mouseover', () => {
          setHoveredCountry(country.name);
          marker.getElement().classList.add('marker-hover');
        });

        marker.on('mouseout', () => {
          setHoveredCountry(null);
          marker.getElement().classList.remove('marker-hover');
        });

        markersRef.current[country.code] = marker;
      }
    });

    return () => {
      Object.values(markersRef.current).forEach(marker => marker.remove());
    };
  }, [countries, onCountryClick]);

  return (
    <div className="map-container">
      <div ref={mapRef} className="map" />
      {hoveredCountry && (
        <div className="map-tooltip">
          Click to explore {hoveredCountry}'s baking traditions
        </div>
      )}
    </div>
  );
}

export default WorldMap;