from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models import models, schemas
from typing import Optional

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
        extra_data=baked_good.extra_data
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
        extra_data=ingredient.extra_data
    )
    
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    
    return db_ingredient

@router.put("/{country_code}", response_model=schemas.Country)
def update_country(
    country_code: str,
    country_update: schemas.CountryCreate,
    db: Session = Depends(get_db)
):
    """
    Update an existing country's information.
    
    This replaces ALL fields, so make sure to include everything.
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
    
    # Update all fields
    country.name = country_update.name
    country.code = country_update.code.upper()
    country.region = country_update.region
    country.overview = country_update.overview
    country.extra_data = country_update.extra_data
    
    db.commit()
    db.refresh(country)
    
    return country


@router.put("/baked-goods/{baked_good_id}", response_model=schemas.BakedGood)
def update_baked_good(
    baked_good_id: int,
    baked_good_update: schemas.BakedGoodCreate,
    db: Session = Depends(get_db)
):
    """
    Update an existing baked good.
    
    You need the baked_good's ID (get it from GET /api/countries/{code})
    """
    # Find the baked good
    baked_good = db.query(models.BakedGood).filter(
        models.BakedGood.id == baked_good_id
    ).first()
    
    if not baked_good:
        raise HTTPException(
            status_code=404,
            detail=f"Baked good with ID {baked_good_id} not found"
        )
    
    # Update fields
    baked_good.name = baked_good_update.name
    baked_good.description = baked_good_update.description
    baked_good.category = baked_good_update.category
    baked_good.extra_data = baked_good_update.extra_data
    
    db.commit()
    db.refresh(baked_good)
    
    return baked_good


@router.put("/ingredients/{ingredient_id}", response_model=schemas.Ingredient)
def update_ingredient(
    ingredient_id: int,
    ingredient_update: schemas.IngredientCreate,
    db: Session = Depends(get_db)
):
    """
    Update an existing ingredient.
    
    You need the ingredient's ID (get it from GET /api/countries/{code})
    """
    # Find the ingredient
    ingredient = db.query(models.Ingredient).filter(
        models.Ingredient.id == ingredient_id
    ).first()
    
    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail=f"Ingredient with ID {ingredient_id} not found"
        )
    
    # Update fields
    ingredient.name = ingredient_update.name
    ingredient.description = ingredient_update.description
    ingredient.extra_data = ingredient_update.extra_data
    
    db.commit()
    db.refresh(ingredient)
    
    return ingredient


@router.delete("/{country_code}")
def delete_country(country_code: str, db: Session = Depends(get_db)):
    """
    Delete a country and all its related data.
    
    WARNING: This also deletes all baked goods and ingredients for this country!
    """
    country = db.query(models.Country).filter(
        models.Country.code == country_code.upper()
    ).first()
    
    if not country:
        raise HTTPException(
            status_code=404,
            detail=f"Country with code '{country_code}' not found"
        )
    
    db.delete(country)
    db.commit()
    
    return {"message": f"Country {country_code} deleted successfully"}


@router.delete("/baked-goods/{baked_good_id}")
def delete_baked_good(baked_good_id: int, db: Session = Depends(get_db)):
    """Delete a specific baked good by ID"""
    baked_good = db.query(models.BakedGood).filter(
        models.BakedGood.id == baked_good_id
    ).first()
    
    if not baked_good:
        raise HTTPException(
            status_code=404,
            detail=f"Baked good with ID {baked_good_id} not found"
        )
    
    db.delete(baked_good)
    db.commit()
    
    return {"message": f"Baked good '{baked_good.name}' deleted successfully"}


@router.delete("/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Delete a specific ingredient by ID"""
    ingredient = db.query(models.Ingredient).filter(
        models.Ingredient.id == ingredient_id
    ).first()
    
    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail=f"Ingredient with ID {ingredient_id} not found"
        )
    
    db.delete(ingredient)
    db.commit()
    
    return {"message": f"Ingredient '{ingredient.name}' deleted successfully"}