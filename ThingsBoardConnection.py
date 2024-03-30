
import logging
import dotenv
import os
from tb_device_mqtt import TBDeviceMqttClient

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ThingsBoard:
    def __init__(self):
        dotenv.load_dotenv()
        
        log.debug(f"Stelle Verbindung zum Backend her: mqtt://{os.environ['TB_HOST']}:{os.environ['TB_PORT']}")


        self.tb_client = TBDeviceMqttClient(
            host = os.environ["TB_HOST"],
            port = int(os.environ["TB_PORT"]),
            username = os.environ["TB_TOKEN"]
        )
        
        self.tb_client.connect()
        
        
    def get_attributes(self, attribute, callback):
        log.info(f"requesting {attribute=} with {callback=}")
        self.tb_client.request_attributes(
            shared_keys = ["enabled", "alarm"],
            callback = lambda attributes, *args: self.receive_shared_attributes(attribute, callback, attributes, *args)
        )
    
    def set_attribute(self, attribute, value):
        log.info(f"setting shared {attribute=} to {value=}")
        self.tb_client.send_attributes({attribute: value})
    
    def subscribe_to_attribute(self, attribute, callback):
        log.info(f"subscribing to {attribute=} with {callback=}")
        self.tb_client.subscribe_to_attribute(attribute, callback=lambda attributes, *args :self.receive_shared_attributes(attribute, callback, attributes, *args))

    def receive_shared_attributes(self, attribute, callback, attributes, *args):
        log.debug(f"Received shared attribute {attribute=}; {callback=}; {attributes=}, {args=}")
        
        shared_attributes = attributes["shared"] if "shared" in attributes else attributes
            
        if attribute in shared_attributes:
            variable = shared_attributes[attribute]
            callback(variable)
            
    def set_callback_for_rpc_request(self, attribute, callback):
        self.tb_client.set_server_side_rpc_request_handler(lambda client, request_body, attr=attribute, cb=callback: self.handle_rpc_request(attr,cb, client, request_body))
        
    
    def handle_rpc_request(self, attribute, callback, client, request_body):
        # RPC Anfrage vom EIN/aus Schalter vom Dashboard verarbeiten
        
        log.debug(f"RPC Anfrage empfangen: {request_body} from {client=}")
        
        if request_body["method"] == "setValue":
            attribute = request_body["params"]["attribute"]
            value = request_body["params"]["value"]
            
            if attribute:
                log.info(f"setze Attribut {attribute} auf {value}")
                callback(value)
                
                # Anfrage zurueck an den server
                # self.tb_client.send_attributes({attribute: value})
                
    def send(self, telemetry):
        log.debug(f"sent telemetry: {telemetry}")
        self.tb_client.send_telemetry(telemetry)



if __name__ == "__main__":
    logging.basicConfig(
        format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level = logging.DEBUG,
    )
    a = {"pulse":100}
    tb = ThingsBoard()
    tb.send(a)
    
