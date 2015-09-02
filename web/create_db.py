from app import db

print("Creating Database!")

db.create_all()
def __init__(self,name,tag,available,x=1,y=1,z=1):
box = Box("Box21","Stock_Cartons", available=True,x=5,y=5,z=5)
db.session.add(box)
db.seession.commit()

print("All Done!")
