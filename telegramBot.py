import requests

def sendMessage(message):
    bot_token = "7571215237:AAHLhK19aPFS5h31EZXCeEqH3nx7Mk_hH7s"
    chat_id = "8070167150"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=payload)
    print(response.json())
    return response.json()

