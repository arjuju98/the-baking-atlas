"""
Helper script to update existing data in the database

Usage:
1. Edit the code below with the data you want to update
2. Run: python3 update_data_helper.py
"""

from app.database.database import SessionLocal
from app.models.models import Country, BakedGood, Ingredient

def update_existing_data():
    """Update existing records in the database"""
    
    db = SessionLocal()
    
    try:
        # ===== UPDATE A BAKED GOOD =====
        
        # Find the baked good you want to update
        date_square = db.query(BakedGood).filter(
            BakedGood.name == "Date Squares"
        ).first()
        
        if date_square:
            print(f"Found: {date_square.name}")
            print(f"Current extra_data: {date_square.extra_data}")
            
            # Update with correct syntax (using arrays for lists)
            date_square.extra_data = {
                "flavor profile": "balance of sweet and salty",
                "other names": ["date crumbles", "matrimonial cake"]  # Now a proper list!
            }
            
            db.commit()
            print(f"✓ Updated {date_square.name}")
            print(f"New extra_data: {date_square.extra_data}\n")
        else:
            print("❌ Date Square not found\n")
        
        
        # ===== UPDATE ANOTHER BAKED GOOD (if you have more) =====
        # Just copy the pattern above and change the name
        
        # Example for updating multiple items at once:
        canadian_goods = db.query(BakedGood).join(Country).filter(
            Country.code == "CA"
        ).all()
        
        print(f"Found {len(canadian_goods)} Canadian baked goods:")
        for good in canadian_goods:
            print(f"  - {good.name}: {good.extra_data}")
        
        print("\n✓ Update complete!")
        print("View at: http://localhost:8000/api/countries/CA")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_existing_data()