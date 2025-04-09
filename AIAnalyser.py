from email.mime import image
from openai import OpenAI
from telegramBot import sendMessage
client = OpenAI(api_key="sk-proj-e0uiUn0xUEIT2bMAwJZMT3BlbkFJJ342ylsoOlPmV7ph8N0Z")

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

'''
print(evaluateListing(
    title="Wooden balance bike",
    price="10",
    location="chelmsford",
    image_url = "https://scontent-lhr6-2.xx.fbcdn.net/v/t45.5328-4/489356302_1618495829540591_8749239229300218959_n.jpg?stp=dst-jpg_p720x720_tt6&_nc_cat=105&ccb=1-7&_nc_sid=247b10&_nc_ohc=GY3Zn_6GWosQ7kNvwGUnqW8&_nc_oc=AdmOOArH3--CHYSupcREQkZmarxSGRqikWsx4O4qIdU5HOBZDXE-ag2-BAZAHzF8HQs&_nc_zt=23&_nc_ht=scontent-lhr6-2.xx&_nc_gid=4KaRIY-c-18fqqMME3bdPQ&oh=00_AfG-qb8xj4KkhuaGVV-DgpJJleTAhHWRPuBpsaxnPpc0ew&oe=67FCB1CC",
    post_url="https://www.facebook.com/marketplace/item/9475395362557116"))

print(evaluateListing(
    title="Carerra racing bike",
    price="30",
    location="chelmsford",
    image_url="https://scontent-lhr6-2.xx.fbcdn.net/v/t45.5328-4/484738651_1739414573274838_3897950431413098078_n.jpg?stp=c0.43.261.261a_dst-jpg_p261x260_tt6&_nc_cat=105&ccb=1-7&_nc_sid=247b10&_nc_ohc=HYD6j9h-jEsQ7kNvwFHuw0g&_nc_oc=AdlPaOJdSeYBF4QnoxPYnFdKetteQwAxJYFhPbMSEw-ZX8mLfoIFlwy1Dtf67-18dsw&_nc_zt=23&_nc_ht=scontent-lhr6-2.xx&_nc_gid=PsS-Yo98UGa5i1j_P8l2fw&oh=00_AfFZPKnqnTh0sCrfakHggkq1TY3EXyQJ1BTBXFhKKJoaEQ&oe=67FCBA6F",
    post_url="https://www.facebook.com/marketplace/item/1320404525838105/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A6efab9ff-9a31-48f6-9af4-c280559cfe5e"
))'''
