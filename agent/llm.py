from openai import AsyncOpenAI

from agent.config import (
    OLLAMA_URL,
    OLLAMA_MODEL,
    MAX_TOKENS,
)


client = AsyncOpenAI(
    base_url=OLLAMA_URL,
    api_key="ollama",
)


async def ask_llm(
    system_prompt: str,
    user_message: str,
):

    response = await client.chat.completions.create(

        model=OLLAMA_MODEL,

        max_tokens=MAX_TOKENS,

        temperature=0.2,

        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )

    return response.choices[0].message.content