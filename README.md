# A Conference Organization Application

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
2. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
3. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
4. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
5. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
6. (Optional) Generate your client library(ies) with [the endpoints tool][6].
7. Deploy your application.
8. Go to API explorer site on local by typing "_ah/api/explorer" to end of local url (do the same on deployed site)
9. Execute the different api methods in the API explorer (do the same on deployed site)

[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:8080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool

## Conference
A Conference object holds information about a conference event. This includes:
* name			: this is required
* description
* organizerUserId	: this is used to identify the user that created this conference
* topics
* city
* startDate
* month
* endDate
* maxAttendees		: the maximum number of seats that can be occupied at this conference
* seatsAvailable	: the number of seats that are left for this conference

### Creating a conference
A conference can be created using the <b>createConference</b> API method. The user passes all the data pertaining to a conference
which is parsed and put into the datastore as a Conference entity.

### Getting created conferences
A user can get all the conferences they've created by using the <b>getConferencesCreated</b> endpoint method.

### Registering/Unregistering a conference
A user can register for a conference using the <b>registerForConference</b> API method. The user provides the conference's web key
and the API method takes care of adding this conference to a list of conferences the user will be attending in the future.

In the same way a user can unregister from a conference using the <b>unregisterFromConference</b> API method. The method removes this
conference from the list of conferences the user will be attending.

### Getting conferences to attend
A user can see which conferences they have registered for by using the <b>getConferencesToAttend</b> API method. The method gets the user's profile and gets the list of sessions the user is registered for.

## Session
A Conference can have session(s). Each session object holds information about a conference session. This includes:
* name			: this is required
* highlights
* speaker
* duration
* typeOfSession
* date
* startTime

### Creating a session
A session can be created by passing the above mentioned data and a conference web key to the <b>createSession</b> API method. The method uses the conference web key to get the conference entity. It checks whether the user is the creator of the conference. It not, then the method returns an error (only conference creators can add sessions to it).

A session key is created and set as the new session's key. All the data is parsed and formatted correctly (date, time, etc.). Finally, a Session entity is created and put into the datastore.

### Getting conference sessions
A user can get all the sessions associated with a conference by passing the conference web key to the <b>getConferencesCreated</b> API method. The method gets the conference via the web key and uses an ancestor query on Sessions to get the conference's sessions.

### Getting conference sessions by type
A user can get a conference's sessions by type by passing the conference web key and session type to the <b>getConferenceSessionsByType</b> API method. The method gets the conference's sessions using an ancestor query on Sessions. Then it filters those sessions by the session type passed to the method.

### Getting sessions by speaker
A user can get sessions that have a certain speaker by passing the speaker name to the <b>getSessionsBySpeaker</b> API method. The method uses a filter query on Sessions to get all sessions with the given speaker.

### Adding a session to wishlist
A user can add a session to a list of sessions they wish to attend by passing a session key to the <b>addSessionToWishlist</b> API method. The method simply gets the user's profile and the session using the session key. It then adds the session (if it exists) to the profile's list of sessions.

### Removing a session from wishlist
A user can remove a session from the list of sessions they wish to attend by passing the session's key to the <b>deleteSessionInWishlist</b> API method. The method gets the user's profile and the session using the session key. It then removes the session (if it exists) from the profile's list of sessions.

### Get featured speaker
When a conference session is created the featured speaker is updated for that conference. This is done by using a task to store the new speaker in cache if the speaker has more sessions than the current featured speaker. The user can use the <b>getFeaturedSpeaker</b> API method to retrieve the featured speaker from cache.

### Session data modeling
These are the property types for each data value in a Session entity
* name			: StringProperty
* highlights		: StringProperty
* speaker		: StringProperty
* duration		: TimeProperty, used to store time values
* typeOfSession		: StringProperty
* date			: DateProperty, used to store date values
* startTime		: TimeProperty, used to store time values

## Additional Queries
Two additional queries have been added to the application.

	1. getOldSessions(): returns sessions that take place before 12/01/05
	2. getNewSessions(): returns sessions that take place after 01/01/10

Another query has been implemented to return non-Workshop sessions that take place before before 7P. Google App Engine currently does not allow multiple inequality operators on different properties for a single query. To overcome this error I implemented two separate queries. 

The first returns sessions that are not of type 'Workshop'.
The second returns sessions that take place before 7P.
I then return the intersection of both queries.
