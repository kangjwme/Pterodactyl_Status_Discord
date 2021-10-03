import discord
import requests
from requests.structures import CaseInsensitiveDict
import json
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

client = discord.Client()

def now_time():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
    return dt2.strftime("%Y-%m-%d %H:%M:%S")
async def status(server_id):
    url = "https://這裡請放網址/api/client/servers/" + server_id + "/resources"
    url2 = "https://這裡請放網址/api/client/servers/" + server_id
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer 這裡請放「個人」API金鑰"
    resp = requests.get(url, headers=headers)
    resp2 = requests.get(url2, headers=headers)
    json_data = json.loads(resp.text)
    json_data_2 = json.loads(resp2.text)
    server_status = json_data["attributes"]["current_state"]
    server_status_text = ""
    if (server_status == "offline"):
        server_status_text = ":no_entry:  關閉"
    elif (server_status == "starting"):
        server_status_text = ":white_check_mark:  正在開啟中"
    elif (server_status == "stopping"):
        server_status_text = ":no_entry:  正在關閉中"
    else:
        server_status_text = ":white_check_mark:  開啟"

    server_memory = int(json_data["attributes"]["resources"]["memory_bytes"]) / 1024 / 1024
    server_memory_max = int(json_data_2["attributes"]["limits"]["memory"]) / 1024
    server_cpu = json_data["attributes"]["resources"]["cpu_absolute"]
    server_cpu_max = int(json_data_2["attributes"]["limits"]["cpu"])
    server_storage = int(json_data["attributes"]["resources"]["disk_bytes"]) / 1024 / 1024
    server_storage_max = int(json_data_2["attributes"]["limits"]["disk"]) / 1024
    embed = discord.Embed(title=f"伺服器狀態",color=0x00f900,description=f"伺服器現在 {server_status_text}")
    embed.add_field(name="<:image1:893930912776073276>  CPU",value=f"{server_cpu} % / {server_cpu_max} %",inline=False)
    embed.add_field(name="<:image0:893930901224980550>  記憶體",value=f"{(server_memory/1024):.2f} GB / {server_memory_max} GB",inline=False)
    embed.add_field(name="<:image2:893930923773542420>  儲存空間",value=f"{(server_storage/1024):.2f} GB / {server_storage_max} GB",inline=False)
    embed.set_footer(text=f"更新時間：{now_time()}")
    return embed

load_dotenv()
@client.event
async def on_ready():
    print('目前登入身份：', client.user)
    print('取得指定頻道ID：', os.getenv('channe_ID'))
    send_channel = client.get_channel(int(os.getenv('channe_ID')))
    msg = await send_channel.send(embed=await status(os.getenv('server_ID')))
    while True:
        await asyncio.sleep(10)
        await msg.edit(embed=await status(os.getenv('server_ID')))

client.run(os.getenv('bot_token'))
