from dataclasses import dataclass, field
from enum import Enum

class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    

@dataclass
class Message:
    role: Role
    content: str
    
    def to_dict(self) -> dict[str, str]:
        return {
            "role": self.role.value,
            "content": self.content
        }

@dataclass
class Prompt:
    messages: list[Message]
    temperature: float