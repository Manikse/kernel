import uuid
import time
from typing import Dict, Any, Optional

class AgentRequest:
    """
    Standardized request format for A2A communication.
    """
    def __init__(self, sender_id: str, receiver_id: str, action: str, params: Dict[str, Any]):
        self.request_id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.action = action  # e.g., 'RESEARCH', 'CODE_REFACTOR', 'SEARCH_WEB'
        self.params = params
        self.timestamp = time.time()

class AgentResponse:
    """
    Standardized response format.
    """
    def __init__(self, request_id: str, status: str, data: Any):
        self.request_id = request_id
        self.status = status  # 'SUCCESS', 'FAILED', 'PENDING'
        self.data = data
        self.timestamp = time.time()

class A2AMessenger:
    """
    The Post Office of the Kernel. 
    Routes messages between different AI agents.
    """
    def __init__(self):
        self.message_history: List[AgentRequest] = []

    def dispatch(self, request: AgentRequest) -> str:
        print(f"[Kernel A2A] Routing action '{request.action}' from {request.sender_id} to {request.receiver_id}")
        self.message_history.append(request)
        return f"Message {request.request_id} delivered."