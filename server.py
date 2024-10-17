import asyncio
import websockets

clients = set()

async def echo(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            for client in clients:
                if client != websocket:
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosedOK:
                        print("Client disconnected.")
                        continue
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed normally.")
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())