import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, WriteError

# DEFAULT_PREFIX that will signify a discord message as a command
DEFAULT_PREFIX = '!'

# Whether the initial connection was successfully established
connected = True

# Attempt to establish a connection with the database, and simply log any errors
# if they occur. The bot should still be able to run if no connection can be
# established.
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/", connect=True,
    serverSelectionTimeoutMS=10)
    omni_db = client["omni_database"]
    guild_col = omni_db["guilds"]
    connected = True
except (ConnectionFailure, ServerSelectionTimeoutError) as err:
    print(err)


"""
Save a prefix for a specific guild
Returns True if the prefix was successfully saved, False otherwise
"""
def set_prefix(guild, prefix):

    try:
        if guild_col.count_documents({"_id": guild.id}):
            update = {"$set" : {"prefix": prefix}}
            guild_col.update_one({"_id": guild.id}, update)
        else:
            guild_col.insert_one({"_id": guild.id, "prefix": prefix})
    except WriteError as err:
        print(err)
        return False

    return True


"""
Returns the prefix for a specific guild
"""
def get_prefix(guild):
    try:
        result = guild_col.find_one({"_id":guild.id})
    except ServerSelectionTimeoutError as err:
        print(err)
        return DEFAULT_PREFIX

    if not result:
        return DEFAULT_PREFIX
    else:
        return result["prefix"]



