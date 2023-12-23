import pygame
import sys
import socket
import threading
import ast
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

logging.info("\tThis is an info message")
logging.warning("This is a warning message")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('127.0.0.1', 5555))
    logging.info("Successfully connected to the server")
except socket.error as e:
    logging.error(f"Could not connect to the server: {e}")