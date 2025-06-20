# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse
from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting
import threading
from http.server import HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    '''
    A simple HTTP request handler that can be used to handle requests in a High Level Analyzer.
    This is not required, but can be useful for analyzers that need to handle HTTP requests.
    '''
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def log_message(self, format, *args):
        '''
        Override the log_message method to prevent logging to stderr.
        This is useful for High Level Analyzers to avoid crashing the extension
        '''
        pass

    def do_GET(self):
        '''
        Handle GET requests.
        '''
        # print("[HTTP] Received GET request for", self.path)
        # print(f"Received GET request for {self.path}")
        parsed_path = urlparse(self.path)
        query_params = dict(parse_qsl(parsed_path.query))

        # Set the response code and headers
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Respond with a simple message
        response_message = f"Hello from High Level Analyzer! You requested: {parsed_path.path}\n"
        response_message += f"Query parameters: {query_params}\n"
        self.wfile.write(response_message.encode('utf-8'))


# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):
    # List of settings that a user can set for this High Level Analyzer.
    my_string_setting = StringSetting()
    my_number_setting = NumberSetting(min_value=0, max_value=100)
    my_choices_setting = ChoicesSetting(choices=('A', 'B'))

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'mytype': {
            'format': 'Output type: {{type}}, Input type: {{data.input_type}}'
        }
    }

    def __init__(self):
        '''
        Initialize HLA.

        Settings can be accessed using the same name used above.
        '''

        print("Settings:", self.my_string_setting,
              self.my_number_setting, self.my_choices_setting)

        # Initialize the webserver in a background thread
        self.server_address = ('0.0.0.0', 8080)
        self.httpd = HTTPServer(self.server_address, RequestHandler)
        self.server_thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.server_thread.start()
        print(f"Webserver started on port {self.server_address}")
        # start the server without threading for debugging purposes
        # Uncomment the line below to run the server in the main thread for debugging purposes
        # Note: This will block the main thread, so it is not recommended for production use
        # self.httpd.serve_forever()

    def decode(self, frame: AnalyzerFrame):
        '''
        Process a frame from the input analyzer, and optionally return a single `AnalyzerFrame` or a list of `AnalyzerFrame`s.

        The type and data values in `frame` will depend on the input analyzer.
        '''

        # Return the data frame itself
        return AnalyzerFrame('mytype', frame.start_time, frame.end_time, {
            'input_type': frame.type
        })

    def shutdown_server(self):
        if hasattr(self, 'httpd'):
            self.server_thread.join()
            self.httpd.server_close()
            print("Webserver shutdown complete.")

    def __del__(self):
        print("HLA is being deleted, shutting down webserver.")
        self.shutdown_server()
