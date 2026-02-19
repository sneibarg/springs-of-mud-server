# UI-Server Integration Guide

## Overview
This document describes how the springs-of-mud-ui client integrates with the springs-of-mud-server using the new authentication flow.

## Authentication Flow

### 1. UI Client Authentication (REST API)
The UI client first authenticates with the REST API to get account and character data.

**Command in UI:**
```
auth <accountName> <password>
```

**What happens:**
1. UI sends POST request to `http://localhost:8169/api/auth/login`
2. REST API validates credentials
3. REST API returns account data including:
   - Account ID
   - Player information
   - List of player characters
4. UI stores this data locally

### 2. List Characters
After authentication, users can view their characters.

**Command in UI:**
```
list
```

**Output:**
```
Available characters:
- Gandalf (Level 50 Human Wizard)
- Aragorn (Level 45 Human Warrior)
```

### 3. Telnet Server Logon
When user selects a character, UI connects to telnet server with payload.

**Command in UI:**
```
logon Gandalf
```

**What happens:**
1. UI creates a payload:
```json
{
  "accountId": "507f1f77bcf86cd799439011",
  "characterId": "507f191e810c19729de860ea",
  "characterName": "Gandalf"
}
```

2. UI connects to telnet server (localhost:6969)
3. UI sends: `logon {"accountId":"...","characterId":"...","characterName":"..."}`
4. Server validates the account and character IDs
5. If valid, character logs into the game

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
   Server: Validates account exists
   Server: Validates character exists and belongs to account
   Server -> Client: "Authentication successful. Logging in as Gandalf..."
   ```

3. **Enter Game**
   ```
   Server -> Client: Room description
   Server -> Client: <50hp 100m 100mv>  (prompt)
   Client: Can now send game commands
   ```

### Protocol Details

#### MessageType.CHAR_LOGON
Indicates a payload-based character logon request.

**Payload Structure:**
```json
{
  "accountId": "string",      // MongoDB ObjectId as string
  "characterId": "string",    // MongoDB ObjectId as string
  "characterName": "string"   // For display purposes
}
```

#### Validation Steps
1. Extract `accountId` and `characterId` from payload
2. Query PlayerService for account by ID
3. Query PlayerService for character list for that account
4. Verify character ID exists in the list
5. If all valid, proceed to create Character object and enter game

### Code Path

**Server:**
```
MudServer.handle_client()
  -> ConnectionHandler.handle_new_connection()
  -> TelnetConnection.receive_message()
  -> MessageCodec.decode_text()  (detects "logon {JSON}")
  -> Returns Message(type=CHAR_LOGON, data=payload)
  -> AuthenticationService.authenticate_with_payload()
  -> Validates and creates Character object
  -> Enters game loop
```

**UI:**
```
MudClientUI.handle_command("auth user pass")
  -> AuthClient.login()
  -> Stores auth_data

MudClientUI.handle_command("list")
  -> Displays auth_data.playerCharacterList

MudClientUI.handle_command("logon Gandalf")
  -> Finds character in auth_data
  -> Creates payload JSON
  -> TelnetClient.send_line("logon {JSON}")
  -> Polls for server responses
```

## Security Considerations

### Account/Character Validation
The server **always validates**:
- Account ID exists in database
- Character ID exists in database
- Character belongs to the account

Even though the UI authenticated via REST, the telnet server independently verifies the IDs to prevent:
- Forged payloads
- Character theft
- Account impersonation

### No Password in Payload
The telnet payload does NOT include passwords. Authentication happens via REST API only. The telnet server validates that the account and character IDs are valid in the database.

## Legacy Support

The server still supports the old authentication flow:

1. Server prompts for account name
2. Server prompts for password
3. Server validates credentials
4. Server shows character list
5. User types character name
6. Character logs in

This is automatically detected when the first message is NOT a CHAR_LOGON type.

## Example Session

### Full UI Flow
```
> auth testuser testpass
Authenticating as testuser...
Authentication successful! Welcome John!
Loaded 2 character(s)

> list
Available characters:
- Mage (Level 10 Elf Mage)
- Warrior (Level 5 Human Warrior)

> logon Mage
Connecting to server and logging in as Mage...
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

## Error Handling

### Invalid Payload
```
> logon InvalidChar
Character 'InvalidChar' not found. Use 'list' to see available characters.
```

### Account Not Found (Server)
```
Server -> Client: "Account validation failed."
Connection closed
```

### Character Not Found (Server)
```
Server -> Client: "Character validation failed."
Connection closed
```

### Not Authenticated
```
> list
Please authenticate first with: auth <accountName> <password>
```

## Configuration

### UI Configuration
- REST API endpoint: `http://localhost:8169` (AuthClient)
- Telnet server: `localhost:6969` (TelnetClient)

### Server Configuration
Configuration from `resources/server.yml`:
```yaml
mudserver:
  host: 0.0.0.0
  port: 6969
  services:
    players:
      endpoints:
        players_endpoint: http://localhost:8169/api/player/players
        # ...
```

## Message Types Reference

### UI -> Server
- `CHAR_LOGON` - Payload-based character logon
- `COMMAND` - Regular game command
- `INPUT` - Empty input (prompt only)

### Server -> UI
- `AUTH_SUCCESS` - Authentication succeeded
- `AUTH_FAILURE` - Authentication failed
- `ROOM_DESCRIPTION` - Room information
- `PROMPT` - Game prompt (hp/mana/mv)
- `SYSTEM` - System message
- `ERROR` - Error message

## Troubleshooting

### UI can't connect to REST API
- Check REST API is running on port 8169
- Verify `AuthClient` base_url is correct
- Check credentials are valid

### UI can't connect to telnet
- Check MudServer is running on port 6969
- Verify `TelnetClient` host/port configuration
- Check firewall settings

### Authentication fails on server
- Check account ID exists in database
- Check character ID exists in database
- Verify character belongs to account
- Check server logs for validation errors

### No messages received from server
- Verify `_poll_telnet_messages()` is being called
- Check `TelnetClient.poll_line()` returns data
- Verify server is sending CRLF-terminated lines
- Check for exceptions in polling loop

---

Generated: 2026-02-19
