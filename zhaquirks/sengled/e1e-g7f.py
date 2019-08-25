"""Sengled E1E-G7F device."""
from zigpy.profiles import zha, zll
import zigpy.types as t
from zigpy.quirks import CustomDevice, CustomCluster
from zigpy.zcl.clusters.general import (
    Basic, BinaryInput, Groups, PollControl, Identify, LevelControl, OnOff, Ota,
    PowerConfiguration, Scenes, )
from zigpy.zcl.clusters.manufacturer_specific import (ManufacturerSpecificCluster )
from zhaquirks.sengled import (
    BasicCluster, SengledCustomDevice
)
DIAGNOSTICS_CLUSTER_ID = 0x0B05  # decimal = 2821
SENGLED_CLUSTER_ID_IN = 64529
SENGLED_CLUSTER_ID_OUT = 64528

class BasicCluster(CustomCluster, Basic):
    """Centralite acceleration cluster."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.attributes = super().attributes.copy()
        self.attributes.update({
            0x0031: ('sengled', t.bitmap16),
        })


class SengledE1EG7F(CustomDevice):
    """Sengled E1E-G7F device."""

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=260 
        #  device_version=0 
        #  input_clusters=[0, 1, 3, 32, 64529] 
        #  output_clusters=[3, 4, 6, 8, 64528]>
        'models_info': [
            ('sengled', 'E1E-G7F')
        ],
        'endpoints': {
            1: {
                'profile_id': zha.PROFILE_ID,
                'device_type': zha.DeviceType.DIMMER_SWITCH,
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    SENGLED_CLUSTER_ID_IN
                ],
                'output_clusters': [
                    Identify.cluster_id,
                    Groups.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    SENGLED_CLUSTER_ID_OUT
                ],
            },
            #  <SimpleDescriptor endpoint=2 profile=260 device_type=12
            #  device_version=0
            #  input_clusters=[0, 1, 3, 15, 64512]
            #  output_clusters=[25]>

        }
    }

    replacement = {
        'endpoints': {
            1: {
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    SENGLED_CLUSTER_ID_IN
                ],
                'output_clusters': [
                    Identify.cluster_id,
                    Groups.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    SENGLED_CLUSTER_ID_OUT
                ],
            },
        },
    }
