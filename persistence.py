import os
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, WriteError

try:
    mongo_ip = os.environ['DB_IP']
except KeyError:
    mongo_ip = 'localhost'

try:
    mongo_port = os.environ['DB_PORT']
except KeyError:
    mongo_port = '27017'

try:
    mongo_name = os.environ['DB_NAME']
except KeyError:
    mongo_name = 'omni_database'

# DEFAULT_PREFIX that will signify a discord message as a command
DEFAULT_PREFIX = '!'

# Number of milliseconds before a database request times out
TIMEOUT_MS = 2000

# Whether or not there is a connection to the database. Used to skip waiting for
# a timeout when it is known there is no connection
connected = False

# Attempt to establish a connection with the database, and simply log any errors
# if they occur. The bot should still be able to run if no connection can be
# established.
if mongo_ip and mongo_port:
    try:
        client = pymongo.MongoClient("mongodb://{}:{}/".format(mongo_ip, mongo_port), connect=True,
                                     serverSelectionTimeoutMS=TIMEOUT_MS)

        omni_db = client[mongo_name]
        guild_col = omni_db["guilds"]

        client.admin.command('ismaster') #test connection
        connected = True
    except (ConnectionFailure, ServerSelectionTimeoutError) as err:
        print("Error connecting to the mongoDB database:\n{}".format(err))
else:
    print('No valid MongoDB ip and/or port given in the DB_IP and DB_PORT environment variables')


def set_prefix(guild, prefix):
    """
    Save a prefix for a specific guild
    Returns True if the prefix was successfully saved, False otherwise
    """
    if not connected:
        return False
    try:
        if guild_col.count_documents({"_id": guild.id}):
            update = {"$set": {"prefix": prefix}}
            guild_col.update_one({"_id": guild.id}, update)
        else:
            guild_col.insert_one({"_id": guild.id, "prefix": prefix})
    except WriteError as e:
        print(e)
        return False

    return True


def get_prefix(guild):
    """
    Returns the prefix for a specific guild
    """
    if not connected:
        return DEFAULT_PREFIX
    try:
        result = guild_col.find_one({"_id": guild.id})
    except ServerSelectionTimeoutError as e:
        print("Error retrieving prefix for guild with id {}:\n{}".format(guild.id, e))
        return DEFAULT_PREFIX

    if not result:
        return DEFAULT_PREFIX
    else:
        return result["prefix"]
