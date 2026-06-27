"""
llm_client.py — A thin abstraction layer over the OpenAI and Anthropic chat
completion APIs, so app.py can call a single get_llm_response() function
regardless of which provider the user picks.
"""

from typing import List, Dict

AVAILABLE_PROVIDERS = {
    "Anthropic (Claude)": {
        "models": [
            "claude-sonnet-4-6",
            "claude-opus-4-7",
            "claude-haiku-4-5-20251001",
        ],
    },
    "OpenAI": {
        "models": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
        ],
    },
}


def get_llm_response(
    provider: str,
    model: str,
    api_key: str,
    system_prompt: str,
    history: List[Dict[str, str]],
) -> str:
    """
    Route the request to the correct provider and return the assistant's
    text response as a plain string.

    `history` is a list of {"role": "user"|"assistant", "content": str}
    dicts, already trimmed to a reasonable window by the caller.
    """
    if provider == "Anthropic (Claude)":
        return _call_anthropic(model, api_key, system_prompt, history)
    elif provider == "OpenAI":
        return _call_openai(model, api_key, system_prompt, history)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def _call_anthropic(
    model: str, api_key: str, system_prompt: str, history: List[Dict[str, str]]
) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    # Anthropic expects history as a list of {"role", "content"} with
    # roles alternating user/assistant — our stored format already matches.
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=history,
    )
    # response.content is a list of content blocks; concatenate text blocks.
    return "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()


def _call_openai(
    model: str, api_key: str, system_prompt: str, history: List[Dict[str, str]]
) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    messages = [{"role": "system", "content": system_prompt}] + history

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()
