import time
def test():
    try:
        while True:
            time.sleep(1)
    finally:
        print('clean')

try:
    test()
except KeyboardInterrupt:
    print("catch keyboard event")
    
