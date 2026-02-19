from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime
from .MessageTypes import MessageType


@dataclass
class Message:
    """
    Structured message for client-server communication.
    Provides a uniform interface for all game messages.
    """
    type: MessageType
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[float] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().timestamp()

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        return {
            'type': self.type.name,
            'data': self.data,
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary"""
        return cls(
            type=MessageType[data['type']],
            data=data.get('data', {}),
            timestamp=data.get('timestamp'),
            session_id=data.get('session_id'),
            metadata=data.get('metadata', {})
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Convenience method to get data field"""
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Convenience method to set data field"""
        self.data[key] = value
