from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models import models, schemas

router = APIRouter(prefix="/api/countries", tags=["countries"])


@router.get("/", response_model=List[schemas.CountryListItem])
def get_all_countries(db: Session = Depends(get_db)):
    """
    Get a list of all countries (without full details).
    
    This is what you'd use to populate your map or country selector.
    """
    countries = db.query(models.Country).all()
    return countries


@router.get("/{country_code}", response_model=schemas.Country)
def get_country_by_code(country_code: str, db: Session = Depends(get_db)):
    """
    Get full details for a specific country by its code (e.g., "JP" for Japan).
    
    This includes all baked goods and ingredients for that country.
    """
    country = db.query(models.Country).filter(
        models.Country.code == country_code.upper()
    ).first()
    
    if not country:
        raise HTTPException(
            status_code=404, 
            detail=f"Country with code '{country_code}' not found"
        )
    
    return country


@router.post("/", response_model=schemas.Country)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    """
    Create a new country entry.
    
    You'll use this to add countries to your database.
    """
    # Check if country code already exists
    existing = db.query(models.Country).filter(
        models.Country.code == country.code.upper()
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Country with code '{country.code}' already exists"
        )
    
    # Create new country
    db_country = models.Country(
        name=country.name,
        code=country.code.upper(),
        region=country.region,
        overview=country.overview,
        extra_data=country.extra_data
    )
    
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    
    return db_country


@router.post("/{country_code}/baked-goods", response_model=schemas.BakedGood)
def add_baked_good(
    country_code: str, 
    baked_good: schemas.BakedGoodCreate,
    db: Session = Depends(get_db)
):
    """
    Add a baked good to a specific country.
    """
    # Find the country
    country = db.query(models.Country).filter(
        models.Country.code == country_code.upper()
    ).first()
    
    if not country:
        raise HTTPException(
            status_code=404,
            detail=f"Country with code '{country_code}' not found"
        )
    
    # Create the baked good
    db_baked_good = models.BakedGood(
        country_id=country.id,
        name=baked_good.name,
        description=baked_good.description,
        category=baked_good.category,
        metadata=baked_good.metadata
    )
    
    db.add(db_baked_good)
    db.commit()
    db.refresh(db_baked_good)
    
    return db_baked_good


@router.post("/{country_code}/ingredients", response_model=schemas.Ingredient)
def add_ingredient(
    country_code: str,
    ingredient: schemas.IngredientCreate,
    db: Session = Depends(get_db)
):
    """
    Add an ingredient to a specific country.
    """
    # Find the country
    country = db.query(models.Country).filter(
        models.Country.code == country_code.upper()
    ).first()
    
    if not country:
        raise HTTPException(
            status_code=404,
            detail=f"Country with code '{country_code}' not found"
        )
    
    # Create the ingredient
    db_ingredient = models.Ingredient(
        country_id=country.id,
        name=ingredient.name,
        description=ingredient.description,
        metadata=ingredient.metadata
    )
    
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    
    return db_ingredient