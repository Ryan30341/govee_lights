"""
Light Control Agent
Handles light control tasks
"""
from govee_api.client import GoveeAPIClient
from agents.task_manager import task_manager

def light_control_handler(task_data: dict):
    """
    Handle light control tasks
    
    Expected task_data:
    {
        'device_id': str,
        'action': str,  # 'on', 'off', 'color', 'brightness', etc.
        'params': dict  # Additional parameters
    }
    """
    client = GoveeAPIClient()
    device_id = task_data.get('device_id')
    action = task_data.get('action')
    params = task_data.get('params', {})
    
    if action == 'color':
        r = params.get('r', 255)
        g = params.get('g', 255)
        b = params.get('b', 255)
        client.set_color(device_id, r, g, b)
    elif action == 'brightness':
        brightness = params.get('brightness', 50)
        client.set_brightness(device_id, brightness)
    elif action == 'on':
        client.control_device(device_id, {'name': 'turn', 'value': 'on'})
    elif action == 'off':
        client.control_device(device_id, {'name': 'turn', 'value': 'off'})

# Register agent
task_manager.register_agent('light_control', light_control_handler)

