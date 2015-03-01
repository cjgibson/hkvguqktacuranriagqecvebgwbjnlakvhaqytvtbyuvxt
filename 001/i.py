###
# AUTHORS: CHRISTIAN GIBSON, 
# PROJECT: REDDIT CHALLENGES
# UPDATED: FEBURARY 28, 2015
# USAGE:   
# EXPECTS: python 2.7.6
###

task = """
create a program that will allow you to enter events organizable by hour.
There must be menu options of some form, and you must be able to easily edit,
add, and delete events without directly changing the source code.

(note that by menu i dont necessarily mean gui. as long as you can easily
access the different options and receive prompts and instructions telling
you how to use the program, it will probably be fine)
"""

import collections
import datetime
import dateutil.parser
import codecs
import json

class organizer(collections.defaultdict):
    def __init__(self, storage='schedule.json'):
        self.storage = storage
        self = self.json_load()
    
    def interactive(self):
        print 'Welcome to your Simple Python Organizer.'
        print (("I've found information for %d events "
                + 'spread across %d dates.') 
               % (sum([len(_s) for _s in self.values()]),
                  len(self)))
        action = raw_input('What would you like to do? (view/add/del/edit/quit) ')
        action = action.lower()
        while True:
            if 'v' in action:
                self.view_events()
            elif 'a' in action:
                self.add_event()
            elif action.startswith('d'):
                self.del_event()
            elif action.startswith('e'):
                self.edit_event()
            elif 'q' in action:
                self.json_dump()
                return
            else:
                print "I'm sorry, I didn't understand your input."
            action = raw_input('Anything else? (view/add/del/edit/quit) ')
        
    
    def view_events(self, limit=30):
        _future, _past = self._split_events()
        
        for _time, name in [(_future, 'Future'),
                             (_past, ' Past ')]:
            if len(_time) > 0:
                print '- - - %s Events - - -' % name
                count = 0
                current = None
                for event_tuple in _time:
                    count += 1
                    event_date, event = event_tuple
                    if current != event_date:
                        print event_date
                        current = event_date
                    if event['detail']:
                        print '    %s : %s' % (event['title'],
                                               event['detail'])
                    else:
                        print '    %s' % event['title']
                    if count % limit == 0:
                        _ = raw_input('Press enter for more event listings.')
            else:
                print 'Found no %s Events.' % name
            
    def _split_events(self):
        call = datetime.datetime.now()
        _future = []
        _past = []
        for event_date, event_array in self.items():
            if event_date > call:
                for event in event_array:
                    _future.append((event_date, event))
            else:
                for event in event_array:
                    _past.append((event_date, event))
        _future = sorted(_future, key=lambda x : x[0], reverse=True)
        _part = sorted(_past, key=lambda x : x[0], reverse=True)
        return _future, _past
    
    def handle_date(self):
        initial = raw_input('Please input the date of the event. ')
        try:
            event_date = dateutil.parser.parse(initial)
            response = raw_input('Is this date correct? %s (yes/no) ' 
                                 % (event_date))
            response = response.lower()
            if 'y' in response:
                return event_date
            else:
                event_date = None
        except:
            event_date = None
        print "Let's try and enter the date manually."
        while not event_date:
            year = raw_input('What year does this event take place in? ')
            month = raw_input('And in which month? ')
            day = raw_input('And which day? ')
            hour = raw_input('At what hour does this event start? ')
            for data in [year, month, day, hour]:
                try:
                    data = self._coerce_numeric(data)
                except:
                    data = None
            if all(data):
                try:
                    event_date = datetime.datetime(year=year,
                                                   month=month,
                                                   day=day,
                                                   hour=hour)
                except:
                    print 'The data entered was not valid.'
        return event_date
    
    def handle_event(self):
        event = {'title' : None,
                 'detail' : None}
        event['title'] = raw_input('What is the title of this event? ')
        event['detail'] = raw_input('Is there any other information I should '
                                    + 'record? ')
        return event
    
    def _coerce_numeric(self, data):
        try:
            data = int(data)
        except ValueError:
            try:
                data = data.lower()
                # JANUARY
                if ('jan' in data
                      or 'gen' in data
                      or 'ene' in data):
                    return 1
                # FEBRUARY
                elif ('feb' in data
                      or 'fev' in data
                      or 'f\xc3\x89v' in data):
                    return 2
                # MARCH
                elif ('mar' in data
                      or 'm\xc3\x84r' in data):
                    return 3
                # APRIL
                elif ('apr' in data
                    or 'abr' in data
                    or 'avr' in data):
                    return 4
                # MAY
                elif ('may' in data
                      or 'mai' in data
                      or 'mag' in data):
                    return 5
                # JUNE
                elif ('jun' in data
                      or 'giu' in data):
                    return 6
                # JULY
                elif ('jul' in data
                      or 'lug' in data):
                    return 7
                elif ('aug' in data
                      or 'ago' in data
                      or 'ao\xc3\x9b' in data):
                    return 8
                # OCTOBER
                elif ('oct' in data
                      or 'okt' in data
                      or 'ott' in data
                      or 'out' in data):
                    return 9
                # NOVEMBER
                elif ('nov' in data):
                    return 10
                # SEPTEMBER
                elif('sep' in data
                     or 'set' in data):
                    return 11
                elif ('dec' in data
                      or 'dic' in data
                      or 'dez' in data
                      or 'd\xc3\x89c' in data):
                    return 12
                else:
                    raise AttributeError
            except AttributeError:
                raise TypeError
        return data
    
    def add_event(self):
        event_date = self.handle_date()
        event = self.handle_event()
        self._add_event(event_date, event)
        print 'Event added.'
    
    def _add_event(self, event_date, event):
        self.setdefault(event_date, []).append(event)
    
    def del_event(self):
        event_date = self.handle_date()
        event = self.handle_event()
        self._del_event(event_date, event)
        print 'Event deleted.'
    
    def _del_event(self, event_date, event):
        if event_date in self.storage:
            try:
                self[event_date].remove(event)
            except ValueError:
                pass
    
    def edit_event(self):
        event_date = self.handle_date()
        old_event = None
        while not old_event:
            old_event = raw_input('What was the title of the event '
                                  + ' you want to edit? ')
            try:
                old_event = self._query_event_by_title(event_date, old_event)
            except:
                print "I couldn't locate an event with that title."
                print 'Below is a list of event titles for the provided date.'
                for event in self._query_event_by_date(event_date):
                    print '    %s' % event['title']
                old_event = None
        new_event = self.handle_event()
        self._edit_event(event_date, old_event, new_event)
    
    def _edit_event(self, event_date, old_event, new_event):
        self._del_event(event_date, old_event)
        self._add_event(event_date, new_event)
    
    def _query_event_by_title(self, event_date, event_title):
        poss = [t for t in self[event_date] if t['title'] == event_title]
        if poss:
            return poss[0]
        else:
            raise KeyError
    
    def _query_event_by_date(self, event_date):
        return self[event_date]
    
    def json_load(self):
        with codecs.open(self.storage, 'r', 'utf-8') as fh:
            _self = json.load(fh)
        new_self = collections.defaultdict(datetime.datetime)
        for k, v in _self.items():
            new_self[datetime.datetime.strptime(k, '%Y-%m-%dT%H:%M:%S')] = v
        return new_self
    
    def json_dump(self):
        with codecs.open(self.storage, 'w', 'utf-8') as fh:
            fh.write(json.dumps(self.serialize()))
    
    def json_dump_readable(self, filename):
        with codecs.open(filename, 'w', 'utf-8') as fh:
            fh.write(json.dumps(self.serialize(),
                                sort_keys=True,
                                indent=2,
                                separators=(',', ': ')))
    
    def serialize(self):
        return dict(zip(
            [k.isoformat() for k in self.keys()],
            [v for v in self.values()]))

if __name__ == '__main__':
    o = organizer()
    try:
        o.interactive()
    except KeyboardInterrupt:
        o.json_dump()