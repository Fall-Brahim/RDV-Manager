from passlib.context import CryptContext

mdp_Haser = CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_Password(plain_password:str,hashed_password:str) -> bool:
    return mdp_Haser(plain_password,hashed_password)
