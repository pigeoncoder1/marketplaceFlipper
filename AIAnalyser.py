from email.mime import image
from openai import OpenAI
from telegramBot import sendMessage
client = OpenAI(api_key="sk-proj-e0uiUn0xUEIT2bMAwJZMT3BlbkFJJ342ylsoOlPmV7ph8N0Z")

def evaluateListing(title, price, location, image_url, post_url):
    prompt = f"""
        You're an expert bike flipper on Facebook Marketplace.
        Your goal is to spot underpriced bikes that can realistically be cleaned or lightly repaired and flipped for £50+ profit.

        You know the value of common brands, models, and components.
        If a bike shows clear potential for resale at profit, even with minor fixes (e.g. surface rust, gear tuning, cleaning), treat it as [YES].

        However, if the bike shows major red flags (e.g. cracked frame, missing key parts, very overpriced), mark it as [NO].

        Listing info:

        Title: {title}

        Price: {price}

        Location: {location}

        URL: {post_url}

        Look at the image and give a confident decision.
        End with a clear verdict: [YES] or [NO].
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

'''result = evaluateListing(
    title="Racing bike",
    price="30",
    location="chelmsford",
    image_url = "https://scontent-lhr6-2.xx.fbcdn.net/v/t45.5328-4/484738651_1739414573274838_3897950431413098078_n.jpg?stp=dst-jpg_p720x720_tt6&_nc_cat=105&ccb=1-7&_nc_sid=247b10&_nc_ohc=HYD6j9h-jEsQ7kNvwFHuw0g&_nc_oc=AdlPaOJdSeYBF4QnoxPYnFdKetteQwAxJYFhPbMSEw-ZX8mLfoIFlwy1Dtf67-18dsw&_nc_zt=23&_nc_ht=scontent-lhr6-2.xx&_nc_gid=K-MwFlks7lmlhi8xZpiXeg&oh=00_AfHjQ2zE_g9ajgGpNAX7y0vsMOSNdQviVA-H3Dh18uusKg&oe=67FCBA6F",
    post_url="https://www.facebook.com/marketplace/item/9475395362557116")'''
