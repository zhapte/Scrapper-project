from app.database import SessionLocal
from app.models import User, Product, Favorite
from sqlalchemy import text
from app.auth.security import hash_password

def seed_database():
    db = SessionLocal()

    try:
        print("Clearing existing database...")
        db.execute(text("""
            TRUNCATE TABLE
                favorites,
                products,
                users
            CASCADE
        """))

        db.commit()
        print("Database cleared")
        
        user1 = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password=hash_password("password123")
        )

        user2 = User(
            first_name="Wei",
            last_name="Zhang",
            email="wei@example.com",
            password=hash_password("password123")
        )

        db.add_all([user1, user2])
        db.commit()

        product1 = Product(
            amazon_asin="B08N5WRWNW",
            name="Echo Dot",
            description="Smart speaker with Alexa",
            current_price=59.99,
            product_url="https://amazon.com/dp/B08N5WRWNW"
        )

        product2 = Product(
            amazon_asin="B0C1J2QW3X",
            name="Wireless Mouse",
            description="Bluetooth wireless mouse",
            current_price=24.99,
            product_url="https://amazon.com/dp/B0C1J2QW3X"
        )

        product3 = Product(
            amazon_asin="B09B8V1LZ3",
            name="Mechanical Keyboard",
            description="RGB mechanical keyboard",
            current_price=89.99,
            product_url="https://amazon.com/dp/B09B8V1LZ3"
        )

        db.add_all([product1, product2, product3])
        db.commit()

        favorite1 = Favorite(
            user_id=user1.user_id,
            product_id=product1.product_id,
            target_price=49.99
        )

        favorite2 = Favorite(
            user_id=user1.user_id,
            product_id=product2.product_id,
            target_price=19.99
        )

        favorite3 = Favorite(
            user_id=user2.user_id,
            product_id=product1.product_id,
            target_price=39.99
        )

        db.add_all([favorite1, favorite2, favorite3])
        db.commit()

        print("Database seeded successfully!")

    except Exception as e:
            db.rollback()
            print(f"Error seeding database: {e}")

    finally:
            db.close()

if __name__ == "__main__":
    seed_database()