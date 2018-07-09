from collections import defaultdict
from datetime import datetime, timedelta

import fire
import requests
import tomd

from dateutil.parser import parse
from ics import Calendar, Event
from lxml import html
from word2number import w2n


class GenerateEvents(object):
    def run(self, start=None, out="event.ics"):
        self.out_file = out
        if start == None:
            self.start_date = datetime.today()
        else:
            self.start_date = parse(start)
        self._get_data()
        self._generate_ics()

    def _get_data(self):
        self.data = None
        url = 'https://magoosh.com/gre/2017/how-to-study-gre-one-month/'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            tree = html.fromstring(r.content)
            entry = tree.cssselect('article.category-study-guides-and-plans section.entry')[0]

            data = defaultdict(list)
            week = 0
            for t in entry.cssselect('*'):
                if t.tag == 'h3' and t.text_content().startswith("Week ") and ", Day" in t.text_content():
                    week += 1
                    data[week].append(t)
                if t.tag == 'p':
                    data[week].append(t)

            data = dict(data)
            if 0 in data:
                del data[0]
            self.data = data
        else:
            print("Couldn't fetch data")

    def _generate_ics(self):
        data = self.data
        if data != None:
            c = Calendar()
            days = list(data.keys())
            days.sort()

            for xday in days:
                day_data = data[xday]
                title = day_data[0].text_content()
                week, day = title.split(", ")
                week = w2n.word_to_num(week.lstrip("Week "))
                day = w2n.word_to_num(day.lstrip("Day "))
                offset = (week - 1) * 7 + (day)
                event_day = self.start_date + timedelta(days=offset)
                event_day = event_day.replace(hour=0, minute=0, second=0, microsecond=0)
                description = "".join([str(html.tostring(el)) for el in day_data])
                description = tomd.convert(description)
                e = Event(name="Magoosh {}".format(title), begin=event_day, end=event_day, description=description)
                e.make_all_day()
                c.events.add(e)

            with open(self.out_file, 'w') as f:
                f.writelines(c)
            print("File written to {}".format(self.out_file))


if __name__ == '__main__':
    fire.Fire(GenerateEvents)
