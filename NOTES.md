
Because of the way you've separated `Ticket` from `TicketFile`, the
subticket relationships are all known to `TicketFile`.  Maybe that
won't turn out to be a problem.  But note that the subtickets of a
ticket are `TicketFiles`, not `Tickets`.

If this starts to bother you, you can have the aubdirectory behavior
overridden or augmented by a header field.

does a TicketFile contain a Ticket, as you have now?  Or is it the
other way around?  I think the latter.  Then ticketfile.load() doesn't
update the ticketfile object, it returns a ticket object that contains
the original ticketfile object.

--------

Probably need a TicketRepository object

--------

What's actually important to have in the CLI utilities?

* `new-ticket1` - no
* `todo` - yes
* `update-last-modified` - no

* `find` - I originally wrote "no, use grep" but actually I think this
   is going to be important.  You'll see a crossreference in the
   Markdown file like "TIC-0123" and want to know what it's talking
   about.  A web interface could insert the title.

* `show` - no
