from mongoengine import *

connect(
    db="web_database",
    host="mongodb+srv://web17_mod8:IDkrkN1JmruWcbSb@web17.k2uu2ec.mongodb.net/?retryWrites=true&w=majority"
)

class Task(Document):
    completed = BooleanField(default=False)
    fullname = StringField(max_length=150)
    email = StringField(max_length=150)