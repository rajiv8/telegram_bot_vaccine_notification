from bot import telegram_chatbot
import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from json import loads

bot = telegram_chatbot()

update_id = None


def make_reply(msg):
    if msg is not None:
        date = datetime.datetime.now()
        dt = date.strftime("%d")
        mt = date.strftime("%m")
        yr = date.strftime("%Y")
        dte = dt+"-"+mt+"-"+yr
        pincode = msg
        API_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?"
        url_args = {
            'pincode': pincode,
            'date': dte
        }
        url = API_URL+"{}".format(urlencode(url_args))
        print(url)
        url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(url)
        # print(response)
        data = response.read()
        jsonData = loads(data)
        # print(jsonData)

        for session in jsonData.keys():
            arr = []
            for centres in jsonData.get(session):
                name = centres['name']
                minAge = centres['min_age_limit']
                available = centres['available_capacity']
                fee = centres['fee']
                timing = centres['slots']
                vaccineType = centres['vaccine']
                dat = centres['date']
                reply = "Vaccine center: {}\nMinimum Age: {}\nSlots Available: {}\nVaccine cost: {}\nDate: {}\nTimming:{}\nVaccine:{}".format(name,minAge,available,fee,dat,timing,vaccineType)
                arr.append(reply)
        return arr


while True:
    print("...")
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = item["message"]["text"]
            except:
                message = None
            # print(message)
            from_ = item["message"]["from"]["id"]
            # print(from_)
            message = str(message)
            # print(message)
            if message.isnumeric() and len(message)==6:
                reply = make_reply(message)
                if len(reply) == 0:
                    bot.send_message(
                        "No vaccination centers available at this pincode.", from_)
                else:
                    for i in range(len(reply)):
                        bot.send_message(reply[i], from_)
            else:
                bot.send_message("Enter a Valid Pincode.",from_)
            
                

            
