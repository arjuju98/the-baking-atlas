"""
Complete database initialization script.
This creates tables AND seeds data.
"""

from app.database.database import SessionLocal, engine, Base
from app.models.models import Country, BakedGood, Ingredient

def init_database():
    """Create all tables and seed initial data"""
    
    print("="*60)
    print("STEP 1: Creating database tables...")
    print("="*60)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully!\n")
    
    print("="*60)
    print("STEP 2: Seeding data...")
    print("="*60)
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = db.query(Country).count()
        if existing_count > 0:
            print(f"\n⚠️  Database already has {existing_count} countries.")
            response = input("Clear existing data and reseed? (yes/no): ")
            if response.lower() != 'yes':
                print("Exiting without changes.")
                return
            
            # Clear existing data
            print("\nClearing existing data...")
            db.query(Ingredient).delete()
            db.query(BakedGood).delete()
            db.query(Country).delete()
            db.commit()
            print("✓ Data cleared")
        
        print("\nAdding Japan...")
        
        # ===== JAPAN =====
        japan = Country(
            name="Japan",
            code="JP",
            region="East Asia",
            overview="Japanese baking blends traditional European techniques with local ingredients and aesthetics. Influenced by Portuguese traders in the 16th century and later by French patisserie, Japanese bakeries have created unique fusion pastries that are now beloved worldwide.",
            extra_data={
                "baking_history": "Portuguese missionaries introduced castella cake in the 1500s",
                "bakery_culture": "Convenience store pastries and kissaten are integral to daily life"
            }
        )
        db.add(japan)
        db.commit()
        db.refresh(japan)
        print(f"  ✓ Added {japan.name}")
        
        # Add Japanese baked goods
        japanese_goods = [
            BakedGood(
                country_id=japan.id,
                name="Melonpan",
                description="Sweet bread with a crispy cookie crust, named for its melon-like appearance",
                category="bread",
                extra_data={"texture": "crispy outside, soft inside"}
            ),
            BakedGood(
                country_id=japan.id,
                name="Castella",
                description="Sponge cake with Portuguese origins, known for its fine, moist texture",
                category="cake",
                extra_data={"origin": "Portuguese pão de Castela"}
            ),
            BakedGood(
                country_id=japan.id,
                name="Anpan",
                description="Soft bread bun filled with sweet azuki bean paste",
                category="bread",
                extra_data={"historical_significance": "First Japanese-Western fusion bread"}
            ),
        ]
        
        for good in japanese_goods:
            db.add(good)
            print(f"    ✓ Added {good.name}")
        
        # Add Japanese ingredients
        japanese_ingredients = [
            Ingredient(
                country_id=japan.id,
                name="Azuki beans",
                description="Small red beans used to make sweet paste (anko)",
                extra_data={"preparation": "boiled and sweetened"}
            ),
            Ingredient(
                country_id=japan.id,
                name="Matcha",
                description="Finely ground green tea powder",
                extra_data={"flavor_profile": "umami, slightly bitter"}
            ),
            Ingredient(
                country_id=japan.id,
                name="Mochi rice flour",
                description="Glutinous rice flour that creates chewy texture",
                extra_data={"texture_contribution": "chewy, sticky"}
            ),
        ]
        
        for ingredient in japanese_ingredients:
            db.add(ingredient)
            print(f"    ✓ Added {ingredient.name}")
        
        db.commit()
        
        print("\n" + "="*60)
        print("✓ DATABASE INITIALIZED SUCCESSFULLY!")
        print("="*60)
        print("\nNext steps:")
        print("1. Start API: uvicorn app.main:app --reload")
        print("2. View docs: http://localhost:8000/docs")
        print("3. Test: http://localhost:8000/api/countries/JP")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()