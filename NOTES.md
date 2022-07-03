
Because of the way you've separated `Ticket` from `TicketFile`, the
subticket relationships are all known to `TicketFile`.  Maybe that
won't turn out to be a problem.  But note that the subtickets of a
ticket are `TicketFiles`, not `Tickets`.

What's actually important to have in the CLI utilities?

* `new-ticket1` - no
* `todo` - yes
* `update-last-modified` - no
* `find` - I originaly wrote "no, use grep" but
   actually I think this is going to be important
* `show` - no


