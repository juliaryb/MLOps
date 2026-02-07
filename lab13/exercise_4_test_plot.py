import asyncio
import base64
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():
    async with streamable_http_client("http://localhost:8003/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "line_plot",
                arguments={
                    "data": [1, 3, 2, 5, 4],
                    "title": "Sample Line Plot",
                    "x_label": "Index",
                    "y_label": "Value",
                },
            )

            encoded_image = result.content[0].text
            image_bytes = base64.b64decode(encoded_image)

            with open("sample_plot.png", "wb") as f:
                f.write(image_bytes)

            print("Saved sample_plot.png")


if __name__ == "__main__":
    asyncio.run(main())
