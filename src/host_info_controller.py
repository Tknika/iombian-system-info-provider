#!/usr/bin/env python3

import logging
import threading
import time

logger = logging.getLogger(__name__)


class HostInfoController(object):

    def __init__(self, host_info, on_update_callback, polling_freq=5):
        self.host_info = host_info
        self.polling_freq = polling_freq
        self.polling_delay = 0
        self.polling_running = False
        self.polling_last_time = 0
        self.polling_thread = None
        self.callback = on_update_callback

    def start_polling(self, polling_delay=0):
        self.polling_delay = polling_delay
        self.polling_running = True
        self.polling_thread = threading.Thread(target=self.__polling)
        self.polling_thread.start()
        logger.debug("Polling job started")

    def stop_polling(self):
        self.polling_running = False
        if self.polling_thread:
            self.polling_thread.join()
        logger.debug("Polling job stopped")
    
    def __polling(self):
        time.sleep(self.polling_delay)
        while(self.polling_running):
            if (time.time() - self.polling_last_time > self.polling_freq):
                has_changed = self.host_info.update()
                if has_changed and self.callback:
                    logger.debug("Changes in the provider!")
                    self.callback(self.host_info.to_json())
                self.polling_last_time = time.time()
            time.sleep(0.5)