import os

class BaseConfig:
    TESTING = False
    SECRET_KEY = "secret"

class Config(BaseConfig): # BaseConfig is the parent class
    
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")

