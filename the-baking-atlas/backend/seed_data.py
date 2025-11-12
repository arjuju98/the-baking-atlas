"""
Script to seed the database with initial data.

This makes it easy to add your test countries without writing raw SQL!
"""

from app.database.database import SessionLocal, engine
from app.models.models import Base, Country, BakedGood, Ingredient

def seed_database():
    """Seed the database with sample data"""
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out if you want to keep data)
        print("Clearing existing data...")
        db.query(Ingredient).delete()
        db.query(BakedGood).delete()
        db.query(Country).delete()
        db.commit()
        
        print("\nAdding countries...")
        
        # ===== JAPAN =====
        japan = Country(
            name="Japan",
            code="JP",
            region="East Asia",
            overview="Japanese baking blends traditional European techniques with local ingredients and aesthetics. Influenced by Portuguese traders in the 16th century and later by French patisserie, Japanese bakeries have created unique fusion pastries that are now beloved worldwide.",
            extra_data={
                "baking_history": "Portuguese missionaries introduced castella cake in the 1500s, which became the foundation of Japanese confectionery",
                "bakery_culture": "Convenience store pastries and kissaten (coffee shops) are integral to daily life"
            }
        )
        db.add(japan)
        db.commit()
        db.refresh(japan)
        print(f"✓ Added {japan.name}")
        
        # Add Japanese baked goods
        japanese_goods = [
            BakedGood(
                country_id=japan.id,
                name="Melonpan",
                description="Sweet bread with a crispy cookie crust, named for its melon-like appearance rather than flavor",
                category="bread",
                metadata={"texture": "crispy outside, soft inside", "common_variations": ["chocolate chip", "matcha"]}
            ),
            BakedGood(
                country_id=japan.id,
                name="Castella",
                description="Sponge cake with Portuguese origins, known for its fine, moist texture and subtle sweetness",
                category="cake",
                metadata={"origin": "Portuguese pão de Castela", "traditional_occasions": ["tea time", "gifts"]}
            ),
            BakedGood(
                country_id=japan.id,
                name="Anpan",
                description="Soft bread bun filled with sweet azuki bean paste, created in 1874 by Yasube Kimura",
                category="bread",
                metadata={"filling_variations": ["koshi-an (smooth)", "tsubu-an (chunky)"], "historical_significance": "First Japanese-Western fusion bread"}
            ),
        ]
        
        for good in japanese_goods:
            db.add(good)
            print(f"  ✓ Added {good.name}")
        
        # Add Japanese ingredients
        japanese_ingredients = [
            Ingredient(
                country_id=japan.id,
                name="Azuki beans",
                description="Small red beans used to make sweet paste (anko) for filling breads and pastries",
                metadata={"preparation": "boiled and sweetened", "traditional_uses": ["anpan", "dorayaki", "taiyaki"]}
            ),
            Ingredient(
                country_id=japan.id,
                name="Matcha",
                description="Finely ground green tea powder, adds earthy flavor and vibrant color",
                metadata={"grade_varieties": ["ceremonial", "culinary"], "flavor_profile": "umami, slightly bitter"}
            ),
            Ingredient(
                country_id=japan.id,
                name="Mochi rice flour",
                description="Glutinous rice flour that creates chewy texture in baked goods",
                metadata={"texture_contribution": "chewy, sticky", "products": ["mochi bread", "daifuku"]}
            ),
        ]
        
        for ingredient in japanese_ingredients:
            db.add(ingredient)
            print(f"  ✓ Added {ingredient.name}")
        
        db.commit()
        
        print("\n" + "="*50)
        print("Database seeded successfully!")
        print("="*50)
        print("\nYou can now:")
        print("1. Start your API: uvicorn app.main:app --reload")
        print("2. View docs at: http://localhost:8000/docs")
        print("3. Test endpoint: http://localhost:8000/api/countries/JP")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()