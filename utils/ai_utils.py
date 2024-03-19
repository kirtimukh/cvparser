import os, dotenv
import json
import openai

from instructions import (
    DIRECTIVE,
    TEMPERATURE,
    TOP_P,
    FREQUENCY_PENALTY,
    PRESENCE_PENALTY,
)

dotenv.load_dotenv()

debug = int(os.getenv("DEBUG", "0"))
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_response_format():
    response_format = ""
    with open("response_format/scores.json") as f:
        response_format = json.dumps(json.load(f))

    return response_format


async def analyze_text_with_openai(text, filepath):
    json_response_format = get_response_format()
    response = await client.chat.completions.create(
        model="gpt-4-0125-preview",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    f"""
                    \n
                    Path to the resume file: {filepath}
                    If the resume file is an image, the resume content was extracted using OCR.
                    Since OCRs are not perfect, please corrections to spellings, punctuations, and bullet points before proceeding.
                    \n
                    {DIRECTIVE}
                    \n
                    Give the response as a json serializable string STRICTLY in this format only: {json_response_format}
                    \n
                    Omit ```json``` and `````` from the response.
                    """
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=TEMPERATURE,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    if debug:
        print(
            f"\nFinished scoring `{filepath}`; total tokens used:",
            response.usage.total_tokens,
        )
    else:
        print(".", end="")
    return response.choices[0].message.content
