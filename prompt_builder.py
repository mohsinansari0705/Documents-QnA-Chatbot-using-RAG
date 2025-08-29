from typing import Union
from pathlib import Path
import yaml

"""
Prompt template construction functions for building modular prompts.
"""


def load_yaml_config(file_path: Union[str, Path]) -> dict:
    """Loads a YAML configuration file."""
    file_path = Path(file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def lowercase_first_char(text: str) -> str:
    """Lowercase the first character of a string."""
    return text[0].lower() + text[1:] if text else text


def format_prompt_section(lead_in: str, value: Union[str, list[str]]) -> str:
    """Formats a prompt section by joining a lead-in with content."""
    if isinstance(value, list):
        formatted_value = "\n".join(f"- {item}" for item in value)
    else:
        formatted_value = value

    return f"{lead_in}\n{formatted_value}"


def build_prompt_from_config(config: dict, input_data: list[str], query: str) -> str:
    """Builds a complete prompt string based on a config dictionary.

    Args:
        config: Dictionary specifying prompt components.
        input_data: Relevant content to be summarized or processed.
        query: User's query or request for information.

    Returns:
        A fully constructed prompt as a string.
    """
    prompt_parts = []

    if role := config.get('role'):
        prompt_parts.append(f"You are {lowercase_first_char(role.strip())}")

    if instruction := config.get('instruction'):
        prompt_parts.append(
            format_prompt_section(
                "Your task is as follows:",
                instruction
            )
        )

    if constraints := config.get('output_constraints'):
        prompt_parts.append(
            format_prompt_section(
                "Ensure your response follows these rules:",
                constraints
            )
        )

    if tone := config.get('style_or_tone'):
        prompt_parts.append(
            format_prompt_section(
                "Follow these style and tone guidelines in your response:",
                tone
            )
        )

    if format := config.get('output_format'):
        prompt_parts.append(
            format_prompt_section(
                "Structure your response as follows:",
                format
            )
        )

    if input_data:
        prompt_parts.append(
            "Here are the relevant contents you need to work with:\n"
            "<<<BEGIN CONTENT>>>\n\n" + "\n\n".join(input_data) + "\n\n<<<END CONTENT>>>"
        )

    if query:
        prompt_parts.append(
            format_prompt_section(
                "User's question:",
                query
            )
        )

    prompt_parts.append("Now perform the task as instructed above.")

    return "\n\n".join(prompt_parts)
