import os
import json
import datetime
import csv
from datetime import datetime
import re
from functools import partial
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory = "messages/inbox"
folders = os.listdir(directory)
folder = "edstoddartfanclub_2zuwpuetxg"
filename = "message_1.json"
chat_name = folder.split("_")[0]
file_name = chat_name + ".csv"

f = open(file_name, "w+")
f.close()

data = json.load(open(os.path.join(directory,folder,filename), "r"))

for message in data["messages"]:
    try:
        date = datetime.fromtimestamp(message["timestamp_ms"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        sender = message["sender_name"]
        content = message["content"]
        with open(file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([date,sender,content])

    except (KeyError,UnicodeEncodeError):
        pass

df = pd.read_csv(file_name,encoding='latin1')
df.columns =['when', 'idiots', 'talk']

idiots = list(set(df["idiots"]))
talk_count = []
talk_length = []
word_counts = []
verbosity = []

for idiot in idiots:
    idiot_messages = df.loc[df['idiots']==idiot]
    talk_count.append(idiot_messages.shape[0])
    char_count = 0
    for message in idiot_messages["talk"]:
        char_count += len(message)
    talk_length.append(float(char_count)/float(idiot_messages.shape[0]))
    word_count = 0
    for message in idiot_messages["talk"]:
        word_count += (1+message.count(" "))
    word_counts.append(word_count)
    verbosity.append(float(char_count)/float(word_count))

d = {'idiots': idiots, 'talk_count': talk_count, 'talk_length': talk_length, "word_count": word_counts, "verbosity": verbosity}
output = pd.DataFrame(data = d)
#talk_count is the number of messages each idiot has sent
#talk_length is the average character character length of each idiot's messages
#verbosity is the average word length of each idiot's messages

count_rank = np.array(output["talk_count"].rank())
length_rank = np.array(output["talk_count"].rank())
verbosity_rank = np.array(output["verbosity"].rank())
shut_up_rank = count_rank + length_rank + verbosity_rank
output["shut the fuck up score"] = shut_up_rank
#idiots are scored based on their ranks in the three metrics

time_differences = {"Jason Lu": 0, "Josh Shipton": 0, "Jes Bromley": 0, "Kartikeya Kaushal": -6, "Declan Barrett": -12, }

d = {}
for idiot in idiots:
    d["{}".format(idiot)] = df.loc[df['idiots']==idiot]


def get_times_list(idiot):
    times = d[idiot]["when"]
    times_list = []
    for time in times:
        times_list.append(round((((int(time[11:13])+24+time_differences[idiot])%24)*3600 + int(time[14:16])*60 + int(time[17:19]))/(3600),2))
    return times_list

plt.hist(get_times_list("Declan Barrett"), bins = np.arange(0, 24, 1)) #change the name here
plt.xticks(range(0, 24))
plt.ylabel("number of messages")
plt.xlabel("time")
plt.show()