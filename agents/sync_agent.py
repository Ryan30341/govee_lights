"""
Synchronization Agent
Handles synchronized effects across multiple light strips
"""
from audio.light_sync import LightSyncCoordinator
from agents.task_manager import task_manager
from govee_api.client import GoveeAPIClient

sync_coordinators = {}

def sync_effect_handler(task_data: dict):
    """
    Handle synchronization effect tasks
    
    Expected task_data:
    {
        'action': str,  # 'start_rolling', 'stop_rolling'
        'strips': list,  # List of device IDs
        'led_counts': list,  # LED counts for each strip
        'speed': float,  # Speed of effect
        'color': tuple  # RGB color tuple
    }
    """
    global sync_coordinators
    
    action = task_data.get('action')
    strips = task_data.get('strips', [])
    led_counts = task_data.get('led_counts', [100, 100])  # Default LED counts
    
    if action == 'start_rolling':
        # Create unique key for this set of strips
        strip_key = '_'.join(sorted(strips))
        
        if strip_key not in sync_coordinators:
            coordinator = LightSyncCoordinator(strips, led_counts)
            sync_coordinators[strip_key] = coordinator
        
        coordinator = sync_coordinators[strip_key]
        speed = task_data.get('speed', 1.0)
        color = tuple(task_data.get('color', (255, 255, 255)))
        
        coordinator.create_rolling_effect(speed, color)
    
    elif action == 'stop_rolling':
        strip_key = '_'.join(sorted(strips))
        if strip_key in sync_coordinators:
            sync_coordinators[strip_key].stop()
            del sync_coordinators[strip_key]

# Register agent
task_manager.register_agent('sync_effect', sync_effect_handler)

