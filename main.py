import logging
from FirebaseComm import FirebaseCom, FirebaseError

logging.basicConfig(format='%(asctime)-15s [%(name)s-%(process)02d] %(levelname)-7s: %(message)s',
                    level=logging.DEBUG,
                    handlers=[
                        logging.StreamHandler()
                    ])



while True:

    try:

        FirebaseCom().getData()

    except FirebaseError:
        logging.fatal("no represented Firebase data")