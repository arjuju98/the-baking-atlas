import { useState, useEffect, useRef } from 'react';
import { X, ChevronDown, ChevronUp } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import './StoryReader.css';

function StoryReader({ story, loading, error, onClose }) {
  const [sourcesExpanded, setSourcesExpanded] = useState(false);
  const overlayRef = useRef(null);

  // Focus overlay on mount for keyboard events
  useEffect(() => {
    if (overlayRef.current) {
      overlayRef.current.focus();
    }
  }, []);

  // Handle Escape key to close
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  if (loading) {
    return (
      <div className="story-reader-overlay" ref={overlayRef} onKeyDown={handleKeyDown} tabIndex={0}>
        <div className="story-reader-backdrop" onClick={onClose} />
        <div className="story-reader-container">
          <StoryLoadingSkeleton onClose={onClose} />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="story-reader-overlay" ref={overlayRef} onKeyDown={handleKeyDown} tabIndex={0}>
        <div className="story-reader-backdrop" onClick={onClose} />
        <div className="story-reader-container">
          <div className="story-reader-error">
            <p>{error}</p>
            <button onClick={onClose}>Go Back</button>
          </div>
        </div>
      </div>
    );
  }

  if (!story) return null;

  return (
    <div className="story-reader-overlay" ref={overlayRef} onKeyDown={handleKeyDown} tabIndex={0}>
      <div className="story-reader-backdrop" onClick={onClose} />
      <div className="story-reader-container">
        {/* Close Button */}
        <button className="story-close-button" onClick={onClose} aria-label="Close story">
          <X size={24} />
        </button>

        {/* Scrollable Content */}
        <div className="story-reader-content">
          {/* Story Header */}
          <header className="story-header">
            <h1 className="story-title">{story.title}</h1>

            <div className="story-meta">
              {story.author_name && (
                <span className="story-author">By {story.author_name}</span>
              )}
              {story.time_context && (
                <span className="story-time-context">{story.time_context}</span>
              )}
            </div>

            {story.regions && story.regions.length > 0 && (
              <div className="story-regions">
                {story.regions.map((region) => (
                  <span key={region.code} className="region-badge">
                    {region.name}
                  </span>
                ))}
              </div>
            )}

            {story.summary && (
              <p className="story-summary">{story.summary}</p>
            )}
          </header>

          {/* Story Body - Markdown */}
          <article className="story-body">
            <ReactMarkdown>{story.body}</ReactMarkdown>
          </article>

          {/* Sources Section */}
          {story.sources && (
            <section className="story-sources">
              <button
                className="sources-toggle"
                onClick={() => setSourcesExpanded(!sourcesExpanded)}
              >
                <span>Sources & References</span>
                {sourcesExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </button>
              {sourcesExpanded && (
                <div className="sources-content">
                  <ReactMarkdown>{story.sources}</ReactMarkdown>
                </div>
              )}
            </section>
          )}

          {/* Tags (future use, show if present) */}
          {story.tags && story.tags.length > 0 && (
            <div className="story-tags">
              {story.tags.map((tag) => (
                <span key={tag.id} className="tag-badge">
                  {tag.name}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function StoryLoadingSkeleton({ onClose }) {
  return (
    <>
      <button className="story-close-button" onClick={onClose} aria-label="Close">
        <X size={24} />
      </button>
      <div className="story-reader-content">
        <div className="story-loading-skeleton">
          <div className="skeleton-line title"></div>
          <div className="skeleton-line meta"></div>
          <div className="skeleton-line meta short"></div>
          <div className="skeleton-divider"></div>
          <div className="skeleton-line body"></div>
          <div className="skeleton-line body"></div>
          <div className="skeleton-line body short"></div>
          <div className="skeleton-line body"></div>
          <div className="skeleton-line body"></div>
        </div>
      </div>
    </>
  );
}

export default StoryReader;
