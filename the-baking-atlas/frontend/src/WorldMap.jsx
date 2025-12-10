import { useRef, useEffect, useState } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const MAPTILER_KEY = import.meta.env.VITE_MAPTILER_KEY;

function WorldMap({ countries, onCountryClick }) {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [hoveredCountry, setHoveredCountry] = useState(null);
  const hoveredStateId = useRef(null);

  // Use refs to always have current data in event handlers
  const countriesRef = useRef(countries);
  const onCountryClickRef = useRef(onCountryClick);

  // Keep refs up to date
  useEffect(() => {
    countriesRef.current = countries;
  }, [countries]);

  useEffect(() => {
    onCountryClickRef.current = onCountryClick;
  }, [onCountryClick]);

  // Helper to check if a country has data (uses ref for current data)
  const hasCountryData = (countryCode) => {
    return countriesRef.current.some(c => c.code === countryCode);
  };

  // Helper to get country by code (uses ref for current data)
  const getCountryByCode = (countryCode) => {
    return countriesRef.current.find(c => c.code === countryCode);
  };

  useEffect(() => {
    if (map.current) return; // Initialize map only once

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: `https://api.maptiler.com/maps/dataviz-light/style.json?key=${MAPTILER_KEY}`,
      center: [0, 20],
      zoom: 1.5,
      minZoom: 1,
      maxZoom: 8,
    });

    map.current.addControl(new maplibregl.NavigationControl(), 'top-left');

    map.current.on('load', () => {
      // Add country boundaries source from MapTiler
      // Use promoteId to set iso_a2 as the feature ID for feature-state to work
      map.current.addSource('countries', {
        type: 'vector',
        url: `https://api.maptiler.com/tiles/countries/tiles.json?key=${MAPTILER_KEY}`,
        promoteId: { 'administrative': 'iso_a2' }
      });

      // Add an invisible but interactive fill layer for ALL countries
      // This ensures mouse events are captured everywhere
      map.current.addLayer({
        id: 'countries-interactive',
        type: 'fill',
        source: 'countries',
        'source-layer': 'administrative',
        filter: ['==', ['get', 'level'], 0],
        paint: {
          'fill-color': 'transparent',
          'fill-opacity': 1
        }
      });

      // Add visible fill layer for countries with data only
      map.current.addLayer({
        id: 'countries-fill',
        type: 'fill',
        source: 'countries',
        'source-layer': 'administrative',
        filter: ['==', ['get', 'level'], 0],
        paint: {
          'fill-color': '#667eea',
          'fill-opacity': [
            'case',
            ['boolean', ['feature-state', 'hover'], false],
            0.6,
            ['boolean', ['feature-state', 'hasData'], false],
            0.4,
            0
          ]
        }
      });

      // Add border layer for countries with data
      map.current.addLayer({
        id: 'countries-border',
        type: 'line',
        source: 'countries',
        'source-layer': 'administrative',
        filter: ['==', ['get', 'level'], 0],
        paint: {
          'line-color': '#764ba2',
          'line-opacity': [
            'case',
            ['boolean', ['feature-state', 'hasData'], false],
            1,
            0
          ],
          'line-width': [
            'case',
            ['boolean', ['feature-state', 'hover'], false],
            2.5,
            1.5
          ]
        }
      });

      // Set initial feature states for countries with data
      updateCountryStates();
    });

    // Hover effect - use the interactive layer for capturing events
    map.current.on('mousemove', 'countries-interactive', (e) => {
      if (e.features.length > 0) {
        const feature = e.features[0];
        const countryCode = feature.properties.iso_a2;

        // Only show hover for countries with data
        if (!hasCountryData(countryCode)) {
          map.current.getCanvas().style.cursor = '';
          // Clear any existing hover state
          if (hoveredStateId.current !== null) {
            map.current.setFeatureState(
              { source: 'countries', sourceLayer: 'administrative', id: hoveredStateId.current },
              { hover: false }
            );
            hoveredStateId.current = null;
            setHoveredCountry(null);
          }
          return;
        }

        map.current.getCanvas().style.cursor = 'pointer';

        // Remove hover from previous if different country
        if (hoveredStateId.current !== null && hoveredStateId.current !== countryCode) {
          map.current.setFeatureState(
            { source: 'countries', sourceLayer: 'administrative', id: hoveredStateId.current },
            { hover: false }
          );
        }

        hoveredStateId.current = countryCode;
        map.current.setFeatureState(
          { source: 'countries', sourceLayer: 'administrative', id: countryCode },
          { hover: true }
        );

        // Find country name from our data
        const country = getCountryByCode(countryCode);
        if (country) {
          setHoveredCountry(country.name);
        }
      }
    });

    map.current.on('mouseleave', 'countries-interactive', () => {
      map.current.getCanvas().style.cursor = '';
      if (hoveredStateId.current !== null) {
        map.current.setFeatureState(
          { source: 'countries', sourceLayer: 'administrative', id: hoveredStateId.current },
          { hover: false }
        );
      }
      hoveredStateId.current = null;
      setHoveredCountry(null);
    });

    // Click handler - use the interactive layer
    map.current.on('click', 'countries-interactive', (e) => {
      if (e.features.length > 0) {
        const feature = e.features[0];
        const countryCode = feature.properties.iso_a2;

        // Only handle clicks for countries with data
        const country = getCountryByCode(countryCode);
        if (country) {
          onCountryClickRef.current(country);
        }
      }
    });

    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, []); // Empty deps - only initialize once

  // Update feature states when countries data changes
  const updateCountryStates = () => {
    if (!map.current || !map.current.isStyleLoaded()) return;

    const source = map.current.getSource('countries');
    if (!source) return;

    // Query all country features and update their state
    const features = map.current.querySourceFeatures('countries', {
      sourceLayer: 'administrative',
      filter: ['==', ['get', 'level'], 0]
    });

    const countryCodesWithData = new Set(countriesRef.current.map(c => c.code));

    features.forEach(feature => {
      const countryCode = feature.properties.iso_a2;
      if (!countryCode) return;

      const hasData = countryCodesWithData.has(countryCode);

      map.current.setFeatureState(
        { source: 'countries', sourceLayer: 'administrative', id: countryCode },
        { hasData }
      );
    });
  };

  // Update states when countries change or map moves
  useEffect(() => {
    if (!map.current) return;

    const handleUpdate = () => updateCountryStates();

    if (map.current.isStyleLoaded()) {
      updateCountryStates();
    }

    map.current.on('sourcedata', handleUpdate);
    map.current.on('moveend', handleUpdate);

    return () => {
      if (map.current) {
        map.current.off('sourcedata', handleUpdate);
        map.current.off('moveend', handleUpdate);
      }
    };
  }, [countries]);

  return (
    <div className="map-container">
      <div ref={mapContainer} className="map" />
      {hoveredCountry && (
        <div className="map-tooltip">
          Click to explore {hoveredCountry}'s baking traditions
        </div>
      )}
    </div>
  );
}

export default WorldMap;
