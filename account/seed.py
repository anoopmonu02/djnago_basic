from faker import Faker

fake = Faker()

def seed_db(n=10) -> None:
    for i in range(0,n):
        