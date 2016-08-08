import logging
import os
import unittest
import json

from avi.netscaler_converter.ns_service_converter import ServiceConverter
import avi.netscaler_converter.ns_util as ns_util

gSAMPLE_CONFIG = None
LOG = logging.getLogger(__name__)


def setUpModule():
    LOG.setLevel(logging.DEBUG)
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    path = "test_output"
    logging.basicConfig(filename=os.path.join(path, 'test.log'),
                        level=logging.DEBUG, format=formatter)
    cfg_file = open('test_ns_service_converter.cfg', 'r')
    cfg = cfg_file.read()
    global gSAMPLE_CONFIG
    gSAMPLE_CONFIG = json.loads(cfg)
    LOG.debug(' read cofig %s', gSAMPLE_CONFIG)
    status_file = "./test_output" + os.path.sep + "ConversionStatus.csv"
    csv_file = open(status_file, 'w')
    ns_util.add_csv_headers(csv_file)



class Test(unittest.TestCase):

    def test_service_conversion(self):
        service_converter = ServiceConverter()
        avi_config = gSAMPLE_CONFIG["avi_config"]
        ns_config_dict = gSAMPLE_CONFIG["ns_config_dict"]
        service_converter.convert(ns_config_dict, avi_config)
        assert avi_config['Pool'][0]
        assert len(avi_config['Pool'][0]['health_monitor_refs']) == 3
        assert len(avi_config['Pool'][0]['servers']) == 6