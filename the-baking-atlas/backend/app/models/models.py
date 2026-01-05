from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base


# Junction tables for many-to-many relationships
story_regions = Table(
    "story_regions",
    Base.metadata,
    Column("story_id", Integer, ForeignKey("stories.id", ondelete="CASCADE"), primary_key=True),
    Column("country_id", Integer, ForeignKey("countries.id", ondelete="CASCADE"), primary_key=True)
)

story_tags = Table(
    "story_tags",
    Base.metadata,
    Column("story_id", Integer, ForeignKey("stories.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class Country(Base):
    """
    Stores information about countries and their baking cultures.
    
    Think of this as the main "chapter" for each country.
    """
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)  # e.g., "Japan"
    code = Column(String(10), unique=True, nullable=False, index=True)  # e.g., "JP"
    region = Column(String(100))  # e.g., "East Asia"
    overview = Column(Text)  # Long description of baking culture
    extra_data = Column(JSON, nullable=True)  # Flexible storage for extra data
    
    # Relationships - this creates easy access to related data
    baked_goods = relationship("BakedGood", back_populates="country", cascade="all, delete-orphan")
    ingredients = relationship("Ingredient", back_populates="country", cascade="all, delete-orphan")
    stories = relationship("Story", secondary=story_regions, back_populates="regions")
    
    def __repr__(self):
        return f"<Country {self.name} ({self.code})>"


class BakedGood(Base):
    """
    Stores individual baked goods for each country.
    
    Each baked good "belongs to" a country via country_id.
    """
    __tablename__ = "baked_goods"
    
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    name = Column(String(200), nullable=False)  # e.g., "Melonpan"
    description = Column(Text)  # What it is, how it tastes, etc.
    category = Column(String(100))  # e.g., "bread", "pastry", "cake"
    extra_data = Column(JSON, nullable=True)  # For flavor notes, occasions, etc.
    
    # Relationship back to country
    country = relationship("Country", back_populates="baked_goods")
    
    def __repr__(self):
        return f"<BakedGood {self.name}>"


class Ingredient(Base):
    """
    Stores common ingredients used in each country's baking.
    
    This helps users discover what makes each region's baking unique.
    """
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    name = Column(String(200), nullable=False)  # e.g., "matcha", "azuki beans"
    description = Column(Text, nullable=True)  # How it's used, what it adds
    extra_data = Column(JSON, nullable=True)  # For seasonal info, alternatives, etc.
    
    # Relationship back to country
    country = relationship("Country", back_populates="ingredients")

    def __repr__(self):
        return f"<Ingredient {self.name}>"


class Story(Base):
    """
    Editorial narrative content about baking cultures.

    Stories are the primary vehicle for deeper understanding,
    explaining the 'why' behind baking practices through
    constraint, history, tension, and continuity.
    """
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), unique=True, nullable=False, index=True)  # URL-friendly identifier
    summary = Column(Text)  # Excerpt for previews
    body = Column(Text, nullable=False)  # Markdown content
    time_context = Column(String(50))  # "historical" | "modern" | "ongoing" | "mixed"
    author_name = Column(String(200))  # Simple string for MVP
    sources = Column(Text, nullable=True)  # References and citations
    published_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    extra_data = Column(JSON, nullable=True)  # Future flexibility (pin coords, etc.)

    # Relationships
    regions = relationship("Country", secondary=story_regions, back_populates="stories")
    tags = relationship("Tag", secondary=story_tags, back_populates="stories")

    def __repr__(self):
        return f"<Story {self.title}>"


class Tag(Base):
    """
    Lightweight tags for cross-story discovery.

    Tags help users find related stories by ingredient,
    technique, or theme without enforcing rigid taxonomy.
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    tag_type = Column(String(50), nullable=True)  # "ingredient" | "technique" | "theme"

    # Relationships
    stories = relationship("Story", secondary=story_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.name}>"