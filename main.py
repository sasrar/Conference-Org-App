#!/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

"""

__author__ = 'sasrar6@gmail.com (Sadaf Asrar)'

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from conference import ConferenceApi

class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )

class DetermineFeaturedSpeakerHandler(webapp2.RequestHandler):
    def post(self):
        """Determine featured speaker."""
        ConferenceApi._cacheFeaturedSpeaker(
            self.request.get('speaker'),
            self.request.get('websafeConferenceKey'))

app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/determine_featured_speaker', DetermineFeaturedSpeakerHandler),
], debug=True)
