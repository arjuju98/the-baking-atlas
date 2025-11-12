from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

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