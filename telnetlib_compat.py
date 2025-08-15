"""
Compatibility module for telnetlib across Python versions.
Provides telnetlib for Python < 3.13 or a compatible wrapper for Python 3.13+
"""

import sys

if sys.version_info >= (3, 13):
    # Python 3.13+ - use the telnetlib from pypi
    import socket
    import selectors
    import time
    
    class Telnet:
        """Basic telnet client compatible with the old telnetlib API"""
        
        def __init__(self, host=None, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
            self.host = host
            self.port = port
            self.timeout = timeout
            self.sock = None
            self.rawq = b''
            self.irawq = 0
            self.cookedq = b''
            self.eof = 0
            self.iacseq = b''
            self.sb = 0
            self.sbdataq = b''
            
            if host is not None:
                self.open(host, port, timeout)
        
        def open(self, host, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
            """Connect to a host."""
            self.eof = 0
            self.host = host
            self.port = port
            self.timeout = timeout
            self.sock = socket.create_connection((host, port), timeout)
            
        def close(self):
            """Close the connection."""
            if self.sock:
                self.sock.close()
            self.sock = None
            self.eof = 1
            
        def get_socket(self):
            """Return the socket object used internally."""
            return self.sock
            
        def fileno(self):
            """Return the fileno() of the socket object used internally."""
            return self.sock.fileno()
            
        def write(self, buffer):
            """Write a string to the socket."""
            if isinstance(buffer, str):
                buffer = buffer.encode('ascii')
            self.sock.sendall(buffer)
            
        def read_until(self, match, timeout=None):
            """Read until a given string is encountered or until timeout."""
            if isinstance(match, str):
                match = match.encode('ascii')
            n = len(match)
            self.process_rawq()
            i = self.cookedq.find(match)
            if i >= 0:
                i = i + n
                buf = self.cookedq[:i]
                self.cookedq = self.cookedq[i:]
                return buf
            if timeout is not None:
                deadline = time.time() + timeout
            while not self.eof:
                if timeout is not None:
                    timeout = deadline - time.time()
                    if timeout < 0:
                        break
                self.fill_rawq()
                self.process_rawq()
                i = self.cookedq.find(match)
                if i >= 0:
                    i = i + n
                    buf = self.cookedq[:i]
                    self.cookedq = self.cookedq[i:]
                    return buf
            return self.cookedq
            
        def read_very_eager(self):
            """Read everything that's possible without blocking."""
            self.process_rawq()
            while not self.eof and self.sock_avail():
                self.fill_rawq()
                self.process_rawq()
            return self.read_very_lazy()
            
        def read_eager(self):
            """Read readily available data."""
            self.process_rawq()
            while not self.eof and self.sock_avail():
                self.fill_rawq()
                self.process_rawq()
            return self.read_very_lazy()
            
        def read_lazy(self):
            """Process and return data that's already in the queues."""
            self.process_rawq()
            return self.read_very_lazy()
            
        def read_very_lazy(self):
            """Return any data available in the cooked queue."""
            buf = self.cookedq
            self.cookedq = b''
            if not buf and self.eof:
                raise EOFError('telnet connection closed')
            return buf
            
        def read_some(self):
            """Read at least one byte of cooked data unless EOF is hit."""
            self.process_rawq()
            while not self.cookedq and not self.eof:
                self.fill_rawq()
                self.process_rawq()
            buf = self.cookedq
            self.cookedq = b''
            if not buf and self.eof:
                raise EOFError('telnet connection closed')
            return buf
            
        def sock_avail(self):
            """Test whether data is available on the socket."""
            with selectors.DefaultSelector() as selector:
                selector.register(self.sock, selectors.EVENT_READ)
                return bool(selector.select(0))
                
        def fill_rawq(self):
            """Fill raw queue from exactly one recv() system call."""
            if self.eof:
                return
            try:
                buf = self.sock.recv(50)
            except:
                buf = b''
            self.eof = not buf
            self.rawq = self.rawq + buf
            
        def process_rawq(self):
            """Transfer from raw queue to cooked queue."""
            buf = self.rawq
            self.rawq = b''
            # Simplified processing - just pass through for basic MUD usage
            # A full implementation would handle telnet IAC sequences
            self.cookedq = self.cookedq + buf
            
else:
    # Python < 3.13 - use the built-in telnetlib
    from telnetlib import Telnet