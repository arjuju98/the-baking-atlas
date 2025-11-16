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
        country_code = "CA"  # Change this
        existing = db.query(Country).filter(Country.code == country_code).first()
        if existing:
            print(f"❌ Country {country_code} already exists!")
            return
        
        # Create the country
        new_country = Country(
            name="Canada",  # Change this
            code="CA",      # Change this
            region="North America",  # Change this
            overview="Canadian baking blends international influence from its rich immigrant history with a strong modern focus on health-conscious and artisinal specialty goods.",  # Change this
            extra_data={
                "baking_history": "Early Canadian baking was shaped by French and British traditions, which led to unique dishes like the butter tart. The 20th century saw the rise of commerical baking and the government fortification of bread.",
                "bakery_culture": "Modern Canadian baking culture has started to skew towards healthier options. While classic goods like pies and donuts are still popular, Canada has seen an increased demand for desserts under the gluten-free or natural sugar umbrella, like date squares or oatcakes."
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
                name="Butter Tart",
                description="Flaky pastry shell with sweet, gooey filling",
                category="pastry",
                extra_data={"consistency": "center can be either runny/gooey or firm, based on user preference",
                            "additions": "raisins" "currants" "pecans"}
            ),
            BakedGood(
                country_id=new_country.id,
                name="Date Squares",
                description="Sweet date filling sandwiched between crumbly oatmeal layers",
                category="bar",
                extra_data={"other names": "date crumbles" "matrimonial cake",
                            "flavor profile": "balance of sweet and salty"}
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
                name="Maple Syrup",
                description="Canadian sweetener used in many recipes, from breakfast to dessert",
                extra_data={"alternatives": "sugar"}
            ),
            Ingredient(
                country_id=new_country.id,
                name="Berries",
                description="Wide array of native berries are used, especially in regional desserts",
                extra_data={"types": "saskatoon" "partridgeberries" "chokecherries"}
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