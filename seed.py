from app.database import SessionLocal, engine, Base
from app import models, auth
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed():
    # Check if admin exists
    admin = db.query(models.User).filter(models.User.email == "admin@kickforecast.com").first()
    if not admin:
        print("Creating admin user...")
        hashed_password = auth.get_password_hash("admin123")
        admin = models.User(
            email="admin@kickforecast.com",
            hashed_password=hashed_password,
            role=models.UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
    else:
        print("Admin user already exists.")

    # Check if posts exist
    if db.query(models.Post).count() == 0:
        print("Creating sample posts...")
        
        posts = [
            models.Post(
                title="Manchester City vs Liverpool Prediction",
                slug="man-city-vs-liverpool-prediction",
                content="""Manchester City host Liverpool in what promises to be a title-deciding clash at the Etihad Stadium.
                
Both teams are in excellent form, but City's home advantage might just be the difference here. Haaland has been unstoppable, and with De Bruyne pulling the strings, Liverpool's defense will be tested to the limit.

However, Liverpool's counter-attacking threat through Salah and Diaz cannot be ignored. We expect a high-scoring game with chances at both ends.

**Key Stats:**
- Man City have won their last 5 home games.
- Liverpool have scored in every away game this season.
- Over 2.5 goals have landed in 4 of the last 5 meetings.

**Prediction:**
We are backing Manchester City to edge this one 3-2 in a thriller.""",
                summary="Title clash at the Etihad. Expect goals as the two giants of English football collide.",
                match_date=datetime.now() + timedelta(days=2),
                home_team="Manchester City",
                away_team="Liverpool",
                prediction="Man City Win & Over 3.5 Goals",
                odds="3.50",
                is_published=True,
                author_id=admin.id
            ),
            models.Post(
                title="Real Madrid vs Barcelona - El Clasico Preview",
                slug="real-madrid-vs-barcelona-el-clasico",
                content="""El Clasico returns to the Bernabeu with both sides fighting for the La Liga top spot.
                
Real Madrid have been pragmatic but effective under Ancelotti, while Xavi's Barcelona are playing with renewed flair. Bellingham's impact for Madrid has been immense, and he could be the key to unlocking the Barca defense.

Barcelona will look to control possession, but Madrid's transition game is lethal.

**Prediction:**
A tight affair, likely ending in a draw or a narrow Madrid win.""",
                summary="El Clasico preview. Can Bellingham make the difference for Los Blancos?",
                match_date=datetime.now() + timedelta(days=5),
                home_team="Real Madrid",
                away_team="Barcelona",
                prediction="Real Madrid Win",
                odds="2.10",
                is_published=True,
                author_id=admin.id
            ),
             models.Post(
                title="Arsenal vs Tottenham - North London Derby",
                slug="arsenal-vs-tottenham-nld",
                content="""The North London Derby is always a fiery encounter. Arsenal are looking to bounce back from a recent defeat, while Spurs are flying high under Ange Postecoglou.
                
Expect goals, cards, and drama.

**Prediction:**
Arsenal to win 2-1.""",
                summary="North London Derby prediction. Sparks will fly at the Emirates.",
                match_date=datetime.now() + timedelta(days=1),
                home_team="Arsenal",
                away_team="Tottenham",
                prediction="Arsenal Win",
                odds="1.85",
                is_published=False, # Draft
                author_id=admin.id
            )
        ]
        
        db.add_all(posts)
        db.commit()
        print("Sample posts created.")
    else:
        print("Posts already exist.")

    db.close()

if __name__ == "__main__":
    seed()
