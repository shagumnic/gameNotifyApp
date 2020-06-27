# shagumSite
A website that notify you when there is discount for a game on Steam or when a game has been released. 
The idea is simple: 
- User create an account on the website then proceed to create a list to add games onto it. A list could be public to everybody else if the user wish to
- When adding for a new game, user could choose to get a list of upcoming games based on their release date (are they released next week, next month, next 6 months or next year), their genres (action, rpg, adventure, ...), and how many results should be display per page: 5, 10, 20, or 30 (the site use Jquery, Waypoint plugin, and Django's pagination features to implement infinite scrolling, which means you don't have to click manually to go on the next page but could just scroll down and it will load). On the other hand, user could instead just search for the name of the game itself and add the right result that pops up.
- He/she will be prompted to ask if he/she wants the website to notify when the game is released or when the game is on discount or both before the game is added to the the current list he/she is on. A user could have multiple lists with multiple games.
- User could choose to be notified only when a game has reached at least the minimum discount rate that they set out.
- User could update their choice by clicking onto a game in a specific list. They could change the choice of notification (switch to notify for discount or notify for both released and discounted, change the desire discount percentage, v.v...)
- The site will use web-push notification instead of sending emails because I think users wouldn't want their emails to be filled with a bunch of notifications. 
- User just need to press the subscribe button once on the bottom left corner so that the browser they're using would allow the site to send notification.
- The website will check daily for new discount on the appropriate games and monthly for any change on the release date (if there's any) of the games. When the game has been released or is currently on discount for the right rate, the site will send the notification about that to user daily until the user update their notification choice for that game.
- In addition, the user could update their profile (email, username, profile image) or reset their password if they forgot about it (must use the same email that they use to register to be able to receive email).
- A game, after it has been added, will contain its steamId and header_image received from Steam's API, desciption, genres, tags, metacritic score (if any) from the RWAG's API. Those information will display properly on each game's page after the user has clicked on it.

The website has been deployed to Heroku: https://shagumsite.herokuapp.com/

# Tools that have been used:
- Python, Javascript, HTML, CSS
- Django 3.0.6
- Bootstrap to help style the webpage and make it responsive.
- django-crispy to make the login, register form looks nicer (styling).
- django-webpush to for the web-push notification function.
- New Relic to help ping the website regularly so that it won't idle and reset the dyno due to Heroku free tier limit.
- Celery to help execute the tasks: update the discount rate, update release date, notify for discount and/or released periodically.
- RabbitMQ and CloudAMQP to serve as a broker server in order for Celery to work.
- Python Imaging Library (PIL) to help modified and save the profile image and header image of the game.
- Amazon S3 to help kept the image when deployed the website to Heroku.
- Steam's API and RAWG's API to get the information about the game.
