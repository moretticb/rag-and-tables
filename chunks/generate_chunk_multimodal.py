import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import sys


def generate(b64_image,prompt):
    vertexai.init(project="PROJECT_GOES_HERE", location="LOCATION_GOES_HERE")
    model = GenerativeModel(
        "gemini-1.5-pro-001",
    )

    image = Part.from_data(
        mime_type="image/png",
        data=base64.b64decode(b64_image),
    )

    responses = model.generate_content(
        [image, prompt],
        generation_config=generation_config,
        safety_settings=None,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
}


if __name__ == "__main__":
    options = ["decomposition","reverse_engineering"]
    if len(sys.argv) > 1:
        for opt in options:
            if sys.argv[1] in opt:
                prompt_file = opt
    else:
        prompt_file = options[0]


    

    with open("../prompts/table_image_b64.txt","r") as f:
        b64_image = f.read()

    with open(f"../prompts/{prompt_file}.txt","r") as f:
        prompt = f.read()


    # removing comments
    prompt =  "".join([row for row in prompt.split("\n") if len(row) > 0 and row[0] != "#"])

    generate(b64_image, prompt)
