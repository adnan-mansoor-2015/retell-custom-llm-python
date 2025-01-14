import websocket
import _thread
import time
import rel
import json
import logging

logging.getLogger("websocket").disabled = True
response_id = 0

def on_message(ws, message):
    global response_id
    response = json.loads(message)

    if response_id in response:
        response_id = response["content"]["response_id"]

    if "content" in response:
        print("GPT: " +  response["content"] + "\n")    

    response_id += 1
    user_input = input("User: ")

    request = {
        "interaction_type": "response_required",
        "response_id": response_id,
        "transcript": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    ws.send(json.dumps(request))

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://9ef4-58-27-252-58.ngrok-free.app/llm-websocket/call_f7ed36406077f7585226c6b5437",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()