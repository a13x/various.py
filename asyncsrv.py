import os.path
import asyncore
import socket
import getopt
import ConfigParser
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

class GpsIncoming(object):
    pass

class Handler(asyncore.dispatcher_with_send):
    def __init__(self, session):
        super(ClassName, self).__init__()
        self.session = session
        
    def handle_read(self):
        data = self.recv(8192)
        data = data.split(',')
        self.save(data)
        self.close()
    
    def make_from(self, data):
        return GpsIncoming(data)
        
    def save(self, data):
        gps_incoming = self.make_from(data)
        self.session.add(gps_incoming)
        self.session.commit()

class SimpleServer(asyncore.dispatcher):

    def __init__(self, host, port, session):
        self.session = session
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = Handler(sock, self.session)

def make_engine(config):
    host = config.get('mysql', 'host')
    print host
    db = config.get('mysql', 'db')
    user = config.get('mysql', 'user')
    pwd = config.get('mysql', 'password')
    return create_engine("mysql://{0}:{1}@{2}/{3}".format(user, pwd, host, db))

def load_session(engine):
    metadata = MetaData(engine)
    gps_incoming = Table('gps_incoming', metadata, autoload=True)
    mapper(GpsIncoming, gps_incoming)
    Session = sessionmaker(bind=engine)
    return Session()

def main():
    config_file = os.path.join(os.path.dirname(__file__), 'asyncsrv.conf')    
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    engine = make_engine(config)
    session = load_session(engine)
    server = SimpleServer('localhost', config.get('main', 'port'), session)
    asyncore.loop()

if __name__ == '__main__':
    main()