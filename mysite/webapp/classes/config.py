

class ConfigSetup:
    @staticmethod
    def get_sensors():
        sensors = [
            {'type': 'DS18B20', 'options': {'name': '28-051693633fff', 'id': 1}},
            {'type': 'DHT11', 'options': {'pin': '4', 'type': '11', 'id': 2}}
        ]
        return sensors

