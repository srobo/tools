Purchasing
----------

If you wish to get a product or service ordered then please follow the
procedure outlined on this page. This procedure is designed to maximise the
transparency of purchasing and also to ensure that we have control over our
spending at all times.

1. Request an order/service through trac by creating a ticket with the
   component set to Purchasing. See the Purchasing Tickets section for more
   information.

   a. If the requested purchase does not go over the specified budget line by
      more than 10% then it can continue. Go to step 2.
   b. If the request purchase does go over the specified budget line by more
      than 10% the request is put on hold. A change the budget must be made if
      this purchase is to continue. This involves getting the steering
      committee to vote for the change. See Budget Modifications for further
      details on this.
   c. The new budget has to be accepted by the steering committee. If it is not
      accepted then the requester/treasurers can revise the changes and try
      again. The purchase request will be denied if this stage cannot be
      passed.

2. The treasurers agree the request is valid (by at least two treasurers
   "ACK"ing the ticket).

3. Purchase occurs. Purchasing ticket updated with relevant information.

4. If physical assets are being purchased they are now added to the inventory.

5. Receipts are added to the purchasing ticket.

   a. If the receipts contain any sensitive data (your credit card number, for
      instance), then you may (you probably should, since trac is public)
      encrypt the attachments using the treasurers' PGP key.

6. The inventory is updated once the assets are delivered.

Purchasing Tickets
~~~~~~~~~~~~~~~~~~

When requesting a purchase a trac ticket must be created outlining all of the
details of the request. This ticket must state the following things:

- The items/service to be purchased
- Where the items/service are to be purchased from
- The cost of the items/service
- The associated budget line for the items/service
- A delivery address (This can just be XXXX's house and the actual address can
  be sent privately to treasurer@…)
- If any of these details are missing then the request will be delayed while
  all of the information is collected and recorded on the ticket.

The ticket is also used to track the status of the order: order numbers/parcel
tracking numbers are to be added to the ticket as comments. Any
quotes/invoices/receipts are to be attached to the ticket, they can be
encrypted using the treasurer public key (attached). All data relating to the
order should be attached to the ticket; for example, if PCBs are being ordered
the gerber files should be attached.

Budget Modifications
~~~~~~~~~~~~~~~~~~~~

Sometimes the budget has to be modified. To get a change to the budget through,
the following must happen:

1. Make sure you're familiar with how our Budgeting works.
2. Push a patch against budget.git into gerrit.
3. Wait for a majority of the steering committee to review your patch. If a
   steering committee member is proposing the change, they cannot participate
   in the vote. If this happens it will be merged.
