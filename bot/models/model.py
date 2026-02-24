from dataclasses import dataclass


@dataclass
class ToolReport:
    tool_name: str
    success: bool
    output: str
