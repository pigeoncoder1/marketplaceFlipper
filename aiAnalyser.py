from email.mime import image
from openai import OpenAI
from telegram import sendMessage
client = OpenAI(api_key="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")

def evaluateListing(title, price, location, image_url, post_url):
    prompt = f"""
            You are an expert Facebook Marketplace bike flipper.
    Your goal is to find undervalued bikes that can be realistically flipped for £50+ profit with minimal effort — such as cleaning, adjusting gears, or fixing a puncture.
    You know how to spot valuable models, reliable components (Shimano, SRAM, hydraulic brakes, alloy or carbon frames), and reputable brands (Carrera, Boardman, Trek, Giant, etc.).
    ❗ Mark [YES] only if:
    The bike is priced well below market for its condition and brand.
    It's complete and structurally sound (no cracked frame, no major rust, no missing drivetrain).
    Any issues visible are minor (dust, seat tear, tuning, flat tyre).
    ❌ Mark [NO] if:
    It’s a kids’ bike, cheap wooden toy, or low-end department store model.
    It has serious problems: bent wheels, rusted chain/derailleur, missing parts, or poor resale brand.
    The price leaves little or no room for profit.
    Listing Info:
    Title: {title}
    Price: {price}

    Location: {location}
    URL: {post_url}
    Review the image and be strict. Only approve bikes that clearly show flipping potential.
    Final Verdict: [YES] or [NO]
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a professional deal evaluator."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content.strip()


