from email.mime import image
from openai import OpenAI
client = OpenAI(api_key="sk-proj-e0uiUn0xUEIT2bMAwJZMT3BlbkFJJ342ylsoOlPmV7ph8N0Z")

def evaluateListing(title, price, location, image_url, post_url):
    prompt = f"""
        You're an expert Facebook Marketplace buyer.

        Listing info:
        - Title: {title}
        - Price: {price}
        - Location: {location}
        - URL: {post_url}

        Look at the image and decide if it's a good deal based on condition, price, value, and if i can comfortably resell for profits of £50+. You need to be pretty strict, if there is something that you're a bit unsure on, e.g. needing verification of something, then mark it as a no.

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

'''print(evaluateListing(
    title="2 bikes",
    price="10",
    location="chelmsford",
    image_url = "https://scontent-lhr6-2.xx.fbcdn.net/v/t45.5328-4/490504768_1887794865313961_5916840921978570661_n.jpg?stp=c43.0.260.260a_dst-jpg_p261x260_tt6&_nc_cat=100&ccb=1-7&_nc_sid=247b10&_nc_ohc=b4KkPKqsGBoQ7kNvwGazcPp&_nc_oc=AdnzrNVmcGq4cxtXivPfZ_OyHrWVVGrpO_foRuOCYH5pF03g5u0oogddbtqBgFG_mUE&_nc_zt=23&_nc_ht=scontent-lhr6-2.xx&_nc_gid=0b5d5kMUu00mBbf2uMo7cw&oh=00_AfGaIMTDrxrsGC60bbH3EwEiUfiTBhaUkaatz3hnddF3xg&oe=67FC72A4",
    post_url="https://www.facebook.com/marketplace/item/9475395362557116"))'''