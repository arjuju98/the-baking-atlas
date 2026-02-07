import './StoryCard.css';

function StoryCard({ story, onClick }) {
  return (
    <div className="story-card" onClick={() => onClick(story.slug)}>
      <div className="story-card-header">
        <h3 className="story-card-title">{story.title}</h3>
        {story.time_context && (
          <span className="story-time-context">{story.time_context}</span>
        )}
      </div>
      {story.summary && (
        <p className="story-card-summary">{story.summary}</p>
      )}
      <span className="story-card-link">Read story</span>
    </div>
  );
}

export default StoryCard;
