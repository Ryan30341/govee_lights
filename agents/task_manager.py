"""
Task Manager for Agent Delegation
Manages and delegates tasks to specialized agents
"""
from typing import Dict, List, Callable
import threading
import queue

class TaskManager:
    """Manages task delegation to specialized agents"""
    
    def __init__(self):
        """Initialize task manager"""
        self.agents: Dict[str, Callable] = {}
        self.task_queue = queue.Queue()
        self.is_running = False
        self.worker_thread = None
    
    def register_agent(self, agent_name: str, agent_function: Callable):
        """
        Register an agent function
        
        Args:
            agent_name: Name identifier for the agent
            agent_function: Function to execute for this agent
        """
        self.agents[agent_name] = agent_function
    
    def submit_task(self, agent_name: str, task_data: Dict):
        """
        Submit a task to an agent
        
        Args:
            agent_name: Name of the agent to handle the task
            task_data: Data dictionary for the task
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not registered")
        
        self.task_queue.put({
            'agent': agent_name,
            'data': task_data
        })
    
    def start(self):
        """Start the task manager worker thread"""
        if self.is_running:
            return
        
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
    
    def stop(self):
        """Stop the task manager"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1.0)
    
    def _worker_loop(self):
        """Internal worker loop that processes tasks"""
        while self.is_running:
            try:
                task = self.task_queue.get(timeout=1.0)
                agent_name = task['agent']
                task_data = task['data']
                
                if agent_name in self.agents:
                    try:
                        self.agents[agent_name](task_data)
                    except Exception as e:
                        print(f"Error executing task for agent '{agent_name}': {e}")
                
                self.task_queue.task_done()
            except queue.Empty:
                continue

# Global task manager instance
task_manager = TaskManager()

# Initialize task manager
task_manager.start()

