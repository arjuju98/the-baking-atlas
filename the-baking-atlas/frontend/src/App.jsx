import { useState, useEffect } from 'react';
import axios from 'axios';
import WorldMap from './WorldMap';
import './App.css';

// API base URL - your backend
const API_URL = 'http://localhost:8000/api';

function App() {
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [viewMode, setViewMode] = useState('map'); // 'map' or 'list'

  // Fetch all countries when component loads
  useEffect(() => {
    fetchCountries();
  }, []);

  const fetchCountries = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/countries/`);
      setCountries(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load countries. Make sure your API is running!');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCountryDetails = async (countryCode) => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/countries/${countryCode}`);
      setSelectedCountry(response.data);
      setError('');
    } catch (err) {
      setError(`Failed to load details for ${countryCode}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCountryClick = (country) => {
    fetchCountryDetails(country.code);
  };

  const handleBackToMap = () => {
    setSelectedCountry(null);
  };

  const toggleViewMode = () => {
    setViewMode(viewMode === 'map' ? 'list' : 'map');
    setSelectedCountry(null);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🌍 The Baking Atlas</h1>
        <p>Explore global baking traditions</p>
        <button onClick={toggleViewMode} className="view-toggle">
          {viewMode === 'map' ? '📋 Switch to List View' : '🗺️ Switch to Map View'}
        </button>
      </header>

      <main className="main-content">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {loading && !selectedCountry ? (
          <div className="loading">Loading...</div>
        ) : selectedCountry ? (
          // Country Detail View
          <CountryDetail 
            country={selectedCountry} 
            onBack={handleBackToMap}
          />
        ) : viewMode === 'map' ? (
          // Map View
          <WorldMap 
            countries={countries}
            onCountryClick={handleCountryClick}
          />
        ) : (
          // List View
          <CountryList 
            countries={countries} 
            onCountryClick={handleCountryClick}
          />
        )}
      </main>
    </div>
  );
}

// Component to display list of countries
function CountryList({ countries, onCountryClick }) {
  return (
    <div className="country-list">
      <h2>Select a Country</h2>
      <div className="country-grid">
        {countries.map((country) => (
          <div 
            key={country.id}
            className="country-card"
            onClick={() => onCountryClick(country)}
          >
            <h3>{country.name}</h3>
            <p className="country-code">{country.code}</p>
            {country.region && <p className="region">{country.region}</p>}
          </div>
        ))}
      </div>
    </div>
  );
}

// Component to display country details
function CountryDetail({ country, onBack }) {
  return (
    <div className="country-detail">
      <button onClick={onBack} className="back-button">
        ← Back to Map
      </button>

      <div className="country-header">
        <h2>{country.name}</h2>
        <span className="country-code-large">{country.code}</span>
      </div>

      {country.region && (
        <p className="region-tag">📍 {country.region}</p>
      )}

      {country.overview && (
        <div className="section">
          <h3>Overview</h3>
          <p>{country.overview}</p>
        </div>
      )}

      {country.extra_data && (
        <div className="section">
          <h3>Additional Information</h3>
          <div className="extra-data">
            {Object.entries(country.extra_data).map(([key, value]) => (
              <div key={key} className="data-item">
                <strong>{key.replace(/_/g, ' ')}:</strong> {value}
              </div>
            ))}
          </div>
        </div>
      )}

      {country.baked_goods && country.baked_goods.length > 0 && (
        <div className="section">
          <h3>🥐 Signature Baked Goods</h3>
          <div className="items-grid">
            {country.baked_goods.map((good) => (
              <div key={good.id} className="item-card">
                <h4>{good.name}</h4>
                <span className="category-badge">{good.category}</span>
                <p>{good.description}</p>
                {good.extra_data && (
                  <div className="item-extra">
                    {Object.entries(good.extra_data).map(([key, value]) => (
                      <div key={key} className="extra-detail">
                        <strong>{key}:</strong> {
                          Array.isArray(value) ? value.join(', ') : value
                        }
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {country.ingredients && country.ingredients.length > 0 && (
        <div className="section">
          <h3>🌾 Common Ingredients</h3>
          <div className="items-grid">
            {country.ingredients.map((ingredient) => (
              <div key={ingredient.id} className="item-card">
                <h4>{ingredient.name}</h4>
                <p>{ingredient.description}</p>
                {ingredient.extra_data && (
                  <div className="item-extra">
                    {Object.entries(ingredient.extra_data).map(([key, value]) => (
                      <div key={key} className="extra-detail">
                        <strong>{key}:</strong> {
                          Array.isArray(value) ? value.join(', ') : value
                        }
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;