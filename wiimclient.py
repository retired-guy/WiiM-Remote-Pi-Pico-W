import urequests as requests

def invokeWiimAction(WiimIp, service, action, detaildict={}):
    if service == 'AVTransport':
        control = "/upnp/control/rendertransport1"
        schema = "schemas-upnp-org"
    elif service == 'RenderingControl':
        control = "/upnp/control/rendercontrol1"
        schema = "schemas-upnp-org"
    elif service == 'PlayQueue':
        control = "/upnp/control/PlayQueue1"
        schema = "schemas-wiimu-com"
        
    url = f"http://{WiimIp}:49152{control}"

    detail = ""
    for key in detaildict:
        value = detaildict[key]
        detail = detail + f"<{key}>{value}</{key}>"
        
    data = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
        <s:Body>
            <u:{action} xmlns:u="urn:{schema}:service:{service}:1">
                <InstanceID>0</InstanceID>
                {detail}
            </u:{action}>
        </s:Body>
    </s:Envelope>
    """
    
    headers = {'Content-Type' : 'text/xml; charset=utf-8',
              'SOAPAction' : f'"urn:{schema}:service:{service}:1#{action}"'}

    resp = requests.post(url, headers=headers, data=data)

    meta = resp.content.decode("UTF-8")

    meta = meta.split("<s:Body>")[1]
    meta = meta.split("</s:Body>")[0]
    items = meta.split("\n")

    dict = {}
    for item in items:
        try:
          name = item.split(">")[0].replace("<","")
          value = item.split(">")[1].split("</")[0]
          if not ":" in name:
              dict[name] = value
        except:
            continue

    return dict

