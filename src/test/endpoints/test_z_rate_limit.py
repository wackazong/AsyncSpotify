# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_rate_limit.py) is part of AsyncSpotify which is released under MIT.             #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import asyncio

import pytest
from aiohttp import ClientOSError

from async_spotify import SpotifyApiClient
from async_spotify.spotify_errors import RateLimitExceeded


@pytest.mark.asyncio
async def test_rate_limit(prepared_api: SpotifyApiClient):
    await prepared_api.create_new_client(request_timeout=5, request_limit=10000)

    album_id = '03dlqdFWY9gwJxGl3AREVy'
    # Somehow I dont get a timeout any more
    try:
        try:
            await asyncio.gather(*[prepared_api.albums.get_one(album_id) for _ in range(10000)])
        except ClientOSError:
            pass
        except asyncio.TimeoutError:
            pass
    except RateLimitExceeded as e:
        assert isinstance(e.retry_after, float)

    await asyncio.sleep(10)
