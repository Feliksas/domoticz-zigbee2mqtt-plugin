from adapters.adapter_with_battery import AdapterWithBattery
from devices.switch.selector_switch import SelectorSwitch
from devices.switch.toggle_switch import ToggleSwitch


class TradfriRemoteControl(AdapterWithBattery):
    def __init__(self, devices):
        super().__init__(devices)

        self.switch = ToggleSwitch(devices, 'switch', 'action')
        
        self.selector_switch = SelectorSwitch(devices, 'sel', 'action', ' (Selector)')
        self.selector_switch.add_level('Off', None)
        
        self.selector_switch.add_level('brightness-up-click', 'brightness_up_click')
        self.selector_switch.add_level('brightness-up-hold', 'brightness_up_hold')
        self.selector_switch.add_level('brightness-up-release', 'brightness_up_release')

        self.selector_switch.add_level('brightness-down-click', 'brightness_down_click')
        self.selector_switch.add_level('brightness-down-hold', 'brightness_down_hold')
        self.selector_switch.add_level('brightness-down-release', 'brightness_down_release')

        self.selector_switch.add_level('arrow-left-click', 'arrow_left_click')
        self.selector_switch.add_level('arrow-left-hold', 'arrow_left_hold')
        self.selector_switch.add_level('arrow-left-release', 'arrow_left_release')

        self.selector_switch.add_level('arrow-right-click', 'arrow_right_click')
        self.selector_switch.add_level('arrow-right-hold', 'arrow_right_hold')
        self.selector_switch.add_level('arrow-right-release', 'arrow_right_release')
       
        self.selector_switch.disable_value_check_on_update()

        self.selector_switch.set_selector_style(SelectorSwitch.SELECTOR_TYPE_MENU)
        self.devices.append(self.switch)
        self.devices.append(self.selector_switch)

    def handleCommand(self, alias, device, device_data, command, level, color):
        device = self.get_device_by_alias(alias)

        if device != None:
            device.handle_command(device_data, command, level, color)

    def handleMqttMessage(self, device_data, message):
        if 'action' not in message.raw:
            return

        converted_message = self.convert_message(message)
        action = message.raw['action']
        
        if action == 'toggle':
            self.switch.handle_message(device_data, converted_message)
        
        if action.startswith('brightness_up'):
            self.selector_switch.handle_message(device_data, converted_message)

        if action.startswith('brightness_down'):
            self.selector_switch.handle_message(device_data, converted_message)

        if action.startswith('arrow_right'):
            self.selector_switch.handle_message(device_data, converted_message)

        if action.startswith('arrow_left'):
            self.selector_switch.handle_message(device_data, converted_message)

        self.update_battery_status(device_data, converted_message)
        self.update_link_quality(device_data, converted_message)
