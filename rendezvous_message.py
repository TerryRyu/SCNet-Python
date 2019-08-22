from utils import make_enum

RendezvousMessage = make_enum('RendezvousMessage', 10000,

    # Enum start
    'REGISTRATION_RENDEZVOUS_CLIENT_REQUEST', # (Serial),
                                              # SP private ip, 
                                              # SP private port 

    'REGISTRATION_RENDEZVOUS_CLIENT_SUCCESS', # (Serial), 
                                              # SP public ip, 
                                              # SP public port

    'REGISTRATION_RELAY_SERVER_REQUEST', # None
    'REGISTRATION_RELAY_SERVER_SUCCESS', # None
    'PING_REQUEST', # None
    'PING_RESPONSE', # None
    'CONNECTION_REQUEST', # TP public ip, 
                          # TP public port

    'CONNECTION_ID_CREATED', # TP public ip, 
                             # TP public port (RanS to SP)

    'CONNECTION_ID_RECEIVED', # TP public ip (SP to RanS)
    'CONNECTION_TARGET_INVALID', # TP public ip, 
                                 # TP public port

    'CONNECTION_FAILED', # None

    # relay
    'RELAY_SERVICE_REQUEST', # SP pubilc ip, 
                             # TP pubilc ip

    'RELAY_SESSION_READY', # None
    'RELAY_SERVER_INFORMATION', # RelS-ip, 
                                # RelS-port, 
                                # 1(SP) or 0(TP)

    'REGISTRATION_RELAY_PEER_REQUEST', # 1(SP) or 0(TP) or None for ping
    'REGISTRATION_RELAY_PEER_SUCCESS', # None
    'REGISTRATION_RELAY_PEER_FAILED', # None
    'RELAY_SESSION_CREATED', # None
    'RELAY_SESSION_CREATING_FAILED', # None
    'RELAY_SESSION_INVALID', # None
    'CONNECTION_RELAY_SERVICE_SUCCESS', # RelS-ip, 
                                        # RelS-port

    'CONNECTION_RELAY_SERVICE_FAILED', # None

    # pub/pub or pri/pub
    'DIRECT_CONNECTION_AVAILABLE', # TP public ip, 
                                   # TP public port

    'DIRECT_CONNECTION_REQUEST', # None
    'DIRECT_CONNECTION_RESPONSE', # None

    # pub/pri
    'REVERSE_CONNECTION_READY', # None
    'REVERSE_CONNECTION', # SP public ip, 
                          # SP public port

    'REVERSE_CONNECTION_REQUEST', # None
    'REVERSE_CONNECTION_RESPONSE', # None

    # pri/pri
    'UDP_HOLE_PUNCHING_AVAILABLE', # SP's public ip, 
                                   # public port, 
                                   # private ip,
                                   # private port to TP (The opposite is also the case.)

    'UDP_HOLE_PUNCHING_REQUEST', # isPublic (1=true, 0=false)
    'UDP_HOLE_PUNCHING_RESPONSE', # isPublic (1=true, 0=false)
    'RENDEZVOUS_MSG_END'
    )