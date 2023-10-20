# P2P Secure File Sharing System

```plaintext
BEGIN P2P Secure File Sharing System

FUNCTION setup:
    INITIALIZE Flask app, database, and necessary libraries

FUNCTION register_user(username, password):
    IF username DOES NOT exist in database:
        hashed_password = HASH(password)
        (public_key, private_key) = GENERATE_DIFFIE_HELLMAN_KEYS()
        STORE username, hashed_password, public_key in database
        RETURN success
    ELSE:
        RETURN error

FUNCTION login_user(username, password):
    hashed_password = RETRIEVE_HASHED_PASSWORD(username)
    IF hashed_password == HASH(password):
        CREATE user session
        RETURN success
    ELSE:
        RETURN error

FUNCTION initiate_key_exchange(target_peer):
    my_public_key = RETRIEVE_MY_PUBLIC_KEY()
    target_public_key = SEND_PUBLIC_KEY_TO_PEER(target_peer, my_public_key)
    shared_secret = COMPUTE_SHARED_SECRET(target_public_key)
    STORE shared_secret for communication with target_peer

FUNCTION receive_key_exchange(requesting_peer, received_public_key):
    my_public_key = RETRIEVE_MY_PUBLIC_KEY()
    shared_secret = COMPUTE_SHARED_SECRET(received_public_key)
    STORE shared_secret for communication with requesting_peer
    RETURN my_public_key

FUNCTION upload_file(file, filename, target_peer):
    shared_secret = RETRIEVE_SHARED_SECRET(target_peer)
    encrypted_file = ENCRYPT(file, shared_secret)
    STORE encrypted_file in database with metadata
    RETURN success

FUNCTION download_file(file_id):
    file, filename = RETRIEVE_FILE_FROM_DATABASE(file_id)
    shared_secret = RETRIEVE_SHARED_SECRET(owner_of_file)
    decrypted_file = DECRYPT(file, shared_secret)
    RETURN decrypted_file

FUNCTION update_file(file_id, new_file):
    shared_secret = RETRIEVE_SHARED_SECRET(owner_of_file)
    encrypted_file = ENCRYPT(new_file, shared_secret)
    UPDATE file in database with new encrypted_file and increment version
    RETURN success

FUNCTION delete_file(file_id):
    DELETE file from database
    RETURN success

FUNCTION malicious_activity_detector(request):
    IF request pattern IS suspicious:
        LOG suspicious activity
        BLOCK request or NOTIFY admin
    ELSE:
        PASS request to designated function

INITIALIZE routes in Flask app linking to functions
RUN Flask app

END P2P Secure File Sharing System
