#!/usr/bin/env python3

import logging
import signal

from iombian_info_provider import IoMBianInfoProvider
from host_info_controller import HostInfoController
from pub_client import PubClient

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)-20s  - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

PUBLISHER_HOST = "127.0.0.1"
PUBLISHER_PORT = 5557
POLLING_FREQ = 5
POLLING_DELAY = 2


def signal_handler(sig, frame):
    logger.debug("Stoping IoMBian Info Provider Service")
    publisher_client.stop()
    info_controller.stop_polling()
    logger.info("IoMBian Info Provider Service stopped")


def on_update(info):
    logger.debug(f"Host info updated: {info}")
    publisher_client.send(info)


if __name__ == "__main__":
    logger.info("Starting IoMBian Info Provider Service")

    publisher_client = PubClient(host=PUBLISHER_HOST, port=PUBLISHER_PORT)
    publisher_client.start()

    iombian_info = IoMBianInfoProvider()
    info_controller = HostInfoController(iombian_info, on_update_callback=on_update, polling_freq=POLLING_FREQ)
    info_controller.start_polling(polling_delay=POLLING_DELAY)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()