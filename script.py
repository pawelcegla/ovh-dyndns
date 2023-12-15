import logging
import sys
import tomllib

import requests

logging.basicConfig(filename='/var/log/dyndns.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.debug('Requests version: %s', requests.__version__)
ip = requests.get('https://api.ipify.org').text
logging.debug('Public IP: %s', ip)
with open(sys.argv[1], 'rb') as f:
    cfg = tomllib.load(f)
    discord_url = cfg['discord']['url']
    for hostname in cfg['credentials'].keys():
        logging.debug('Hostname: %s', hostname)
        creds = cfg['credentials'][hostname]
        dyndns_url = 'https://www.ovh.com/nic/update?system=dyndns&hostname={}&myip={}'.format(hostname, ip)
        dyndns = requests.get(dyndns_url, auth=(creds['username'], creds['password'])).text
        logging.debug('DynDNS responded: %s', dyndns)
        if dyndns.startswith('good'):
            discord = requests.post(
                discord_url,
                json={'content': '`{}` A record got updated to `{}`'.format(hostname, ip)}).status_code
            logging.debug('Discord responded: %s', discord)
