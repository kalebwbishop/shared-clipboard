import asyncio
import websockets
import pyperclip
import time
import json

last_message = ""
last_timestamp = 0

async def send_message(websocket):
    global last_message
    global last_timestamp

    while True:
        await asyncio.sleep(0.5)

        new_message = pyperclip.paste()

        if (last_message == new_message):
            continue

        last_message = new_message
        last_timestamp = time.time()

        message = {
            "content": last_message,
            "timestamp": last_timestamp
        }

        await websocket.send(json.dumps(message))
        print(f"Sent message: {message}")

async def receive_message(websocket):
    global last_timestamp

    while True:
        await asyncio.sleep(0.5)

        message = await websocket.recv()

        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError:
            continue

        if (data["timestamp"] < last_timestamp):
            continue
        
        pyperclip.copy(data["content"])
        print(f"Received message: {data}")

async def main():
    uri = "ws://10.2.33.21:8765"
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
            send_message(websocket),
            receive_message(websocket)
        )


if __name__ == "__main__":
    asyncio.run(main())
    