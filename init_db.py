from backend.database import engine, SessionLocal, Base
from backend.models import User, PestInfo
from backend.auth import get_password_hash
from sqlalchemy.orm import Session

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 1. Create Admin User
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("Creating admin user...")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created: admin / admin123")
        else:
            print("Admin user already exists.")
            
        # 2. Populate Pest Info
        pest_names = [
            "Ants", "Bees", "Beetles", "Caterpillars", "Earthworms", 
            "Earwigs", "Grasshoppers", "Moths", "Slugs", "Snails", 
            "Wasps", "Weevils"
        ]
        
        print("Populating pest info...")
        for name in pest_names:
            pest = db.query(PestInfo).filter(PestInfo.name == name).first()
            if not pest:
                new_pest = PestInfo(
                    name=name,
                    description=f"Description for {name}. Please update via Admin panel.",
                    control_methods=f"Control methods for {name}."
                )
                db.add(new_pest)
        
        db.commit()
        print("Pest info populated.")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

