import os
import asyncio
import aiofiles
import aiohttp
import config
import datetime
import pytz
from atproto import Client, client_utils

async def main():
    # Login to Bluesky
    client = Client()
    client.login(config.username, config.password)
    async with aiohttp.ClientSession() as session:
        # Get info from bunnies.io
        async with session.get('https://api.bunnies.io/v2/loop/random/?media=gif,png,mp4') as bunny:
            data = await bunny.json()
            image = data["media"]["mp4"]
            seen = data["thisServed"]
            total = data["totalServed"]
            id = data["id"]
    async with aiohttp.ClientSession() as session:
        # Download video from Bluesky - as Bluesky does not yet support user GIFs, we use MP4 instead.
        async with session.get(image) as mp4:
            assert mp4.status == 200
            data = await mp4.read()
    # Save video to disk - This may not be needed (TODO)
    async with aiofiles.open("bunny.mp4", "wb") as outfile:
        await outfile.write(data)
    # Read video from disk - This may not be needed (TODO)
    async with aiofiles.open('bunny.mp4', mode='rb') as v:
        videofile = await v.read()
    # Build post text with client_utils TextBuilder
    tb = client_utils.TextBuilder()
    tb.text(f"🔢 ID: {id}\n\n👀 This bunny has been seen {seen} times.\n\n🐰 {total} total bunnies served.\n\n")
    tb.link(f"🔗 Source on bunnies.io", f"https://www.bunnies.io/#{id}")
    tb.text(f"\n\n")
    tb.tag("#bunny", "bunny")
    tb.text(" ")
    tb.tag("#bnuy", "bnuy")
    tb.text(" ")
    tb.tag("#rabbit", "rabbit")
    tb.text(" ")
    tb.tag("#animal", "animal")
    tb.text(" ")
    tb.tag("#animals", "animals")
    tb.text(" ")
    tb.tag("#rabbit", "rabbit")
    tb.text(" ")
    tb.tag("#cute", "cute")
    # Set timezone - Change this to fit your timezone
    tz = pytz.timezone("America/Chicago")
    # Post to Bluesky
    post = client.send_video(tb,videofile,"A cute bunny from bunnies.io")
    # Get current time and localize to timezone specified earlier
    now = datetime.datetime.now()
    posttime = tz.localize(now)
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    # Print to terminal with time sent
    print("sent bunny! " + posttime.strftime(format))
    # Sleep for one hour - task will restart after sleep ends
    await asyncio.sleep(3600)

# Run forever via async task
loop = asyncio.get_event_loop()
task = loop.create_task(main())
loop.run_forever()
