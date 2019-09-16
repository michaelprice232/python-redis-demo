"""
Application to demonstrate working with Redis as a key value store
"""

import redis
import random
import sys

redis_server_name = 'redis'
redis_port = 6379
redis_database_number = 0

number_of_users = 5


def connect_to_redis_server(server_name, port, database_number):
    """Connect to a Redis server"""
    # Exit script if unable to connect to Redis instance
    # Connections are only actually made when actual commands are issued, so we use the PING command to test
    try:
        redis_connection = redis.Redis(host=server_name, port=port, db=database_number)
        redis_connection.ping()
    except Exception as e:
        sys.exit("Error: Unable to connect to Redis instance! Exiting")

    # Connected successfully
    print("Connected to Redis server. Server: {}, Port: {}, Database Number: {}\n"
          .format(server_name, port, database_number))

    return redis_connection


def user_play_game(user, redis_connection):
    """User playing a game, resulting in a score which is written to Redis"""

    # Check to see if this is an new user
    new_user = check_if_user_is_new(user, redis_connection)

    # Generate a random number to simulate the user's score in the game, as we don't currently have interactive users
    users_score = random.randint(1, 101)

    # Set the value for the user in Redis
    update_key = redis_connection.set(user, users_score)

    # Check that Redis has been successfully updated. Exit program if we are unable to write result to Redis
    if not update_key:
        sys.exit("Error: Unable to update Redis! Exiting")

    # Print result to console based on whether the user is new or not
    if new_user:
        print("You are a new user, welcome {}, a score of {} has been recorded".format(user, users_score))
    else:
        print("Welcome back {}, a score of {} has been recorded".format(user, users_score))


def check_if_user_is_new(user, redis_connection):
    """Check if the user is a new user by checking whether they have a previously recorded score in Redis"""
    result = redis_connection.exists(user)

    # Redis query result is 1 if a key exists for the user (0 if it doesn't exist)
    if result == 1:
        return False        # User is not new (existing user)
    elif result == 0:
        return True         # User is new


# Execute if running the script directly
if __name__ == '__main__':
    # Connect to Redis server
    r = connect_to_redis_server(redis_server_name, redis_port, redis_database_number)

    # Simulate a number users playing a game and generating a score, which is stored in Redis
    for user_number in range(0, number_of_users):

        # Generate the username based on the iteration number
        username = "user" + str(user_number)

        # Simulate playing the game for the user. Write score to Redis
        user_play_game(username, r)

    # Get (retrieve) a key:value pair in Redis. Decode the byte return object to a string
    print("\nRetrieving all player results from Redis...")
    for user_number in range(0, number_of_users):
        username = "user" + str(user_number)
        print(username, r.get(username).decode("utf-8"))

    # Close the connection to Redis
    r.close()
    print("\nClosed connection: ", r)
