# webserver

This project is an example of how to embed a simple HTTP webserver inside a Saleae High Level Analyzer (HLA) extension using Python's `http.server` and threading.
This project is based on the default HLA extension files.

## Features
- Serves HTTP requests on port 8080
- Responds to GET requests and can serve static files (e.g., `index.html`)
- Runs the webserver in a background thread so it does not block the analyzer
- Shuts down the webserver cleanly when the analyzer is destroyed

## Getting started

1. Build your extension by updating the Python files for your needs
2. Create a public Github repo and push your code
3. Update this README
4. Open the Logic app and publish your extension
5. Create a Github release
6. Debug your hardware like you've never done before :)
