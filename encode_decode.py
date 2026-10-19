import bcrypt

password = "test"

hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print(hashed) #byte-Objekt

print(hashed.decode('utf-8')) # bytes zu String -> in DB speichern

print(bcrypt.checkpw(password.encode('utf-8'), hashed))


from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

password = "test"

# Passwort hashen
hashed = ph.hash(password)
print("argon2", hashed)

#Passwort prüfen

try:
    ok = ph.verify(hashed, password)
    print(ok) # True
except VerifyMismatchError:
    print(False)