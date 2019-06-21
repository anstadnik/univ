"""This is the program for measuring some code metrics"""
from system import System

def main():
    """This is the main function"""
    system = System()
    system.create_default()
    system.run()

if __name__ == "__main__":
    main()
