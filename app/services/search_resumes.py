from app.services.get_tokens import tokens
import httpx
from app.services.code import get_access_token_from_refresh_token


async def search_resumes(search, step=0):
    access_token = tokens.access_token
    headers = {
        "Authorization": "Bearer " + access_token,
        "User-Agent": "api-test-agent",
    }
    search.generate_search_link()
    print(search.url)
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(search.url, headers=headers)

    if "oauth_error" in response.json().keys():
        await get_access_token_from_refresh_token()
        step += 1
        await search_resumes(search, step)
        if step == 3:
            return "Error"

    try:
        resumes = response.json()["items"]
        return resumes
    except KeyError as e:
        print(f"Error: {response.json()}")
        return {"status": "error"}
