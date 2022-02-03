import logging
import time
from FirebaseComm import FirebaseCom, FirebaseError

logging.basicConfig(format='%(asctime)-15s [%(name)s-%(process)02d] %(levelname)-7s: %(message)s',
                    level=logging.DEBUG,
                    handlers=[
                        logging.StreamHandler()
                    ])



while True:

    try:

        FirebaseCom().getData()
        #time.sleep(1)
    except FirebaseError:
        logging.fatal("no represented Firebase data")