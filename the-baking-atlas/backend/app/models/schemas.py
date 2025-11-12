from pydantic import BaseModel
from typing import Optional, List, Dict, Any

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

class Country(CountryBase):
    """Schema for returning a country (includes ID and relationships)"""
    id: int
    baked_goods: List[BakedGood] = []
    ingredients: List[Ingredient] = []
    
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