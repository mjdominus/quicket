
# `TicketRepository`

Probably need a `TicketRepository` object

## Repository meta dir

There can be a top-level directory in the ticket repository
where metainformation is stored, analogous to `.git`.  It can contain
the format of ticket IDs, the current ID number, and,
in the future, the SQLite database.

Putting any of this stuff in a per-user configuration directory was a silly idea.

## Repository layout

Instead of putting a ticket in `<title>.md` and its subtickets in
`<title>.d/<sub-title>.md`, maybe put the ticket in
`<title>/ticket.md` and the subtickets in `<title>/<sub-title>`.  That
is, a ticket is not a markdown file with an associated directory, but
just a directory.

The advantage of the earlier scheme is that it's trivial to make a new ticket: just create the file.

Comporomise: Why not both?  `<title>.md` is a ticket, but if you want
it to have subtickets you have to move it to
`<title>/ticket.md`. Leave it the way it is for now, you can always
change it later.

# Actually important CLI utilities

* `new-ticket1` - no
* `todo` - yes
* `update-last-modified` - no

* `find` - I originally wrote "no, use grep" but actually I think this
   is going to be important.  You'll see a crossreference in the
   Markdown file like "TIC-0123" and want to know what it's talking
   about.  A web interface could insert the title.

* `show` - no

# Upcoming problem with "waiting" status

Your [`README`](README.md) overloads the `waiting` status.  You are using it both
for tickets that have a wakeup time and also for tickets with
unfinished prerequisite tickets.  Will this be a problem?  Maybe.

The [`README`](README.md) says that if a ticket has unfinished prerequisite
tickets, `todo` will update its status to `waiting`.  But it also says
that if a ticket's "wakeup time" is in the past, its status gets
updated to "ready for work".

Actually I think there is no conflict in this particular case. The
rule is:

* If the ticket has prerequisites or a wakeup time, then update its
  status as follows:

  > if all its prerequisites are finished, and  
  >    its waiting time, if it has one, is in the past, then  
  >        update its status to "ready for work"  
  > else,
  >        update its status to "waiting"

This isn't quite right because it could update from "waiting to start"
and it should never do that automatically.  No problem, just forbid
that.   You can imagine a list of allowed transitions; don't let the
status updater do any forbidden transitions.  But on second thought,
maybe this isn't wrong.  Wouldn't it make sense to create a "waiting
to start" ticket with a wakeup date and have it wake up to the "ready
for work" state?

But also, if a ticket is in a "waiting" state, has no prerequisistes
and no wakeup date, that is an error, and the program should warn
about it.

>  Better rename "waiting to start" to something that sounds less like
> "waiting".  It is _not_ an error for "waiting to start" to have
> neither a wakeup date nor prerequisites.  Maybe "not started".

It is also an error for a ticket to be "not started" if it has
subtickets that were started.  Maybe update that automatically.

## Gray, blue, and green statuses

You seem to have reinvented Jira's trichotomy of gray, blue, and green
statuses.  If a ticket has any blue subtickets, it must be blue.
If it has any green subtickets, it must be blue or green.

  * Gray
    * Waiting to start
    * Ready for work
  * Blue
    * In progress
    * Waiting
  * Green
    * Done
    * Will not do

It there a blue "On hold" status which means that work is stopped but
it's not waiting for anything in particular?  I think no, that's how
you get forgotten tickets.  If you've stopped work on it but you're
not waiting for _something_ to happen, that's "Won't do".
