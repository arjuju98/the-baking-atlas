import { X } from 'lucide-react';
import './InfoPanel.css';

function InfoPanel({ isOpen, countryData, loading, error, onClose }) {
  // Don't render anything if not open
  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop - clicking it closes the panel */}
      <div 
        className={`panel-backdrop ${isOpen ? 'visible' : ''}`}
        onClick={onClose}
      />
      
      {/* The actual panel */}
      <div className={`info-panel ${isOpen ? 'open' : ''}`}>
        {/* Fixed Panel Header */}
        <div className="panel-header">
          {countryData && (
            <div className="country-title">
              <h1>{countryData.name}</h1>
              <span className="country-code-badge">{countryData.code}</span>
            </div>
          )}
          <button
            className="close-button"
            onClick={onClose}
            aria-label="Close panel"
          >
            <X size={24} />
          </button>
        </div>

        {/* Scrollable Content Area */}
        <div className="panel-content">
          {loading && <LoadingSkeleton />}

          {error && (
            <div className="panel-error">
              <p>⚠️ {error}</p>
              <button onClick={onClose}>Close</button>
            </div>
          )}

          {!loading && !error && countryData && (
            <CountryContent country={countryData} showTitle={false} />
          )}
        </div>
      </div>
    </>
  );
}

// Loading skeleton while fetching data
function LoadingSkeleton() {
  return (
    <div className="loading-skeleton">
      <div className="skeleton-header">
        <div className="skeleton-box large"></div>
        <div className="skeleton-box small"></div>
      </div>
      <div className="skeleton-section">
        <div className="skeleton-box medium"></div>
        <div className="skeleton-box medium"></div>
        <div className="skeleton-box medium"></div>
      </div>
    </div>
  );
}

// Main country content component
function CountryContent({ country, showTitle = true }) {
  return (
    <>
      {/* Country Header - only shown if showTitle is true */}
      {showTitle && (
        <div className="country-title">
          <h1>{country.name}</h1>
          <span className="country-code-badge">{country.code}</span>
        </div>
      )}

      {country.region && (
        <p className="country-region">📍 {country.region}</p>
      )}

      {/* Overview Section */}
      {country.overview && (
        <div className="content-section">
          <h2>Overview</h2>
          <p>{country.overview}</p>
        </div>
      )}

      {/* Additional Information from extra_data */}
      {country.extra_data && Object.keys(country.extra_data).length > 0 && (
        <div className="content-section">
          <h2>Additional Information</h2>
          <div className="extra-info">
            {Object.entries(country.extra_data).map(([key, value]) => (
              <div key={key} className="info-item">
                <strong>{key.replace(/_/g, ' ')}:</strong>
                <span>{value}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Signature Baked Goods */}
      {country.baked_goods && country.baked_goods.length > 0 && (
        <div className="content-section">
          <h2>🥐 Signature Baked Goods</h2>
          <div className="items-list">
            {country.baked_goods.map((good) => (
              <div key={good.id} className="item">
                <div className="item-header">
                  <h3>{good.name}</h3>
                  {good.category && (
                    <span className="category-tag">{good.category}</span>
                  )}
                </div>
                <p className="item-description">{good.description}</p>
                
                {good.extra_data && (
                  <div className="item-details">
                    {Object.entries(good.extra_data).map(([key, value]) => (
                      <div key={key} className="detail">
                        <strong>{key}:</strong>{' '}
                        {Array.isArray(value) ? value.join(', ') : value}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Ingredients */}
      {country.ingredients && country.ingredients.length > 0 && (
        <div className="content-section">
          <h2>🌾 Key Ingredients</h2>
          <div className="items-list">
            {country.ingredients.map((ingredient) => (
              <div key={ingredient.id} className="item">
                <h3>{ingredient.name}</h3>
                <p className="item-description">{ingredient.description}</p>
                
                {ingredient.extra_data && (
                  <div className="item-details">
                    {Object.entries(ingredient.extra_data).map(([key, value]) => (
                      <div key={key} className="detail">
                        <strong>{key}:</strong>{' '}
                        {Array.isArray(value) ? value.join(', ') : value}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}

export default InfoPanel;
