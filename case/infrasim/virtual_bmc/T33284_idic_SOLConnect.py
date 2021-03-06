'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''
from case.CBaseCase import *

class T33284_idic_SOLConnect(CBaseCase):
    '''
    [Purpose ]: Verify SOL to host is workable on virtual node
    [Author  ]: forrest.gu@emc.com
    '''
    def __init__(self):
        CBaseCase.__init__(self, self.__class__.__name__)
    
    def config(self):
        CBaseCase.config(self)
        # To do: Case specific config
        self.enable_node_ssh()

    def test(self):

        for obj_node in self.stack.walk_node():

            self.log('INFO', 'Activate SOL on node {} ...'.format(obj_node.get_name()))
            obj_node.sol_activate(log_dir=self.str_work_directory)

            self.log('INFO', 'Power cycle node {} then check SOL ...'.format(obj_node.get_name()))
            obj_node.get_bmc().ipmi.ipmitool_standard_cmd('chassis power cycle')
            
            self.log('INFO', 'Verify if SOL on node {} is alive in 60s ...'.format(obj_node.get_name()))
            if obj_node.sol_is_alive():
                self.log('INFO', 'Node {} SOL to virtual host is alive'.format(obj_node.get_name()))
            else:
                self.result(FAIL, 'Node {} SOL to virtual host is not alive'.format(obj_node.get_name()))
            obj_node.sol_deactivate()
    
    def deconfig(self):
        # To do: Case specific deconfig
        self.log('INFO', 'Wait 30s for all nodes to boot ...')
        time.sleep(30)
        CBaseCase.deconfig(self)
