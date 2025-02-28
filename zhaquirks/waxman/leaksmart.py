"""Device handler for WAXMAN leakSMART."""
# pylint: disable=W0102
from zigpy.profiles import zha
from zigpy.quirks import CustomCluster, CustomDevice
import zigpy.types as t
from zigpy.zcl.clusters.general import (
    Basic, Identify, Ota, PowerConfiguration, PollControl)
from zigpy.zcl.clusters.homeautomation import ApplianceEventAlerts
from zigpy.zcl.clusters.measurement import TemperatureMeasurement
from zigpy.zcl.clusters.security import IasZone

from zhaquirks import Bus, LocalDataCluster

WAXMAN_CMDID = 0x0001

ZONE_STATE = 0
ZONE_TYPE = 0x0001
MOISTURE_TYPE = 0x002A

MANUFACTURER_SPECIFIC_CLUSTER_ID = 0xFC02  # decimal = 64514


class EmulatedIasZone(LocalDataCluster, IasZone):
    """Emulated IAS zone cluster."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.endpoint.device.ias_bus.add_listener(self)
        super()._update_attribute(ZONE_TYPE, MOISTURE_TYPE)

    async def bind(self):
        """Bind cluster."""
        result = await self.endpoint.device.app_cluster.bind()
        return result

    async def write_attributes(self, attributes, is_report=False,
                               manufacturer=None, unsupported_attrs=[]):
        """Ignore write_attributes."""
        return (0,)

    def update_state(self, value):
        """Update IAS state."""
        super().listener_event(
            'cluster_command',
            None,
            ZONE_STATE,
            [value]
        )


class WAXMANApplianceEventAlerts(CustomCluster, ApplianceEventAlerts):
    """WAXMAN specific ApplianceEventAlert cluster."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.client_commands = super().client_commands.copy()
        self.client_commands.update({
            WAXMAN_CMDID: ('alerts_notification', (t.uint8_t, t.bitmap24),
                           False),
        })
        self.endpoint.device.app_cluster = self

    def handle_cluster_request(self, tsn, command_id, args):
        """Handle a cluster command received on this cluster."""
        if command_id == WAXMAN_CMDID:
            state = bool(args[1] & 0x1000)

            self.endpoint.device.ias_bus.listener_event(
                'update_state',
                state
            )


class WAXMANleakSMARTv2(CustomDevice):
    """Custom device representing WAXMAN leakSMART v2."""

    def __init__(self, *args, **kwargs):
        """Init."""
        self.ias_bus = Bus()
        super().__init__(*args, **kwargs)

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=770
        #  device_version=0
        #  input_clusters=[0, 1, 3, 32, 1026, 2818, 64514]
        #  output_clusters=[3, 25]>
        'models_info': [
            ('WAXMAN', 'leakSMART Water Sensor V2'),
        ],
        'endpoints': {
            1: {
                'profile_id': zha.PROFILE_ID,
                'device_type': zha.DeviceType.TEMPERATURE_SENSOR,
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    ApplianceEventAlerts.cluster_id,
                    MANUFACTURER_SPECIFIC_CLUSTER_ID
                ],
                'output_clusters': [
                    Identify.cluster_id,
                    Ota.cluster_id
                ],
            },
        }
    }

    replacement = {
        'endpoints': {
            1: {
                'profile_id': zha.PROFILE_ID,
                'device_type': zha.DeviceType.TEMPERATURE_SENSOR,
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    WAXMANApplianceEventAlerts,
                    EmulatedIasZone
                ],
                'output_clusters': [
                    Identify.cluster_id,
                    Ota.cluster_id
                ],
            },
        }
    }
