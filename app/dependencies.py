from typing import Annotated
from fastapi import Header, HTTPException


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "coneofsilence":
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
