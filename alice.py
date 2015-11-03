from AESCipher import AESCipher, BS
import socket
import sys
import pickle
import os

MESSAGE_COUNT = 10
PUBLIC_KEY_FILE = 'bob-python.pub'
OUTPUT_FILE = 'msgs.txt'

class Alice():

  def __init__(self):
    self.session_key = self.generate_random_key()
    pass

  @staticmethod
  def generate_random_key():
    return os.urandom(BS)

  def encrypt_session_key(self, public_key):
    self.encrypted_session_key = AESCipher(public_key).encrypt(self.session_key) 

  def send_session_key(self):
    pass

  def receive_message(self):
    pass

  def get_public_key(self):
    pass

  def connect(self):
    # get public key from file
    public_key = self.get_public_key()

    # encrypt session key
    self.encrypt_session_key(public_key);
    self.send_message(self.encrypted_session_key)

    for i in xrange(MESSAGE_COUNT):
      message = self.receive_message()
      print message




if __name__ == '__main__':
  alice = Alice()
  alice.connect()