# PromptPay - Get your electric bill directly in your Lightning wallet

## Recurring payments over Lightning using bolt12

### Flow

- User signs up for recurring payments on merchant’s website.
- Merchant displays a QR code that provides a pubkey with which they commit to sending future invoice requests via a URL or blinded path to submit the user’s BOLT12-withdraw offer.
- The user’s wallet stores this pubkey and associates it with this particular subscription.
  - This prevents the user from receiving spurious requests from imposters.
- When the bill is almost due, the merchant sends the user a bolt12 invoice over the Lightning network.
- The user’s node holds onto the invoice until the user is ready to pay.
- The user’s wallet has a tab that displays pending bills and their amounts and due dates.
- The user’s wallet sends the user periodic notifications as the due date nears.
- The user can choose to pay or ignore requests at any time.
- If the payment is ignored, the invoice disappears from the user’s wallet.
- The invoice is saved on the user’s node until the expiry date in case the user mistakenly ignored it (maybe the user can request another invoice?).
- If the user chooses to send payment, he just hits “confirm” on the invoice and the payment executes.

### Backend - CLN plugin

#### RPC methods:
**Merchant side:**
- **subscriptiongenerate**: Generate new merchant subscription QR (an offer?)
- **subscriptionaccept**: Associate client offer with merchant offer
- **subscriptioninvoice**: Send invoice

**Client side:**
- **subscribe**: Generate client offer to send to merchant
- client app calls this - Send generated client offer to merchant
- **subcriptionpayinvoice**: Pay invoice (can probably handle this by catching the invoice payment itself)
  - Delete invoice from our DB, mark subscription as paid

#### Hooks:
**Client side:**

**onion_message_recv**
- Happens when merchant calls sendinvoice rpc on their side
  - Plugin stores invoice in DB

### Frontend
#### Merchant website
- Button to generate subscription QR
  - Sends request to plugin’s subscriptiongenerate RPC
- **Rest endpoints**:
  - Generate subscription QR (button) (displays QR when button is pressed)

#### Zeus (or any CLN client app)
**Client app:**
- Subscriptions/bills tab
- Scan subscription QR
- Ask user to confirm subscription
- If they accept, call subscribe plugin RPC

### Use Cases

- Your food doesn’t go bad when electricity company turns off your electricity service for lack of payment.
- Your servers and nodes don’t go down and you can still work and use YouTube and Netflix when you forget to pay your internet bill.
- You can save money by not paying invoices for subscriptions you no longer need, rather than having them be paid automatically without notice.
- Your service provider overcharges you and neither the service provider or your bank will give a refund, with Promptpay you'll be able to catch any overcharges before actually paying the invoice.
- Better managing of your finances by knowing in advance how much you’re spending on subscriptions, rather than reviewing your transaction history retroactively.

### Possible future directions

- Instead of sending the invoice directly when payment is due, the merchant could send a reminder or notification. If the client confirms, the merchant creates the invoice. While this adds a step—requiring the client to confirm the invoice again—it streamlines the initial process and gives the client more freedom and control over the transaction.