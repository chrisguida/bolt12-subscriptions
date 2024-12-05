# PromptPay - Get your electric bill directly in your Lightning wallet

## Recurring payments over Lightning using bolt12

### Flow

- User signs up for recurring payments on merchant’s website
- Merchant displays a QR which provides a pubkey with which they commit to sending future invoice requests a url or blinded path to send the user’s bolt12-withdraw offer to
- The user’s wallet stores this pubkey and associates it with this particular subscription
  - This prevents the user from receiving spurious requests from imposters
- When the bill is almost due, the merchant sends the user a bolt12 invoice over the Lightning network.
- The user’s node holds onto the invoice until the user is ready to pay.
- The user’s wallet has a tab that displays pending bills and their amounts and due dates.
- The user’s wallet sends the user periodic notifications as the due date nears.
- The user can choose to pay or ignore requests at any time.
- If the payment is ignored, the invoice disappears from the user’s wallet.
- The invoice is saved on the user’s node until the expiry date in case the user mistakenly ignored it (maybe the user can request another invoice?)
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
  - Sends request to plugin’s generatesubscription RPC
- **Rest endpoints**:
  - Generate subscription QR (button) (displays QR when button is pressed)

#### Zeus (or any CLN client app)
**Client app:**
- Subscriptions/bills tab
- Scan subscription QR
- Ask user to confirm subscription
- If they accept, call subscribe plugin RPC

### Use Cases

- Your food doesn’t go bad when electricity company turns off your electricity service for lack of payment
- Your servers and nodes don’t go down and you can still work and use YouTube and Netflix when you forget to pay your internet bill
- You can save money by not paying invoices for subscriptions you no longer need, rather than having them be paid automatically without notice.
