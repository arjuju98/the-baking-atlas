from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.models import models, schemas

router = APIRouter(prefix="/api/stories", tags=["stories"])


def get_or_create_tag(db: Session, tag_name: str, tag_type: Optional[str] = None) -> models.Tag:
    """Helper to get existing tag or create new one."""
    tag = db.query(models.Tag).filter(models.Tag.name == tag_name.lower()).first()
    if not tag:
        tag = models.Tag(name=tag_name.lower(), tag_type=tag_type)
        db.add(tag)
        db.flush()  # Get ID without committing
    return tag


@router.get("/", response_model=List[schemas.StoryListItem])
def get_all_stories(
    region: Optional[str] = Query(None, description="Filter by country code"),
    tag: Optional[str] = Query(None, description="Filter by tag name"),
    time_context: Optional[str] = Query(None, description="Filter by time context"),
    db: Session = Depends(get_db)
):
    """
    Get a list of all stories (without full body content).

    Supports filtering by region (country code), tag, or time_context.
    """
    query = db.query(models.Story)

    if region:
        query = query.join(models.Story.regions).filter(
            models.Country.code == region.upper()
        )

    if tag:
        query = query.join(models.Story.tags).filter(
            models.Tag.name == tag.lower()
        )

    if time_context:
        query = query.filter(models.Story.time_context == time_context)

    stories = query.order_by(models.Story.published_at.desc()).all()
    return stories


@router.get("/{slug}", response_model=schemas.Story)
def get_story_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Get full story content by its URL slug.
    """
    story = db.query(models.Story).filter(models.Story.slug == slug).first()

    if not story:
        raise HTTPException(
            status_code=404,
            detail=f"Story with slug '{slug}' not found"
        )

    return story


@router.post("/", response_model=schemas.Story)
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db)):
    """
    Create a new story.

    Pass region_codes as a list of country codes (e.g., ["JP", "KR"]).
    Pass tag_names as a list of tag names (tags are created if they don't exist).
    """
    # Check if slug already exists
    existing = db.query(models.Story).filter(models.Story.slug == story.slug).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Story with slug '{story.slug}' already exists"
        )

    # Create the story
    db_story = models.Story(
        title=story.title,
        slug=story.slug,
        summary=story.summary,
        body=story.body,
        time_context=story.time_context,
        author_name=story.author_name,
        sources=story.sources,
        extra_data=story.extra_data
    )

    # Associate regions (countries)
    if story.region_codes:
        for code in story.region_codes:
            country = db.query(models.Country).filter(
                models.Country.code == code.upper()
            ).first()
            if country:
                db_story.regions.append(country)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Country with code '{code}' not found"
                )

    # Associate tags (create if not exist)
    if story.tag_names:
        for tag_name in story.tag_names:
            tag = get_or_create_tag(db, tag_name)
            db_story.tags.append(tag)

    db.add(db_story)
    db.commit()
    db.refresh(db_story)

    return db_story


@router.put("/{slug}", response_model=schemas.Story)
def update_story(
    slug: str,
    story_update: schemas.StoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing story.

    Only provided fields will be updated.
    """
    story = db.query(models.Story).filter(models.Story.slug == slug).first()

    if not story:
        raise HTTPException(
            status_code=404,
            detail=f"Story with slug '{slug}' not found"
        )

    # Update scalar fields if provided
    if story_update.title is not None:
        story.title = story_update.title
    if story_update.slug is not None:
        # Check new slug doesn't conflict
        if story_update.slug != slug:
            existing = db.query(models.Story).filter(
                models.Story.slug == story_update.slug
            ).first()
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Story with slug '{story_update.slug}' already exists"
                )
        story.slug = story_update.slug
    if story_update.summary is not None:
        story.summary = story_update.summary
    if story_update.body is not None:
        story.body = story_update.body
    if story_update.time_context is not None:
        story.time_context = story_update.time_context
    if story_update.author_name is not None:
        story.author_name = story_update.author_name
    if story_update.sources is not None:
        story.sources = story_update.sources
    if story_update.extra_data is not None:
        story.extra_data = story_update.extra_data

    # Update regions if provided
    if story_update.region_codes is not None:
        story.regions.clear()
        for code in story_update.region_codes:
            country = db.query(models.Country).filter(
                models.Country.code == code.upper()
            ).first()
            if country:
                story.regions.append(country)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Country with code '{code}' not found"
                )

    # Update tags if provided
    if story_update.tag_names is not None:
        story.tags.clear()
        for tag_name in story_update.tag_names:
            tag = get_or_create_tag(db, tag_name)
            story.tags.append(tag)

    db.commit()
    db.refresh(story)

    return story


@router.delete("/{slug}")
def delete_story(slug: str, db: Session = Depends(get_db)):
    """
    Delete a story by its slug.
    """
    story = db.query(models.Story).filter(models.Story.slug == slug).first()

    if not story:
        raise HTTPException(
            status_code=404,
            detail=f"Story with slug '{slug}' not found"
        )

    db.delete(story)
    db.commit()

    return {"message": f"Story '{story.title}' deleted successfully"}


# === TAG ENDPOINTS ===

@router.get("/tags/", response_model=List[schemas.Tag])
def get_all_tags(
    tag_type: Optional[str] = Query(None, description="Filter by tag type"),
    db: Session = Depends(get_db)
):
    """
    Get all available tags.

    Optionally filter by tag_type (ingredient, technique, theme).
    """
    query = db.query(models.Tag)

    if tag_type:
        query = query.filter(models.Tag.tag_type == tag_type)

    return query.order_by(models.Tag.name).all()


@router.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    """
    Create a new tag.
    """
    existing = db.query(models.Tag).filter(models.Tag.name == tag.name.lower()).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Tag '{tag.name}' already exists"
        )

    db_tag = models.Tag(name=tag.name.lower(), tag_type=tag.tag_type)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return db_tag


@router.delete("/tags/{tag_name}")
def delete_tag(tag_name: str, db: Session = Depends(get_db)):
    """
    Delete a tag by name.
    """
    tag = db.query(models.Tag).filter(models.Tag.name == tag_name.lower()).first()

    if not tag:
        raise HTTPException(
            status_code=404,
            detail=f"Tag '{tag_name}' not found"
        )

    db.delete(tag)
    db.commit()

    return {"message": f"Tag '{tag_name}' deleted successfully"}
