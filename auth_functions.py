import bcrypt

def hash_password(password):
    """
    Hashes a password for storing securely.
    
    Args:
        password (str): The plain-text password to hash.
        
    Returns:
        str: The hashed password, decoded to a string for database storage.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password, hashed_password):
    """
    Verifies a plain-text password against a hashed one from the database.
    
    Args:
        plain_password (str): The password entered by the user.
        hashed_password (str): The hashed password stored in the database.
        
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    # Ensure the hashed password from the DB is in bytes format
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
        
    # Check the plain-text password against the hashed version
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

