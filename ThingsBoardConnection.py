
import logging
import dotenv
import os
from tb_device_mqtt import TBDeviceMqttClient

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


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
        self.tb_client.request_attributes(
            shared_keys = ["enabled", "alarm"],
            callback = lambda attributes, *args: self.receive_shared_attributes(attribute, callback, attributes, *args)
        )
        
    def subscribe_to_attribute(self, attribute, callback):
        log.info(f"subscribing to {attribute=} with {callback=}")
        log.info(self.tb_client.subscribe_to_attribute(attribute, callback=lambda attributes, *args :self.receive_shared_attributes(attribute, callback, attributes, *args)))    

    def receive_shared_attributes(self, attribute, callback, attributes, *args):
        log.info(f"Received shared attribute {attribute=}; {callback=}; {attributes=}, {args=}")
        
        shared_attributes = attributes["shared"] if "shared" in attributes else attributes
            
        if attribute in shared_attributes:
            variable = shared_attributes[attribute]
            callback(variable)
            
        # log.info(f"{alarm = }, {enabled = }")

    def handle_rpc_request(self, client, request_body):
        # RPC Anfrage vom EIN/aus Schalter vom Dashboard verarbeiten
        
        log.info(f"RPC Anfrage empfangen: {request_body} from {client=}")
        
        if request_body["method"] == "setAttributeValue":
            attribute = request_body["params"]["attribute"]
            value = request_body["params"]["values"]
            
            if attribute:
                log.info(f"setze Attribut {attribute} auf {value}")
                
                # Anfrage zurueck an den server
                self.tb_client.send_attributes({attribute: value})
                
    def send(self, telemetry):
        self.tb_client.send_telemetry(telemetry)



if __name__ == "__main__":
    
    a = {"a":4}
    tb = ThingsBoard()
    tb.send(a)
