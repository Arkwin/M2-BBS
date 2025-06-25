# BBS Integration for MQTT Meshtastic Client

This document describes the BBS (Bulletin Board System) integration that has been added to the MQTT Meshtastic client, featuring an interactive menu system similar to TC² mesh.

## Features

### 1. Interactive Welcome Menu
When someone sends a direct message to your node, they automatically receive a welcome menu:

```
Welcome to the DMV Mesh
[B]ulletin
[M]ail
[U]tils
[F]ortune
```

### 2. Menu Options

#### **B - Bulletin Boards**
Lists available bulletin boards:
```
Available Boards:
[1] GENERAL
[2] ANNOUNCEMENTS
[3] TECH
[4] TEST

Reply with board number to view posts.
```

#### **M - Mail System**
Shows mail options:
```
Mail Options:
[C]ompose new mail
[I]nbox
[S]ent mail
[D]elete mail

Reply with option letter.
```

#### **U - Utilities**
Provides utility functions:
```
Utilities:
[N]ode info
[P]osition
[T]raceroute
[H]elp

Reply with option letter.
```

#### **F - Fortune**
Sends a random fortune from the `fortunes.txt` file.

### 3. BBS Message Processing
The system can process and handle BBS-specific messages with the following formats:

- **BULLETIN**: `BULLETIN|board|sender|subject|content|unique_id`
- **MAIL**: `MAIL|sender_id|sender|recipient_id|subject|content|unique_id`
- **DELETE_BULLETIN**: `DELETE_BULLETIN|bulletin_id`
- **DELETE_MAIL**: `DELETE_MAIL|unique_id`
- **CHANNEL**: `CHANNEL|name|url`

### 4. BBS Message Sending
Functions are available to send BBS messages to other nodes:

- `send_bulletin_to_bbs_nodes()` - Send bulletins to configured BBS nodes
- `send_mail_to_bbs_nodes()` - Send mail messages to BBS nodes
- `send_delete_bulletin_to_bbs_nodes()` - Send bulletin deletion notifications
- `send_delete_mail_to_bbs_nodes()` - Send mail deletion notifications
- `send_channel_to_bbs_nodes()` - Send channel information

### 5. Configuration
BBS settings are stored in `bbs_config.json`:

```json
{
    "bbs_enabled": true,
    "bbs_nodes": [],
    "bbs_boards": ["GENERAL", "ANNOUNCEMENTS", "TECH", "TEST"],
    "auto_response_enabled": true,
    "auto_response_delay": 3.0,
    "sync_interval_minutes": 15
}
```

### 6. GUI Integration
- Added "Test BBS" button to test BBS functionality
- BBS messages are processed before regular messages
- Debug logging for BBS operations

## Usage

### Interactive Menu System
1. **Send a direct message** to any node running this BBS system
2. **Receive welcome menu** automatically after 3 seconds
3. **Reply with menu option** (B, M, U, or F)
4. **Follow sub-menus** as prompted

### Testing BBS Functionality
1. Click the "Test BBS" button to send a test bulletin message
2. If BBS nodes are configured, the message will be sent to those nodes
3. If no BBS nodes are configured, the message will be sent as a broadcast

### Configuring BBS Nodes
Edit the `bbs_config.json` file to add node IDs to the `bbs_nodes` array:

```json
{
    "bbs_nodes": [1234567890, 9876543210]
}
```

### Fortune System
The system uses `fortunes.txt` for the fortune feature. Each fortune should be separated by `%` on its own line:

```
Fortune 1
%
Fortune 2
%
Fortune 3
```

## Message Flow

1. **Incoming Direct Message**: Any direct message triggers the welcome menu
2. **Menu Selection**: Single-letter responses (B, M, U, F) are processed as menu selections
3. **BBS Message Check**: Non-menu messages are checked for BBS format
4. **Regular Processing**: If not a BBS message, it's processed as a normal chat message

## Integration with TC²-BBS Server

This integration adapts the TC²-BBS server functions to work with MQTT instead of direct serial/TCP connections. The core BBS functionality from the server has been preserved while adapting the communication layer to use the existing MQTT infrastructure.

## Future Enhancements

- Database integration for storing bulletins and mail
- User state management for BBS sessions
- Bulletin board browsing interface
- Mail composition and management interface
- Channel directory management
- Extended menu options and sub-menus 