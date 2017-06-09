from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Layout, Building, User

engine = create_engine('sqlite:///cocbuildingwithuser.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create dummy user
User1 = User(name="Steve Fan", email="fanyinze@gmail.com",
             picture='http://aretecap.com/wp-content/uploads/2015/01/dummy-profile.png')
session.add(User1)
session.commit()

# Buildings for Base1 layout
layout1 = Layout(user_id=1, name="Base 1")

session.add(layout1)
session.commit()

building1 = Building(user_id=1, name="Cannon", category = "defense", description="Cannons are great for point defense",
                     level="9", layout=layout1)

session.add(building1)
session.commit()

building2 = Building(user_id=1, name="Archer Tower", category = "defense", description="Archer Towers have longer range than cannons, unlike cannons they can attack flying enemies",
                     level="9", layout=layout1)

session.add(building2)
session.commit()

building3 = Building(user_id=1, name="Wizard Tower", category = "defense", description="The Ultimate Arcane Defense that cast powerful area effect spells",
                     level="9", layout=layout1)

session.add(building3)
session.commit()

building4 = Building(user_id=1, name="Air Defense", category = "defense", description="This anti-air tower is deadly against flying enemies",
                     level="9", layout=layout1)

session.add(building4)
session.commit()

building5 = Building(user_id=1, name="Hidden Tesla", category = "defense", description="When an enemy walks or flies close enough, the tower springs up and fires it using the power of Electrickery!",
                     level="9", layout=layout1)

session.add(building5)
session.commit()

building6 = Building(user_id=1, name="X-Bow", category = "defense", description="The X-Bow shoots mystical bolts with terrifying power",
                     level="9", layout=layout1)

session.add(building6)
session.commit()

building7 = Building(user_id=1, name="Bomb Tower", category = "defense", description="Bomb Towers bombard nearby ground troops and go up in a big BOOM when destroyed",
                     level="9", layout=layout1)

session.add(building7)
session.commit()

building8 = Building(user_id=1, name="Bomb", category = "trap", description="Nothing says 'STAY OUT' quite like a good old-fashioned hidden bomb",
                     level="9", layout=layout1)

session.add(building8)
session.commit()

building9 = Building(user_id=1, name="Air Bomb", category = "trap", description="Latest invention in the field of flying pest control. This trap can blast multiple air units in a small area",
                     level="9", layout=layout1)

session.add(building9)
session.commit()

building10 = Building(user_id=1, name="Giant Bomb", category = "trap", description="When you're looking for a Big Boom, you need the Giant Bomb",
                     level="1", layout=layout1)

session.add(building10)
session.commit()

building11 = Building(user_id=1, name="Gold Mine", category = "resource", description="The Gold Mine produces gold",
                     level="9", layout=layout1)

session.add(building11)
session.commit()

building12 = Building(user_id=1, name="Elixir Collector", category = "resource", description="Elixir is pumped from the Ley Lines coursing underneath your village",
                     level="9", layout=layout1)

session.add(building12)
session.commit()

building13 = Building(user_id=1, name="Dark Elixir Drill", category = "resource", description="Our Alchemists have finally figured a way to extract pure Dark Elixir, the rarest form of the magical substance",
                     level="4", layout=layout1)

session.add(building13)
session.commit()



# Buildings for base2
layout2 = Layout(user_id=1, name = 'Base 2')

session.add(layout2)
session.commit()


building1 = Building(user_id=1, name="Bomb", category = "trap", description="Nothing says 'STAY OUT' quite like a good old-fashioned hidden bomb",
                     level="1", layout=layout2)

session.add(building1)
session.commit()

building2 = Building(user_id=1, name="Air Bomb", category = "trap", description="Latest invention in the field of flying pest control. This trap can blast multiple air units in a small area",
                     level="1", layout=layout2)

session.add(building2)
session.commit()


building3 = Building(user_id=1, name="Seeking Air Mine", category = "trap", description="This trap does devastating damage to a single air unit",
                     level="9", layout=layout2)

session.add(building3)
session.commit()

building4 = Building(user_id=1, name="Cannon", category = "defense", description="Cannons are great for point defense",
                     level="2", layout=layout2)

session.add(building4)
session.commit()

building5 = Building(user_id=1, name="Archer Tower", category = "defense", description="Archer Towers have longer range than cannons, unlike cannons they can attack flying enemies",
                     level="2", layout=layout2)

session.add(building5)
session.commit()

building6 = Building(user_id=1, name="Gold Mine", category = "resource", description="The Gold Mine produces gold",
                     level="9", layout=layout2)

session.add(building6)
session.commit()

building7 = Building(user_id=1, name="Elixir Collector", category = "resource", description="Elixir is pumped from the Ley Lines coursing underneath your village",
                     level="9", layout=layout2)

session.add(building7)
session.commit()

# Buildings for resource
layout3 = Layout(user_id=1, name = 'Base 3')

session.add(layout3)
session.commit()


building1 = Building(user_id=1, name="Gold Mine", category = "resource", description="The Gold Mine produces gold",
                     level="2", layout=layout3)

session.add(building1)
session.commit()

building2 = Building(user_id=1, name="Elixir Collector", category = "resource", description="Elixir is pumped from the Ley Lines coursing underneath your village",
                     level="2", layout=layout3)

session.add(building2)
session.commit()

building3 = Building(user_id=1, name="Cannon", category = "defense", description="Cannons are great for point defense",
                     level="3", layout=layout3)

session.add(building3)
session.commit()

building4 = Building(user_id=1, name="Archer Tower", category = "defense", description="Archer Towers have longer range than cannons, unlike cannons they can attack flying enemies",
                     level="3", layout=layout3)

session.add(building4)
session.commit()

building5 = Building(user_id=1, name="Bomb", category = "trap", description="Nothing says 'STAY OUT' quite like a good old-fashioned hidden bomb",
                     level="1", layout=layout3)

session.add(building5)
session.commit()

print 'added buildings'
