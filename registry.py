from device import Device, find, union


class DeviceRegistry:
    def __init__(self):
        self.devices = {}       # id -> Device
        self.parent = {}        # id -> id (union-find)
        self.ip_index = {}      # ip -> id
        self.serial_index = {}  # serial -> id
        self._next_id = 0

    def _new_id(self) -> int:
        new_id = self._next_id
        self._next_id += 1
        self.parent[new_id] = new_id
        return new_id

    def register_neighbor(self, hostname: str, ip: str) -> Device:
        if ip in self.ip_index:
            stored_id = self.ip_index[ip]
            canonical_id = find(self.parent, stored_id)
            return self.devices[canonical_id]

        new_id = self._new_id()
        new_device = Device(id=new_id, hostname=hostname, ips={ip})
        self.devices[new_id] = new_device
        self.ip_index[ip] = new_id
        return new_device



    def confirm_device(self, device_id: str, serial: str, model: str, version: str) -> Device:
        canonical_id = find(self.parent, device_id)
        device = self.devices[canonical_id]

        if serial in self.serial_index:
            existing_id = find(self.parent, self.serial_index[serial])
            if existing_id != canonical_id:
                # true duplicate: same serial, different id -> merge
                existing_device = self.devices[existing_id]
                device.ips |= existing_device.ips
                del self.devices[existing_id]
                canonical_id = union(self.parent, canonical_id, existing_id)

        self.serial_index[serial] = canonical_id
        device.serial = serial
        device.model = model
        device.version = version
        device.confirmed = True
        return device
