import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        for exchange_name in ["rpc-replies", "direct-rpc-requests"]:
            exchange = rabbitpy.Exchange(channel, exchange_name, exchange_type="direct")
            exchange.declare()
