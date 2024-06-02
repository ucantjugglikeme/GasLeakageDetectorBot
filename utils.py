import aiomqtt

from config import data


GAS_TOPIC = "gas-leak-detection/+/+/gas-data"


async def mqtt_listen():
    async with aiomqtt.Client(
        data["mqtt_server"], 
        username=data["mqtt_user"], 
        password=data["mqtt_pass"]
    ) as client:
        await client.subscribe(GAS_TOPIC)
        async for message in client.messages:
            print(message.payload)