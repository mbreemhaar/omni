import os

import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, WriteError

mongo_ip = os.environ['DB_IP']
mongo_port = os.environ['DB_PORT']

# DEFAULT_PREFIX that will signify a discord message as a command
DEFAULT_PREFIX = '!'

# Whether the initial connection was successfully established
connected = True

# Attempt to establish a connection with the database, and simply log any errors
# if they occur. The bot should still be able to run if no connection can be
# established.
if mongo_ip and mongo_port:
    try:
        client = pymongo.MongoClient("mongodb://{}:{}/".format(mongo_ip, mongo_port), connect=True,
        serverSelectionTimeoutMS=10)
        omni_db = client["omni_database"]

        global guild_col
        guild_col = omni_db["guilds"]

        global connected
        connected = True
    except (ConnectionFailure, ServerSelectionTimeoutError) as err:
        print(err)
else:
    print('No valid MongoDB ip and/or port given in the DB_IP and DB_PORT environment variables')


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
