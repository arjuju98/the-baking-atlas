import { useState, useEffect, useRef, useCallback } from 'react';
import { Routes, Route, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import WorldMap from './WorldMap';
import InfoPanel from './components/InfoPanel';
import StoryReader from './components/StoryReader';
import './App.css';

// API base URL - your backend
const API_URL = 'http://localhost:8000/api';

function App() {
  const navigate = useNavigate();

  // Country/Map state
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Story state
  const [activeStory, setActiveStory] = useState(null);
  const [storyLoading, setStoryLoading] = useState(false);
  const [storyError, setStoryError] = useState('');
  const [countriesWithStories, setCountriesWithStories] = useState(new Set());

  // Preserve map context when navigating to story
  const mapContextRef = useRef(null);

  // Fetch all countries and stories when component loads
  useEffect(() => {
    fetchCountries();
    fetchAllStories();
  }, []);

  const fetchCountries = async () => {
    try {
      const response = await axios.get(`${API_URL}/countries/`);
      setCountries(response.data);
    } catch (err) {
      console.error('Failed to load countries:', err);
    }
  };

  const fetchAllStories = async () => {
    try {
      const response = await axios.get(`${API_URL}/stories/`);
      // Build set of country codes that have stories
      const codesWithStories = new Set();
      response.data.forEach(story => {
        story.regions?.forEach(region => {
          codesWithStories.add(region.code);
        });
      });
      setCountriesWithStories(codesWithStories);
    } catch (err) {
      console.error('Failed to load stories:', err);
    }
  };

  const fetchStory = useCallback(async (slug) => {
    try {
      setStoryLoading(true);
      setStoryError('');
      const response = await axios.get(`${API_URL}/stories/${slug}`);
      setActiveStory(response.data);
    } catch (err) {
      setStoryError(`Failed to load story. Please try again.`);
      console.error(err);
    } finally {
      setStoryLoading(false);
    }
  }, []);

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

  const handleStoryClick = (slug) => {
    // Save current map context before navigating
    mapContextRef.current = {
      selectedCountryCode: selectedCountry?.code,
      isPanelOpen
    };
    navigate(`/stories/${slug}`);
  };

  const handleCloseStory = () => {
    setActiveStory(null);
    setStoryError('');

    // Restore map context
    if (mapContextRef.current) {
      const { selectedCountryCode, isPanelOpen: wasOpen } = mapContextRef.current;
      if (selectedCountryCode && wasOpen) {
        fetchCountryDetails(selectedCountryCode);
      }
      mapContextRef.current = null;
    }

    navigate('/');
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
          countriesWithStories={countriesWithStories}
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
        onStoryClick={handleStoryClick}
      />

      {/* Story Reader Route */}
      <Routes>
        <Route path="/" element={null} />
        <Route
          path="/stories/:slug"
          element={
            <StoryRoute
              fetchStory={fetchStory}
              activeStory={activeStory}
              storyLoading={storyLoading}
              storyError={storyError}
              onClose={handleCloseStory}
            />
          }
        />
      </Routes>
    </div>
  );
}

// Wrapper component to handle story route
function StoryRoute({ fetchStory, activeStory, storyLoading, storyError, onClose }) {
  const { slug } = useParams();

  useEffect(() => {
    if (slug) {
      fetchStory(slug);
    }
  }, [slug, fetchStory]);

  return (
    <StoryReader
      story={activeStory}
      loading={storyLoading}
      error={storyError}
      onClose={onClose}
    />
  );
}

export default App;