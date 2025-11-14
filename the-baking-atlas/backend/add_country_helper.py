"""
Helper script to easily add new countries without editing init_database.py

Usage:
1. Edit the data in this file
2. Run: python3 add_country_helper.py
3. Data gets added to your existing database
"""

from app.database.database import SessionLocal
from app.models.models import Country, BakedGood, Ingredient

def add_new_country():
    """Add a new country with its baked goods and ingredients"""
    
    db = SessionLocal()
    
    try:
        # ===== EDIT THIS SECTION TO ADD YOUR COUNTRY =====
        
        # Check if country already exists
        country_code = "IT"  # Change this
        existing = db.query(Country).filter(Country.code == country_code).first()
        if existing:
            print(f"❌ Country {country_code} already exists!")
            return
        
        # Create the country
        new_country = Country(
            name="Italy",  # Change this
            code="IT",      # Change this
            region="Southwestern Europe",  # Change this
            overview="Italian pastry culture is defined by its strong regional diversity and deep family-oriented values. Italian pastries rely heavily on local ingredients and are often less sweet than other types, relying on natural sweetness from ingredients like citrus, nuts and fresh fruit.",  # Change this
            extra_data={
                "baking_history": "Initial pastries from Ancient Roman times were simple confections made with honey, nuts and dried fruits. Over time, new ingredients like sugar, cocoa and vanilla enriched the variety of pastries.",
                "bakery_culture": "Arab rule in Sicily influenced the development of the cannoli in the 9th century, while monastic influence can be credited for the creation of other pastries like the sfogliatella in the 17th century."
            }
        )
        db.add(new_country)
        db.commit()
        db.refresh(new_country)
        print(f"✓ Added {new_country.name}")
        
        # Add baked goods
        baked_goods = [
            BakedGood(
                country_id=new_country.id,
                name="Cannolo (Cannoli)",
                description="Tube-shaped, fried pastry shell with sweet filling",
                category="pastry",
                extra_data={"shell texture": "crisp and flaky",
                            "filling": "smooth and rich"}
            ),
            BakedGood(
                country_id=new_country.id,
                name="Sfogliatella",
                description="Shell-shaped, flaky pastry with sweet filling",
                category="pastry",
                extra_data={"texture": "crispy", "flaky": "thin",
                            "meaning": "translated to - small, thin leaf"}
            ),
            # Add more baked goods here
        ]
        
        for good in baked_goods:
            db.add(good)
            print(f"  ✓ Added {good.name}")
        
        # Add ingredients
        ingredients = [
            Ingredient(
                country_id=new_country.id,
                name="Ricotta",
                description="provides creaminess found in many Italian pastries",
                extra_data={"fat_content": "82% minimum"}
            ),
            Ingredient(
                country_id=new_country.id,
                name="Semolina",
                description="Used in dough, adds slightly coarse texture",
                extra_data={"flavor_notes": "vital in introducing nutty flavor"}
            ),
            # Add more ingredients here
        ]
        
        for ingredient in ingredients:
            db.add(ingredient)
            print(f"  ✓ Added {ingredient.name}")
        
        db.commit()
        
        # ===== END EDIT SECTION =====
        
        print("\n✓ Country added successfully!")
        print(f"View at: http://localhost:8000/api/countries/{country_code}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_new_country()