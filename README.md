# Sandbag
## What is this
Sandbag is a lightweight test server built with Flask, a Python web framework. It offers a simple and convenient way to set up a local server for various purposes.

## Features
- Easy Setup: Sandbag can be quickly deployed with just a few commands, making it a breeze to get a test server up and running.
- Communication Testing: Use Sandbag to verify communication between different components of your application or test APIs and network connections.
- Browser Developer Tools: Sandbag provides a playground for exploring and experimenting with browser developer tools, such as inspecting network traffic, debugging JavaScript, and more.

## Getting Started
1. Clone the repository:
```
https://github.com/riiim400th/sandbag.git
```

```
cd sandbag
```

2. Install the required dependencies:
```
python3 -m pip install -r requirements.txt
```

3.Start the server:
```
python3 ./app.py
```
The server will start running at `http://localhost:5000` by default.

## Usage
Once the server is running, you can access it through your web browser or make requests using tools like cURL or Postman. Sandbag provides a simple web interface where you can interact with the server and explore its functionality.
For communication testing, you can send requests to different endpoints and observe the responses. This can be useful for verifying the behavior of your application or testing third-party APIs.
To experience browser developer tools, open the web interface in your preferred browser and right-click to access the developer tools. From there, you can inspect network traffic, debug JavaScript, and explore various other features provided by modern web browsers.

## Contributing
Contributions to Sandbag are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the project's GitHub repository.

## License
Sandbag is released under the MIT License.
