#!/usr/bin/python3
""" Check response
"""

if __name__ == "__main__":
    try:
        from api.v1.auth.session_exp_auth import SessionExpAuth
        sea = SessionExpAuth()
        user_id = "User1"
        session_id = sea.create_session(user_id)
        if session_id is None:
            print("create_session should return a Session ID if user_id is valid")
            exit(1)
        session_info = sea.user_id_by_session_id.get(session_id)
        if session_info is None:
            print("create_session should create a dictionary linked to the session ID")
            exit(1)
        if session_info.get('created_at') is None:
            print("create_session should create a dictionary linked to the session ID with created_at")
            exit(1)

        # delete created_at
        del session_info['created_at']
        sea.user_id_by_session_id[session_id] = session_info

        user_id_r = sea.user_id_for_session_id(session_id)
        print(user_id_r)
        if user_id_r is not None:
            print("user_id_for_session_id should return None if the created_at is None")
            exit(1)
        
        print("OK", end="")
    except:
        import sys
        print("Error: {}".format(sys.exc_info()))