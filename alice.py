from AESCipher import AESCipher, BS
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket
import sys
import pickle
import os

PUBLIC_KEY_FILE = 'bob-python.pub'
OUTPUT_FILE = 'msgs.txt'
BUFFER_SIZE = 1024

class Alice():

  def __init__(self, host, port):
    self.session_key = self.generate_random_key()
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((host, port))
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.aes = AESCipher(self.session_key)

  @staticmethod
  def generate_random_key():
    return os.urandom(BS)

  def encrypt_session_key(self, public_key):
    self.encrypted_session_key = public_key.encrypt(self.session_key)

  def send_message(self, message):
    lol = pickle.dumps(message)
    self.socket.send(lol)
    pass

  def receive_message(self):
    return self.socket.recv(BUFFER_SIZE)

  def get_public_key(self):
    with open(PUBLIC_KEY_FILE, "r") as f:
      public_key = RSA.importKey(f.read())
    return PKCS1_OAEP.new(public_key)

  def receive_all_message(self):
    messages = ''

    while(True):
      message = self.receive_message()
      if (len(message) == 0):
        break
      messages += message

    return messages

  def decode_message(self, messages):
    message_list = messages.split(".")

    full_message = ''

    for message in message_list:
      if (len(message) == 0):
        break
      real_message = pickle.loads(message+'.')
      full_message += self.aes.decrypt(real_message)

    return full_message

  def write_to_file(self, message):

    with open(OUTPUT_FILE, 'w') as f:
      f.seek(0)
      f.truncate()
      f.write(message)

  def connect(self):
    # get public key from file
    public_key = self.get_public_key()

    # encrypt session key
    self.encrypt_session_key(public_key)

    # send encrypted session key
    self.send_message(self.encrypted_session_key)

    # receive all message
    messages = self.receive_all_message()

    # get plaintext message
    messages = self.decode_message(messages)

    # write to file
    self.write_to_file(messages)

    # close socket
    self.socket.close()



if __name__ == '__main__':
  HOST = sys.argv[1]
  PORT = int(sys.argv[2])
  alice = Alice(HOST, PORT)
  alice.connect()