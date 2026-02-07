import base64
import io
from typing import Annotated, Optional

import matplotlib.pyplot as plt
from fastmcp import FastMCP

mcp = FastMCP("visualization-server")


@mcp.tool(description="Create a line plot from numeric data and return it as a base64-encoded PNG image")
def line_plot(
    data: Annotated[list[float], "Y-axis values for the line plot"],
    title: Annotated[Optional[str], "Plot title"] = None,
    x_label: Annotated[Optional[str], "X-axis label"] = None,
    y_label: Annotated[Optional[str], "Y-axis label"] = None,
) -> str:
    # create the plot
    plt.figure()
    plt.plot(data)

    if title:
        plt.title(title)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)

    # save plot to in-memory buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    # encode as base64
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")

    return encoded_image


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8003)
