"""Phillips RWL021 device."""
from zigpy.profiles import zha, zll
import zigpy.types as t
from zigpy.quirks import CustomDevice, CustomCluster
from zigpy.zcl.clusters.general import (
    Basic, BinaryInput, Groups, Identify, LevelControl, OnOff, Ota,
    PowerConfiguration, Scenes)

DIAGNOSTICS_CLUSTER_ID = 0x0B05  # decimal = 2821


class BasicCluster(CustomCluster, Basic):
    """Centralite acceleration cluster."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.attributes = super().attributes.copy()
        self.attributes.update({
            0x0031: ('phillips', t.bitmap16),
        })


class PhilipsRWL021(CustomDevice):
    """Phillips RWL021 device."""

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=49246 device_type=2096
        #  device_version=2
        #  input_clusters=[0]
        #  output_clusters=[0, 3, 4, 6, 8, 5]>
        'endpoints': {
            1: {
                'profile_id': zll.PROFILE_ID,
                'device_type': zll.DeviceType.SCENE_CONTROLLER,
                'input_clusters': [
                    Basic.cluster_id
                ],
                'output_clusters': [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Scenes.cluster_id
                ],
            },
            #  <SimpleDescriptor endpoint=2 profile=260 device_type=12
            #  device_version=0
            #  input_clusters=[0, 1, 3, 15, 64512]
            #  output_clusters=[25]>
            2: {
                'profile_id': zha.PROFILE_ID,
                'device_type': zha.DeviceType.SIMPLE_SENSOR,
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    BinaryInput.cluster_id,
                    64512
                ],
                'output_clusters': [
                    Ota.cluster_id
                ],
            },
        }
    }

    replacement = {
        'endpoints': {
            1: {
                'input_clusters': [
                    Basic.cluster_id
                ],
                'output_clusters': [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Scenes.cluster_id
                ],
            },
            2: {
                'input_clusters': [
                    BasicCluster,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    BinaryInput.cluster_id,
                    64512
                ],
                'output_clusters': [
                    Ota.cluster_id
                ],
            },
        },
    }
