from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# === SCHEMAS FOR READING DATA (what API returns) ===

class BakedGoodBase(BaseModel):
    """Base schema for baked goods"""
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class BakedGood(BakedGoodBase):
    """Schema for returning a baked good (includes ID)"""
    id: int
    country_id: int
    
    class Config:
        from_attributes = True


class IngredientBase(BaseModel):
    """Base schema for ingredients"""
    name: str
    description: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class Ingredient(IngredientBase):
    """Schema for returning an ingredient (includes ID)"""
    id: int
    country_id: int
    
    class Config:
        from_attributes = True


class CountryBase(BaseModel):
    """Base schema for countries"""
    name: str
    code: str
    region: Optional[str] = None
    overview: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


class StoryRef(BaseModel):
    """Minimal story reference for country responses"""
    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    time_context: Optional[str] = None

    class Config:
        from_attributes = True


class Country(CountryBase):
    """Schema for returning a country (includes ID and relationships)"""
    id: int
    baked_goods: List[BakedGood] = []
    ingredients: List[Ingredient] = []
    stories: List[StoryRef] = []

    class Config:
        from_attributes = True


class CountryListItem(BaseModel):
    """Simplified schema for listing countries (without full details)"""
    id: int
    name: str
    code: str
    region: Optional[str] = None
    
    class Config:
        from_attributes = True


# === SCHEMAS FOR CREATING DATA ===

class CountryCreate(BaseModel):
    """Schema for creating a new country"""
    name: str
    code: str
    region: Optional[str] = None
    overview: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class BakedGoodCreate(BaseModel):
    """Schema for creating a new baked good"""
    country_id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class IngredientCreate(BaseModel):
    """Schema for creating a new ingredient"""
    country_id: int
    name: str
    description: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


# === TAG SCHEMAS ===

class TagBase(BaseModel):
    """Base schema for tags"""
    name: str
    tag_type: Optional[str] = None  # "ingredient" | "technique" | "theme"


class Tag(TagBase):
    """Schema for returning a tag (includes ID)"""
    id: int

    class Config:
        from_attributes = True


class TagCreate(TagBase):
    """Schema for creating a new tag"""
    pass


# === STORY SCHEMAS ===

class RegionRef(BaseModel):
    """Minimal region reference for story responses"""
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True


class StoryBase(BaseModel):
    """Base schema for stories"""
    title: str
    slug: str
    summary: Optional[str] = None
    body: str
    time_context: Optional[str] = None  # "historical" | "modern" | "ongoing" | "mixed"
    author_name: Optional[str] = None
    sources: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


class Story(StoryBase):
    """Schema for returning a full story (includes ID, timestamps, relationships)"""
    id: int
    published_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    regions: List[RegionRef] = []
    tags: List[Tag] = []

    class Config:
        from_attributes = True


class StoryListItem(BaseModel):
    """Simplified schema for listing stories (without full body)"""
    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    time_context: Optional[str] = None
    author_name: Optional[str] = None
    published_at: Optional[datetime] = None
    regions: List[RegionRef] = []
    tags: List[Tag] = []

    class Config:
        from_attributes = True


class StoryCreate(BaseModel):
    """Schema for creating a new story"""
    title: str
    slug: str
    summary: Optional[str] = None
    body: str
    time_context: Optional[str] = None
    author_name: Optional[str] = None
    sources: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None
    region_codes: List[str] = []  # List of country codes to associate
    tag_names: List[str] = []  # List of tag names to associate (created if not exist)


class StoryUpdate(BaseModel):
    """Schema for updating a story (all fields optional)"""
    title: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    body: Optional[str] = None
    time_context: Optional[str] = None
    author_name: Optional[str] = None
    sources: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None
    region_codes: Optional[List[str]] = None
    tag_names: Optional[List[str]] = None