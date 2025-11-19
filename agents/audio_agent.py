"""
Audio Processing Agent
Handles audio-reactive lighting tasks
"""
from audio.frequency_analyzer import FrequencyAnalyzer
from agents.task_manager import task_manager
from govee_api.client import GoveeAPIClient
import time

audio_analyzer = None
client = None

def audio_reactive_handler(task_data: dict):
    """
    Handle audio-reactive lighting tasks
    
    Expected task_data:
    {
        'action': str,  # 'start', 'stop'
        'device_ids': list,  # List of device IDs to control
        'duration': int  # Optional duration in seconds
    }
    """
    global audio_analyzer, client
    
    action = task_data.get('action')
    device_ids = task_data.get('device_ids', [])
    
    if action == 'start':
        if not audio_analyzer:
            audio_analyzer = FrequencyAnalyzer()
            audio_analyzer.start_stream()
            client = GoveeAPIClient()
        
        # Process audio and update lights
        duration = task_data.get('duration', None)
        start_time = time.time()
        
        while True:
            if duration and (time.time() - start_time) > duration:
                break
            
            try:
                color = audio_analyzer.get_current_color()
                for device_id in device_ids:
                    client.set_color(device_id, *color)
            except Exception as e:
                print(f"Error in audio-reactive mode: {e}")
                break
            
            time.sleep(0.1)  # Update 10 times per second
    
    elif action == 'stop':
        if audio_analyzer:
            audio_analyzer.stop_stream()
            audio_analyzer.cleanup()
            audio_analyzer = None

# Register agent
task_manager.register_agent('audio_reactive', audio_reactive_handler)

