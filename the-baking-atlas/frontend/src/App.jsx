import { useState, useEffect } from 'react';
import axios from 'axios';
import WorldMap from './WorldMap';
import InfoPanel from './components/InfoPanel';
import './App.css';

// API base URL - your backend
const API_URL = 'http://localhost:8000/api';

function App() {
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch all countries when component loads
  useEffect(() => {
    fetchCountries();
  }, []);

  const fetchCountries = async () => {
    try {
      const response = await axios.get(`${API_URL}/countries/`);
      setCountries(response.data);
    } catch (err) {
      console.error('Failed to load countries:', err);
    }
  };

  const fetchCountryDetails = async (countryCode) => {
    try {
      setLoading(true);
      setError('');
      setIsPanelOpen(true); // Open panel immediately with loading state
      
      const response = await axios.get(`${API_URL}/countries/${countryCode}`);
      setSelectedCountry(response.data);
    } catch (err) {
      setError(`Failed to load details for ${countryCode}. Please try again.`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCountryClick = (country) => {
    fetchCountryDetails(country.code);
  };

  const handleClosePanel = () => {
    setIsPanelOpen(false);
    // Small delay before clearing data so panel can slide out smoothly
    setTimeout(() => {
      setSelectedCountry(null);
      setError('');
    }, 200);
  };

  return (
    <div className="app">
      {/* Fixed Header */}
      <header className="header">
        <div className="header-content">
          <div className="header-left">
            <h1>🌍 The Baking Atlas</h1>
            <p>Explore global baking traditions</p>
          </div>
          <div className="header-right">
            <a href="#about" className="about-link">About</a>
          </div>
        </div>
      </header>

      {/* Full-screen Map */}
      <main className="map-container-wrapper">
        <WorldMap 
          countries={countries}
          onCountryClick={handleCountryClick}
        />
      </main>

      {/* Slide-in Info Panel */}
      <InfoPanel
        isOpen={isPanelOpen}
        countryData={selectedCountry}
        loading={loading}
        error={error}
        onClose={handleClosePanel}
      />
    </div>
  );
}

export default App;