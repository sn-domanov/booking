from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def get_password_hash(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hash: str) -> bool:
    return password_hash.verify(plain, hash)
