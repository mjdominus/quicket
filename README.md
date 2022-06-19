Very simple ticketing system

# Underlying principle

> A ticket is a file

The file is written in Markdown.

Don't worry about GUI, about attachements, blah blah blah.
Files can be attached from GDrive and linked from the file.

Files can be organized hierarcically.  The tool will just search all
the directories.  Maybe in the future you can have an `archived`
directory where you throw old tickets you want to ignore.

It would be quite easy to put a web front-end on this.  Probably
someone even has a prepacked GUI markdown editor.  With a web
front-end, it becomes a phone app.

Reminder: You've tried twice to use Jira.  It never lasated long
because Jira is slow and clumsy.

# Metainformation

The file has a metainformation block at the top that includes

  * title
  * ID
  * creation time
  * last activity time
  * current status
  * wakeup time
  * tags

Anything else?  Maybe not.
Freeform stuff should be allowed probably

## IDs

Can be arbitrarily assigned strings or sequence numbers or something.

If you get to the point of displaying the Markdown as HTML, you can
hack the Markdown processor to specially handle link URIs of the form
`quicket:IDNUMBER`.


## Statuses include:

  * Waiting to start
  * Ready to start
  * In progress
  * Waiting
  * Done
  * Will not do

## Hierarchy

Tickets have subtickets. If a ticket is in `file.md`, its subtickets
are in the directory `file.sub`.  Simple.

# Utility programs

## `new-ticket`

Write a new file template.  Includes allocating an ID.

## `to-do`

List tickets that are ready to start, are in progress, or are
"waiting" with "wakeup date" in the past.

## `update-last-modifed`

After making changes to a bunch of tickets, go through and update the
“last activity time” in the changed files.

## `find`

Given an ID, what file contains that ticket?  (Filenames should be
descriptive.)

## `show`

Given an ID (or maybe title match) display a tree of the title and the
subticket titles.

## Others

If you need them, but for example `change-status` is totally superfluous.

Maybe some kind of trivial reporting.  But the way to go on this is a
utility that turns the metainformation into a SQLite file that you can
query.
