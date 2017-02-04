################################################################################
#  THIS FILE IS 100% GENERATED BY ZPROJECT; DO NOT EDIT EXCEPT EXPERIMENTALLY  #
#  Read the zproject/README.md for information about making permanent changes. #
################################################################################

from __future__ import print_function
import os
import re
import sys

from cffi import FFI

ffi = FFI()

try:
    # If LD_LIBRARY_PATH or your OSs equivalent is set, this is the only way to
    # load the library.  If we use find_library below, we get the wrong result.
    if os.name == 'posix':
        if sys.platform == 'darwin':
            libpath = 'libzyre.2.dylib'
        else:
            libpath = 'libzyre.so.2'
    elif os.name == 'nt':
        libpath = 'libzyre.dll'
    lib = ffi.dlopen(libpath)
except OSError:
    libpath = find_library("zyre")
    if not libpath:
        raise ImportError("Unable to find libzyre")
    lib = ffi.dlopen(libpath)

# Custom setup for zyre


cdefs = '''
typedef struct _zyre_t zyre_t;
typedef struct _zyre_event_t zyre_event_t;
// CLASS: zyre
// Constructor, creates a new Zyre node. Note that until you start the
// node it is silent and invisible to other nodes on the network.     
// The node name is provided to other nodes during discovery. If you  
// specify NULL, Zyre generates a randomized node name from the UUID. 
zyre_t *
    zyre_new (const char *name);

// Destructor, destroys a Zyre node. When you destroy a node, any
// messages it is sending or receiving will be discarded.        
void
    zyre_destroy (zyre_t **self_p);

// Return our node UUID string, after successful initialization
const char *
    zyre_uuid (zyre_t *self);

// Return our node name, after successful initialization
const char *
    zyre_name (zyre_t *self);

// Set node header; these are provided to other nodes during discovery
// and come in each ENTER message.                                    
void
    zyre_set_header (zyre_t *self, const char *name, ......);

// Set verbose mode; this tells the node to log all traffic as well as
// all major events.                                                  
void
    zyre_set_verbose (zyre_t *self);

// Set UDP beacon discovery port; defaults to 5670, this call overrides
// that so you can create independent clusters on the same network, for
// e.g. development vs. production. Has no effect after zyre_start().  
void
    zyre_set_port (zyre_t *self, int port_nbr);

// Set the peer evasiveness timeout, in milliseconds. Default is 5000.
// This can be tuned in order to deal with expected network conditions
// and the response time expected by the application. This is tied to 
// the beacon interval and rate of messages received.                 
void
    zyre_set_evasive_timeout (zyre_t *self, int interval);

// Set the peer expiration timeout, in milliseconds. Default is 30000.
// This can be tuned in order to deal with expected network conditions
// and the response time expected by the application. This is tied to 
// the beacon interval and rate of messages received.                 
void
    zyre_set_expired_timeout (zyre_t *self, int interval);

// Set UDP beacon discovery interval, in milliseconds. Default is instant
// beacon exploration followed by pinging every 1,000 msecs.             
void
    zyre_set_interval (zyre_t *self, size_t interval);

// Set network interface for UDP beacons. If you do not set this, CZMQ will
// choose an interface for you. On boxes with several interfaces you should
// specify which one you want to use, or strange things can happen.        
void
    zyre_set_interface (zyre_t *self, const char *value);

// By default, Zyre binds to an ephemeral TCP port and broadcasts the local 
// host name using UDP beaconing. When you call this method, Zyre will use  
// gossip discovery instead of UDP beaconing. You MUST set-up the gossip    
// service separately using zyre_gossip_bind() and _connect(). Note that the
// endpoint MUST be valid for both bind and connect operations. You can use 
// inproc://, ipc://, or tcp:// transports (for tcp://, use an IP address   
// that is meaningful to remote as well as local nodes). Returns 0 if       
// the bind was successful, else -1.                                        
int
    zyre_set_endpoint (zyre_t *self, ......);

// Set-up gossip discovery of other nodes. At least one node in the cluster
// must bind to a well-known gossip endpoint, so other nodes can connect to
// it. Note that gossip endpoints are completely distinct from Zyre node   
// endpoints, and should not overlap (they can use the same transport).    
void
    zyre_gossip_bind (zyre_t *self, ......);

// Set-up gossip discovery of other nodes. A node may connect to multiple
// other nodes, for redundancy paths. For details of the gossip network  
// design, see the CZMQ zgossip class.                                   
void
    zyre_gossip_connect (zyre_t *self, ......);

// Start node, after setting header values. When you start a node it
// begins discovery and connection. Returns 0 if OK, -1 if it wasn't
// possible to start the node.                                      
int
    zyre_start (zyre_t *self);

// Stop node; this signals to other peers that this node will go away.
// This is polite; however you can also just destroy the node without 
// stopping it.                                                       
void
    zyre_stop (zyre_t *self);

// Join a named group; after joining a group you can send messages to
// the group and all Zyre nodes in that group will receive them.     
int
    zyre_join (zyre_t *self, const char *group);

// Leave a group
int
    zyre_leave (zyre_t *self, const char *group);

// Receive next message from network; the message may be a control
// message (ENTER, EXIT, JOIN, LEAVE) or data (WHISPER, SHOUT).   
// Returns zmsg_t object, or NULL if interrupted                  
zmsg_t *
    zyre_recv (zyre_t *self);

// Send message to single peer, specified as a UUID string
// Destroys message after sending                         
int
    zyre_whisper (zyre_t *self, const char *peer, zmsg_t **msg_p);

// Send message to a named group 
// Destroys message after sending
int
    zyre_shout (zyre_t *self, const char *group, zmsg_t **msg_p);

// Send formatted string to a single peer specified as UUID string
int
    zyre_whispers (zyre_t *self, const char *peer, ......);

// Send formatted string to a named group
int
    zyre_shouts (zyre_t *self, const char *group, ......);

// Return zlist of current peer ids.
zlist_t *
    zyre_peers (zyre_t *self);

// Return zlist of current peers of this group.
zlist_t *
    zyre_peers_by_group (zyre_t *self, const char *name);

// Return zlist of currently joined groups.
zlist_t *
    zyre_own_groups (zyre_t *self);

// Return zlist of groups known through connected peers.
zlist_t *
    zyre_peer_groups (zyre_t *self);

// Return the endpoint of a connected peer.
char *
    zyre_peer_address (zyre_t *self, const char *peer);

// Return the value of a header of a conected peer.
// Returns null if peer or key doesn't exits.      
char *
    zyre_peer_header_value (zyre_t *self, const char *peer, const char *name);

// Return socket for talking to the Zyre node, for polling
zsock_t *
    zyre_socket (zyre_t *self);

// Print zyre node information to stdout
void
    zyre_print (zyre_t *self);

// Return the Zyre version for run-time API detection; returns
// major * 10000 + minor * 100 + patch, as a single integer.  
uint64_t
    zyre_version (void);

// Self test of this class.
void
    zyre_test (bool verbose);

// CLASS: zyre event
// Constructor: receive an event from the zyre node, wraps zyre_recv.
// The event may be a control message (ENTER, EXIT, JOIN, LEAVE) or  
// data (WHISPER, SHOUT).                                            
zyre_event_t *
    zyre_event_new (zyre_t *node);

// Destructor; destroys an event instance
void
    zyre_event_destroy (zyre_event_t **self_p);

// Returns event type, as printable uppercase string. Choices are:   
// "ENTER", "EXIT", "JOIN", "LEAVE", "EVASIVE", "WHISPER" and "SHOUT"
// and for the local node: "STOP"                                    
const char *
    zyre_event_type (zyre_event_t *self);

// Return the sending peer's uuid as a string
const char *
    zyre_event_peer_uuid (zyre_event_t *self);

// Return the sending peer's public name as a string
const char *
    zyre_event_peer_name (zyre_event_t *self);

// Return the sending peer's ipaddress as a string
const char *
    zyre_event_peer_addr (zyre_event_t *self);

// Returns the event headers, or NULL if there are none
zhash_t *
    zyre_event_headers (zyre_event_t *self);

// Returns value of a header from the message headers   
// obtained by ENTER. Return NULL if no value was found.
const char *
    zyre_event_header (zyre_event_t *self, const char *name);

// Returns the group name that a SHOUT event was sent to
const char *
    zyre_event_group (zyre_event_t *self);

// Returns the incoming message payload; the caller can modify the
// message but does not own it and should not destroy it.         
zmsg_t *
    zyre_event_msg (zyre_event_t *self);

// Returns the incoming message payload, and pass ownership to the   
// caller. The caller must destroy the message when finished with it.
// After called on the given event, further calls will return NULL.  
zmsg_t *
    zyre_event_get_msg (zyre_event_t *self);

// Print event to zsys log
void
    zyre_event_print (zyre_event_t *self);

// Self test of this class.
void
    zyre_event_test (bool verbose);

'''
cdefs = re.sub(r';[^;]*\bva_list\b[^;]*;', ';', cdefs, flags=re.S) # we don't support anything with a va_list arg

ffi.set_source("zyre.zyre_cffi", None)
ffi.cdef(cdefs)

ffiwrapper = FFI()
ffiwrapper.cdef('''
void
   zyre_destroy_py (void *self);

void
   zyre_event_destroy_py (void *self);

''')

ffiwrapper.set_source("zyre.zyre_py_destructors",
                      libraries=['zyre'], source='''
#include <zyre.h>
void
zyre_destroy_py (void *self)
{
   zyre_destroy ((zyre_t **) &self);
}

void
zyre_event_destroy_py (void *self)
{
   zyre_event_destroy ((zyre_event_t **) &self);
}

''')

if __name__ == "__main__":
    ffi.compile()
    ffiwrapper.compile()
