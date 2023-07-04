from WmVoice.models import User
from hashlib import sha256


FIRST_NAMES = ('John', 'Andy', 'Joe')
LAST_NAMES = ('Johnson', 'Smith', 'Williams')


def addUser(fname, lname):
    try:
        name = f"{fname} {lname}"
        email = f"{fname}.{lname}@example.com"
        password = sha256(email.encode('utf-8')).hexdigest()
        user = User.objects.create(
            email=email,
            name=name,
            password=password,
        )
        print(f"Added user : {user.name}")
    except Exception as e:
        print(f"Failed to create user. Exception trace : {e}")


def populateUsers():
    for fname in FIRST_NAMES:
        for lname in LAST_NAMES:
            addUser(fname, lname)
