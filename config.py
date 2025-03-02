# backend/config.py
import os

class Config:
    # Replace with your MongoDB Atlas connection string
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://yashpetkar07:Petkaryash07@cluster0.zuowc.mongodb.net/GymManager?retryWrites=true&w=majority')
    DEBUG = True
