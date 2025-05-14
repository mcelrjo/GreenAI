# In app/services/image_service.py
import base64
import openai

async def handle_image_diagnosis(file):
    contents = await file.read()
    b64_img = base64.b64encode(contents).decode()

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "What's wrong with this turfgrass?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
            ]}
        ],
        max_tokens=1000
    )
    return response.choices[0].message["content"]
