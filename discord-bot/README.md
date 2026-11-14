# Marketplace Guard

A professional Discord bot in Python (discord.py 2.x) for a marketplace server:
moderation, owner tools, a **verification panel**, a **configurable prefix**,
**`say` as the bot**, and a **marketplace panel** with a heading, banner GIF,
category sections and priced items.

---

## Features

| Area | What you get |
| --- | --- |
| Moderation | ban, unban, kick, timeout, warnings (stored), purge, slowmode, lock/unlock, add/remove role, nickname — usable via a configurable **moderator role** or Discord permissions |
| Verification | One command sets the channel **and** the role; a persistent button grants the role on click |
| Tickets | Panel button opens a private channel, asks **what item** and **how many**, auto-fills the shop price, with staff **Claim** and **Close** buttons, plus a saved **transcript** posted to a staff channel on close |
| Logs | Choose a channel that receives an audit trail of moderation, ticket, shop, verification and bot-message activity |
| Marketplace | Heading + GIF banner + thumbnail + footer, up to 8 category sections, each with its own GIF, description and colour, and items with price, stock and description. Management is limited to a configurable **shop staff role** |
| Owner | reload cogs, list servers, leave a server, sync commands, live stats, shutdown, eval |
| Utility | `say` / `embed` as the bot, help menu, prefix management, user/server info, ping, uptime |
| Storage | Everything is saved in `data/settings.json`, so settings survive restarts |

---

## 1. Create the bot application

1. Open the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application**.
2. Go to **Bot** → **Reset Token** and copy the token (never share it).
3. On the same **Bot** page enable these privileged intents:
   - **Message Content Intent** (required for prefix commands)
   - **Server Members Intent** (required for member lookups)
4. Invite the bot with this link (replace `YOUR_CLIENT_ID`):

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

Administrator is recommended for a marketplace server; without it the bot needs
Manage Roles, Manage Channels, Manage Messages, Moderate Members, Kick, Ban,
Send Messages, Embed Links and Read Message History.

> **Important:** in **Server Settings → Roles**, drag the bot's role **above** your
> verification role, otherwise Discord will not let it hand out the role.

---

## 2. Install and run

Python 3.10+ is required.

```bash
cd discord-bot
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env      # Windows  (macOS/Linux: cp .env.example .env)
```

Open `.env` and paste your token:

```env
DISCORD_TOKEN=your-token-here
DEFAULT_PREFIX=!
```

Start the bot:

```bash
python main.py
```

Logs are printed to the console and saved in `logs/bot.log`.

---

## 3. Quick start

```
!prefix set ?
?help
```

### Verification panel

```
!verification setup #verify @Verified
!verification title ✅ Verify to enter
!verification description Read the rules, then click the button below.\n\nBy verifying you accept the server rules.
!verification button Verify me
!verification image https://media.tenor.com/your-gif.gif
!verification color #57F287
!verification refresh
```

- `setup #channel @role` posts the panel and stores which role it grants.
- Clicking **Verify** gives that role; staff cannot double-verify, bots above the
  verify role are checked automatically.
- `!verification remove` deletes the panel and its settings.

### Marketplace panel

```
!shop role @Shop Staff      # only this role (plus admins) can manage the shop
!shop channel #marketplace
!shop heading 🛒 Abhishek's Marketplace
!shop description Nitro, boosts and more.\nOpen a ticket to order.
!shop banner https://media.tenor.com/your-banner.gif
!shop thumbnail https://i.imgur.com/your-logo.png
!shop footer Prices in USD • Open a ticket to buy
!shop color #5865F2

!shop addsection Nitro | 🚀 | Discord Nitro & Server Boosts | https://media.tenor.com/nitro.gif | #FF6B6B
!shop additem
#   ^ no arguments: the bot asks for section, name, price, stock and description one at a time
!shop additem Nitro | 1 Month Boost | $4.99 | In stock | Instant delivery
!shop additem Nitro | 1 Year Boost | $39.99 | 2 left | Best value
!shop additem Nitro | 14 Boost Pack | $24.99 | In stock

!shop post
```

- The **banner** is rendered above the heading, the heading above every section,
  and each section above its items — exactly like a store page.
- Sections use `name | emoji | description | banner URL | #colour`; everything
  after the name is optional.
- Items use `section | name | price | stock | description`.
- Every change automatically edits the posted panel. If nothing is posted yet,
  run `!shop post`.
- `!shop role @Shop Staff` restricts every shop command to that role. Only members
  with **Manage Server** can change the role; administrators and the server owner
  always keep access. Until a role is chosen, Manage Server holders can manage the shop.
- `!shop list` shows numbered sections/items (you can target them with numbers),
  `!shop preview` shows the panel without publishing it.

### Ticket panel

```
!ticket setup #support @Staff
!ticket category #Tickets
!ticket log #ticket-logs
!ticket title 🎟️ Buy something
!ticket description Click below to open a private ticket.\nTell us what you want and how many.
!ticket image https://media.tenor.com/your-banner.gif
!ticket button Open a ticket
```

- `ticket setup #channel [@staff]` posts the panel in the channel you choose.
- A member clicks **Open a ticket**, then types **what they are buying** and **how many**
  (plus an optional note). The bot creates a private channel only they and staff can see,
  and shows the item, quantity, and the matching shop price if the item exists.
- Staff press **Claim** to take the ticket (the button shows who claimed it) and
  **Close** to delete the channel after a 5-second notice. The opener can also close.
- `ticket category #Tickets` chooses where ticket channels are created (optional).
- When a ticket closes, the full conversation is saved to
  `data/transcripts/<guild id>/ticket-NNNN-<time>.txt` and uploaded to the channel
  set with `ticket log #channel` (falling back to the bot log channel).

### Bot logs

```
!logs channel #bot-logs
!logs test
```

- `logs channel #channel` picks where the bot records what it does (Manage Server).
- Recorded: bans, kicks, timeouts, warnings, purges, slowmode, lock/unlock, role and
  nickname changes, tickets opened/claimed/closed, shop edits and panel posts,
  verification panel changes, and messages sent with `say` / `embed`.
- `logs disable` turns logging off, `logs status` shows the current channel.

---

## Command reference

Default prefix is `!` — change it per server with `!prefix set <new>`.

### Configuration
| Command | Description |
| --- | --- |
| `prefix` | Show the current prefix |
| `prefix set <new>` | Change the prefix (Manage Server) |
| `prefix reset` | Back to the default prefix |
| `modrole <@role\|none>` | Staff role that can use every moderation command (Manage Server) |
| `help [command]` | Interactive command guide |

### Announcements
| Command | Description |
| --- | --- |
| `say [#channel] <text>` | Send a message as the bot (attachments are forwarded) |
| `embed [#channel] <title> \| <description>` | Send a rich embed as the bot |

### Moderation
Members need either the permission listed here **or** the role set with `!modrole @Moderator`; administrators and the server owner always pass.

| Command | Description |
| --- | --- |
| `ban <user> [reason]` | Ban a user (works for users who already left) |
| `unban <user id> [reason]` | Unban a user |
| `kick <member> [reason]` | Kick a member |
| `timeout <member> <duration> [reason]` | Timeout, e.g. `10m`, `1h30m`, `2d` (max 28d) |
| `untimeout <member> [reason]` | Remove a timeout |
| `warn <member> [reason]` | Add a stored warning and DM the member |
| `warnings [member]` | Show warning history |
| `delwarn <member> <id>` | Delete one warning |
| `clearwarns <member>` | Delete all warnings |
| `purge <amount\|all> [target]` | Delete messages, or `all` to clear the channel. Target can be `bots`, `humans`, or `@member` |
| `slowmode <duration\|off>` | Set channel slowmode |
| `lock [channel]` / `unlock [channel]` | Stop/allow members sending messages |
| `addrole <member> <role>` | Give a role |
| `removerole <member> <role>` | Take a role |
| `nick <member> [nickname]` | Change or reset a nickname |

### Verification
| Command | Description |
| --- | --- |
| `verification setup <#channel> <@role> [title]` | Post the panel and bind the role |
| `verification title <text>` | Panel title |
| `verification description <text>` | Panel text (`\n` for new lines) |
| `verification button <label>` | Button text |
| `verification image <url\|none>` | Banner GIF/image |
| `verification color <#hex>` | Embed colour |
| `verification refresh` | Re-render the panel |
| `verification remove` | Delete the panel |
| `verification status` | Show settings |

`verify` and `v` work as aliases of `verification`.

### Marketplace
| Command | Description |
| --- | --- |
| `shop role <@role\|none>` | Staff role that can manage the shop (Manage Server to set) |
| `shop channel <#channel>` | Where the panel is posted |
| `shop heading <title>` | Big title |
| `shop description <text>` | Text under the title (`\n` for new lines) |
| `shop banner <url\|none>` | GIF/picture at the very top |
| `shop thumbnail <url\|none>` | Small logo |
| `shop footer <text>` | Footer line |
| `shop color <#hex>` | Default colour |
| `shop addsection <name> \| [emoji] \| [description] \| [banner] \| [#color]` | Add a category |
| `shop renamesection <section> \| <name>` | Rename |
| `shop sectiondesc <section> \| <text>` | What type of items the section holds |
| `shop sectionbanner <section> \| <url\|none>` | Section GIF |
| `shop sectioncolor <section> \| <#hex>` | Section colour |
| `shop removesection <section>` | Delete a section |
| `shop additem` | Guided setup: asks for each field in turn |
| `shop additem <section> \| <name> \| <price> \| [stock] \| [description]` | Add an item in one line |
| `shop setprice <section> \| <item> \| <price>` | Change a price |
| `shop setstock <section> \| <item> \| <status>` | `In stock`, `Out of stock`, `2 left`… |
| `shop itemdesc <section> \| <item> \| <text>` | Item description |
| `shop itememoji <section> \| <item> \| <emoji>` | Emoji beside an item |
| `shop renameitem <section> \| <item> \| <name>` | Rename an item |
| `shop removeitem <section> \| <item>` | Delete an item |
| `shop list` | Numbered overview of the shop |
| `shop preview` | Preview the panel |
| `shop post [#channel]` | Publish/replace the panel |
| `shop reset` | Delete the panel and all shop content |

`market`, `marketplace` and `store` are aliases of `shop`.

> Comments: quote values that contain `|`? No — `|` is the separator, so avoid it
> inside names/descriptions. Use `\n` for a line break.

### Tickets
| Command | Description |
| --- | --- |
| `ticket setup <#channel> [@staff]` | Post the ticket panel and set the staff role |
| `ticket category <#category\|none>` | Where ticket channels are created |
| `ticket log <#channel\|none>` | Where closed-ticket transcripts are posted |
| `ticket role <@role\|none>` | Role that can see, claim and close tickets |
| `ticket title <text>` | Panel title |
| `ticket description <text>` | Panel text (`\n` for new lines) |
| `ticket image <url\|none>` | Banner GIF/image |
| `ticket thumbnail <url\|none>` | Panel thumbnail |
| `ticket footer <text>` | Panel footer |
| `ticket color <#hex>` | Embed colour |
| `ticket button <label>` | Panel button text |
| `ticket refresh` | Re-render the posted panel |
| `ticket close` | Close the ticket in the current channel |
| `ticket status` | Show ticket settings |

`tickets` and `support` are aliases of `ticket`.

### Logs
| Command | Description |
| --- | --- |
| `logs channel <#channel>` | Set the bot log channel (Manage Server) |
| `logs disable` | Stop sending bot logs |
| `logs test` | Send a test entry to the log channel |
| `logs status` | Show the current log channel |

`log` and `logging` are aliases of `logs`.

### Owner only
| Command | Description |
| --- | --- |
| `reload <cog>` | Reload one cog (`moderation`, `marketplace`…) |
| `reloadall` | Reload every cog |
| `sync` | Sync application commands |
| `servers` | List servers |
| `leave <guild id>` | Leave a server |
| `shutdown` | Stop the bot |
| `eval <code>` | Run Python (owner only, careful) |
| `botstats` | Library/hosting details |

The owner is the Discord account that owns the application.

---

## Project layout

```
discord-bot/
├── main.py                 # entry point, prefix resolver, error handler
├── core/
│   ├── config.py           # paths, colours, env values
│   ├── database.py         # async JSON settings store
│   └── utils.py            # embeds, duration parsing, confirmation view
├── cogs/
│   ├── logs.py             # configurable bot audit log channel
│   ├── utility.py          # help, prefix, say, info
│   ├── moderation.py       # moderation suite
│   ├── verification.py     # persistent verification button
│   ├── marketplace.py      # shop panel builder
│   ├── tickets.py          # ticket panel, private channels, claim/close
│   └── owner.py            # owner tools
└── data/settings.json      # created automatically
```

Back up `data/settings.json` to keep your warnings and shop configuration.
