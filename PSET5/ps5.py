# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import traceback


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
  def __init__(self, guide, title, description, link, pubdate):
    self.guide = guide
    self.title = title
    self.description = description
    self.link = link
    self.pubdate = pubdate

  def get_guid(self):
    return self.guide

  def get_title(self):
    return self.title

  def get_description(self):
    return self.description

  def get_link(self):
    return self.link

  def get_pubdate(self):
    return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
  def evaluate(self, story):
    """
    Returns True if an alert should be generated
    for the given news item, or False otherwise.
    """
    # DO NOT CHANGE THIS!
    raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        # Remove punctuation and normalize whitespace
        for punc in string.punctuation:
            text = text.replace(punc, ' ')
        text = ' '.join(text.lower().split())  # Normalize spaces
        phrase = ' '.join(self.phrase.split())  # Normalize phrase spaces

        # Check if the phrase is in the text as whole words
        return f' {phrase} ' in f' {text} '

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
   def evaluate(self, story):
      return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):  # Fixed class name
   def evaluate(self, story):
      return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time_str):
      self.time = datetime.strptime(time_str, "%d %b %Y %H:%M:%S")
      self.time = pytz.timezone("EST").localize(self.time)
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        if pubdate.tzinfo is None:
          pubdate = pytz.timezone("EST").localize(pubdate)
        return pubdate < self.time

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        if pubdate.tzinfo is None:
            pubdate = pytz.timezone("EST").localize(pubdate)
        return pubdate > self.time



# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
  def __init__(self, other_trigger):
    self.other = other_trigger
  
  def evaluate(self, story):
    return not self.other.evaluate(story)


# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
      self.trigger1 = trigger1
      self.trigger2 = trigger2

    def evaluate(self, story):
       return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
      self.trigger1 = trigger1
      self.trigger2 = trigger2

    def evaluate(self, story):
       return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    filtered = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered.append(story)
                break  
    return filtered



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    triggers = {}
    trigger_list = []

    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if not line or line.startswith('#'):  # Skip empty lines and comments
            continue

        parts = line.split(',')
        if parts[0] == "ADD":
            # Ensure all trigger names in the ADD line exist in the triggers dictionary
            for name in parts[1:]:
                if name in triggers:
                    trigger_list.append(triggers[name])
                else:
                    print(f"Warning: Trigger '{name}' not defined.")
        else:
            # Ensure the line has enough parts to define a trigger
            if len(parts) < 3:
                print(f"Warning: Invalid trigger definition: {line}")
                continue

            trigger_name = parts[0]
            trigger_type = parts[1]

            try:
                if trigger_type == "TITLE":
                    triggers[trigger_name] = TitleTrigger(parts[2])
                elif trigger_type == "DESCRIPTION":
                    triggers[trigger_name] = DescriptionTrigger(parts[2])
                elif trigger_type == "AFTER":
                    triggers[trigger_name] = AfterTrigger(parts[2])
                elif trigger_type == "BEFORE":
                    triggers[trigger_name] = BeforeTrigger(parts[2])
                elif trigger_type == "AND":
                    triggers[trigger_name] = AndTrigger(triggers[parts[2]], triggers[parts[3]])
                elif trigger_type == "OR":
                    triggers[trigger_name] = OrTrigger(triggers[parts[2]], triggers[parts[3]])
                else:
                    print(f"Warning: Unknown trigger type '{trigger_type}' in line: {line}")
            except IndexError:
                print(f"Warning: Missing arguments for trigger in line: {line}")
            except KeyError as e:
                print(f"Warning: Undefined trigger used in AND/OR: {e}")
    return trigger_list
    


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guide() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guide())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

