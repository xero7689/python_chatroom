__author__ = 'xero-mac'

'''Process_request version 1
    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self)

    def process_request_thread(self, request, client_address):
        """Handle one request thread
        """
        try:
            self.finish_request(request, client_address)
        except:
            #  maybe writing a shut down request method here.
            pass

    def process_request(self, request, client_address):
        """Init thread of request
        """
        t = threading.Thread(target=self.process_request_thread,
                             args=(request, client_address))
        t.daemon = self.daemon_threads
        t.start()

    def verify_request(self, request, client_address):
        return True
'''

'''For process_request thread
if self.verify_request(request, client_address):
    try:
        self.process_request(request, client_address)
    except:
        logging.debug("process_request error")
'''