# UI-Server Integration Guide (Settings-Based Authentication)

## Overview
The springs-of-mud-ui client integrates with the springs-of-mud-server using a settings-based authentication flow. Users authenticate through the Connection Settings dialog, which securely handles passwords and saves connection profiles.

## Authentication Flow

### 1. Configure Connection in Settings
Users open **Settings → Connections** to configure their connection.

**Connection Settings Fields:**
- **Connection Name** - A friendly name for this connection profile
- **Authentication Server URL** - REST API endpoint (e.g., `http://localhost:8169`)
- **Account Name** - Username for authentication
- **Password** - Password (masked input, stored obfuscated)
- **Telnet Host** - MUD server hostname (e.g., `localhost`)
- **Telnet Port** - MUD server port (e.g., `6969`)

**Actions:**
- **New** - Clear fields to create a new connection
- **Save** - Save connection profile to local storage
- **Connect** - Authenticate with the REST API

### 2. Authenticate via REST API
When user clicks "Connect":

1. UI sends POST to `{Authentication Server URL}/api/auth/login`
2. Payload: `{"accountName": "...", "password": "..."}`
3. REST API validates credentials
4. REST API returns:
   - Account ID
   - Player information (firstName, lastName, etc.)
   - List of player characters

5. UI stores auth data and telnet connection info
6. UI displays: "Authenticated as [Name]"
7. Settings dialog closes automatically

### 3. List Characters
After authentication, users can view their characters.

**Command:**
```
list
```

**Output:**
```
Available characters:
- Gandalf (Level 50 Human Wizard)
- Aragorn (Level 45 Human Warrior)
```

### 4. Logon to Telnet Server
User selects a character to play.

**Command:**
```
logon Gandalf
```

**What happens:**
1. UI validates character exists in authenticated account
2. UI connects to telnet server (host/port from connection settings)
3. UI builds payload:
```json
{
  "accountId": "507f1f77bcf86cd799439011",
  "characterId": "507f191e810c19729de860ea",
  "characterName": "Gandalf"
}
```
4. UI sends: `logon {"accountId":"...","characterId":"...","characterName":"..."}`
5. Server validates account and character IDs
6. If valid, character logs into game

## Server-Side Processing

### Message Flow

1. **Connection Established**
   ```
   Client -> Server: TCP connection
   Server -> Client: Welcome message (ASCII art)
   ```

2. **Authentication Payload**
   ```
   Client -> Server: logon {"accountId":"...","characterId":"...","characterName":"..."}
   Server: Validates account exists in database
   Server: Validates character exists and belongs to account
   Server -> Client: "Authentication successful. Logging in as Gandalf..."
   ```

3. **Enter Game**
   ```
   Server -> Client: [Room Name]
   Server -> Client: Room description
   Server -> Client: Exits: north, south, east, west
   Server -> Client: <50hp 100m 100mv>  (prompt)
   Client: Can now send game commands
   ```

## Connection Profiles

### Saved Connections
Connection profiles are saved to `resources/connections.json`:

```json
[
  {
    "name": "Local Development",
    "server_url": "http://localhost:8169",
    "account_name": "testuser",
    "password": "dGVzdHBhc3M=",
    "telnet_host": "localhost",
    "telnet_port": "6969"
  }
]
```

**Security Notes:**
- Passwords are base64-encoded (obfuscated, not encrypted)
- This provides basic protection from casual viewing
- For production, consider stronger encryption methods
- Connection profiles stored locally on user's machine

### Managing Connections
- **Load** - Click connection name in list to load it
- **Edit** - Load connection, modify fields, click Save
- **Delete** - (Future feature)

## User Workflow

### First Time Setup
1. Launch springs-of-mud-ui
2. Click **Settings → Connections**
3. Fill in connection details:
   - Name: "My Server"
   - Auth Server: http://localhost:8169
   - Account: myusername
   - Password: mypassword
   - Telnet Host: localhost
   - Telnet Port: 6969
4. Click **Save** (saves for future use)
5. Click **Connect** (authenticates)

### Subsequent Sessions
1. Launch springs-of-mud-ui
2. Click **Settings → Connections**
3. Click saved connection name in list
4. Click **Connect**
5. Type `list` to see characters
6. Type `logon CharacterName`
7. Play!

## UI Commands

```
help          - Show available commands
list          - Show your characters (after authentication)
logon <name>  - Log character onto telnet server
quit          - Exit the application

[any other]   - Sent to telnet server (if connected)
```

## Security Considerations

### Password Handling
- **Never shown in UI** - Password field uses `mask_char="*"`
- **Toggle visibility** - "Show Password" button for verification
- **No command-line exposure** - No `auth` command that would show password
- **Local storage only** - Saved connections stored on user's machine

### Validation Chain
1. **REST API** validates username/password
2. **Telnet Server** validates account ID and character ID
3. **Database** is source of truth for both

Even if someone forges a payload, the telnet server independently verifies the IDs exist and match.

## Error Handling

### Connection Settings Errors
- **Missing fields** - "Please enter account name and password"
- **Authentication failed** - Shows error dialog with exception message
- **Network error** - Shows connection failed message

### Logon Errors
```
> list
Please authenticate first via Settings -> Connections

> logon InvalidChar
Character 'InvalidChar' not found. Use 'list' to see available characters.
```

### Server Validation Errors
```
Server: Account validation failed.
Server: Character validation failed.
```

## Configuration

### UI Configuration
- Connection profiles: `resources/connections.json`
- Default telnet port: 6969
- Default REST API: http://localhost:8169

### Server Configuration
From `resources/server.yml`:
```yaml
mudserver:
  host: 0.0.0.0
  port: 6969
  services:
    players:
      endpoints:
        players_endpoint: http://localhost:8169/api/player/players
```

## Advantages of Settings-Based Auth

✓ **Secure** - No password exposure in command line or logs
✓ **Convenient** - Save multiple connection profiles
✓ **User-Friendly** - GUI form with validation
✓ **Professional** - Matches modern application patterns
✓ **Flexible** - Easy to switch between servers/accounts

## Example Session

```
[Launch springs-of-mud-ui]

Welcome to Springs of MUD Client!
Type 'help' and press Enter.
Connected. Type 'help' and press Enter.
...

[User opens Settings -> Connections]
[Fills in connection details]
[Clicks Connect]

Authenticated as John Doe
Telnet server: localhost:6969
Loaded 2 character(s)
Type 'list' to see your characters, then 'logon <name>' to play

> list

Available characters:
- Mage (Level 10 Elf Mage)
- Warrior (Level 5 Human Warrior)

> logon Mage
Connecting to localhost:6969 as Mage...
Authentication successful. Logging in as Mage...
[Town Square]
A bustling market square filled with merchants and travelers.
Exits: north, south, east, west
<100hp 50m 100mv>

> look
[Town Square]
A bustling market square filled with merchants and travelers.
Exits: north, south, east, west
<100hp 50m 100mv>
```

## Troubleshooting

### Can't authenticate
- Check REST API is running on configured port
- Verify account name and password are correct
- Check network connectivity

### Can't connect to telnet
- Check MudServer is running on configured port
- Verify telnet host/port in connection settings
- Check firewall settings

### Characters not showing
- Verify authentication was successful
- Check REST API returned character list
- Look for errors in connection status message

---

Generated: 2026-02-19
