# Chat Application Protocol

A robust chat application implemented using Python and socket programming. This application features a custom-built protocol designed and implemented by me. Users can connect to the server, authenticate using hardcoded credentials, and send/receive messages in real-time.

## Features
* __Custom Protocol:__ The application uses a proprietary protocol developed from scratch, ensuring a unique and tailored chat experience.
* __Real-time Chat:__ Once authenticated, users can send and receive messages in real-time.
* __Stateful Design:__ The application maintains states according to the DFA, ensuring a secure and robust chat experience.
* __GUI Interface:__ The client-side uses tkinter for a user-friendly graphical interface.

## Hardcoded Credentials
For the purpose of this demo, the following hardcoded credentials have been set:
* __ID:__ Akshay | __Password:__ qwerty
* __ID:__ John | __Password:__ password
* __ID:__ Sara | __Password:__ 12345

Note: It's advisable to implement a more secure authentication method for production usage.

## Requirements
* Python 3.x
* Libraries: socket, threading, tkinter, and selectors

## Usage

1. Start the server:
```bash
python Server.py
```
2. Start the client:
```bash
python Client.py
```
3. Enter one of the hardcoded credentials to authenticate and begin chatting.

## Troubleshooting
If you encounter the error "Error occurred... Please check if the HOST address and PORT number are correct," ensure the HOST address and PORT number match your machine's settings. You might need to update the IPv4 address in client.py with your machine's address.

## Analysis
The program is designed with a focus on robustness and statefulness. It has been rigorously tested to ensure it handles various input scenarios, including incorrect credentials and different case variations for user IDs and passwords. Its adherence to a DFA-based state ensures that even fuzzing introduces only minor errors.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
