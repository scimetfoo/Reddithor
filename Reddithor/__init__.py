#!/usr/bin/env python

import os
import requests
import platform
import subprocess

if(os.environ.get('TRAVIS')!='true'):
    import pygtk

    pygtk.require('2.0')
    import gtk

    import webbrowser

    try:
        import appindicator
    except ImportError:
        import appindicator_replacement as appindicator

    from appindicator_replacement import get_icon_filename
    
import json
import argparse
from os.path import expanduser
import signal
import datetime

from reddithor_fetch import ReddithorFetch
from version import Version
from custom_dialog import EntryDialog

class Reddithor:
    reddit_url = "https://reddit.com/"
    UPDATE_URL = "https://github.com/Murtaza0xFF/Reddithor#upgrade"
    ABOUT_URL = "https://github.com/Murtaza0xFF/Reddithor"
    filename = 'reddithor'
    def __init__(self, args):
        self.args = args
        home = expanduser("~")
        with open(home + '/.'+self.filename+'.json', 'a+') as content_file:
            content_file.seek(0)
            content = content_file.read()
            try:
                self.db = dict(json.loads(content))
            except ValueError:
                self.db = dict()


        # create an indicator applet
        self.ind = appindicator.Indicator("Reddithor", "Reddithor", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon(get_icon_filename("snoo.png"))

        # create a menu
        self.menu = gtk.Menu()

        #The default state is false, and it toggles when you click on it
        self.commentState = args.comments

        # create items for the menu - refresh, quit and a separator
        menuSeparator = gtk.SeparatorMenuItem()
        menuSeparator.show()
        self.menu.append(menuSeparator)

        btnComments = gtk.CheckMenuItem("Show Comments")
        btnComments.show()
        btnComments.set_active(args.comments)
        btnComments.connect("activate", self.toggleComments)
        self.menu.append(btnComments)

        btnAbout = gtk.MenuItem("About")
        btnAbout.show()
        btnAbout.connect("activate", self.showAbout)
        self.menu.append(btnAbout)

        btnRefresh = gtk.MenuItem("Refresh")
        btnRefresh.show()
        #the last parameter is for not running the timer
        btnRefresh.connect("activate", self.refresh, True)
        self.menu.append(btnRefresh)

        btnComments = gtk.MenuItem("Choose subreddit")
        btnComments.show()
        btnComments.connect("activate", self.showDialog)
        self.menu.append(btnComments)

        if Version.new_available():
            btnUpdate = gtk.MenuItem("New Update Available")
            btnUpdate.show()
            btnUpdate.connect('activate',self.showUpdate)
            self.menu.append(btnUpdate)

        btnQuit = gtk.MenuItem("Quit")
        btnQuit.show()
        btnQuit.connect("activate", self.quit)
        self.menu.append(btnQuit)

        self.menu.show()

        self.ind.set_menu(self.menu)
        self.refresh()

    def toggleComments(self, widget):
        """Whether comments page is opened or not"""
        self.commentState = not self.commentState

    def showUpdate(self,widget):
        """Handle the update button"""
        webbrowser.open(Reddithor.UPDATE_URL)
        # Remove the update button once clicked
        self.menu.remove(widget)


    def showAbout(self, widget):
        """Handle the about btn"""
        webbrowser.open(Reddithor.ABOUT_URL)

    def showDialog(self, widget):
        dialog = EntryDialog(None, 
            gtk.DIALOG_MODAL, gtk.MESSAGE_OTHER, 
            gtk.BUTTONS_OK_CANCEL, "Enter a subreddit (Ex: science/new )")
        sub = dialog.run()
        dialog.destroy()
        if sub != None:
            self.db['subreddit'] = sub
            self.refresh()

    def quit(self, widget, data=None):
        """ Handler for the quit button"""
        l = self.db
        home = expanduser("~")

        with open(home + '/.'+self.filename+'.json', 'w+') as file:
            file.write(json.dumps(l))

        gtk.main_quit()

    def run(self):
        signal.signal(signal.SIGINT, self.quit)
        gtk.main()
        return 0

    def open(self, widget, event=None, data=None):
        """Opens the link in the web browser"""
        #We disconnect and reconnect the event in case we have
        #to set it to active and we don't want the signal to be processed
        if not widget.get_active():
            widget.disconnect(widget.signal_id)
            widget.set_active(True)
            widget.signal_id = widget.connect('activate', self.open)
        if 'widget' in self.db:
            self.db['widget'].append(widget.item_id)
        else:
            self.db['widget'] = [widget.item_id]
        webbrowser.open(widget.url)

        if self.commentState:
            if not widget.is_self:
                webbrowser.open(self.reddit_url + widget.post_id)

    def addItem(self, item):
        """Adds an item to the menu"""
        #This is in the case of YC Job Postings, which we skip
        if item['data']['score'] == 0 or item['data']['score'] is None:
            return

        i = gtk.CheckMenuItem(
            "(" + str(item['data']['score']).zfill(3) + "/" + 
            str(item['data']['num_comments']).zfill(3) + ")    " + item['data']['title'])
        if 'widget' in self.db:
            visited =  item['data']['id'] in self.db['widget']
            i.set_active(visited)
        url = item['data']['url']
        #i.reddituploads.com urls in json have &amp;. Need to get rid of them.
        url = url.replace("amp;", '')
        i.url = url
        tooltip = "{url}\nPosted by {user} {timeago}".format(url=url, 
            user=item['data']['author'], timeago= datetime.datetime.fromtimestamp(item['data']['created_utc'])
            .strftime('%Y-%m-%d %H:%M:%S'))
        i.set_tooltip_text(tooltip)
        i.signal_id = i.connect('activate', self.open)
        i.post_id = item['data']['id']
        i.is_self = item['data']['is_self']
        i.item_id = item['data']['id']
        self.menu.prepend(i)
        i.show()

    def refresh(self, widget=None, no_timer=False):

        """Refreshes the menu """
        try:
            if 'subreddit' in self.db:
                subreddit = self.db['subreddit']
            else:
                subreddit = None
            # Create an array of 20 false to denote matches in History
            searchResults = [False]*20
            data = list(reversed(ReddithorFetch.getHomePage(subreddit)[0:20]))
            urls = [item['data']['url'] for item in data]
           
            #Remove all the current stories
            for i in self.menu.get_children():
                if hasattr(i, 'url'):
                    self.menu.remove(i)

            #Add back all the refreshed news
            for index, item in enumerate(data):
                # item['history'] = searchResults[index]
                self.addItem(item)
        # Catch network errors
        except requests.exceptions.RequestException as e:
            print ("[+] There was an error in fetching news items " + str(e))
        finally:
            # Call every 2 minutes
            if not no_timer:
                gtk.timeout_add(2*60*1000, self.refresh, widget, no_timer)

    # Merges two boolean arrays, using OR operation against each pair
    def mergeBoolArray(self, original, patch):
        for index, var in enumerate(original):
            original[index] = original[index] or patch[index]
        return original

def main():
    parser = argparse.ArgumentParser(description='Reddithor in your System Tray')
    parser.add_argument('-v','--version', action='version', version=Version.current())
    parser.add_argument('-c','--comments', dest='comments',action='store_true', help="Open the reddit comments as well as the link of the post")
    parser.set_defaults(comments=True)
    args = parser.parse_args()
    indicator = Reddithor(args)
    indicator.run()

if __name__ == "__main__":
    main()