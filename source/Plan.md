# Login page
* User can't select 'create user' - this has to be done by another user [admin]
* User types username and password
* If correct: User is redirected to main mage
* If not: User is given a message describing what went wrong

# First login
* User is presented with a screen consisting of the following:
** A [menu bar] to the left
** A [user settings] window on the main screen

## Menu bar
* The menu bar has the user's name on top
* A [user settings] icon is displayed next to the name
*

## User settings
### Organization
* On top, the user can select between organizations
* Next to that, there is a list of which roles the user has within the current organization
### Production
* Below, the user can select between productions within the organization
* Next to that, there is a list of which roles the user has in the current production
### Personal
* At the bottom, the user can change the following:
  * Display name
  * E-mail address: Private, this organization, this production
  * Phone numbers: Private, this organization, this production
  * Password

# Not first login
* Organization and production is set to the last used
* The [user settings] settings can be accessed via the [user settings] icon on the menubar

# Menu bar
* The menubar could (based on settings) collapse, either automatically, or on click
* The menu bar has the user's name on top
* A [user settings] icon is displayed next to the name
* Below the user's name the user can select mode, based on the user's roles: [edit, review, show]
* There is also a [settings] button, which opens a [settings] panel
* Below this, there is a [revert/save/export] area, with buttons that is displayed dynamically
* There is also a [sync] area, with advanced options for syncing
* At the bottom, there is a navigation area, which could be populated

## revert/save/export area
* The user can export the manuscript as a pdf, sheet music, and different reports
## Sync area
* The user can turn on or off sending the location in the manuscript to server
* The user can turn on/off/auto follow location from server
** If auto, the follow turns off when the user navigates manually
* The user can choose who to follow.
** This can be an individual, a role, a group, etc

# Main window
* At the center, the main window receives keypresses by default
* Usually, the main window displays the manuscript, but it can be other things, such as pdfs

# Settings
## Styling
* The user can select between different styles for the main interface
* The user can select between different styles for the manuscript
