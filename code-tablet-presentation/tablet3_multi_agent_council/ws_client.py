import asyncio, websockets

async def main():
    uri = "ws://localhost:9000/council"
    async with websockets.connect(uri) as ws:
        await ws.send("Design a minimal social media app.")
        while True:
            try:
                msg = await ws.recv()
                print(msg)
            except websockets.exceptions.ConnectionClosed:
                break

if __name__ == "__main__":
    asyncio.run(main())
