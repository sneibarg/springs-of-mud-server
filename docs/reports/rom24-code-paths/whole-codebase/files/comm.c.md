# src/comm.c

Role: translation_unit. Disposition: **pending**. SHA-256: `194bef63707bfc9cf4544b922382f7c455c6c075c043a8d9ee05aa59faeb21bb`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## main

[Source line 346](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:346); ends at line 430. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/comm.c:338` (declaration_or_dispatch_reference).

Dependencies: `defined`, `malloc_debug`, `gettimeofday`, `strcpy`, `ctime`, `cshow`, `csetmode`, `cecho2file`, `fopen`, `perror`, `exit`, `is_number`, `fprintf`, `atoi`, `boot_db`, `log_string`, `game_loop_mac_msdos`, `init_socket`, `sprintf`, `game_loop_unix`, `close`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.main.if.001` | 351 | `if defined(unix)` |  | pending |
| `comm.main.if.002` | 358 | `if defined(MALLOC_DEBUG)` |  | pending |
| `comm.main.if.003` | 372 | `if defined(macintosh)` |  | pending |
| `comm.main.if.004` | 382 | `if ( ( fpReserve = fopen( NULL_FILE, "r" ) ) == NULL )` |  | pending |
| `comm.main.if.005` | 392 | `if ( argc > 1 )` |  | pending |
| `comm.main.if.006` | 394 | `if ( !is_number( argv[1] ) )` |  | pending |
| `comm.main.if.007` | 399 | `if ( ( port = atoi( argv[1] ) ) <= 1024 )` |  | pending |
| `comm.main.if.008` | 409 | `if defined(macintosh)` |  | pending |
| `comm.main.or.001` | 409 | `\|\| defined(MSDOS)` |  | pending |
| `comm.main.if.009` | 415 | `if defined(unix)` |  | pending |
| `comm.main.return.001` | 429 | `return 0;` |  | pending |

## init_socket

[Source line 435](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:435); ends at line 493. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- main: `src/comm.c:416` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:322` (declaration_or_dispatch_reference).

Dependencies: `socket`, `perror`, `exit`, `setsockopt`, `close`, `defined`, `htons`, `bind`, `listen`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.init_socket.if.001` | 442 | `if ( ( fd = socket( AF_INET, SOCK_STREAM, 0 ) ) < 0 )` |  | pending |
| `comm.init_socket.if.002` | 448 | `if ( setsockopt( fd, SOL_SOCKET, SO_REUSEADDR,     (char *) &x, sizeof(x) ) < 0 )` |  | pending |
| `comm.init_socket.if.003` | 456 | `if defined(SO_DONTLINGER)` |  | pending |
| `comm.init_socket.and.001` | 456 | `&& !defined(SYSV)` |  | pending |
| `comm.init_socket.if.004` | 463 | `if ( setsockopt( fd, SOL_SOCKET, SO_DONTLINGER, 	(char *) &ld, sizeof(ld) ) < 0 )` |  | pending |
| `comm.init_socket.if.005` | 477 | `if ( bind( fd, (struct sockaddr *) &sa, sizeof(sa) ) < 0 )` |  | pending |
| `comm.init_socket.if.006` | 485 | `if ( listen( fd, 3 ) < 0 )` |  | pending |
| `comm.init_socket.return.001` | 492 | `return fd;` |  | pending |

## game_loop_mac_msdos

[Source line 499](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:499); ends at line 653. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- main: `src/comm.c:412` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:315` (declaration_or_dispatch_reference).

Dependencies: `gettimeofday`, `str_dup`, `alloc_mem`, `write_to_buffer`, `defined`, `kbhit`, `read_from_descriptor`, `save_char_obj`, `close_socket`, `read_from_buffer`, `stop_idling`, `substitute_alias`, `nanny`, `update_handler`, `process_output`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.game_loop_mac_msdos.if.001` | 526 | `if ( help_greeting[0] == '.' )` |  | pending |
| `comm.game_loop_mac_msdos.while.001` | 533 | `while ( !merc_down )` |  | pending |
| `comm.game_loop_mac_msdos.for.001` | 540 | `for ( d = descriptor_list; d != NULL; d = d_next )` |  | pending |
| `comm.game_loop_mac_msdos.if.002` | 545 | `if defined(MSDOS)` |  | pending |
| `comm.game_loop_mac_msdos.if.003` | 546 | `if ( kbhit( ) )` |  | pending |
| `comm.game_loop_mac_msdos.if.004` | 549 | `if ( d->character != NULL )` |  | pending |
| `comm.game_loop_mac_msdos.if.005` | 551 | `if ( !read_from_descriptor( d ) )` |  | pending |
| `comm.game_loop_mac_msdos.if.006` | 553 | `if ( d->character != NULL && d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_mac_msdos.and.001` | 553 | `&& d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_mac_msdos.continue.001` | 557 | `continue;` |  | pending |
| `comm.game_loop_mac_msdos.if.007` | 561 | `if (d->character != NULL && d->character->daze > 0)` |  | pending |
| `comm.game_loop_mac_msdos.and.002` | 561 | `&& d->character->daze > 0)` |  | pending |
| `comm.game_loop_mac_msdos.if.008` | 564 | `if ( d->character != NULL && d->character->wait > 0 )` |  | pending |
| `comm.game_loop_mac_msdos.and.003` | 564 | `&& d->character->wait > 0 )` |  | pending |
| `comm.game_loop_mac_msdos.continue.002` | 567 | `continue;` |  | pending |
| `comm.game_loop_mac_msdos.if.009` | 571 | `if ( d->incomm[0] != '\0' )` |  | pending |
| `comm.game_loop_mac_msdos.if.010` | 576 | `if ( d->connected == CON_PLAYING )` |  | pending |
| `comm.game_loop_mac_msdos.for.002` | 597 | `for ( d = descriptor_list; d != NULL; d = d_next )` |  | pending |
| `comm.game_loop_mac_msdos.if.011` | 601 | `if ( ( d->fcommand \|\| d->outtop > 0 ) )` |  | pending |
| `comm.game_loop_mac_msdos.or.001` | 601 | `\|\| d->outtop > 0 ) )` |  | pending |
| `comm.game_loop_mac_msdos.if.012` | 603 | `if ( !process_output( d, TRUE ) )` |  | pending |
| `comm.game_loop_mac_msdos.if.013` | 605 | `if ( d->character != NULL && d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_mac_msdos.and.004` | 605 | `&& d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_mac_msdos.for.003` | 620 | `for ( ; ; )` |  | pending |
| `comm.game_loop_mac_msdos.if.014` | 624 | `if defined(MSDOS)` |  | pending |
| `comm.game_loop_mac_msdos.if.015` | 625 | `if ( kbhit( ) )` |  | pending |
| `comm.game_loop_mac_msdos.if.016` | 628 | `if ( dcon.character != NULL )` |  | pending |
| `comm.game_loop_mac_msdos.if.017` | 630 | `if ( !read_from_descriptor( &dcon ) )` |  | pending |
| `comm.game_loop_mac_msdos.if.018` | 632 | `if ( dcon.character != NULL && d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_mac_msdos.and.005` | 632 | `&& d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_mac_msdos.if.019` | 637 | `if defined(MSDOS)` |  | pending |
| `comm.game_loop_mac_msdos.break.001` | 638 | `break;` |  | pending |
| `comm.game_loop_mac_msdos.if.020` | 645 | `if ( delta >= 1000000 / PULSE_PER_SECOND )` |  | pending |
| `comm.game_loop_mac_msdos.break.002` | 646 | `break;` |  | pending |
| `comm.game_loop_mac_msdos.return.001` | 652 | `return;` |  | pending |

## game_loop_unix

[Source line 659](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:659); ends at line 852. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- main: `src/comm.c:420` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:321` (declaration_or_dispatch_reference).

Dependencies: `signal`, `gettimeofday`, `defined`, `malloc_verify`, `abort`, `FD_ZERO`, `FD_SET`, `UMAX`, `select`, `perror`, `exit`, `FD_ISSET`, `init_descriptor`, `FD_CLR`, `save_char_obj`, `close_socket`, `read_from_descriptor`, `read_from_buffer`, `stop_idling`, `show_string`, `substitute_alias`, `nanny`, `update_handler`, `process_output`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.game_loop_unix.while.001` | 669 | `while ( !merc_down )` |  | pending |
| `comm.game_loop_unix.if.001` | 677 | `if defined(MALLOC_DEBUG)` |  | pending |
| `comm.game_loop_unix.if.002` | 678 | `if ( malloc_verify( ) != 1 )` |  | pending |
| `comm.game_loop_unix.for.001` | 690 | `for ( d = descriptor_list; d; d = d->next )` |  | pending |
| `comm.game_loop_unix.if.003` | 698 | `if ( select( maxdesc+1, &in_set, &out_set, &exc_set, &null_time ) < 0 )` |  | pending |
| `comm.game_loop_unix.if.004` | 707 | `if ( FD_ISSET( control, &in_set ) )` |  | pending |
| `comm.game_loop_unix.for.002` | 713 | `for ( d = descriptor_list; d != NULL; d = d_next )` |  | pending |
| `comm.game_loop_unix.if.005` | 716 | `if ( FD_ISSET( d->descriptor, &exc_set ) )` |  | pending |
| `comm.game_loop_unix.if.006` | 720 | `if ( d->character && d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_unix.and.001` | 720 | `&& d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_unix.for.003` | 730 | `for ( d = descriptor_list; d != NULL; d = d_next )` |  | pending |
| `comm.game_loop_unix.if.007` | 735 | `if ( FD_ISSET( d->descriptor, &in_set ) )` |  | pending |
| `comm.game_loop_unix.if.008` | 737 | `if ( d->character != NULL )` |  | pending |
| `comm.game_loop_unix.if.009` | 739 | `if ( !read_from_descriptor( d ) )` |  | pending |
| `comm.game_loop_unix.if.010` | 742 | `if ( d->character != NULL && d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_unix.and.002` | 742 | `&& d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_unix.continue.001` | 746 | `continue;` |  | pending |
| `comm.game_loop_unix.if.011` | 750 | `if (d->character != NULL && d->character->daze > 0)` |  | pending |
| `comm.game_loop_unix.and.003` | 750 | `&& d->character->daze > 0)` |  | pending |
| `comm.game_loop_unix.if.012` | 753 | `if ( d->character != NULL && d->character->wait > 0 )` |  | pending |
| `comm.game_loop_unix.and.004` | 753 | `&& d->character->wait > 0 )` |  | pending |
| `comm.game_loop_unix.continue.002` | 756 | `continue;` |  | pending |
| `comm.game_loop_unix.if.013` | 760 | `if ( d->incomm[0] != '\0' )` |  | pending |
| `comm.game_loop_unix.if.014` | 765 | `if (d->showstr_point)` |  | pending |
| `comm.game_loop_unix.if.015` | 767 | `if ( d->connected == CON_PLAYING )` |  | pending |
| `comm.game_loop_unix.for.004` | 788 | `for ( d = descriptor_list; d != NULL; d = d_next )` |  | pending |
| `comm.game_loop_unix.if.016` | 792 | `if ( ( d->fcommand \|\| d->outtop > 0 ) 	    &&   FD_ISSET(d->descriptor, &out_set) )` |  | pending |
| `comm.game_loop_unix.or.001` | 792 | `\|\| d->outtop > 0 )` |  | pending |
| `comm.game_loop_unix.and.005` | 793 | `&&   FD_ISSET(d->descriptor, &out_set) )` |  | pending |
| `comm.game_loop_unix.if.017` | 795 | `if ( !process_output( d, TRUE ) )` |  | pending |
| `comm.game_loop_unix.if.018` | 797 | `if ( d->character != NULL && d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_unix.and.006` | 797 | `&& d->connected == CON_PLAYING)` |  | pending |
| `comm.game_loop_unix.while.002` | 821 | `while ( usecDelta < 0 )` |  | pending |
| `comm.game_loop_unix.while.003` | 827 | `while ( usecDelta >= 1000000 )` |  | pending |
| `comm.game_loop_unix.if.019` | 833 | `if ( secDelta > 0 \|\| ( secDelta == 0 && usecDelta > 0 ) )` |  | pending |
| `comm.game_loop_unix.or.002` | 833 | `\|\| ( secDelta == 0 && usecDelta > 0 ) )` |  | pending |
| `comm.game_loop_unix.and.007` | 833 | `&& usecDelta > 0 ) )` |  | pending |
| `comm.game_loop_unix.if.020` | 839 | `if ( select( 0, NULL, NULL, NULL, &stall_time ) < 0 )` |  | pending |
| `comm.game_loop_unix.return.001` | 851 | `return;` |  | pending |

## init_descriptor

[Source line 858](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:858); ends at line 957. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_unix: `src/comm.c:708` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:323` (declaration_or_dispatch_reference).

Dependencies: `getsockname`, `accept`, `perror`, `defined`, `fcntl`, `new_descriptor`, `alloc_mem`, `getpeername`, `str_dup`, `ntohl`, `sprintf`, `log_string`, `gethostbyaddr`, `check_ban`, `write_to_descriptor`, `close`, `free_descriptor`, `write_to_buffer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.init_descriptor.if.001` | 869 | `if ( ( desc = accept( control, (struct sockaddr *) &sock, &size) ) < 0 )` |  | pending |
| `comm.init_descriptor.return.001` | 872 | `return;` |  | pending |
| `comm.init_descriptor.if.002` | 875 | `if !defined(FNDELAY)` |  | pending |
| `comm.init_descriptor.if.003` | 879 | `if ( fcntl( desc, F_SETFL, FNDELAY ) == -1 )` |  | pending |
| `comm.init_descriptor.return.002` | 882 | `return;` |  | pending |
| `comm.init_descriptor.if.004` | 898 | `if ( getpeername( desc, (struct sockaddr *) &sock, &size ) < 0 )` |  | pending |
| `comm.init_descriptor.ternary.001` | 920 | `? from->h_name : buf );` |  | pending |
| `comm.init_descriptor.if.005` | 931 | `if ( check_ban(dnew->host,BAN_ALL))` |  | pending |
| `comm.init_descriptor.return.003` | 937 | `return;` |  | pending |
| `comm.init_descriptor.if.006` | 950 | `if ( help_greeting[0] == '.' )` |  | pending |
| `comm.init_descriptor.return.004` | 956 | `return;` |  | pending |

## close_socket

[Source line 962](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:962); ends at line 1028. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_quit: `src/act_comm.c:1429` (lexical_call_candidate).
- do_quit: `src/act_comm.c:1441` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:564` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:587` (lexical_call_candidate).
- do_reboot: `src/act_wiz.c:2025` (lexical_call_candidate).
- do_shutdown: `src/act_wiz.c:2059` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2611` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:556` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:608` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:635` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:723` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:745` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:800` (lexical_call_candidate).
- write_to_buffer: `src/comm.c:1488` (lexical_call_candidate).
- nanny: `src/comm.c:1564` (lexical_call_candidate).
- nanny: `src/comm.c:1570` (lexical_call_candidate).
- nanny: `src/comm.c:1589` (lexical_call_candidate).
- nanny: `src/comm.c:1596` (lexical_call_candidate).
- nanny: `src/comm.c:1609` (lexical_call_candidate).
- nanny: `src/comm.c:1628` (lexical_call_candidate).
- nanny: `src/comm.c:1636` (lexical_call_candidate).
- nanny: `src/comm.c:1655` (lexical_call_candidate).
- nanny: `src/comm.c:1699` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2104` (declaration_or_dispatch_reference).

Dependencies: `process_output`, `write_to_buffer`, `sprintf`, `log_string`, `act`, `wiznet`, `free_char`, `bug`, `close`, `free_descriptor`, `defined`, `exit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.close_socket.if.001` | 966 | `if ( dclose->outtop > 0 )` |  | pending |
| `comm.close_socket.if.002` | 969 | `if ( dclose->snoop_by != NULL )` |  | pending |
| `comm.close_socket.for.001` | 978 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `comm.close_socket.if.003` | 980 | `if ( d->snoop_by == dclose )` |  | pending |
| `comm.close_socket.if.004` | 985 | `if ( ( ch = dclose->character ) != NULL )` |  | pending |
| `comm.close_socket.if.005` | 990 | `if ( dclose->connected == CON_PLAYING && !merc_down)` |  | pending |
| `comm.close_socket.and.001` | 990 | `&& !merc_down)` |  | pending |
| `comm.close_socket.ternary.001` | 998 | `? dclose->original :` |  | pending |
| `comm.close_socket.if.006` | 1003 | `if ( d_next == dclose )` |  | pending |
| `comm.close_socket.if.007` | 1006 | `if ( dclose == descriptor_list )` |  | pending |
| `comm.close_socket.for.002` | 1014 | `for ( d = descriptor_list; d && d->next != dclose; d = d->next )` |  | pending |
| `comm.close_socket.and.002` | 1014 | `&& d->next != dclose;` |  | pending |
| `comm.close_socket.if.008` | 1016 | `if ( d != NULL )` |  | pending |
| `comm.close_socket.if.009` | 1024 | `if defined(MSDOS)` |  | pending |
| `comm.close_socket.or.001` | 1024 | `\|\| defined(macintosh)` |  | pending |
| `comm.close_socket.return.001` | 1027 | `return;` |  | pending |

## read_from_descriptor

[Source line 1032](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1032); ends at line 1098. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_mac_msdos: `src/comm.c:551` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:630` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:739` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:316` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/comm.c:324` (declaration_or_dispatch_reference).

Dependencies: `strlen`, `sprintf`, `log_string`, `write_to_descriptor`, `defined`, `getc`, `putc`, `read`, `perror`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.read_from_descriptor.if.001` | 1037 | `if ( d->incomm[0] != '\0' )` |  | pending |
| `comm.read_from_descriptor.return.001` | 1038 | `return TRUE;` |  | pending |
| `comm.read_from_descriptor.if.002` | 1042 | `if ( iStart >= sizeof(d->inbuf) - 10 )` |  | pending |
| `comm.read_from_descriptor.return.002` | 1048 | `return FALSE;` |  | pending |
| `comm.read_from_descriptor.if.003` | 1052 | `if defined(macintosh)` |  | pending |
| `comm.read_from_descriptor.for.001` | 1053 | `for ( ; ; )` |  | pending |
| `comm.read_from_descriptor.if.004` | 1057 | `if ( c == '\0' \|\| c == EOF )` |  | pending |
| `comm.read_from_descriptor.or.001` | 1057 | `\|\| c == EOF )` |  | pending |
| `comm.read_from_descriptor.break.001` | 1058 | `break;` |  | pending |
| `comm.read_from_descriptor.if.005` | 1060 | `if ( c == '\r' )` |  | pending |
| `comm.read_from_descriptor.if.006` | 1063 | `if ( iStart > sizeof(d->inbuf) - 10 )` |  | pending |
| `comm.read_from_descriptor.break.002` | 1064 | `break;` |  | pending |
| `comm.read_from_descriptor.if.007` | 1068 | `if defined(MSDOS)` |  | pending |
| `comm.read_from_descriptor.or.002` | 1068 | `\|\| defined(unix)` |  | pending |
| `comm.read_from_descriptor.for.002` | 1069 | `for ( ; ; )` |  | pending |
| `comm.read_from_descriptor.if.008` | 1075 | `if ( nRead > 0 )` |  | pending |
| `comm.read_from_descriptor.if.009` | 1078 | `if ( d->inbuf[iStart-1] == '\n' \|\| d->inbuf[iStart-1] == '\r' )` |  | pending |
| `comm.read_from_descriptor.or.003` | 1078 | `\|\| d->inbuf[iStart-1] == '\r' )` |  | pending |
| `comm.read_from_descriptor.break.003` | 1079 | `break;` |  | pending |
| `comm.read_from_descriptor.if.010` | 1081 | `if ( nRead == 0 )` |  | pending |
| `comm.read_from_descriptor.return.003` | 1084 | `return FALSE;` |  | pending |
| `comm.read_from_descriptor.if.011` | 1086 | `if ( errno == EWOULDBLOCK )` |  | pending |
| `comm.read_from_descriptor.break.004` | 1087 | `break;` |  | pending |
| `comm.read_from_descriptor.return.004` | 1091 | `return FALSE;` |  | pending |
| `comm.read_from_descriptor.return.005` | 1097 | `return TRUE;` |  | pending |

## read_from_buffer

[Source line 1105](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1105); ends at line 1210. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_mac_msdos: `src/comm.c:570` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:759` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:341` (declaration_or_dispatch_reference).

Dependencies: `write_to_descriptor`, `isascii`, `isprint`, `strcmp`, `sprintf`, `log_string`, `wiznet`, `get_trust`, `strcpy`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.read_from_buffer.if.001` | 1112 | `if ( d->incomm[0] != '\0' )` |  | pending |
| `comm.read_from_buffer.return.001` | 1113 | `return;` |  | pending |
| `comm.read_from_buffer.for.001` | 1118 | `for ( i = 0; d->inbuf[i] != '\n' && d->inbuf[i] != '\r'; i++ )` |  | pending |
| `comm.read_from_buffer.and.001` | 1118 | `&& d->inbuf[i] != '\r';` |  | pending |
| `comm.read_from_buffer.if.002` | 1120 | `if ( d->inbuf[i] == '\0' )` |  | pending |
| `comm.read_from_buffer.return.002` | 1121 | `return;` |  | pending |
| `comm.read_from_buffer.for.002` | 1127 | `for ( i = 0, k = 0; d->inbuf[i] != '\n' && d->inbuf[i] != '\r'; i++ )` |  | pending |
| `comm.read_from_buffer.and.002` | 1127 | `&& d->inbuf[i] != '\r';` |  | pending |
| `comm.read_from_buffer.if.003` | 1129 | `if ( k >= MAX_INPUT_LENGTH - 2 )` |  | pending |
| `comm.read_from_buffer.for.003` | 1134 | `for ( ; d->inbuf[i] != '\0'; i++ )` |  | pending |
| `comm.read_from_buffer.if.004` | 1136 | `if ( d->inbuf[i] == '\n' \|\| d->inbuf[i] == '\r' )` |  | pending |
| `comm.read_from_buffer.or.001` | 1136 | `\|\| d->inbuf[i] == '\r' )` |  | pending |
| `comm.read_from_buffer.break.001` | 1137 | `break;` |  | pending |
| `comm.read_from_buffer.break.002` | 1141 | `break;` |  | pending |
| `comm.read_from_buffer.if.005` | 1144 | `if ( d->inbuf[i] == '\b' && k > 0 )` |  | pending |
| `comm.read_from_buffer.and.003` | 1144 | `&& k > 0 )` |  | pending |
| `comm.read_from_buffer.if.006` | 1146 | `if ( isascii(d->inbuf[i]) && isprint(d->inbuf[i]) )` |  | pending |
| `comm.read_from_buffer.and.004` | 1146 | `&& isprint(d->inbuf[i]) )` |  | pending |
| `comm.read_from_buffer.if.007` | 1153 | `if ( k == 0 )` |  | pending |
| `comm.read_from_buffer.if.008` | 1161 | `if ( k > 1 \|\| d->incomm[0] == '!' )` |  | pending |
| `comm.read_from_buffer.or.002` | 1161 | `\|\| d->incomm[0] == '!' )` |  | pending |
| `comm.read_from_buffer.if.009` | 1163 | `if ( d->incomm[0] != '!' && strcmp( d->incomm, d->inlast ) )` |  | pending |
| `comm.read_from_buffer.and.005` | 1163 | `&& strcmp( d->incomm, d->inlast ) )` |  | pending |
| `comm.read_from_buffer.if.010` | 1169 | `if (++d->repeat >= 25 && d->character 	    &&  d->connected == CON_PLAYING)` |  | pending |
| `comm.read_from_buffer.and.006` | 1169 | `&& d->character` |  | pending |
| `comm.read_from_buffer.and.007` | 1170 | `&&  d->connected == CON_PLAYING)` |  | pending |
| `comm.read_from_buffer.if.011` | 1176 | `if (d->incomm[0] == '!')` |  | pending |
| `comm.read_from_buffer.if.012` | 1197 | `if ( d->incomm[0] == '!' )` |  | pending |
| `comm.read_from_buffer.while.001` | 1205 | `while ( d->inbuf[i] == '\n' \|\| d->inbuf[i] == '\r' )` |  | pending |
| `comm.read_from_buffer.or.003` | 1205 | `\|\| d->inbuf[i] == '\r' )` |  | pending |
| `comm.read_from_buffer.for.004` | 1207 | `for ( j = 0; ( d->inbuf[j] = d->inbuf[i+j] ) != '\0'; j++ )` |  | pending |
| `comm.read_from_buffer.return.003` | 1209 | `return;` |  | pending |

## process_output

[Source line 1217](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1217); ends at line 1311. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_mac_msdos: `src/comm.c:603` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:795` (lexical_call_candidate).
- close_socket: `src/comm.c:967` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:340` (declaration_or_dispatch_reference).

Dependencies: `write_to_buffer`, `can_see`, `sprintf`, `IS_NPC`, `UPPER`, `IS_SET`, `bust_a_prompt`, `write_to_descriptor`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.process_output.if.001` | 1224 | `if (!merc_down && d->showstr_point)` |  | pending |
| `comm.process_output.and.001` | 1224 | `&& d->showstr_point)` |  | pending |
| `comm.process_output.if.002` | 1226 | `if (fPrompt && !merc_down && d->connected == CON_PLAYING)` |  | pending |
| `comm.process_output.and.002` | 1226 | `&& !merc_down && d->connected == CON_PLAYING)` |  | pending |
| `comm.process_output.and.003` | 1226 | `&& d->connected == CON_PLAYING)` |  | pending |
| `comm.process_output.if.003` | 1234 | `if ((victim = ch->fighting) != NULL && can_see(ch,victim))` |  | pending |
| `comm.process_output.and.004` | 1234 | `&& can_see(ch,victim))` |  | pending |
| `comm.process_output.if.004` | 1240 | `if (victim->max_hit > 0)` |  | pending |
| `comm.process_output.if.005` | 1245 | `if (percent >= 100)` |  | pending |
| `comm.process_output.if.006` | 1247 | `if (percent >= 90)` |  | pending |
| `comm.process_output.if.007` | 1249 | `if (percent >= 75)` |  | pending |
| `comm.process_output.if.008` | 1251 | `if (percent >= 50)` |  | pending |
| `comm.process_output.if.009` | 1253 | `if (percent >= 30)` |  | pending |
| `comm.process_output.if.010` | 1255 | `if (percent >= 15)` |  | pending |
| `comm.process_output.if.011` | 1257 | `if (percent >= 0)` |  | pending |
| `comm.process_output.ternary.001` | 1263 | `? victim->short_descr : victim->name,wound);` |  | pending |
| `comm.process_output.ternary.002` | 1269 | `? d->original : d->character;` |  | pending |
| `comm.process_output.if.012` | 1270 | `if (!IS_SET(ch->comm, COMM_COMPACT) )` |  | pending |
| `comm.process_output.if.013` | 1274 | `if ( IS_SET(ch->comm, COMM_PROMPT) )` |  | pending |
| `comm.process_output.if.014` | 1277 | `if (IS_SET(ch->comm,COMM_TELNET_GA))` |  | pending |
| `comm.process_output.if.015` | 1284 | `if ( d->outtop == 0 )` |  | pending |
| `comm.process_output.return.001` | 1285 | `return TRUE;` |  | pending |
| `comm.process_output.if.016` | 1290 | `if ( d->snoop_by != NULL )` |  | pending |
| `comm.process_output.if.017` | 1292 | `if (d->character != NULL)` |  | pending |
| `comm.process_output.if.018` | 1301 | `if ( !write_to_descriptor( d->descriptor, d->outbuf, d->outtop ) )` |  | pending |
| `comm.process_output.return.002` | 1304 | `return FALSE;` |  | pending |
| `comm.process_output.return.003` | 1309 | `return TRUE;` |  | pending |

## bust_a_prompt

[Source line 1317](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1317); ends at line 1453. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- process_output: `src/comm.c:1275` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:343` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `send_to_char`, `IS_SET`, `can_see_room`, `IS_AFFECTED`, `strcat`, `IS_NPC`, `exp_per_level`, `IS_GOOD`, `IS_EVIL`, `room_is_dark`, `IS_IMMORTAL`, `write_to_buffer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.bust_a_prompt.if.001` | 1332 | `if (str == NULL \|\| str[0] == '\0')` |  | pending |
| `comm.bust_a_prompt.or.001` | 1332 | `\|\| str[0] == '\0')` |  | pending |
| `comm.bust_a_prompt.return.001` | 1337 | `return;` |  | pending |
| `comm.bust_a_prompt.if.002` | 1340 | `if (IS_SET(ch->comm,COMM_AFK))` |  | pending |
| `comm.bust_a_prompt.return.002` | 1343 | `return;` |  | pending |
| `comm.bust_a_prompt.while.001` | 1346 | `while( *str != '\0' )` |  | pending |
| `comm.bust_a_prompt.if.003` | 1348 | `if( *str != '%' )` |  | pending |
| `comm.bust_a_prompt.continue.001` | 1351 | `continue;` |  | pending |
| `comm.bust_a_prompt.switch.001` | 1354 | `switch( *str )` |  | pending |
| `comm.bust_a_prompt.default.001` | 1356 | `default :` |  | pending |
| `comm.bust_a_prompt.break.001` | 1357 | `break;` |  | pending |
| `comm.bust_a_prompt.case.001` | 1358 | `case 'e':` |  | pending |
| `comm.bust_a_prompt.for.001` | 1361 | `for (door = 0; door < 6; door++)` |  | pending |
| `comm.bust_a_prompt.if.004` | 1363 | `if ((pexit = ch->in_room->exit[door]) != NULL 		&&  pexit ->u1.to_room != NULL 		&&  (can_see_room(ch,pexit->u1.to_room) 		\|\|   (IS_AFFECTED(ch,AFF_INFRARED)  		&&    !IS_AFFECTED(ch,AFF_BLIND))) 		&&  !IS_SET(pexit->exit_info,EX_CLOSED))` |  | pending |
| `comm.bust_a_prompt.and.001` | 1364 | `&&  pexit ->u1.to_room != NULL` |  | pending |
| `comm.bust_a_prompt.and.002` | 1365 | `&&  (can_see_room(ch,pexit->u1.to_room)` |  | pending |
| `comm.bust_a_prompt.or.002` | 1366 | `\|\|   (IS_AFFECTED(ch,AFF_INFRARED)` |  | pending |
| `comm.bust_a_prompt.and.003` | 1367 | `&&    !IS_AFFECTED(ch,AFF_BLIND)))` |  | pending |
| `comm.bust_a_prompt.and.004` | 1368 | `&&  !IS_SET(pexit->exit_info,EX_CLOSED))` |  | pending |
| `comm.bust_a_prompt.if.005` | 1374 | `if (!found)` |  | pending |
| `comm.bust_a_prompt.break.002` | 1377 | `break;` |  | pending |
| `comm.bust_a_prompt.case.002` | 1378 | `case 'c' :` |  | pending |
| `comm.bust_a_prompt.break.003` | 1380 | `break;` |  | pending |
| `comm.bust_a_prompt.case.003` | 1381 | `case 'h' :` |  | pending |
| `comm.bust_a_prompt.break.004` | 1383 | `break;` |  | pending |
| `comm.bust_a_prompt.case.004` | 1384 | `case 'H' :` |  | pending |
| `comm.bust_a_prompt.break.005` | 1386 | `break;` |  | pending |
| `comm.bust_a_prompt.case.005` | 1387 | `case 'm' :` |  | pending |
| `comm.bust_a_prompt.break.006` | 1389 | `break;` |  | pending |
| `comm.bust_a_prompt.case.006` | 1390 | `case 'M' :` |  | pending |
| `comm.bust_a_prompt.break.007` | 1392 | `break;` |  | pending |
| `comm.bust_a_prompt.case.007` | 1393 | `case 'v' :` |  | pending |
| `comm.bust_a_prompt.break.008` | 1395 | `break;` |  | pending |
| `comm.bust_a_prompt.case.008` | 1396 | `case 'V' :` |  | pending |
| `comm.bust_a_prompt.break.009` | 1398 | `break;` |  | pending |
| `comm.bust_a_prompt.case.009` | 1399 | `case 'x' :` |  | pending |
| `comm.bust_a_prompt.break.010` | 1401 | `break;` |  | pending |
| `comm.bust_a_prompt.case.010` | 1402 | `case 'X' :` |  | pending |
| `comm.bust_a_prompt.ternary.001` | 1403 | `? 0 :` |  | pending |
| `comm.bust_a_prompt.break.011` | 1405 | `break;` |  | pending |
| `comm.bust_a_prompt.case.011` | 1406 | `case 'g' :` |  | pending |
| `comm.bust_a_prompt.break.012` | 1408 | `break;` |  | pending |
| `comm.bust_a_prompt.case.012` | 1409 | `case 's' :` |  | pending |
| `comm.bust_a_prompt.break.013` | 1411 | `break;` |  | pending |
| `comm.bust_a_prompt.case.013` | 1412 | `case 'a' :` |  | pending |
| `comm.bust_a_prompt.if.006` | 1413 | `if( ch->level > 9 )` |  | pending |
| `comm.bust_a_prompt.ternary.002` | 1416 | `? "good" : IS_EVIL(ch) ?` |  | pending |
| `comm.bust_a_prompt.ternary.003` | 1416 | `?` |  | pending |
| `comm.bust_a_prompt.break.014` | 1418 | `break;` |  | pending |
| `comm.bust_a_prompt.case.014` | 1419 | `case 'r' :` |  | pending |
| `comm.bust_a_prompt.if.007` | 1420 | `if( ch->in_room != NULL )` |  | pending |
| `comm.bust_a_prompt.and.005` | 1422 | `&& IS_SET(ch->act,PLR_HOLYLIGHT)) \|\|` |  | pending |
| `comm.bust_a_prompt.or.003` | 1422 | `\|\|` |  | pending |
| `comm.bust_a_prompt.and.006` | 1423 | `&& !room_is_dark( ch->in_room )))` |  | pending |
| `comm.bust_a_prompt.ternary.004` | 1424 | `? ch->in_room->name : "darkness");` |  | pending |
| `comm.bust_a_prompt.break.015` | 1427 | `break;` |  | pending |
| `comm.bust_a_prompt.case.015` | 1428 | `case 'R' :` |  | pending |
| `comm.bust_a_prompt.if.008` | 1429 | `if( IS_IMMORTAL( ch ) && ch->in_room != NULL )` |  | pending |
| `comm.bust_a_prompt.and.007` | 1429 | `&& ch->in_room != NULL )` |  | pending |
| `comm.bust_a_prompt.break.016` | 1433 | `break;` |  | pending |
| `comm.bust_a_prompt.case.016` | 1434 | `case 'z' :` |  | pending |
| `comm.bust_a_prompt.if.009` | 1435 | `if( IS_IMMORTAL( ch ) && ch->in_room != NULL )` |  | pending |
| `comm.bust_a_prompt.and.008` | 1435 | `&& ch->in_room != NULL )` |  | pending |
| `comm.bust_a_prompt.break.017` | 1439 | `break;` |  | pending |
| `comm.bust_a_prompt.case.017` | 1440 | `case '%' :` |  | pending |
| `comm.bust_a_prompt.break.018` | 1442 | `break;` |  | pending |
| `comm.bust_a_prompt.while.002` | 1445 | `while( (*point = *i) != '\0' )` |  | pending |
| `comm.bust_a_prompt.if.010` | 1450 | `if (ch->prefix[0] != '\0')` |  | pending |
| `comm.bust_a_prompt.return.003` | 1452 | `return;` |  | pending |

## write_to_buffer

[Source line 1460](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1460); ends at line 1504. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_mac_msdos: `src/comm.c:527` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:529` (lexical_call_candidate).
- init_descriptor: `src/comm.c:951` (lexical_call_candidate).
- init_descriptor: `src/comm.c:953` (lexical_call_candidate).
- close_socket: `src/comm.c:971` (lexical_call_candidate).
- process_output: `src/comm.c:1225` (lexical_call_candidate).
- process_output: `src/comm.c:1265` (lexical_call_candidate).
- process_output: `src/comm.c:1271` (lexical_call_candidate).
- process_output: `src/comm.c:1278` (lexical_call_candidate).
- process_output: `src/comm.c:1293` (lexical_call_candidate).
- process_output: `src/comm.c:1294` (lexical_call_candidate).
- process_output: `src/comm.c:1295` (lexical_call_candidate).
- bust_a_prompt: `src/comm.c:1448` (lexical_call_candidate).
- bust_a_prompt: `src/comm.c:1451` (lexical_call_candidate).
- nanny: `src/comm.c:1577` (lexical_call_candidate).
- nanny: `src/comm.c:1588` (lexical_call_candidate).
- nanny: `src/comm.c:1595` (lexical_call_candidate).
- nanny: `src/comm.c:1608` (lexical_call_candidate).
- nanny: `src/comm.c:1617` (lexical_call_candidate).
- nanny: `src/comm.c:1618` (lexical_call_candidate).
- nanny: `src/comm.c:1627` (lexical_call_candidate).
- nanny: `src/comm.c:1634` (lexical_call_candidate).
- nanny: `src/comm.c:1641` (lexical_call_candidate).
- nanny: `src/comm.c:1649` (lexical_call_candidate).
- nanny: `src/comm.c:1654` (lexical_call_candidate).
- nanny: `src/comm.c:1659` (lexical_call_candidate).
- nanny: `src/comm.c:1703` (lexical_call_candidate).
- nanny: `src/comm.c:1713` (lexical_call_candidate).
- nanny: `src/comm.c:1723` (lexical_call_candidate).
- nanny: `src/comm.c:1734` (lexical_call_candidate).
- nanny: `src/comm.c:1739` (lexical_call_candidate).
- nanny: `src/comm.c:1746` (lexical_call_candidate).
- nanny: `src/comm.c:1753` (lexical_call_candidate).
- nanny: `src/comm.c:1758` (lexical_call_candidate).
- nanny: `src/comm.c:1769` (lexical_call_candidate).
- nanny: `src/comm.c:1778` (lexical_call_candidate).
- nanny: `src/comm.c:1784` (lexical_call_candidate).
- nanny: `src/comm.c:1789` (lexical_call_candidate).
- nanny: `src/comm.c:1795` (lexical_call_candidate).
- nanny: `src/comm.c:1796` (lexical_call_candidate).
- nanny: `src/comm.c:1801` (lexical_call_candidate).
- nanny: `src/comm.c:1802` (lexical_call_candidate).
- nanny: `src/comm.c:1804` (lexical_call_candidate).
- nanny: `src/comm.c:1805` (lexical_call_candidate).
- nanny: `src/comm.c:1819` (lexical_call_candidate).
- nanny: `src/comm.c:1828` (lexical_call_candidate).
- nanny: `src/comm.c:1829` (lexical_call_candidate).
- nanny: `src/comm.c:1834` (lexical_call_candidate).
- nanny: `src/comm.c:1835` (lexical_call_candidate).
- nanny: `src/comm.c:1837` (lexical_call_candidate).
- nanny: `src/comm.c:1838` (lexical_call_candidate).
- nanny: `src/comm.c:1865` (lexical_call_candidate).
- nanny: `src/comm.c:1880` (lexical_call_candidate).
- nanny: `src/comm.c:1892` (lexical_call_candidate).
- nanny: `src/comm.c:1901` (lexical_call_candidate).
- nanny: `src/comm.c:1913` (lexical_call_candidate).
- nanny: `src/comm.c:1914` (lexical_call_candidate).
- nanny: `src/comm.c:1915` (lexical_call_candidate).
- nanny: `src/comm.c:1926` (lexical_call_candidate).
- nanny: `src/comm.c:1927` (lexical_call_candidate).
- nanny: `src/comm.c:1931` (lexical_call_candidate).
- nanny: `src/comm.c:1936` (lexical_call_candidate).
- nanny: `src/comm.c:1937` (lexical_call_candidate).
- nanny: `src/comm.c:1938` (lexical_call_candidate).
- nanny: `src/comm.c:1943` (lexical_call_candidate).
- nanny: `src/comm.c:1951` (lexical_call_candidate).
- nanny: `src/comm.c:1958` (lexical_call_candidate).
- nanny: `src/comm.c:1959` (lexical_call_candidate).
- nanny: `src/comm.c:1969` (lexical_call_candidate).
- nanny: `src/comm.c:1973` (lexical_call_candidate).
- nanny: `src/comm.c:1979` (lexical_call_candidate).
- nanny: `src/comm.c:1983` (lexical_call_candidate).
- nanny: `src/comm.c:1993` (lexical_call_candidate).
- nanny: `src/comm.c:1998` (lexical_call_candidate).
- nanny: `src/comm.c:2032` (lexical_call_candidate).
- nanny: `src/comm.c:2033` (lexical_call_candidate).
- nanny: `src/comm.c:2043` (lexical_call_candidate).
- nanny: `src/comm.c:2057` (lexical_call_candidate).
- nanny: `src/comm.c:2065` (lexical_call_candidate).
- nanny: `src/comm.c:2066` (lexical_call_candidate).
- nanny: `src/comm.c:2067` (lexical_call_candidate).
- nanny: `src/comm.c:2071` (lexical_call_candidate).
- check_playing: `src/comm.c:2303` (lexical_call_candidate).
- check_playing: `src/comm.c:2304` (lexical_call_candidate).
- send_to_char: `src/comm.c:2340` (lexical_call_candidate).
- show_string: `src/comm.c:2404` (lexical_call_candidate).
- act_new: `src/comm.c:2555` (lexical_call_candidate).
- interpret: `src/interp.c:449` (lexical_call_candidate).
- interpret: `src/interp.c:450` (lexical_call_candidate).
- interpret: `src/interp.c:451` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2105` (declaration_or_dispatch_reference).

Dependencies: `strlen`, `bug`, `close_socket`, `alloc_mem`, `strncpy`, `free_mem`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.write_to_buffer.if.001` | 1465 | `if ( length <= 0 )` |  | pending |
| `comm.write_to_buffer.if.002` | 1471 | `if ( d->outtop == 0 && !d->fcommand )` |  | pending |
| `comm.write_to_buffer.and.001` | 1471 | `&& !d->fcommand )` |  | pending |
| `comm.write_to_buffer.while.001` | 1481 | `while ( d->outtop + length >= d->outsize )` |  | pending |
| `comm.write_to_buffer.if.003` | 1485 | `if (d->outsize >= 32000)` |  | pending |
| `comm.write_to_buffer.return.001` | 1489 | `return;` |  | pending |
| `comm.write_to_buffer.return.002` | 1503 | `return;` |  | pending |

## write_to_descriptor

[Source line 1514](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1514); ends at line 1536. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- init_descriptor: `src/comm.c:933` (lexical_call_candidate).
- read_from_descriptor: `src/comm.c:1046` (lexical_call_candidate).
- read_from_buffer: `src/comm.c:1131` (lexical_call_candidate).
- process_output: `src/comm.c:1301` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:317` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/comm.c:325` (declaration_or_dispatch_reference).

Dependencies: `defined`, `strlen`, `UMIN`, `write`, `perror`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.write_to_descriptor.if.001` | 1520 | `if defined(macintosh)` |  | pending |
| `comm.write_to_descriptor.or.001` | 1520 | `\|\| defined(MSDOS)` |  | pending |
| `comm.write_to_descriptor.if.002` | 1521 | `if ( desc == 0 )` |  | pending |
| `comm.write_to_descriptor.if.003` | 1525 | `if ( length <= 0 )` |  | pending |
| `comm.write_to_descriptor.for.001` | 1528 | `for ( iStart = 0; iStart < length; iStart += nWrite )` |  | pending |
| `comm.write_to_descriptor.if.004` | 1531 | `if ( ( nWrite = write( desc, txt + iStart, nBlock ) ) < 0 )` |  | pending |
| `comm.write_to_descriptor.return.001` | 1532 | `return FALSE;` |  | pending |
| `comm.write_to_descriptor.return.002` | 1535 | `return TRUE;` |  | pending |

## nanny

[Source line 1543](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1543); ends at line 2134. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_mac_msdos: `src/comm.c:579` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:770` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:339` (declaration_or_dispatch_reference).

Dependencies: `isspace`, `bug`, `close_socket`, `UPPER`, `check_parse_name`, `write_to_buffer`, `load_char_obj`, `IS_SET`, `sprintf`, `log_string`, `check_ban`, `check_reconnect`, `IS_IMMORTAL`, `defined`, `strcmp`, `crypt`, `check_playing`, `wiznet`, `get_trust`, `do_function`, `str_cmp`, `free_char`, `strlen`, `free_string`, `str_dup`, `one_argument`, `race_lookup`, `group_add`, `strcpy`, `strcat`, `class_lookup`, `new_gen_data`, `list_group_costs`, `weapon_lookup`, `send_to_char`, `exp_per_level`, `free_gen_data`, `parse_gen_groups`, `reset_char`, `set_title`, `obj_to_char`, `create_object`, `get_obj_index`, `char_to_room`, `get_room_index`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.nanny.while.001` | 1554 | `while ( isspace(*argument) )` |  | pending |
| `comm.nanny.switch.001` | 1559 | `switch ( d->connected )` |  | pending |
| `comm.nanny.default.001` | 1562 | `default:` |  | pending |
| `comm.nanny.return.001` | 1565 | `return;` |  | pending |
| `comm.nanny.case.001` | 1567 | `case CON_GET_NAME:` |  | pending |
| `comm.nanny.if.001` | 1568 | `if ( argument[0] == '\0' )` |  | pending |
| `comm.nanny.return.002` | 1571 | `return;` |  | pending |
| `comm.nanny.if.002` | 1575 | `if ( !check_parse_name( argument ) )` |  | pending |
| `comm.nanny.return.003` | 1578 | `return;` |  | pending |
| `comm.nanny.if.003` | 1584 | `if (IS_SET(ch->act, PLR_DENY))` |  | pending |
| `comm.nanny.return.004` | 1590 | `return;` |  | pending |
| `comm.nanny.if.004` | 1593 | `if (check_ban(d->host,BAN_PERMIT) && !IS_SET(ch->act,PLR_PERMIT))` |  | pending |
| `comm.nanny.and.001` | 1593 | `&& !IS_SET(ch->act,PLR_PERMIT))` |  | pending |
| `comm.nanny.return.005` | 1597 | `return;` |  | pending |
| `comm.nanny.if.005` | 1600 | `if ( check_reconnect( d, argument, FALSE ) )` |  | pending |
| `comm.nanny.if.006` | 1606 | `if ( wizlock && !IS_IMMORTAL(ch))` |  | pending |
| `comm.nanny.and.002` | 1606 | `&& !IS_IMMORTAL(ch))` |  | pending |
| `comm.nanny.return.006` | 1610 | `return;` |  | pending |
| `comm.nanny.if.007` | 1614 | `if ( fOld )` |  | pending |
| `comm.nanny.return.007` | 1620 | `return;` |  | pending |
| `comm.nanny.if.008` | 1625 | `if (newlock)` |  | pending |
| `comm.nanny.return.008` | 1629 | `return;` |  | pending |
| `comm.nanny.if.009` | 1632 | `if (check_ban(d->host,BAN_NEWBIES))` |  | pending |
| `comm.nanny.return.009` | 1637 | `return;` |  | pending |
| `comm.nanny.return.010` | 1643 | `return;` |  | pending |
| `comm.nanny.break.001` | 1645 | `break;` |  | pending |
| `comm.nanny.case.002` | 1647 | `case CON_GET_OLD_PASSWORD:` |  | pending |
| `comm.nanny.if.010` | 1648 | `if defined(unix)` |  | pending |
| `comm.nanny.if.011` | 1652 | `if ( strcmp( crypt( argument, ch->pcdata->pwd ), ch->pcdata->pwd ))` |  | pending |
| `comm.nanny.return.011` | 1656 | `return;` |  | pending |
| `comm.nanny.if.012` | 1661 | `if (check_playing(d,ch->name))` |  | pending |
| `comm.nanny.return.012` | 1662 | `return;` |  | pending |
| `comm.nanny.if.013` | 1664 | `if ( check_reconnect( d, ch->name, TRUE ) )` |  | pending |
| `comm.nanny.return.013` | 1665 | `return;` |  | pending |
| `comm.nanny.if.014` | 1671 | `if ( IS_IMMORTAL(ch) )` |  | pending |
| `comm.nanny.break.002` | 1681 | `break;` |  | pending |
| `comm.nanny.case.003` | 1685 | `case CON_BREAK_CONNECT:` |  | pending |
| `comm.nanny.switch.002` | 1686 | `switch( *argument )` |  | pending |
| `comm.nanny.case.004` | 1688 | `case 'y' : case 'Y':` |  | pending |
| `comm.nanny.case.005` | 1688 | `case 'Y':` |  | pending |
| `comm.nanny.for.001` | 1689 | `for ( d_old = descriptor_list; d_old != NULL; d_old = d_next )` |  | pending |
| `comm.nanny.if.015` | 1692 | `if (d_old == d \|\| d_old->character == NULL)` |  | pending |
| `comm.nanny.or.001` | 1692 | `\|\| d_old->character == NULL)` |  | pending |
| `comm.nanny.continue.001` | 1693 | `continue;` |  | pending |
| `comm.nanny.if.016` | 1695 | `if (str_cmp(ch->name,d_old->original ? 		    d_old->original->name : d_old->character->name))` |  | pending |
| `comm.nanny.ternary.001` | 1695 | `?` |  | pending |
| `comm.nanny.continue.002` | 1697 | `continue;` |  | pending |
| `comm.nanny.if.017` | 1701 | `if (check_reconnect(d,ch->name,TRUE))` |  | pending |
| `comm.nanny.return.014` | 1702 | `return;` |  | pending |
| `comm.nanny.if.018` | 1704 | `if ( d->character != NULL )` |  | pending |
| `comm.nanny.break.003` | 1710 | `break;` |  | pending |
| `comm.nanny.case.006` | 1712 | `case 'n' : case 'N':` |  | pending |
| `comm.nanny.case.007` | 1712 | `case 'N':` |  | pending |
| `comm.nanny.if.019` | 1714 | `if ( d->character != NULL )` |  | pending |
| `comm.nanny.break.004` | 1720 | `break;` |  | pending |
| `comm.nanny.default.002` | 1722 | `default:` |  | pending |
| `comm.nanny.break.005` | 1724 | `break;` |  | pending |
| `comm.nanny.break.006` | 1726 | `break;` |  | pending |
| `comm.nanny.case.008` | 1728 | `case CON_CONFIRM_NEW_NAME:` |  | pending |
| `comm.nanny.switch.003` | 1729 | `switch ( *argument )` |  | pending |
| `comm.nanny.case.009` | 1731 | `case 'y': case 'Y':` |  | pending |
| `comm.nanny.case.010` | 1731 | `case 'Y':` |  | pending |
| `comm.nanny.break.007` | 1736 | `break;` |  | pending |
| `comm.nanny.case.011` | 1738 | `case 'n': case 'N':` |  | pending |
| `comm.nanny.case.012` | 1738 | `case 'N':` |  | pending |
| `comm.nanny.break.008` | 1743 | `break;` |  | pending |
| `comm.nanny.default.003` | 1745 | `default:` |  | pending |
| `comm.nanny.break.009` | 1747 | `break;` |  | pending |
| `comm.nanny.break.010` | 1749 | `break;` |  | pending |
| `comm.nanny.case.013` | 1751 | `case CON_GET_NEW_PASSWORD:` |  | pending |
| `comm.nanny.if.020` | 1752 | `if defined(unix)` |  | pending |
| `comm.nanny.if.021` | 1756 | `if ( strlen(argument) < 5 )` |  | pending |
| `comm.nanny.return.015` | 1761 | `return;` |  | pending |
| `comm.nanny.for.002` | 1765 | `for ( p = pwdnew; *p != '\0'; p++ )` |  | pending |
| `comm.nanny.if.022` | 1767 | `if ( *p == '~' )` |  | pending |
| `comm.nanny.return.016` | 1772 | `return;` |  | pending |
| `comm.nanny.break.011` | 1780 | `break;` |  | pending |
| `comm.nanny.case.014` | 1782 | `case CON_CONFIRM_NEW_PASSWORD:` |  | pending |
| `comm.nanny.if.023` | 1783 | `if defined(unix)` |  | pending |
| `comm.nanny.if.024` | 1787 | `if ( strcmp( crypt( argument, ch->pcdata->pwd ), ch->pcdata->pwd ) )` |  | pending |
| `comm.nanny.return.017` | 1792 | `return;` |  | pending |
| `comm.nanny.for.003` | 1797 | `for ( race = 1; race_table[race].name != NULL; race++ )` |  | pending |
| `comm.nanny.if.025` | 1799 | `if (!race_table[race].pc_race)` |  | pending |
| `comm.nanny.break.012` | 1800 | `break;` |  | pending |
| `comm.nanny.break.013` | 1807 | `break;` |  | pending |
| `comm.nanny.case.015` | 1809 | `case CON_GET_NEW_RACE:` |  | pending |
| `comm.nanny.if.026` | 1812 | `if (!strcmp(arg,"help"))` |  | pending |
| `comm.nanny.if.027` | 1815 | `if (argument[0] == '\0')` |  | pending |
| `comm.nanny.break.014` | 1821 | `break;` |  | pending |
| `comm.nanny.if.028` | 1826 | `if (race == 0 \|\| !race_table[race].pc_race)` |  | pending |
| `comm.nanny.or.002` | 1826 | `\|\| !race_table[race].pc_race)` |  | pending |
| `comm.nanny.for.004` | 1830 | `for ( race = 1; race_table[race].name != NULL; race++ )` |  | pending |
| `comm.nanny.if.029` | 1832 | `if (!race_table[race].pc_race)` |  | pending |
| `comm.nanny.break.015` | 1833 | `break;` |  | pending |
| `comm.nanny.break.016` | 1840 | `break;` |  | pending |
| `comm.nanny.for.005` | 1845 | `for (i = 0; i < MAX_STATS; i++)` |  | pending |
| `comm.nanny.for.006` | 1855 | `for (i = 0; i < 5; i++)` |  | pending |
| `comm.nanny.if.030` | 1857 | `if (pc_race_table[race].skills[i] == NULL)` |  | pending |
| `comm.nanny.break.017` | 1858 | `break;` |  | pending |
| `comm.nanny.break.018` | 1867 | `break;` |  | pending |
| `comm.nanny.case.016` | 1870 | `case CON_GET_NEW_SEX:` |  | pending |
| `comm.nanny.switch.004` | 1871 | `switch ( argument[0] )` |  | pending |
| `comm.nanny.case.017` | 1873 | `case 'm': case 'M': ch->sex = SEX_MALE;` |  | pending |
| `comm.nanny.case.018` | 1873 | `case 'M': ch->sex = SEX_MALE;` |  | pending |
| `comm.nanny.break.019` | 1875 | `break;` |  | pending |
| `comm.nanny.case.019` | 1876 | `case 'f': case 'F': ch->sex = SEX_FEMALE;` |  | pending |
| `comm.nanny.case.020` | 1876 | `case 'F': ch->sex = SEX_FEMALE;` |  | pending |
| `comm.nanny.break.020` | 1878 | `break;` |  | pending |
| `comm.nanny.default.004` | 1879 | `default:` |  | pending |
| `comm.nanny.return.018` | 1881 | `return;` |  | pending |
| `comm.nanny.for.007` | 1885 | `for ( iClass = 0; iClass < MAX_CLASS; iClass++ )` |  | pending |
| `comm.nanny.if.031` | 1887 | `if ( iClass > 0 )` |  | pending |
| `comm.nanny.break.021` | 1894 | `break;` |  | pending |
| `comm.nanny.case.021` | 1896 | `case CON_GET_NEW_CLASS:` |  | pending |
| `comm.nanny.if.032` | 1899 | `if ( iClass == -1 )` |  | pending |
| `comm.nanny.return.019` | 1903 | `return;` |  | pending |
| `comm.nanny.break.022` | 1917 | `break;` |  | pending |
| `comm.nanny.case.022` | 1919 | `case CON_GET_ALIGNMENT:` |  | pending |
| `comm.nanny.switch.005` | 1920 | `switch( argument[0])` |  | pending |
| `comm.nanny.case.023` | 1922 | `case 'g' : case 'G' : ch->alignment = 750;` |  | pending |
| `comm.nanny.case.024` | 1922 | `case 'G' : ch->alignment = 750;` |  | pending |
| `comm.nanny.break.023` | 1922 | `break;` |  | pending |
| `comm.nanny.case.025` | 1923 | `case 'n' : case 'N' : ch->alignment = 0;` |  | pending |
| `comm.nanny.case.026` | 1923 | `case 'N' : ch->alignment = 0;` |  | pending |
| `comm.nanny.break.024` | 1923 | `break;` |  | pending |
| `comm.nanny.case.027` | 1924 | `case 'e' : case 'E' : ch->alignment = -750;` |  | pending |
| `comm.nanny.case.028` | 1924 | `case 'E' : ch->alignment = -750;` |  | pending |
| `comm.nanny.break.025` | 1924 | `break;` |  | pending |
| `comm.nanny.default.005` | 1925 | `default:` |  | pending |
| `comm.nanny.return.020` | 1928 | `return;` |  | pending |
| `comm.nanny.break.026` | 1940 | `break;` |  | pending |
| `comm.nanny.case.029` | 1942 | `case CON_DEFAULT_CHOICE:` |  | pending |
| `comm.nanny.switch.006` | 1944 | `switch ( argument[0] )` |  | pending |
| `comm.nanny.case.030` | 1946 | `case 'y': case 'Y':` |  | pending |
| `comm.nanny.case.031` | 1946 | `case 'Y':` |  | pending |
| `comm.nanny.break.027` | 1955 | `break;` |  | pending |
| `comm.nanny.case.032` | 1956 | `case 'n': case 'N':` |  | pending |
| `comm.nanny.case.033` | 1956 | `case 'N':` |  | pending |
| `comm.nanny.for.008` | 1962 | `for ( i = 0; weapon_table[i].name != NULL; i++)` |  | pending |
| `comm.nanny.if.033` | 1963 | `if (ch->pcdata->learned[*weapon_table[i].gsn] > 0)` |  | pending |
| `comm.nanny.break.028` | 1971 | `break;` |  | pending |
| `comm.nanny.default.006` | 1972 | `default:` |  | pending |
| `comm.nanny.return.021` | 1974 | `return;` |  | pending |
| `comm.nanny.break.029` | 1976 | `break;` |  | pending |
| `comm.nanny.case.034` | 1978 | `case CON_PICK_WEAPON:` |  | pending |
| `comm.nanny.if.034` | 1981 | `if (weapon == -1 \|\| ch->pcdata->learned[*weapon_table[weapon].gsn] <= 0)` |  | pending |
| `comm.nanny.or.003` | 1981 | `\|\| ch->pcdata->learned[*weapon_table[weapon].gsn] <= 0)` |  | pending |
| `comm.nanny.for.009` | 1986 | `for ( i = 0; weapon_table[i].name != NULL; i++)` |  | pending |
| `comm.nanny.if.035` | 1987 | `if (ch->pcdata->learned[*weapon_table[i].gsn] > 0)` |  | pending |
| `comm.nanny.return.022` | 1994 | `return;` |  | pending |
| `comm.nanny.break.030` | 2001 | `break;` |  | pending |
| `comm.nanny.case.035` | 2003 | `case CON_GEN_GROUPS:` |  | pending |
| `comm.nanny.if.036` | 2006 | `if (!str_cmp(argument,"done"))` |  | pending |
| `comm.nanny.if.037` | 2008 | `if (ch->pcdata->points == pc_race_table[ch->race].points)` |  | pending |
| `comm.nanny.break.031` | 2011 | `break;` |  | pending |
| `comm.nanny.if.038` | 2014 | `if (ch->pcdata->points <= 40 + pc_race_table[ch->race].points)` |  | pending |
| `comm.nanny.break.032` | 2020 | `break;` |  | pending |
| `comm.nanny.if.039` | 2027 | `if (ch->pcdata->points < 40)` |  | pending |
| `comm.nanny.for.010` | 2036 | `for ( i = 0; weapon_table[i].name != NULL; i++)` |  | pending |
| `comm.nanny.if.040` | 2037 | `if (ch->pcdata->learned[*weapon_table[i].gsn] > 0)` |  | pending |
| `comm.nanny.break.033` | 2045 | `break;` |  | pending |
| `comm.nanny.if.041` | 2048 | `if (!parse_gen_groups(ch,argument))` |  | pending |
| `comm.nanny.break.034` | 2054 | `break;` |  | pending |
| `comm.nanny.case.036` | 2056 | `case CON_READ_IMOTD:` |  | pending |
| `comm.nanny.break.035` | 2060 | `break;` |  | pending |
| `comm.nanny.case.037` | 2062 | `case CON_READ_MOTD:` |  | pending |
| `comm.nanny.if.042` | 2063 | `if ( ch->pcdata == NULL \|\| ch->pcdata->pwd[0] == '\0')` |  | pending |
| `comm.nanny.or.004` | 2063 | `\|\| ch->pcdata->pwd[0] == '\0')` |  | pending |
| `comm.nanny.if.043` | 2079 | `if ( ch->level == 0 )` |  | pending |
| `comm.nanny.ternary.002` | 2093 | `? 1 : 0] );` |  | pending |
| `comm.nanny.if.044` | 2104 | `if ( ch->in_room != NULL )` |  | pending |
| `comm.nanny.if.045` | 2108 | `if ( IS_IMMORTAL(ch) )` |  | pending |
| `comm.nanny.if.046` | 2123 | `if (ch->pet != NULL)` |  | pending |
| `comm.nanny.break.036` | 2130 | `break;` |  | pending |
| `comm.nanny.return.023` | 2133 | `return;` |  | pending |

## check_parse_name

[Source line 2141](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2141); ends at line 2240. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:1575` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:334` (declaration_or_dispatch_reference).

Dependencies: `is_exact_name`, `LOWER`, `str_cmp`, `capitalize`, `str_prefix`, `str_suffix`, `strlen`, `defined`, `isalpha`, `isupper`, `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.check_parse_name.if.001` | 2148 | `if (is_exact_name(name, 	"all auto immortal self someone something the you loner"))` |  | pending |
| `comm.check_parse_name.return.001` | 2151 | `return FALSE;` |  | pending |
| `comm.check_parse_name.for.001` | 2155 | `for (clan = 0; clan < MAX_CLAN; clan++)` |  | pending |
| `comm.check_parse_name.if.002` | 2157 | `if (LOWER(name[0]) == LOWER(clan_table[clan].name[0]) 	&&  !str_cmp(name,clan_table[clan].name))` |  | pending |
| `comm.check_parse_name.and.001` | 2158 | `&&  !str_cmp(name,clan_table[clan].name))` |  | pending |
| `comm.check_parse_name.return.002` | 2159 | `return FALSE;` |  | pending |
| `comm.check_parse_name.if.003` | 2162 | `if (str_cmp(capitalize(name),"Alander") && (!str_prefix("Alan",name)     \|\| !str_suffix("Alander",name)))` |  | pending |
| `comm.check_parse_name.and.002` | 2162 | `&& (!str_prefix("Alan",name)` |  | pending |
| `comm.check_parse_name.or.001` | 2163 | `\|\| !str_suffix("Alander",name)))` |  | pending |
| `comm.check_parse_name.return.003` | 2164 | `return FALSE;` |  | pending |
| `comm.check_parse_name.if.004` | 2170 | `if ( strlen(name) <  2 )` |  | pending |
| `comm.check_parse_name.return.004` | 2171 | `return FALSE;` |  | pending |
| `comm.check_parse_name.if.005` | 2173 | `if defined(MSDOS)` |  | pending |
| `comm.check_parse_name.if.006` | 2174 | `if ( strlen(name) >  8 )` |  | pending |
| `comm.check_parse_name.return.005` | 2175 | `return FALSE;` |  | pending |
| `comm.check_parse_name.if.007` | 2178 | `if defined(macintosh)` |  | pending |
| `comm.check_parse_name.or.002` | 2178 | `\|\| defined(unix)` |  | pending |
| `comm.check_parse_name.if.008` | 2179 | `if ( strlen(name) > 12 )` |  | pending |
| `comm.check_parse_name.return.006` | 2180 | `return FALSE;` |  | pending |
| `comm.check_parse_name.for.002` | 2193 | `for ( pc = name; *pc != '\0'; pc++ )` |  | pending |
| `comm.check_parse_name.if.009` | 2195 | `if ( !isalpha(*pc) )` |  | pending |
| `comm.check_parse_name.return.007` | 2196 | `return FALSE;` |  | pending |
| `comm.check_parse_name.if.010` | 2198 | `if ( isupper(*pc))` |  | pending |
| `comm.check_parse_name.if.011` | 2200 | `if (adjcaps)` |  | pending |
| `comm.check_parse_name.if.012` | 2208 | `if ( LOWER(*pc) != 'i' && LOWER(*pc) != 'l' )` |  | pending |
| `comm.check_parse_name.and.003` | 2208 | `&& LOWER(*pc) != 'l' )` |  | pending |
| `comm.check_parse_name.if.013` | 2212 | `if ( fIll )` |  | pending |
| `comm.check_parse_name.return.008` | 2213 | `return FALSE;` |  | pending |
| `comm.check_parse_name.if.014` | 2215 | `if (cleancaps \|\| (total_caps > (strlen(name)) / 2 && strlen(name) < 3))` |  | pending |
| `comm.check_parse_name.or.003` | 2215 | `\|\| (total_caps > (strlen(name)) / 2 && strlen(name) < 3))` |  | pending |
| `comm.check_parse_name.and.004` | 2215 | `&& strlen(name) < 3))` |  | pending |
| `comm.check_parse_name.return.009` | 2216 | `return FALSE;` |  | pending |
| `comm.check_parse_name.for.003` | 2227 | `for ( iHash = 0; iHash < MAX_KEY_HASH; iHash++ )` |  | pending |
| `comm.check_parse_name.for.004` | 2229 | `for ( pMobIndex  = mob_index_hash[iHash]; 		  pMobIndex != NULL; 		  pMobIndex  = pMobIndex->next )` |  | pending |
| `comm.check_parse_name.if.015` | 2233 | `if ( is_name( name, pMobIndex->player_name ) )` |  | pending |
| `comm.check_parse_name.return.010` | 2234 | `return FALSE;` |  | pending |
| `comm.check_parse_name.return.011` | 2239 | `return TRUE;` |  | pending |

## check_reconnect

[Source line 2247](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2247); ends at line 2283. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:1600` (lexical_call_candidate).
- nanny: `src/comm.c:1664` (lexical_call_candidate).
- nanny: `src/comm.c:1701` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:335` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `str_cmp`, `free_string`, `str_dup`, `free_char`, `send_to_char`, `act`, `sprintf`, `log_string`, `wiznet`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.check_reconnect.for.001` | 2251 | `for ( ch = char_list; ch != NULL; ch = ch->next )` |  | pending |
| `comm.check_reconnect.if.001` | 2253 | `if ( !IS_NPC(ch) 	&&   (!fConn \|\| ch->desc == NULL) 	&&   !str_cmp( d->character->name, ch->name ) )` |  | pending |
| `comm.check_reconnect.and.001` | 2254 | `&&   (!fConn \|\| ch->desc == NULL)` |  | pending |
| `comm.check_reconnect.or.001` | 2254 | `\|\| ch->desc == NULL)` |  | pending |
| `comm.check_reconnect.and.002` | 2255 | `&&   !str_cmp( d->character->name, ch->name ) )` |  | pending |
| `comm.check_reconnect.if.002` | 2257 | `if ( fConn == FALSE )` |  | pending |
| `comm.check_reconnect.return.001` | 2278 | `return TRUE;` |  | pending |
| `comm.check_reconnect.return.002` | 2282 | `return FALSE;` |  | pending |

## check_playing

[Source line 2290](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2290); ends at line 2311. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:1661` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:337` (declaration_or_dispatch_reference).

Dependencies: `str_cmp`, `write_to_buffer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.check_playing.for.001` | 2294 | `for ( dold = descriptor_list; dold; dold = dold->next )` |  | pending |
| `comm.check_playing.if.001` | 2296 | `if ( dold != d 	&&   dold->character != NULL 	&&   dold->connected != CON_GET_NAME 	&&   dold->connected != CON_GET_OLD_PASSWORD 	&&   !str_cmp( name, dold->original 	         ? dold->original->name : dold->character->name ) )` |  | pending |
| `comm.check_playing.and.001` | 2297 | `&&   dold->character != NULL` |  | pending |
| `comm.check_playing.and.002` | 2298 | `&&   dold->connected != CON_GET_NAME` |  | pending |
| `comm.check_playing.and.003` | 2299 | `&&   dold->connected != CON_GET_OLD_PASSWORD` |  | pending |
| `comm.check_playing.and.004` | 2300 | `&&   !str_cmp( name, dold->original` |  | pending |
| `comm.check_playing.ternary.001` | 2301 | `? dold->original->name : dold->character->name ) )` |  | pending |
| `comm.check_playing.return.001` | 2306 | `return TRUE;` |  | pending |
| `comm.check_playing.return.002` | 2310 | `return FALSE;` |  | pending |

## stop_idling

[Source line 2315](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2315); ends at line 2330. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_mac_msdos: `src/comm.c:574` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:763` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:342` (declaration_or_dispatch_reference).

Dependencies: `get_room_index`, `char_from_room`, `char_to_room`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.stop_idling.if.001` | 2317 | `if ( ch == NULL     \|\|   ch->desc == NULL     \|\|   ch->desc->connected != CON_PLAYING     \|\|   ch->was_in_room == NULL      \|\|   ch->in_room != get_room_index(ROOM_VNUM_LIMBO))` |  | pending |
| `comm.stop_idling.or.001` | 2318 | `\|\|   ch->desc == NULL` |  | pending |
| `comm.stop_idling.or.002` | 2319 | `\|\|   ch->desc->connected != CON_PLAYING` |  | pending |
| `comm.stop_idling.or.003` | 2320 | `\|\|   ch->was_in_room == NULL` |  | pending |
| `comm.stop_idling.or.004` | 2321 | `\|\|   ch->in_room != get_room_index(ROOM_VNUM_LIMBO))` |  | pending |
| `comm.stop_idling.return.001` | 2322 | `return;` |  | pending |
| `comm.stop_idling.return.002` | 2329 | `return;` |  | pending |

## send_to_char

[Source line 2337](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2337); ends at line 2342. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_delet: `src/act_comm.c:48` (lexical_call_candidate).
- do_delete: `src/act_comm.c:62` (lexical_call_candidate).
- do_delete: `src/act_comm.c:79` (lexical_call_candidate).
- do_delete: `src/act_comm.c:83` (lexical_call_candidate).
- do_delete: `src/act_comm.c:84` (lexical_call_candidate).
- do_delete: `src/act_comm.c:85` (lexical_call_candidate).
- do_channels: `src/act_comm.c:99` (lexical_call_candidate).
- do_channels: `src/act_comm.c:100` (lexical_call_candidate).
- do_channels: `src/act_comm.c:102` (lexical_call_candidate).
- do_channels: `src/act_comm.c:104` (lexical_call_candidate).
- do_channels: `src/act_comm.c:106` (lexical_call_candidate).
- do_channels: `src/act_comm.c:108` (lexical_call_candidate).
- do_channels: `src/act_comm.c:110` (lexical_call_candidate).
- do_channels: `src/act_comm.c:112` (lexical_call_candidate).
- do_channels: `src/act_comm.c:114` (lexical_call_candidate).
- do_channels: `src/act_comm.c:116` (lexical_call_candidate).
- do_channels: `src/act_comm.c:118` (lexical_call_candidate).
- do_channels: `src/act_comm.c:120` (lexical_call_candidate).
- do_channels: `src/act_comm.c:122` (lexical_call_candidate).
- do_channels: `src/act_comm.c:124` (lexical_call_candidate).
- do_channels: `src/act_comm.c:126` (lexical_call_candidate).
- do_channels: `src/act_comm.c:128` (lexical_call_candidate).
- do_channels: `src/act_comm.c:130` (lexical_call_candidate).
- do_channels: `src/act_comm.c:132` (lexical_call_candidate).
- do_channels: `src/act_comm.c:134` (lexical_call_candidate).
- do_channels: `src/act_comm.c:136` (lexical_call_candidate).
- do_channels: `src/act_comm.c:140` (lexical_call_candidate).
- do_channels: `src/act_comm.c:142` (lexical_call_candidate).
- do_channels: `src/act_comm.c:144` (lexical_call_candidate).
- do_channels: `src/act_comm.c:147` (lexical_call_candidate).
- do_channels: `src/act_comm.c:149` (lexical_call_candidate).
- do_channels: `src/act_comm.c:151` (lexical_call_candidate).
- do_channels: `src/act_comm.c:153` (lexical_call_candidate).
- do_channels: `src/act_comm.c:155` (lexical_call_candidate).
- do_channels: `src/act_comm.c:157` (lexical_call_candidate).
- do_channels: `src/act_comm.c:159` (lexical_call_candidate).
- do_channels: `src/act_comm.c:161` (lexical_call_candidate).
- do_channels: `src/act_comm.c:163` (lexical_call_candidate).
- do_channels: `src/act_comm.c:166` (lexical_call_candidate).
- do_channels: `src/act_comm.c:169` (lexical_call_candidate).
- do_channels: `src/act_comm.c:176` (lexical_call_candidate).
- do_channels: `src/act_comm.c:179` (lexical_call_candidate).
- do_channels: `src/act_comm.c:185` (lexical_call_candidate).
- do_channels: `src/act_comm.c:189` (lexical_call_candidate).
- do_channels: `src/act_comm.c:192` (lexical_call_candidate).
- do_channels: `src/act_comm.c:195` (lexical_call_candidate).
- do_channels: `src/act_comm.c:198` (lexical_call_candidate).
- do_deaf: `src/act_comm.c:209` (lexical_call_candidate).
- do_deaf: `src/act_comm.c:214` (lexical_call_candidate).
- do_quiet: `src/act_comm.c:225` (lexical_call_candidate).
- do_quiet: `src/act_comm.c:230` (lexical_call_candidate).
- do_afk: `src/act_comm.c:241` (lexical_call_candidate).
- do_afk: `src/act_comm.c:246` (lexical_call_candidate).
- do_replay: `src/act_comm.c:255` (lexical_call_candidate).
- do_replay: `src/act_comm.c:261` (lexical_call_candidate).
- do_auction: `src/act_comm.c:279` (lexical_call_candidate).
- do_auction: `src/act_comm.c:284` (lexical_call_candidate).
- do_auction: `src/act_comm.c:292` (lexical_call_candidate).
- do_auction: `src/act_comm.c:298` (lexical_call_candidate).
- do_auction: `src/act_comm.c:306` (lexical_call_candidate).
- do_gossip: `src/act_comm.c:334` (lexical_call_candidate).
- do_gossip: `src/act_comm.c:339` (lexical_call_candidate).
- do_gossip: `src/act_comm.c:347` (lexical_call_candidate).
- do_gossip: `src/act_comm.c:353` (lexical_call_candidate).
- do_gossip: `src/act_comm.c:361` (lexical_call_candidate).
- do_grats: `src/act_comm.c:389` (lexical_call_candidate).
- do_grats: `src/act_comm.c:394` (lexical_call_candidate).
- do_grats: `src/act_comm.c:402` (lexical_call_candidate).
- do_grats: `src/act_comm.c:408` (lexical_call_candidate).
- do_grats: `src/act_comm.c:416` (lexical_call_candidate).
- do_quote: `src/act_comm.c:444` (lexical_call_candidate).
- do_quote: `src/act_comm.c:449` (lexical_call_candidate).
- do_quote: `src/act_comm.c:457` (lexical_call_candidate).
- do_quote: `src/act_comm.c:463` (lexical_call_candidate).
- do_quote: `src/act_comm.c:471` (lexical_call_candidate).
- do_question: `src/act_comm.c:500` (lexical_call_candidate).
- do_question: `src/act_comm.c:505` (lexical_call_candidate).
- do_question: `src/act_comm.c:513` (lexical_call_candidate).
- do_question: `src/act_comm.c:519` (lexical_call_candidate).
- do_question: `src/act_comm.c:526` (lexical_call_candidate).
- do_answer: `src/act_comm.c:555` (lexical_call_candidate).
- do_answer: `src/act_comm.c:560` (lexical_call_candidate).
- do_answer: `src/act_comm.c:568` (lexical_call_candidate).
- do_answer: `src/act_comm.c:574` (lexical_call_candidate).
- do_answer: `src/act_comm.c:581` (lexical_call_candidate).
- do_music: `src/act_comm.c:610` (lexical_call_candidate).
- do_music: `src/act_comm.c:615` (lexical_call_candidate).
- do_music: `src/act_comm.c:623` (lexical_call_candidate).
- do_music: `src/act_comm.c:629` (lexical_call_candidate).
- do_music: `src/act_comm.c:636` (lexical_call_candidate).
- do_clantalk: `src/act_comm.c:664` (lexical_call_candidate).
- do_clantalk: `src/act_comm.c:671` (lexical_call_candidate).
- do_clantalk: `src/act_comm.c:676` (lexical_call_candidate).
- do_clantalk: `src/act_comm.c:684` (lexical_call_candidate).
- do_clantalk: `src/act_comm.c:691` (lexical_call_candidate).
- do_immtalk: `src/act_comm.c:717` (lexical_call_candidate).
- do_immtalk: `src/act_comm.c:722` (lexical_call_candidate).
- do_say: `src/act_comm.c:751` (lexical_call_candidate).
- do_shout: `src/act_comm.c:770` (lexical_call_candidate).
- do_shout: `src/act_comm.c:775` (lexical_call_candidate).
- do_shout: `src/act_comm.c:783` (lexical_call_candidate).
- do_tell: `src/act_comm.c:819` (lexical_call_candidate).
- do_tell: `src/act_comm.c:825` (lexical_call_candidate).
- do_tell: `src/act_comm.c:831` (lexical_call_candidate).
- do_tell: `src/act_comm.c:839` (lexical_call_candidate).
- do_tell: `src/act_comm.c:850` (lexical_call_candidate).
- do_reply: `src/act_comm.c:909` (lexical_call_candidate).
- do_reply: `src/act_comm.c:915` (lexical_call_candidate).
- do_reply: `src/act_comm.c:944` (lexical_call_candidate).
- do_yell: `src/act_comm.c:980` (lexical_call_candidate).
- do_yell: `src/act_comm.c:986` (lexical_call_candidate).
- do_emote: `src/act_comm.c:1012` (lexical_call_candidate).
- do_emote: `src/act_comm.c:1018` (lexical_call_candidate).
- do_pmote: `src/act_comm.c:1037` (lexical_call_candidate).
- do_pmote: `src/act_comm.c:1043` (lexical_call_candidate).
- do_bug: `src/act_comm.c:1369` (lexical_call_candidate).
- do_typo: `src/act_comm.c:1376` (lexical_call_candidate).
- do_rent: `src/act_comm.c:1382` (lexical_call_candidate).
- do_qui: `src/act_comm.c:1389` (lexical_call_candidate).
- do_quit: `src/act_comm.c:1405` (lexical_call_candidate).
- do_quit: `src/act_comm.c:1411` (lexical_call_candidate).
- do_quit: `src/act_comm.c:1414` (lexical_call_candidate).
- do_save: `src/act_comm.c:1456` (lexical_call_candidate).
- do_follow: `src/act_comm.c:1473` (lexical_call_candidate).
- do_follow: `src/act_comm.c:1479` (lexical_call_candidate).
- do_follow: `src/act_comm.c:1493` (lexical_call_candidate).
- do_order: `src/act_comm.c:1625` (lexical_call_candidate).
- do_order: `src/act_comm.c:1631` (lexical_call_candidate).
- do_order: `src/act_comm.c:1637` (lexical_call_candidate).
- do_order: `src/act_comm.c:1651` (lexical_call_candidate).
- do_order: `src/act_comm.c:1657` (lexical_call_candidate).
- do_order: `src/act_comm.c:1664` (lexical_call_candidate).
- do_order: `src/act_comm.c:1688` (lexical_call_candidate).
- do_order: `src/act_comm.c:1691` (lexical_call_candidate).
- do_group: `src/act_comm.c:1712` (lexical_call_candidate).
- do_group: `src/act_comm.c:1727` (lexical_call_candidate).
- do_group: `src/act_comm.c:1735` (lexical_call_candidate).
- do_group: `src/act_comm.c:1741` (lexical_call_candidate).
- do_group: `src/act_comm.c:1753` (lexical_call_candidate).
- do_split: `src/act_comm.c:1803` (lexical_call_candidate).
- do_split: `src/act_comm.c:1814` (lexical_call_candidate).
- do_split: `src/act_comm.c:1820` (lexical_call_candidate).
- do_split: `src/act_comm.c:1826` (lexical_call_candidate).
- do_split: `src/act_comm.c:1839` (lexical_call_candidate).
- do_split: `src/act_comm.c:1851` (lexical_call_candidate).
- do_split: `src/act_comm.c:1865` (lexical_call_candidate).
- do_split: `src/act_comm.c:1873` (lexical_call_candidate).
- do_gtell: `src/act_comm.c:1914` (lexical_call_candidate).
- do_gtell: `src/act_comm.c:1920` (lexical_call_candidate).
- do_commands: `src/act_comm.c:1948` (lexical_call_candidate).
- do_commands: `src/act_comm.c:1950` (lexical_call_candidate).
- do_commands: `src/act_comm.c:1955` (lexical_call_candidate).
- do_wizhelp: `src/act_comm.c:1973` (lexical_call_candidate).
- do_wizhelp: `src/act_comm.c:1975` (lexical_call_candidate).
- do_wizhelp: `src/act_comm.c:1980` (lexical_call_candidate).
- do_enter: `src/act_enter.c:84` (lexical_call_candidate).
- do_enter: `src/act_enter.c:91` (lexical_call_candidate).
- do_enter: `src/act_enter.c:99` (lexical_call_candidate).
- do_enter: `src/act_enter.c:125` (lexical_call_candidate).
- do_enter: `src/act_enter.c:212` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:226` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:227` (lexical_call_candidate).
- show_char_to_char_0: `src/act_info.c:268` (lexical_call_candidate).
- show_char_to_char_0: `src/act_info.c:401` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:428` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:460` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:470` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:474` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:475` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:476` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:484` (lexical_call_candidate).
- show_char_to_char: `src/act_info.c:513` (lexical_call_candidate).
- check_blind: `src/act_info.c:530` (lexical_call_candidate).
- do_scroll: `src/act_info.c:549` (lexical_call_candidate).
- do_scroll: `src/act_info.c:554` (lexical_call_candidate).
- do_scroll: `src/act_info.c:561` (lexical_call_candidate).
- do_scroll: `src/act_info.c:569` (lexical_call_candidate).
- do_scroll: `src/act_info.c:576` (lexical_call_candidate).
- do_scroll: `src/act_info.c:581` (lexical_call_candidate).
- do_socials: `src/act_info.c:597` (lexical_call_candidate).
- do_socials: `src/act_info.c:599` (lexical_call_candidate).
- do_socials: `src/act_info.c:603` (lexical_call_candidate).
- do_autolist: `src/act_info.c:645` (lexical_call_candidate).
- do_autolist: `src/act_info.c:646` (lexical_call_candidate).
- do_autolist: `src/act_info.c:648` (lexical_call_candidate).
- do_autolist: `src/act_info.c:650` (lexical_call_candidate).
- do_autolist: `src/act_info.c:652` (lexical_call_candidate).
- do_autolist: `src/act_info.c:654` (lexical_call_candidate).
- do_autolist: `src/act_info.c:656` (lexical_call_candidate).
- do_autolist: `src/act_info.c:658` (lexical_call_candidate).
- do_autolist: `src/act_info.c:660` (lexical_call_candidate).
- do_autolist: `src/act_info.c:662` (lexical_call_candidate).
- do_autolist: `src/act_info.c:664` (lexical_call_candidate).
- do_autolist: `src/act_info.c:666` (lexical_call_candidate).
- do_autolist: `src/act_info.c:668` (lexical_call_candidate).
- do_autolist: `src/act_info.c:670` (lexical_call_candidate).
- do_autolist: `src/act_info.c:672` (lexical_call_candidate).
- do_autolist: `src/act_info.c:674` (lexical_call_candidate).
- do_autolist: `src/act_info.c:676` (lexical_call_candidate).
- do_autolist: `src/act_info.c:678` (lexical_call_candidate).
- do_autolist: `src/act_info.c:680` (lexical_call_candidate).
- do_autolist: `src/act_info.c:682` (lexical_call_candidate).
- do_autolist: `src/act_info.c:684` (lexical_call_candidate).
- do_autolist: `src/act_info.c:686` (lexical_call_candidate).
- do_autolist: `src/act_info.c:688` (lexical_call_candidate).
- do_autolist: `src/act_info.c:690` (lexical_call_candidate).
- do_autolist: `src/act_info.c:692` (lexical_call_candidate).
- do_autolist: `src/act_info.c:694` (lexical_call_candidate).
- do_autolist: `src/act_info.c:696` (lexical_call_candidate).
- do_autolist: `src/act_info.c:698` (lexical_call_candidate).
- do_autolist: `src/act_info.c:700` (lexical_call_candidate).
- do_autolist: `src/act_info.c:703` (lexical_call_candidate).
- do_autolist: `src/act_info.c:705` (lexical_call_candidate).
- do_autolist: `src/act_info.c:708` (lexical_call_candidate).
- do_autolist: `src/act_info.c:710` (lexical_call_candidate).
- do_autolist: `src/act_info.c:713` (lexical_call_candidate).
- do_autolist: `src/act_info.c:715` (lexical_call_candidate).
- do_autoassist: `src/act_info.c:725` (lexical_call_candidate).
- do_autoassist: `src/act_info.c:730` (lexical_call_candidate).
- do_autoexit: `src/act_info.c:742` (lexical_call_candidate).
- do_autoexit: `src/act_info.c:747` (lexical_call_candidate).
- do_autogold: `src/act_info.c:759` (lexical_call_candidate).
- do_autogold: `src/act_info.c:764` (lexical_call_candidate).
- do_autoloot: `src/act_info.c:776` (lexical_call_candidate).
- do_autoloot: `src/act_info.c:781` (lexical_call_candidate).
- do_autosac: `src/act_info.c:793` (lexical_call_candidate).
- do_autosac: `src/act_info.c:798` (lexical_call_candidate).
- do_autosplit: `src/act_info.c:810` (lexical_call_candidate).
- do_autosplit: `src/act_info.c:815` (lexical_call_candidate).
- do_brief: `src/act_info.c:824` (lexical_call_candidate).
- do_brief: `src/act_info.c:829` (lexical_call_candidate).
- do_compact: `src/act_info.c:838` (lexical_call_candidate).
- do_compact: `src/act_info.c:843` (lexical_call_candidate).
- do_show: `src/act_info.c:852` (lexical_call_candidate).
- do_show: `src/act_info.c:857` (lexical_call_candidate).
- do_prompt: `src/act_info.c:870` (lexical_call_candidate).
- do_prompt: `src/act_info.c:875` (lexical_call_candidate).
- do_prompt: `src/act_info.c:897` (lexical_call_candidate).
- do_combine: `src/act_info.c:905` (lexical_call_candidate).
- do_combine: `src/act_info.c:910` (lexical_call_candidate).
- do_noloot: `src/act_info.c:922` (lexical_call_candidate).
- do_noloot: `src/act_info.c:927` (lexical_call_candidate).
- do_nofollow: `src/act_info.c:939` (lexical_call_candidate).
- do_nofollow: `src/act_info.c:944` (lexical_call_candidate).
- do_nosummon: `src/act_info.c:956` (lexical_call_candidate).
- do_nosummon: `src/act_info.c:961` (lexical_call_candidate).
- do_nosummon: `src/act_info.c:969` (lexical_call_candidate).
- do_nosummon: `src/act_info.c:974` (lexical_call_candidate).
- do_look: `src/act_info.c:998` (lexical_call_candidate).
- do_look: `src/act_info.c:1004` (lexical_call_candidate).
- do_look: `src/act_info.c:1015` (lexical_call_candidate).
- do_look: `src/act_info.c:1028` (lexical_call_candidate).
- do_look: `src/act_info.c:1033` (lexical_call_candidate).
- do_look: `src/act_info.c:1036` (lexical_call_candidate).
- do_look: `src/act_info.c:1041` (lexical_call_candidate).
- do_look: `src/act_info.c:1042` (lexical_call_candidate).
- do_look: `src/act_info.c:1047` (lexical_call_candidate).
- do_look: `src/act_info.c:1061` (lexical_call_candidate).
- do_look: `src/act_info.c:1067` (lexical_call_candidate).
- do_look: `src/act_info.c:1074` (lexical_call_candidate).
- do_look: `src/act_info.c:1080` (lexical_call_candidate).
- do_look: `src/act_info.c:1092` (lexical_call_candidate).
- do_look: `src/act_info.c:1100` (lexical_call_candidate).
- do_look: `src/act_info.c:1125` (lexical_call_candidate).
- do_look: `src/act_info.c:1134` (lexical_call_candidate).
- do_look: `src/act_info.c:1142` (lexical_call_candidate).
- do_look: `src/act_info.c:1143` (lexical_call_candidate).
- do_look: `src/act_info.c:1157` (lexical_call_candidate).
- do_look: `src/act_info.c:1165` (lexical_call_candidate).
- do_look: `src/act_info.c:1172` (lexical_call_candidate).
- do_look: `src/act_info.c:1173` (lexical_call_candidate).
- do_look: `src/act_info.c:1184` (lexical_call_candidate).
- do_look: `src/act_info.c:1196` (lexical_call_candidate).
- do_look: `src/act_info.c:1208` (lexical_call_candidate).
- do_look: `src/act_info.c:1215` (lexical_call_candidate).
- do_look: `src/act_info.c:1220` (lexical_call_candidate).
- do_look: `src/act_info.c:1222` (lexical_call_candidate).
- do_examine: `src/act_info.c:1257` (lexical_call_candidate).
- do_examine: `src/act_info.c:1297` (lexical_call_candidate).
- do_exits: `src/act_info.c:1375` (lexical_call_candidate).
- do_worth: `src/act_info.c:1387` (lexical_call_candidate).
- do_worth: `src/act_info.c:1396` (lexical_call_candidate).
- do_score: `src/act_info.c:1413` (lexical_call_candidate).
- do_score: `src/act_info.c:1419` (lexical_call_candidate).
- do_score: `src/act_info.c:1426` (lexical_call_candidate).
- do_score: `src/act_info.c:1434` (lexical_call_candidate).
- do_score: `src/act_info.c:1439` (lexical_call_candidate).
- do_score: `src/act_info.c:1445` (lexical_call_candidate).
- do_score: `src/act_info.c:1459` (lexical_call_candidate).
- do_score: `src/act_info.c:1464` (lexical_call_candidate).
- do_score: `src/act_info.c:1472` (lexical_call_candidate).
- do_score: `src/act_info.c:1476` (lexical_call_candidate).
- do_score: `src/act_info.c:1479` (lexical_call_candidate).
- do_score: `src/act_info.c:1481` (lexical_call_candidate).
- do_score: `src/act_info.c:1483` (lexical_call_candidate).
- do_score: `src/act_info.c:1488` (lexical_call_candidate).
- do_score: `src/act_info.c:1491` (lexical_call_candidate).
- do_score: `src/act_info.c:1494` (lexical_call_candidate).
- do_score: `src/act_info.c:1497` (lexical_call_candidate).
- do_score: `src/act_info.c:1500` (lexical_call_candidate).
- do_score: `src/act_info.c:1503` (lexical_call_candidate).
- do_score: `src/act_info.c:1506` (lexical_call_candidate).
- do_score: `src/act_info.c:1509` (lexical_call_candidate).
- do_score: `src/act_info.c:1512` (lexical_call_candidate).
- do_score: `src/act_info.c:1525` (lexical_call_candidate).
- do_score: `src/act_info.c:1541` (lexical_call_candidate).
- do_score: `src/act_info.c:1568` (lexical_call_candidate).
- do_score: `src/act_info.c:1575` (lexical_call_candidate).
- do_score: `src/act_info.c:1577` (lexical_call_candidate).
- do_score: `src/act_info.c:1579` (lexical_call_candidate).
- do_score: `src/act_info.c:1584` (lexical_call_candidate).
- do_score: `src/act_info.c:1590` (lexical_call_candidate).
- do_score: `src/act_info.c:1592` (lexical_call_candidate).
- do_score: `src/act_info.c:1599` (lexical_call_candidate).
- do_score: `src/act_info.c:1605` (lexical_call_candidate).
- do_score: `src/act_info.c:1608` (lexical_call_candidate).
- do_score: `src/act_info.c:1609` (lexical_call_candidate).
- do_score: `src/act_info.c:1610` (lexical_call_candidate).
- do_score: `src/act_info.c:1611` (lexical_call_candidate).
- do_score: `src/act_info.c:1612` (lexical_call_candidate).
- do_score: `src/act_info.c:1613` (lexical_call_candidate).
- do_score: `src/act_info.c:1614` (lexical_call_candidate).
- do_score: `src/act_info.c:1615` (lexical_call_candidate).
- do_score: `src/act_info.c:1616` (lexical_call_candidate).
- do_score: `src/act_info.c:1617` (lexical_call_candidate).
- do_affects: `src/act_info.c:1630` (lexical_call_candidate).
- do_affects: `src/act_info.c:1641` (lexical_call_candidate).
- do_affects: `src/act_info.c:1649` (lexical_call_candidate).
- do_affects: `src/act_info.c:1654` (lexical_call_candidate).
- do_affects: `src/act_info.c:1657` (lexical_call_candidate).
- do_affects: `src/act_info.c:1662` (lexical_call_candidate).
- do_time: `src/act_info.c:1705` (lexical_call_candidate).
- do_time: `src/act_info.c:1711` (lexical_call_candidate).
- do_weather: `src/act_info.c:1731` (lexical_call_candidate).
- do_weather: `src/act_info.c:1741` (lexical_call_candidate).
- do_help: `src/act_info.c:1803` (lexical_call_candidate).
- do_whois: `src/act_info.c:1823` (lexical_call_candidate).
- do_whois: `src/act_info.c:1880` (lexical_call_candidate).
- do_who: `src/act_info.c:1945` (lexical_call_candidate).
- do_who: `src/act_info.c:1980` (lexical_call_candidate).
- do_count: `src/act_info.c:2103` (lexical_call_candidate).
- do_inventory: `src/act_info.c:2108` (lexical_call_candidate).
- do_equipment: `src/act_info.c:2121` (lexical_call_candidate).
- do_equipment: `src/act_info.c:2128` (lexical_call_candidate).
- do_equipment: `src/act_info.c:2131` (lexical_call_candidate).
- do_equipment: `src/act_info.c:2132` (lexical_call_candidate).
- do_equipment: `src/act_info.c:2136` (lexical_call_candidate).
- do_equipment: `src/act_info.c:2142` (lexical_call_candidate).
- do_compare: `src/act_info.c:2163` (lexical_call_candidate).
- do_compare: `src/act_info.c:2169` (lexical_call_candidate).
- do_compare: `src/act_info.c:2186` (lexical_call_candidate).
- do_compare: `src/act_info.c:2193` (lexical_call_candidate).
- do_where: `src/act_info.c:2269` (lexical_call_candidate).
- do_where: `src/act_info.c:2286` (lexical_call_candidate).
- do_where: `src/act_info.c:2290` (lexical_call_candidate).
- do_where: `src/act_info.c:2307` (lexical_call_candidate).
- do_consider: `src/act_info.c:2332` (lexical_call_candidate).
- do_consider: `src/act_info.c:2338` (lexical_call_candidate).
- do_consider: `src/act_info.c:2344` (lexical_call_candidate).
- do_title: `src/act_info.c:2398` (lexical_call_candidate).
- do_title: `src/act_info.c:2407` (lexical_call_candidate).
- do_description: `src/act_info.c:2428` (lexical_call_candidate).
- do_description: `src/act_info.c:2449` (lexical_call_candidate).
- do_description: `src/act_info.c:2450` (lexical_call_candidate).
- do_description: `src/act_info.c:2459` (lexical_call_candidate).
- do_description: `src/act_info.c:2473` (lexical_call_candidate).
- do_description: `src/act_info.c:2483` (lexical_call_candidate).
- do_description: `src/act_info.c:2484` (lexical_call_candidate).
- do_report: `src/act_info.c:2501` (lexical_call_candidate).
- do_practice: `src/act_info.c:2539` (lexical_call_candidate).
- do_practice: `src/act_info.c:2541` (lexical_call_candidate).
- do_practice: `src/act_info.c:2545` (lexical_call_candidate).
- do_practice: `src/act_info.c:2549` (lexical_call_candidate).
- do_practice: `src/act_info.c:2558` (lexical_call_candidate).
- do_practice: `src/act_info.c:2570` (lexical_call_candidate).
- do_practice: `src/act_info.c:2576` (lexical_call_candidate).
- do_practice: `src/act_info.c:2586` (lexical_call_candidate).
- do_practice: `src/act_info.c:2596` (lexical_call_candidate).
- do_wimpy: `src/act_info.c:2644` (lexical_call_candidate).
- do_wimpy: `src/act_info.c:2650` (lexical_call_candidate).
- do_wimpy: `src/act_info.c:2656` (lexical_call_candidate).
- do_password: `src/act_info.c:2718` (lexical_call_candidate).
- do_password: `src/act_info.c:2725` (lexical_call_candidate).
- do_password: `src/act_info.c:2731` (lexical_call_candidate).
- do_password: `src/act_info.c:2744` (lexical_call_candidate).
- do_password: `src/act_info.c:2753` (lexical_call_candidate).
- move_char: `src/act_move.c:84` (lexical_call_candidate).
- move_char: `src/act_move.c:100` (lexical_call_candidate).
- move_char: `src/act_move.c:106` (lexical_call_candidate).
- move_char: `src/act_move.c:122` (lexical_call_candidate).
- move_char: `src/act_move.c:133` (lexical_call_candidate).
- move_char: `src/act_move.c:163` (lexical_call_candidate).
- move_char: `src/act_move.c:184` (lexical_call_candidate).
- find_door: `src/act_move.c:320` (lexical_call_candidate).
- do_open: `src/act_move.c:339` (lexical_call_candidate).
- do_open: `src/act_move.c:350` (lexical_call_candidate).
- do_open: `src/act_move.c:356` (lexical_call_candidate).
- do_open: `src/act_move.c:362` (lexical_call_candidate).
- do_open: `src/act_move.c:374` (lexical_call_candidate).
- do_open: `src/act_move.c:376` (lexical_call_candidate).
- do_open: `src/act_move.c:378` (lexical_call_candidate).
- do_open: `src/act_move.c:380` (lexical_call_candidate).
- do_open: `src/act_move.c:397` (lexical_call_candidate).
- do_open: `src/act_move.c:399` (lexical_call_candidate).
- do_open: `src/act_move.c:403` (lexical_call_candidate).
- do_close: `src/act_move.c:433` (lexical_call_candidate).
- do_close: `src/act_move.c:446` (lexical_call_candidate).
- do_close: `src/act_move.c:452` (lexical_call_candidate).
- do_close: `src/act_move.c:464` (lexical_call_candidate).
- do_close: `src/act_move.c:466` (lexical_call_candidate).
- do_close: `src/act_move.c:468` (lexical_call_candidate).
- do_close: `src/act_move.c:485` (lexical_call_candidate).
- do_close: `src/act_move.c:489` (lexical_call_candidate).
- do_lock: `src/act_move.c:534` (lexical_call_candidate).
- do_lock: `src/act_move.c:546` (lexical_call_candidate).
- do_lock: `src/act_move.c:551` (lexical_call_candidate).
- do_lock: `src/act_move.c:557` (lexical_call_candidate).
- do_lock: `src/act_move.c:563` (lexical_call_candidate).
- do_lock: `src/act_move.c:569` (lexical_call_candidate).
- do_lock: `src/act_move.c:581` (lexical_call_candidate).
- do_lock: `src/act_move.c:583` (lexical_call_candidate).
- do_lock: `src/act_move.c:585` (lexical_call_candidate).
- do_lock: `src/act_move.c:587` (lexical_call_candidate).
- do_lock: `src/act_move.c:589` (lexical_call_candidate).
- do_lock: `src/act_move.c:606` (lexical_call_candidate).
- do_lock: `src/act_move.c:608` (lexical_call_candidate).
- do_lock: `src/act_move.c:610` (lexical_call_candidate).
- do_lock: `src/act_move.c:612` (lexical_call_candidate).
- do_lock: `src/act_move.c:615` (lexical_call_candidate).
- do_unlock: `src/act_move.c:642` (lexical_call_candidate).
- do_unlock: `src/act_move.c:653` (lexical_call_candidate).
- do_unlock: `src/act_move.c:659` (lexical_call_candidate).
- do_unlock: `src/act_move.c:665` (lexical_call_candidate).
- do_unlock: `src/act_move.c:671` (lexical_call_candidate).
- do_unlock: `src/act_move.c:677` (lexical_call_candidate).
- do_unlock: `src/act_move.c:689` (lexical_call_candidate).
- do_unlock: `src/act_move.c:691` (lexical_call_candidate).
- do_unlock: `src/act_move.c:693` (lexical_call_candidate).
- do_unlock: `src/act_move.c:695` (lexical_call_candidate).
- do_unlock: `src/act_move.c:697` (lexical_call_candidate).
- do_unlock: `src/act_move.c:714` (lexical_call_candidate).
- do_unlock: `src/act_move.c:716` (lexical_call_candidate).
- do_unlock: `src/act_move.c:718` (lexical_call_candidate).
- do_unlock: `src/act_move.c:720` (lexical_call_candidate).
- do_unlock: `src/act_move.c:723` (lexical_call_candidate).
- do_pick: `src/act_move.c:751` (lexical_call_candidate).
- do_pick: `src/act_move.c:770` (lexical_call_candidate).
- do_pick: `src/act_move.c:782` (lexical_call_candidate).
- do_pick: `src/act_move.c:788` (lexical_call_candidate).
- do_pick: `src/act_move.c:794` (lexical_call_candidate).
- do_pick: `src/act_move.c:800` (lexical_call_candidate).
- do_pick: `src/act_move.c:817` (lexical_call_candidate).
- do_pick: `src/act_move.c:819` (lexical_call_candidate).
- do_pick: `src/act_move.c:821` (lexical_call_candidate).
- do_pick: `src/act_move.c:823` (lexical_call_candidate).
- do_pick: `src/act_move.c:825` (lexical_call_candidate).
- do_pick: `src/act_move.c:843` (lexical_call_candidate).
- do_pick: `src/act_move.c:845` (lexical_call_candidate).
- do_pick: `src/act_move.c:847` (lexical_call_candidate).
- do_pick: `src/act_move.c:849` (lexical_call_candidate).
- do_pick: `src/act_move.c:852` (lexical_call_candidate).
- do_stand: `src/act_move.c:879` (lexical_call_candidate).
- do_stand: `src/act_move.c:885` (lexical_call_candidate).
- do_stand: `src/act_move.c:893` (lexical_call_candidate).
- do_stand: `src/act_move.c:909` (lexical_call_candidate).
- do_stand: `src/act_move.c:913` (lexical_call_candidate).
- do_stand: `src/act_move.c:939` (lexical_call_candidate).
- do_stand: `src/act_move.c:962` (lexical_call_candidate).
- do_stand: `src/act_move.c:966` (lexical_call_candidate).
- do_rest: `src/act_move.c:981` (lexical_call_candidate).
- do_rest: `src/act_move.c:991` (lexical_call_candidate).
- do_rest: `src/act_move.c:1004` (lexical_call_candidate).
- do_rest: `src/act_move.c:1022` (lexical_call_candidate).
- do_rest: `src/act_move.c:1028` (lexical_call_candidate).
- do_rest: `src/act_move.c:1053` (lexical_call_candidate).
- do_rest: `src/act_move.c:1059` (lexical_call_candidate).
- do_rest: `src/act_move.c:1083` (lexical_call_candidate).
- do_sit: `src/act_move.c:1116` (lexical_call_candidate).
- do_sit: `src/act_move.c:1126` (lexical_call_candidate).
- do_sit: `src/act_move.c:1139` (lexical_call_candidate).
- do_sit: `src/act_move.c:1156` (lexical_call_candidate).
- do_sit: `src/act_move.c:1162` (lexical_call_candidate).
- do_sit: `src/act_move.c:1185` (lexical_call_candidate).
- do_sit: `src/act_move.c:1200` (lexical_call_candidate).
- do_sit: `src/act_move.c:1205` (lexical_call_candidate).
- do_sleep: `src/act_move.c:1237` (lexical_call_candidate).
- do_sleep: `src/act_move.c:1245` (lexical_call_candidate).
- do_sleep: `src/act_move.c:1258` (lexical_call_candidate).
- do_sleep: `src/act_move.c:1266` (lexical_call_candidate).
- do_sleep: `src/act_move.c:1298` (lexical_call_candidate).
- do_wake: `src/act_move.c:1317` (lexical_call_candidate).
- do_wake: `src/act_move.c:1320` (lexical_call_candidate).
- do_sneak: `src/act_move.c:1339` (lexical_call_candidate).
- do_hide: `src/act_move.c:1367` (lexical_call_candidate).
- do_visible: `src/act_move.c:1396` (lexical_call_candidate).
- do_recall: `src/act_move.c:1410` (lexical_call_candidate).
- do_recall: `src/act_move.c:1418` (lexical_call_candidate).
- do_recall: `src/act_move.c:1428` (lexical_call_candidate).
- do_recall: `src/act_move.c:1443` (lexical_call_candidate).
- do_recall: `src/act_move.c:1451` (lexical_call_candidate).
- do_train: `src/act_move.c:1493` (lexical_call_candidate).
- do_train: `src/act_move.c:1500` (lexical_call_candidate).
- do_train: `src/act_move.c:1570` (lexical_call_candidate).
- do_train: `src/act_move.c:1592` (lexical_call_candidate).
- do_train: `src/act_move.c:1609` (lexical_call_candidate).
- do_train: `src/act_move.c:1630` (lexical_call_candidate).
- get_obj: `src/act_obj.c:98` (lexical_call_candidate).
- get_obj: `src/act_obj.c:140` (lexical_call_candidate).
- do_get: `src/act_obj.c:210` (lexical_call_candidate).
- do_get: `src/act_obj.c:246` (lexical_call_candidate).
- do_get: `src/act_obj.c:257` (lexical_call_candidate).
- do_get: `src/act_obj.c:270` (lexical_call_candidate).
- do_get: `src/act_obj.c:282` (lexical_call_candidate).
- do_get: `src/act_obj.c:320` (lexical_call_candidate).
- do_put: `src/act_obj.c:360` (lexical_call_candidate).
- do_put: `src/act_obj.c:366` (lexical_call_candidate).
- do_put: `src/act_obj.c:378` (lexical_call_candidate).
- do_put: `src/act_obj.c:393` (lexical_call_candidate).
- do_put: `src/act_obj.c:399` (lexical_call_candidate).
- do_put: `src/act_obj.c:405` (lexical_call_candidate).
- do_put: `src/act_obj.c:411` (lexical_call_candidate).
- do_put: `src/act_obj.c:419` (lexical_call_candidate).
- do_drop: `src/act_obj.c:501` (lexical_call_candidate).
- do_drop: `src/act_obj.c:516` (lexical_call_candidate).
- do_drop: `src/act_obj.c:525` (lexical_call_candidate).
- do_drop: `src/act_obj.c:537` (lexical_call_candidate).
- do_drop: `src/act_obj.c:581` (lexical_call_candidate).
- do_drop: `src/act_obj.c:590` (lexical_call_candidate).
- do_drop: `src/act_obj.c:596` (lexical_call_candidate).
- do_give: `src/act_obj.c:667` (lexical_call_candidate).
- do_give: `src/act_obj.c:682` (lexical_call_candidate).
- do_give: `src/act_obj.c:691` (lexical_call_candidate).
- do_give: `src/act_obj.c:697` (lexical_call_candidate).
- do_give: `src/act_obj.c:703` (lexical_call_candidate).
- do_give: `src/act_obj.c:769` (lexical_call_candidate).
- do_give: `src/act_obj.c:775` (lexical_call_candidate).
- do_give: `src/act_obj.c:781` (lexical_call_candidate).
- do_give: `src/act_obj.c:795` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:836` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:844` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:850` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:899` (lexical_call_candidate).
- do_fill: `src/act_obj.c:953` (lexical_call_candidate).
- do_fill: `src/act_obj.c:959` (lexical_call_candidate).
- do_fill: `src/act_obj.c:976` (lexical_call_candidate).
- do_fill: `src/act_obj.c:982` (lexical_call_candidate).
- do_fill: `src/act_obj.c:988` (lexical_call_candidate).
- do_fill: `src/act_obj.c:994` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1020` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1027` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1033` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1041` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1063` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1071` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1078` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1084` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1090` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1155` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1163` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1170` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1177` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1192` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1209` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1228` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1230` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1232` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1240` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1267` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1273` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1281` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1287` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1307` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1309` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1318` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1384` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1425` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1454` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1567` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1582` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1603` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1611` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1666` (lexical_call_candidate).
- do_wear: `src/act_obj.c:1682` (lexical_call_candidate).
- do_wear: `src/act_obj.c:1702` (lexical_call_candidate).
- do_remove: `src/act_obj.c:1723` (lexical_call_candidate).
- do_remove: `src/act_obj.c:1729` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1758` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1766` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1774` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1804` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1810` (lexical_call_candidate).
- do_quaff: `src/act_obj.c:1849` (lexical_call_candidate).
- do_quaff: `src/act_obj.c:1855` (lexical_call_candidate).
- do_quaff: `src/act_obj.c:1861` (lexical_call_candidate).
- do_quaff: `src/act_obj.c:1867` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1897` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1903` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1909` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1924` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1934` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:1961` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:1967` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2051` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2057` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2063` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2076` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2085` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2148` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2154` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2160` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2170` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2193` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2233` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2253` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2269` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2276` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2284` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2290` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2296` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2304` (lexical_call_candidate).
- find_keeper: `src/act_obj.c:2328` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2511` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2538` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2549` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2555` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2563` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2569` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2580` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2608` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2684` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2690` (lexical_call_candidate).
- do_list: `src/act_obj.c:2763` (lexical_call_candidate).
- do_list: `src/act_obj.c:2775` (lexical_call_candidate).
- do_list: `src/act_obj.c:2781` (lexical_call_candidate).
- do_list: `src/act_obj.c:2785` (lexical_call_candidate).
- do_list: `src/act_obj.c:2812` (lexical_call_candidate).
- do_list: `src/act_obj.c:2833` (lexical_call_candidate).
- do_list: `src/act_obj.c:2838` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2857` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2874` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2901` (lexical_call_candidate).
- do_value: `src/act_obj.c:2949` (lexical_call_candidate).
- do_value: `src/act_obj.c:2972` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:58` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:63` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:71` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:78` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:100` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:101` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:121` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:122` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:130` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:138` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:146` (lexical_call_candidate).
- wiznet: `src/act_wiz.c:169` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:189` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:194` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:200` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:201` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:208` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:215` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:217` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:223` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:239` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:290` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:304` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:310` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:316` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:323` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:325` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:332` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:334` (lexical_call_candidate).
- do_smote: `src/act_wiz.c:352` (lexical_call_candidate).
- do_smote: `src/act_wiz.c:358` (lexical_call_candidate).
- do_smote: `src/act_wiz.c:364` (lexical_call_candidate).
- do_smote: `src/act_wiz.c:368` (lexical_call_candidate).
- do_smote: `src/act_wiz.c:369` (lexical_call_candidate).
- do_smote: `src/act_wiz.c:378` (lexical_call_candidate).
- do_smote: `src/act_wiz.c:379` (lexical_call_candidate).
- do_smote: `src/act_wiz.c:429` (lexical_call_candidate).
- do_smote: `src/act_wiz.c:430` (lexical_call_candidate).
- do_bamfin: `src/act_wiz.c:447` (lexical_call_candidate).
- do_bamfin: `src/act_wiz.c:453` (lexical_call_candidate).
- do_bamfin: `src/act_wiz.c:461` (lexical_call_candidate).
- do_bamfout: `src/act_wiz.c:477` (lexical_call_candidate).
- do_bamfout: `src/act_wiz.c:483` (lexical_call_candidate).
- do_bamfout: `src/act_wiz.c:491` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:506` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:512` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:518` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:524` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:529` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:532` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:551` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:565` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:573` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:588` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:594` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:611` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:617` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:623` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:632` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:633` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:643` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:644` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:649` (lexical_call_candidate).
- do_echo: `src/act_wiz.c:661` (lexical_call_candidate).
- do_echo: `src/act_wiz.c:670` (lexical_call_candidate).
- do_echo: `src/act_wiz.c:671` (lexical_call_candidate).
- do_echo: `src/act_wiz.c:672` (lexical_call_candidate).
- do_recho: `src/act_wiz.c:687` (lexical_call_candidate).
- do_recho: `src/act_wiz.c:698` (lexical_call_candidate).
- do_recho: `src/act_wiz.c:699` (lexical_call_candidate).
- do_recho: `src/act_wiz.c:700` (lexical_call_candidate).
- do_zecho: `src/act_wiz.c:713` (lexical_call_candidate).
- do_zecho: `src/act_wiz.c:724` (lexical_call_candidate).
- do_zecho: `src/act_wiz.c:725` (lexical_call_candidate).
- do_zecho: `src/act_wiz.c:726` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:740` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:746` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:751` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:753` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:754` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:755` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:756` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:757` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:793` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:825` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:832` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:839` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:845` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:858` (lexical_call_candidate).
- do_at: `src/act_wiz.c:875` (lexical_call_candidate).
- do_at: `src/act_wiz.c:881` (lexical_call_candidate).
- do_at: `src/act_wiz.c:888` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:926` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:932` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:943` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:987` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:993` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:999` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1049` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1050` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1051` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1052` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1053` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1098` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1114` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1121` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1128` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1137` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1143` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1149` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1152` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1154` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1156` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1159` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1164` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1166` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1170` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1173` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1175` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1177` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1195` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1215` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1221` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1227` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1232` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1236` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1240` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1245` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1249` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1259` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1264` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1274` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1278` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1279` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1280` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1285` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1286` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1287` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1292` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1293` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1294` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1299` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1300` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1301` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1304` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1311` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1315` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1316` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1317` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1320` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1327` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1332` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1336` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1339` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1342` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1345` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1348` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1351` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1354` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1357` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1360` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1363` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1374` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1379` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1385` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1393` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1399` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1404` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1414` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1418` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1420` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1425` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1427` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1430` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1437` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1442` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1476` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1485` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1515` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1535` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1541` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1547` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1557` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1563` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1578` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1585` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1593` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1598` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1605` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1612` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1616` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1626` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1631` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1642` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1646` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1651` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1657` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1663` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1669` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1675` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1680` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1686` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1693` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1698` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1704` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1718` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1735` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1736` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1737` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1738` (lexical_call_candidate).
- do_mfind: `src/act_wiz.c:1779` (lexical_call_candidate).
- do_mfind: `src/act_wiz.c:1803` (lexical_call_candidate).
- do_mfind: `src/act_wiz.c:1809` (lexical_call_candidate).
- do_ofind: `src/act_wiz.c:1830` (lexical_call_candidate).
- do_ofind: `src/act_wiz.c:1854` (lexical_call_candidate).
- do_ofind: `src/act_wiz.c:1860` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1883` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1919` (lexical_call_candidate).
- do_reboo: `src/act_wiz.c:1999` (lexical_call_candidate).
- do_shutdow: `src/act_wiz.c:2033` (lexical_call_candidate).
- do_protect: `src/act_wiz.c:2070` (lexical_call_candidate).
- do_protect: `src/act_wiz.c:2076` (lexical_call_candidate).
- do_protect: `src/act_wiz.c:2083` (lexical_call_candidate).
- do_protect: `src/act_wiz.c:2089` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2107` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2113` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2119` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2125` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2138` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2145` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2152` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2162` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2172` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2187` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2196` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2202` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2208` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2214` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2221` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2227` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2243` (lexical_call_candidate).
- do_return: `src/act_wiz.c:2258` (lexical_call_candidate).
- do_return: `src/act_wiz.c:2262` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2323` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2333` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2343` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2353` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2365` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2391` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2401` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2439` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2440` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2441` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2472` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2478` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2487` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2505` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2515` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2521` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2528` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2539` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2577` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2583` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2592` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2598` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2600` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2637` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2643` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2649` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2656` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2662` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2677` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2678` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2694` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2695` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2704` (lexical_call_candidate).
- do_trust: `src/act_wiz.c:2727` (lexical_call_candidate).
- do_trust: `src/act_wiz.c:2733` (lexical_call_candidate).
- do_trust: `src/act_wiz.c:2740` (lexical_call_candidate).
- do_trust: `src/act_wiz.c:2746` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2786` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2815` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2821` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2838` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2852` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2858` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2864` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2870` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2877` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2878` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2885` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2886` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2907` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2916` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2921` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2928` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2934` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2944` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2949` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2966` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2972` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2979` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2986` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2987` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2994` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2995` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3014` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3020` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3026` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3032` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3039` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3040` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3047` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3048` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3067` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3073` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3079` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3086` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3087` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3094` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3095` (lexical_call_candidate).
- do_peace: `src/act_wiz.c:3117` (lexical_call_candidate).
- do_wizlock: `src/act_wiz.c:3129` (lexical_call_candidate).
- do_wizlock: `src/act_wiz.c:3134` (lexical_call_candidate).
- do_newlock: `src/act_wiz.c:3150` (lexical_call_candidate).
- do_newlock: `src/act_wiz.c:3155` (lexical_call_candidate).
- do_slookup: `src/act_wiz.c:3171` (lexical_call_candidate).
- do_slookup: `src/act_wiz.c:3183` (lexical_call_candidate).
- do_slookup: `src/act_wiz.c:3190` (lexical_call_candidate).
- do_slookup: `src/act_wiz.c:3196` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3212` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3213` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3214` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3215` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3216` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3264` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3265` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3266` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3267` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3273` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3279` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3287` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3296` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3303` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3340` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3341` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3342` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3343` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3344` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3345` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3351` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3373` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3388` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3402` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3417` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3432` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3444` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3459` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3477` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3489` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3496` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3519` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3532` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3545` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3558` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3569` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3580` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3591` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3597` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3609` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3615` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3627` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3633` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3645` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3651` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3667` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3673` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3685` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3717` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3718` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3719` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3720` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3721` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3729` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3742` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3776` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3788` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3794` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3808` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3840` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3879` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3880` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3881` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3882` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3883` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3889` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:3991` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:3992` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:3993` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:3994` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:4000` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:4007` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:4016` (lexical_call_candidate).
- do_sockets: `src/act_wiz.c:4075` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4100` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4108` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4121` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4143` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4166` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4188` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4194` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4202` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4208` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4214` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4222` (lexical_call_candidate).
- do_invis: `src/act_wiz.c:4246` (lexical_call_candidate).
- do_invis: `src/act_wiz.c:4252` (lexical_call_candidate).
- do_invis: `src/act_wiz.c:4260` (lexical_call_candidate).
- do_invis: `src/act_wiz.c:4268` (lexical_call_candidate).
- do_incognito: `src/act_wiz.c:4291` (lexical_call_candidate).
- do_incognito: `src/act_wiz.c:4297` (lexical_call_candidate).
- do_incognito: `src/act_wiz.c:4305` (lexical_call_candidate).
- do_incognito: `src/act_wiz.c:4313` (lexical_call_candidate).
- do_holylight: `src/act_wiz.c:4330` (lexical_call_candidate).
- do_holylight: `src/act_wiz.c:4335` (lexical_call_candidate).
- do_prefi: `src/act_wiz.c:4345` (lexical_call_candidate).
- do_prefix: `src/act_wiz.c:4357` (lexical_call_candidate).
- do_prefix: `src/act_wiz.c:4361` (lexical_call_candidate).
- substitute_alias: `src/alias.c:52` (lexical_call_candidate).
- substitute_alias: `src/alias.c:87` (lexical_call_candidate).
- do_alia: `src/alias.c:100` (lexical_call_candidate).
- do_alias: `src/alias.c:128` (lexical_call_candidate).
- do_alias: `src/alias.c:131` (lexical_call_candidate).
- do_alias: `src/alias.c:141` (lexical_call_candidate).
- do_alias: `src/alias.c:148` (lexical_call_candidate).
- do_alias: `src/alias.c:164` (lexical_call_candidate).
- do_alias: `src/alias.c:169` (lexical_call_candidate).
- do_alias: `src/alias.c:175` (lexical_call_candidate).
- do_alias: `src/alias.c:189` (lexical_call_candidate).
- do_alias: `src/alias.c:196` (lexical_call_candidate).
- do_alias: `src/alias.c:204` (lexical_call_candidate).
- do_unalias: `src/alias.c:227` (lexical_call_candidate).
- do_unalias: `src/alias.c:247` (lexical_call_candidate).
- do_unalias: `src/alias.c:257` (lexical_call_candidate).
- ban_site: `src/ban.c:153` (lexical_call_candidate).
- ban_site: `src/ban.c:188` (lexical_call_candidate).
- ban_site: `src/ban.c:209` (lexical_call_candidate).
- ban_site: `src/ban.c:220` (lexical_call_candidate).
- ban_site: `src/ban.c:252` (lexical_call_candidate).
- do_allow: `src/ban.c:277` (lexical_call_candidate).
- do_allow: `src/ban.c:288` (lexical_call_candidate).
- do_allow: `src/ban.c:299` (lexical_call_candidate).
- do_allow: `src/ban.c:305` (lexical_call_candidate).
- bust_a_prompt: `src/comm.c:1336` (lexical_call_candidate).
- bust_a_prompt: `src/comm.c:1342` (lexical_call_candidate).
- nanny: `src/comm.c:2004` (lexical_call_candidate).
- nanny: `src/comm.c:2010` (lexical_call_candidate).
- nanny: `src/comm.c:2019` (lexical_call_candidate).
- nanny: `src/comm.c:2024` (lexical_call_candidate).
- nanny: `src/comm.c:2031` (lexical_call_candidate).
- nanny: `src/comm.c:2049` (lexical_call_candidate).
- nanny: `src/comm.c:2100` (lexical_call_candidate).
- nanny: `src/comm.c:2102` (lexical_call_candidate).
- check_reconnect: `src/comm.c:2268` (lexical_call_candidate).
- page_to_char: `src/comm.c:2354` (lexical_call_candidate).
- page_to_char: `src/comm.c:2359` (lexical_call_candidate).
- do_areas: `src/db.c:2735` (lexical_call_candidate).
- do_areas: `src/db.c:2749` (lexical_call_candidate).
- do_memory: `src/db.c:2764` (lexical_call_candidate).
- do_memory: `src/db.c:2765` (lexical_call_candidate).
- do_memory: `src/db.c:2766` (lexical_call_candidate).
- do_memory: `src/db.c:2767` (lexical_call_candidate).
- do_memory: `src/db.c:2768` (lexical_call_candidate).
- do_memory: `src/db.c:2769` (lexical_call_candidate).
- do_memory: `src/db.c:2771` (lexical_call_candidate).
- do_memory: `src/db.c:2772` (lexical_call_candidate).
- do_memory: `src/db.c:2774` (lexical_call_candidate).
- do_memory: `src/db.c:2775` (lexical_call_candidate).
- do_memory: `src/db.c:2776` (lexical_call_candidate).
- do_memory: `src/db.c:2777` (lexical_call_candidate).
- do_memory: `src/db.c:2781` (lexical_call_candidate).
- do_memory: `src/db.c:2785` (lexical_call_candidate).
- append_file: `src/db.c:3268` (lexical_call_candidate).
- poison_effect: `src/effects.c:469` (lexical_call_candidate).
- shock_effect: `src/effects.c:557` (lexical_call_candidate).
- one_hit: `src/fight.c:601` (lexical_call_candidate).
- damage: `src/fight.c:695` (lexical_call_candidate).
- damage: `src/fight.c:822` (lexical_call_candidate).
- damage: `src/fight.c:830` (lexical_call_candidate).
- damage: `src/fight.c:838` (lexical_call_candidate).
- damage: `src/fight.c:844` (lexical_call_candidate).
- damage: `src/fight.c:849` (lexical_call_candidate).
- damage: `src/fight.c:851` (lexical_call_candidate).
- is_safe: `src/fight.c:1008` (lexical_call_candidate).
- is_safe: `src/fight.c:1014` (lexical_call_candidate).
- is_safe: `src/fight.c:1024` (lexical_call_candidate).
- is_safe: `src/fight.c:1041` (lexical_call_candidate).
- is_safe: `src/fight.c:1055` (lexical_call_candidate).
- is_safe: `src/fight.c:1063` (lexical_call_candidate).
- is_safe: `src/fight.c:1072` (lexical_call_candidate).
- is_safe: `src/fight.c:1081` (lexical_call_candidate).
- is_safe: `src/fight.c:1087` (lexical_call_candidate).
- check_killer: `src/fight.c:1250` (lexical_call_candidate).
- group_gain: `src/fight.c:1753` (lexical_call_candidate).
- do_berserk: `src/fight.c:2130` (lexical_call_candidate).
- do_berserk: `src/fight.c:2137` (lexical_call_candidate).
- do_berserk: `src/fight.c:2143` (lexical_call_candidate).
- do_berserk: `src/fight.c:2149` (lexical_call_candidate).
- do_berserk: `src/fight.c:2175` (lexical_call_candidate).
- do_berserk: `src/fight.c:2203` (lexical_call_candidate).
- do_bash: `src/fight.c:2221` (lexical_call_candidate).
- do_bash: `src/fight.c:2230` (lexical_call_candidate).
- do_bash: `src/fight.c:2237` (lexical_call_candidate).
- do_bash: `src/fight.c:2249` (lexical_call_candidate).
- do_bash: `src/fight.c:2260` (lexical_call_candidate).
- do_dirt: `src/fight.c:2352` (lexical_call_candidate).
- do_dirt: `src/fight.c:2361` (lexical_call_candidate).
- do_dirt: `src/fight.c:2368` (lexical_call_candidate).
- do_dirt: `src/fight.c:2380` (lexical_call_candidate).
- do_dirt: `src/fight.c:2391` (lexical_call_candidate).
- do_dirt: `src/fight.c:2438` (lexical_call_candidate).
- do_dirt: `src/fight.c:2449` (lexical_call_candidate).
- do_trip: `src/fight.c:2485` (lexical_call_candidate).
- do_trip: `src/fight.c:2495` (lexical_call_candidate).
- do_trip: `src/fight.c:2502` (lexical_call_candidate).
- do_trip: `src/fight.c:2513` (lexical_call_candidate).
- do_trip: `src/fight.c:2531` (lexical_call_candidate).
- do_kill: `src/fight.c:2597` (lexical_call_candidate).
- do_kill: `src/fight.c:2603` (lexical_call_candidate).
- do_kill: `src/fight.c:2619` (lexical_call_candidate).
- do_kill: `src/fight.c:2630` (lexical_call_candidate).
- do_kill: `src/fight.c:2642` (lexical_call_candidate).
- do_murde: `src/fight.c:2656` (lexical_call_candidate).
- do_murder: `src/fight.c:2672` (lexical_call_candidate).
- do_murder: `src/fight.c:2681` (lexical_call_candidate).
- do_murder: `src/fight.c:2687` (lexical_call_candidate).
- do_murder: `src/fight.c:2698` (lexical_call_candidate).
- do_murder: `src/fight.c:2710` (lexical_call_candidate).
- do_backstab: `src/fight.c:2737` (lexical_call_candidate).
- do_backstab: `src/fight.c:2743` (lexical_call_candidate).
- do_backstab: `src/fight.c:2749` (lexical_call_candidate).
- do_backstab: `src/fight.c:2755` (lexical_call_candidate).
- do_backstab: `src/fight.c:2766` (lexical_call_candidate).
- do_backstab: `src/fight.c:2772` (lexical_call_candidate).
- do_flee: `src/fight.c:2813` (lexical_call_candidate).
- do_flee: `src/fight.c:2842` (lexical_call_candidate).
- do_flee: `src/fight.c:2845` (lexical_call_candidate).
- do_flee: `src/fight.c:2848` (lexical_call_candidate).
- do_flee: `src/fight.c:2857` (lexical_call_candidate).
- do_rescue: `src/fight.c:2872` (lexical_call_candidate).
- do_rescue: `src/fight.c:2878` (lexical_call_candidate).
- do_rescue: `src/fight.c:2884` (lexical_call_candidate).
- do_rescue: `src/fight.c:2890` (lexical_call_candidate).
- do_rescue: `src/fight.c:2896` (lexical_call_candidate).
- do_rescue: `src/fight.c:2902` (lexical_call_candidate).
- do_rescue: `src/fight.c:2908` (lexical_call_candidate).
- do_rescue: `src/fight.c:2915` (lexical_call_candidate).
- do_kick: `src/fight.c:2943` (lexical_call_candidate).
- do_kick: `src/fight.c:2953` (lexical_call_candidate).
- do_disarm: `src/fight.c:2985` (lexical_call_candidate).
- do_disarm: `src/fight.c:2993` (lexical_call_candidate).
- do_disarm: `src/fight.c:2999` (lexical_call_candidate).
- do_disarm: `src/fight.c:3005` (lexical_call_candidate).
- do_sla: `src/fight.c:3054` (lexical_call_candidate).
- do_slay: `src/fight.c:3068` (lexical_call_candidate).
- do_slay: `src/fight.c:3074` (lexical_call_candidate).
- do_slay: `src/fight.c:3080` (lexical_call_candidate).
- do_slay: `src/fight.c:3086` (lexical_call_candidate).
- do_flag: `src/flags.c:63` (lexical_call_candidate).
- do_flag: `src/flags.c:64` (lexical_call_candidate).
- do_flag: `src/flags.c:65` (lexical_call_candidate).
- do_flag: `src/flags.c:66` (lexical_call_candidate).
- do_flag: `src/flags.c:67` (lexical_call_candidate).
- do_flag: `src/flags.c:68` (lexical_call_candidate).
- do_flag: `src/flags.c:69` (lexical_call_candidate).
- do_flag: `src/flags.c:75` (lexical_call_candidate).
- do_flag: `src/flags.c:81` (lexical_call_candidate).
- do_flag: `src/flags.c:87` (lexical_call_candidate).
- do_flag: `src/flags.c:96` (lexical_call_candidate).
- do_flag: `src/flags.c:105` (lexical_call_candidate).
- do_flag: `src/flags.c:117` (lexical_call_candidate).
- do_flag: `src/flags.c:153` (lexical_call_candidate).
- do_flag: `src/flags.c:165` (lexical_call_candidate).
- do_flag: `src/flags.c:177` (lexical_call_candidate).
- do_flag: `src/flags.c:187` (lexical_call_candidate).
- do_flag: `src/flags.c:208` (lexical_call_candidate).
- char_to_room: `src/handler.c:1447` (lexical_call_candidate).
- do_heal: `src/healer.c:58` (lexical_call_candidate).
- do_heal: `src/healer.c:68` (lexical_call_candidate).
- do_heal: `src/healer.c:69` (lexical_call_candidate).
- do_heal: `src/healer.c:70` (lexical_call_candidate).
- do_heal: `src/healer.c:71` (lexical_call_candidate).
- do_heal: `src/healer.c:72` (lexical_call_candidate).
- do_heal: `src/healer.c:73` (lexical_call_candidate).
- do_heal: `src/healer.c:74` (lexical_call_candidate).
- do_heal: `src/healer.c:75` (lexical_call_candidate).
- do_heal: `src/healer.c:76` (lexical_call_candidate).
- do_heal: `src/healer.c:77` (lexical_call_candidate).
- do_heal: `src/healer.c:78` (lexical_call_candidate).
- do_heal: `src/healer.c:188` (lexical_call_candidate).
- interpret: `src/interp.c:393` (lexical_call_candidate).
- interpret: `src/interp.c:460` (lexical_call_candidate).
- interpret: `src/interp.c:472` (lexical_call_candidate).
- interpret: `src/interp.c:477` (lexical_call_candidate).
- interpret: `src/interp.c:481` (lexical_call_candidate).
- interpret: `src/interp.c:485` (lexical_call_candidate).
- interpret: `src/interp.c:489` (lexical_call_candidate).
- interpret: `src/interp.c:493` (lexical_call_candidate).
- interpret: `src/interp.c:497` (lexical_call_candidate).
- check_social: `src/interp.c:551` (lexical_call_candidate).
- check_social: `src/interp.c:558` (lexical_call_candidate).
- check_social: `src/interp.c:563` (lexical_call_candidate).
- check_social: `src/interp.c:567` (lexical_call_candidate).
- check_social: `src/interp.c:577` (lexical_call_candidate).
- check_social: `src/interp.c:591` (lexical_call_candidate).
- do_commands: `src/interp.c:761` (lexical_call_candidate).
- do_commands: `src/interp.c:763` (lexical_call_candidate).
- do_commands: `src/interp.c:768` (lexical_call_candidate).
- do_wizhelp: `src/interp.c:786` (lexical_call_candidate).
- do_wizhelp: `src/interp.c:788` (lexical_call_candidate).
- do_wizhelp: `src/interp.c:793` (lexical_call_candidate).
- check_dispel: `src/magic.c:269` (lexical_call_candidate).
- check_dispel: `src/magic.c:270` (lexical_call_candidate).
- do_cast: `src/magic.c:319` (lexical_call_candidate).
- do_cast: `src/magic.c:328` (lexical_call_candidate).
- do_cast: `src/magic.c:334` (lexical_call_candidate).
- do_cast: `src/magic.c:367` (lexical_call_candidate).
- do_cast: `src/magic.c:375` (lexical_call_candidate).
- do_cast: `src/magic.c:393` (lexical_call_candidate).
- do_cast: `src/magic.c:401` (lexical_call_candidate).
- do_cast: `src/magic.c:419` (lexical_call_candidate).
- do_cast: `src/magic.c:431` (lexical_call_candidate).
- do_cast: `src/magic.c:442` (lexical_call_candidate).
- do_cast: `src/magic.c:448` (lexical_call_candidate).
- do_cast: `src/magic.c:461` (lexical_call_candidate).
- do_cast: `src/magic.c:476` (lexical_call_candidate).
- do_cast: `src/magic.c:482` (lexical_call_candidate).
- do_cast: `src/magic.c:499` (lexical_call_candidate).
- do_cast: `src/magic.c:522` (lexical_call_candidate).
- do_cast: `src/magic.c:530` (lexical_call_candidate).
- do_cast: `src/magic.c:541` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:612` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:617` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:635` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:648` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:656` (lexical_call_candidate).
- spell_armor: `src/magic.c:746` (lexical_call_candidate).
- spell_armor: `src/magic.c:759` (lexical_call_candidate).
- spell_bless: `src/magic.c:827` (lexical_call_candidate).
- spell_bless: `src/magic.c:845` (lexical_call_candidate).
- spell_blindness: `src/magic.c:870` (lexical_call_candidate).
- spell_call_lightning: `src/magic.c:910` (lexical_call_candidate).
- spell_call_lightning: `src/magic.c:916` (lexical_call_candidate).
- spell_call_lightning: `src/magic.c:922` (lexical_call_candidate).
- spell_call_lightning: `src/magic.c:942` (lexical_call_candidate).
- spell_calm: `src/magic.c:991` (lexical_call_candidate).
- spell_cancellation: `src/magic.c:1026` (lexical_call_candidate).
- spell_cancellation: `src/magic.c:1177` (lexical_call_candidate).
- spell_cancellation: `src/magic.c:1179` (lexical_call_candidate).
- spell_chain_lightning: `src/magic.c:1265` (lexical_call_candidate).
- spell_change_sex: `src/magic.c:1287` (lexical_call_candidate).
- spell_change_sex: `src/magic.c:1306` (lexical_call_candidate).
- spell_charm_person: `src/magic.c:1322` (lexical_call_candidate).
- spell_charm_person: `src/magic.c:1336` (lexical_call_candidate).
- spell_continual_light: `src/magic.c:1441` (lexical_call_candidate).
- spell_control_weather: `src/magic.c:1472` (lexical_call_candidate).
- spell_control_weather: `src/magic.c:1474` (lexical_call_candidate).
- spell_create_rose: `src/magic.c:1498` (lexical_call_candidate).
- spell_create_water: `src/magic.c:1524` (lexical_call_candidate).
- spell_create_water: `src/magic.c:1530` (lexical_call_candidate).
- spell_cure_blindness: `src/magic.c:1566` (lexical_call_candidate).
- spell_cure_blindness: `src/magic.c:1574` (lexical_call_candidate).
- spell_cure_blindness: `src/magic.c:1578` (lexical_call_candidate).
- spell_cure_critical: `src/magic.c:1591` (lexical_call_candidate).
- spell_cure_critical: `src/magic.c:1593` (lexical_call_candidate).
- spell_cure_disease: `src/magic.c:1605` (lexical_call_candidate).
- spell_cure_disease: `src/magic.c:1613` (lexical_call_candidate).
- spell_cure_disease: `src/magic.c:1617` (lexical_call_candidate).
- spell_cure_light: `src/magic.c:1630` (lexical_call_candidate).
- spell_cure_light: `src/magic.c:1632` (lexical_call_candidate).
- spell_cure_poison: `src/magic.c:1645` (lexical_call_candidate).
- spell_cure_poison: `src/magic.c:1653` (lexical_call_candidate).
- spell_cure_poison: `src/magic.c:1657` (lexical_call_candidate).
- spell_cure_serious: `src/magic.c:1668` (lexical_call_candidate).
- spell_cure_serious: `src/magic.c:1670` (lexical_call_candidate).
- spell_curse: `src/magic.c:1747` (lexical_call_candidate).
- spell_demonfire: `src/magic.c:1763` (lexical_call_candidate).
- spell_demonfire: `src/magic.c:1774` (lexical_call_candidate).
- spell_detect_evil: `src/magic.c:1791` (lexical_call_candidate).
- spell_detect_evil: `src/magic.c:1804` (lexical_call_candidate).
- spell_detect_evil: `src/magic.c:1806` (lexical_call_candidate).
- spell_detect_good: `src/magic.c:1819` (lexical_call_candidate).
- spell_detect_good: `src/magic.c:1832` (lexical_call_candidate).
- spell_detect_good: `src/magic.c:1834` (lexical_call_candidate).
- spell_detect_hidden: `src/magic.c:1848` (lexical_call_candidate).
- spell_detect_hidden: `src/magic.c:1861` (lexical_call_candidate).
- spell_detect_hidden: `src/magic.c:1863` (lexical_call_candidate).
- spell_detect_invis: `src/magic.c:1877` (lexical_call_candidate).
- spell_detect_invis: `src/magic.c:1891` (lexical_call_candidate).
- spell_detect_invis: `src/magic.c:1893` (lexical_call_candidate).
- spell_detect_magic: `src/magic.c:1907` (lexical_call_candidate).
- spell_detect_magic: `src/magic.c:1921` (lexical_call_candidate).
- spell_detect_magic: `src/magic.c:1923` (lexical_call_candidate).
- spell_detect_poison: `src/magic.c:1936` (lexical_call_candidate).
- spell_detect_poison: `src/magic.c:1938` (lexical_call_candidate).
- spell_detect_poison: `src/magic.c:1942` (lexical_call_candidate).
- spell_dispel_magic: `src/magic.c:2021` (lexical_call_candidate).
- spell_dispel_magic: `src/magic.c:2022` (lexical_call_candidate).
- spell_dispel_magic: `src/magic.c:2182` (lexical_call_candidate).
- spell_dispel_magic: `src/magic.c:2184` (lexical_call_candidate).
- spell_earthquake: `src/magic.c:2193` (lexical_call_candidate).
- spell_earthquake: `src/magic.c:2213` (lexical_call_candidate).
- spell_enchant_armor: `src/magic.c:2229` (lexical_call_candidate).
- spell_enchant_armor: `src/magic.c:2235` (lexical_call_candidate).
- spell_enchant_armor: `src/magic.c:2316` (lexical_call_candidate).
- spell_enchant_weapon: `src/magic.c:2407` (lexical_call_candidate).
- spell_enchant_weapon: `src/magic.c:2413` (lexical_call_candidate).
- spell_enchant_weapon: `src/magic.c:2509` (lexical_call_candidate).
- spell_energy_drain: `src/magic.c:2633` (lexical_call_candidate).
- spell_energy_drain: `src/magic.c:2651` (lexical_call_candidate).
- spell_energy_drain: `src/magic.c:2652` (lexical_call_candidate).
- spell_faerie_fire: `src/magic.c:2740` (lexical_call_candidate).
- spell_faerie_fog: `src/magic.c:2752` (lexical_call_candidate).
- spell_faerie_fog: `src/magic.c:2769` (lexical_call_candidate).
- spell_floating_disc: `src/magic.c:2792` (lexical_call_candidate).
- spell_fly: `src/magic.c:2807` (lexical_call_candidate).
- spell_fly: `src/magic.c:2820` (lexical_call_candidate).
- spell_frenzy: `src/magic.c:2835` (lexical_call_candidate).
- spell_frenzy: `src/magic.c:2844` (lexical_call_candidate).
- spell_frenzy: `src/magic.c:2877` (lexical_call_candidate).
- spell_gate: `src/magic.c:2903` (lexical_call_candidate).
- spell_gate: `src/magic.c:2912` (lexical_call_candidate).
- spell_gate: `src/magic.c:2922` (lexical_call_candidate).
- spell_giant_strength: `src/magic.c:2940` (lexical_call_candidate).
- spell_giant_strength: `src/magic.c:2954` (lexical_call_candidate).
- spell_haste: `src/magic.c:2985` (lexical_call_candidate).
- spell_haste: `src/magic.c:2997` (lexical_call_candidate).
- spell_haste: `src/magic.c:2998` (lexical_call_candidate).
- spell_haste: `src/magic.c:3016` (lexical_call_candidate).
- spell_haste: `src/magic.c:3019` (lexical_call_candidate).
- spell_heal: `src/magic.c:3030` (lexical_call_candidate).
- spell_heal: `src/magic.c:3032` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3117` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3127` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3161` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3162` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3185` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3195` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3206` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3217` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3224` (lexical_call_candidate).
- spell_identify: `src/magic.c:3245` (lexical_call_candidate).
- spell_identify: `src/magic.c:3253` (lexical_call_candidate).
- spell_identify: `src/magic.c:3257` (lexical_call_candidate).
- spell_identify: `src/magic.c:3258` (lexical_call_candidate).
- spell_identify: `src/magic.c:3259` (lexical_call_candidate).
- spell_identify: `src/magic.c:3264` (lexical_call_candidate).
- spell_identify: `src/magic.c:3265` (lexical_call_candidate).
- spell_identify: `src/magic.c:3266` (lexical_call_candidate).
- spell_identify: `src/magic.c:3271` (lexical_call_candidate).
- spell_identify: `src/magic.c:3272` (lexical_call_candidate).
- spell_identify: `src/magic.c:3273` (lexical_call_candidate).
- spell_identify: `src/magic.c:3278` (lexical_call_candidate).
- spell_identify: `src/magic.c:3279` (lexical_call_candidate).
- spell_identify: `src/magic.c:3280` (lexical_call_candidate).
- spell_identify: `src/magic.c:3283` (lexical_call_candidate).
- spell_identify: `src/magic.c:3290` (lexical_call_candidate).
- spell_identify: `src/magic.c:3294` (lexical_call_candidate).
- spell_identify: `src/magic.c:3295` (lexical_call_candidate).
- spell_identify: `src/magic.c:3296` (lexical_call_candidate).
- spell_identify: `src/magic.c:3299` (lexical_call_candidate).
- spell_identify: `src/magic.c:3306` (lexical_call_candidate).
- spell_identify: `src/magic.c:3312` (lexical_call_candidate).
- spell_identify: `src/magic.c:3317` (lexical_call_candidate).
- spell_identify: `src/magic.c:3322` (lexical_call_candidate).
- spell_identify: `src/magic.c:3325` (lexical_call_candidate).
- spell_identify: `src/magic.c:3326` (lexical_call_candidate).
- spell_identify: `src/magic.c:3327` (lexical_call_candidate).
- spell_identify: `src/magic.c:3328` (lexical_call_candidate).
- spell_identify: `src/magic.c:3329` (lexical_call_candidate).
- spell_identify: `src/magic.c:3330` (lexical_call_candidate).
- spell_identify: `src/magic.c:3331` (lexical_call_candidate).
- spell_identify: `src/magic.c:3332` (lexical_call_candidate).
- spell_identify: `src/magic.c:3333` (lexical_call_candidate).
- spell_identify: `src/magic.c:3334` (lexical_call_candidate).
- spell_identify: `src/magic.c:3344` (lexical_call_candidate).
- spell_identify: `src/magic.c:3348` (lexical_call_candidate).
- spell_identify: `src/magic.c:3356` (lexical_call_candidate).
- spell_identify: `src/magic.c:3367` (lexical_call_candidate).
- spell_identify: `src/magic.c:3397` (lexical_call_candidate).
- spell_identify: `src/magic.c:3408` (lexical_call_candidate).
- spell_identify: `src/magic.c:3413` (lexical_call_candidate).
- spell_identify: `src/magic.c:3447` (lexical_call_candidate).
- spell_infravision: `src/magic.c:3465` (lexical_call_candidate).
- spell_infravision: `src/magic.c:3480` (lexical_call_candidate).
- spell_invis: `src/magic.c:3532` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3637` (lexical_call_candidate).
- spell_mass_invis: `src/magic.c:3701` (lexical_call_candidate).
- spell_mass_invis: `src/magic.c:3712` (lexical_call_candidate).
- spell_null: `src/magic.c:3721` (lexical_call_candidate).
- spell_pass_door: `src/magic.c:3735` (lexical_call_candidate).
- spell_pass_door: `src/magic.c:3750` (lexical_call_candidate).
- spell_plague: `src/magic.c:3765` (lexical_call_candidate).
- spell_plague: `src/magic.c:3780` (lexical_call_candidate).
- spell_poison: `src/magic.c:3851` (lexical_call_candidate).
- spell_poison: `src/magic.c:3863` (lexical_call_candidate).
- spell_protection_evil: `src/magic.c:3879` (lexical_call_candidate).
- spell_protection_evil: `src/magic.c:3893` (lexical_call_candidate).
- spell_protection_good: `src/magic.c:3908` (lexical_call_candidate).
- spell_protection_good: `src/magic.c:3922` (lexical_call_candidate).
- spell_ray_of_truth: `src/magic.c:3937` (lexical_call_candidate).
- spell_ray_of_truth: `src/magic.c:3944` (lexical_call_candidate).
- spell_ray_of_truth: `src/magic.c:3952` (lexical_call_candidate).
- spell_recharge: `src/magic.c:3981` (lexical_call_candidate).
- spell_recharge: `src/magic.c:3987` (lexical_call_candidate).
- spell_recharge: `src/magic.c:3993` (lexical_call_candidate).
- spell_recharge: `src/magic.c:4037` (lexical_call_candidate).
- spell_refresh: `src/magic.c:4056` (lexical_call_candidate).
- spell_refresh: `src/magic.c:4058` (lexical_call_candidate).
- spell_refresh: `src/magic.c:4060` (lexical_call_candidate).
- spell_remove_curse: `src/magic.c:4098` (lexical_call_candidate).
- spell_sanctuary: `src/magic.c:4127` (lexical_call_candidate).
- spell_sanctuary: `src/magic.c:4142` (lexical_call_candidate).
- spell_shield: `src/magic.c:4156` (lexical_call_candidate).
- spell_shield: `src/magic.c:4171` (lexical_call_candidate).
- spell_sleep: `src/magic.c:4224` (lexical_call_candidate).
- spell_slow: `src/magic.c:4239` (lexical_call_candidate).
- spell_slow: `src/magic.c:4250` (lexical_call_candidate).
- spell_slow: `src/magic.c:4251` (lexical_call_candidate).
- spell_slow: `src/magic.c:4260` (lexical_call_candidate).
- spell_slow: `src/magic.c:4261` (lexical_call_candidate).
- spell_slow: `src/magic.c:4278` (lexical_call_candidate).
- spell_stone_skin: `src/magic.c:4294` (lexical_call_candidate).
- spell_stone_skin: `src/magic.c:4309` (lexical_call_candidate).
- spell_summon: `src/magic.c:4337` (lexical_call_candidate).
- spell_teleport: `src/magic.c:4364` (lexical_call_candidate).
- spell_teleport: `src/magic.c:4371` (lexical_call_candidate).
- spell_ventriloquate: `src/magic.c:4399` (lexical_call_candidate).
- spell_weaken: `src/magic.c:4423` (lexical_call_candidate).
- spell_word_of_recall: `src/magic.c:4442` (lexical_call_candidate).
- spell_word_of_recall: `src/magic.c:4449` (lexical_call_candidate).
- spell_farsight: `src/magic2.c:48` (lexical_call_candidate).
- spell_portal: `src/magic2.c:76` (lexical_call_candidate).
- spell_portal: `src/magic2.c:84` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:129` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:137` (lexical_call_candidate).
- do_play: `src/music.c:233` (lexical_call_candidate).
- do_play: `src/music.c:239` (lexical_call_candidate).
- do_play: `src/music.c:298` (lexical_call_candidate).
- do_play: `src/music.c:305` (lexical_call_candidate).
- do_play: `src/music.c:313` (lexical_call_candidate).
- do_play: `src/music.c:322` (lexical_call_candidate).
- do_play: `src/music.c:326` (lexical_call_candidate).
- do_unread: `src/note.c:87` (lexical_call_candidate).
- do_unread: `src/note.c:94` (lexical_call_candidate).
- do_unread: `src/note.c:101` (lexical_call_candidate).
- do_unread: `src/note.c:108` (lexical_call_candidate).
- do_unread: `src/note.c:115` (lexical_call_candidate).
- do_unread: `src/note.c:119` (lexical_call_candidate).
- parse_note: `src/note.c:607` (lexical_call_candidate).
- parse_note: `src/note.c:616` (lexical_call_candidate).
- parse_note: `src/note.c:627` (lexical_call_candidate).
- parse_note: `src/note.c:643` (lexical_call_candidate).
- parse_note: `src/note.c:651` (lexical_call_candidate).
- parse_note: `src/note.c:665` (lexical_call_candidate).
- parse_note: `src/note.c:674` (lexical_call_candidate).
- parse_note: `src/note.c:677` (lexical_call_candidate).
- parse_note: `src/note.c:680` (lexical_call_candidate).
- parse_note: `src/note.c:683` (lexical_call_candidate).
- parse_note: `src/note.c:686` (lexical_call_candidate).
- parse_note: `src/note.c:697` (lexical_call_candidate).
- parse_note: `src/note.c:708` (lexical_call_candidate).
- parse_note: `src/note.c:714` (lexical_call_candidate).
- parse_note: `src/note.c:722` (lexical_call_candidate).
- parse_note: `src/note.c:733` (lexical_call_candidate).
- parse_note: `src/note.c:739` (lexical_call_candidate).
- parse_note: `src/note.c:771` (lexical_call_candidate).
- parse_note: `src/note.c:780` (lexical_call_candidate).
- parse_note: `src/note.c:787` (lexical_call_candidate).
- parse_note: `src/note.c:799` (lexical_call_candidate).
- parse_note: `src/note.c:811` (lexical_call_candidate).
- parse_note: `src/note.c:818` (lexical_call_candidate).
- parse_note: `src/note.c:854` (lexical_call_candidate).
- parse_note: `src/note.c:861` (lexical_call_candidate).
- parse_note: `src/note.c:870` (lexical_call_candidate).
- parse_note: `src/note.c:876` (lexical_call_candidate).
- parse_note: `src/note.c:888` (lexical_call_candidate).
- parse_note: `src/note.c:896` (lexical_call_candidate).
- parse_note: `src/note.c:902` (lexical_call_candidate).
- parse_note: `src/note.c:911` (lexical_call_candidate).
- parse_note: `src/note.c:912` (lexical_call_candidate).
- parse_note: `src/note.c:922` (lexical_call_candidate).
- parse_note: `src/note.c:928` (lexical_call_candidate).
- parse_note: `src/note.c:934` (lexical_call_candidate).
- parse_note: `src/note.c:942` (lexical_call_candidate).
- parse_note: `src/note.c:957` (lexical_call_candidate).
- do_scan: `src/scan.c:61` (lexical_call_candidate).
- do_scan: `src/scan.c:77` (lexical_call_candidate).
- scan_char: `src/scan.c:125` (lexical_call_candidate).
- do_gain: `src/skills.c:63` (lexical_call_candidate).
- do_gain: `src/skills.c:83` (lexical_call_candidate).
- do_gain: `src/skills.c:95` (lexical_call_candidate).
- do_gain: `src/skills.c:97` (lexical_call_candidate).
- do_gain: `src/skills.c:101` (lexical_call_candidate).
- do_gain: `src/skills.c:103` (lexical_call_candidate).
- do_gain: `src/skills.c:109` (lexical_call_candidate).
- do_gain: `src/skills.c:122` (lexical_call_candidate).
- do_gain: `src/skills.c:124` (lexical_call_candidate).
- do_gain: `src/skills.c:128` (lexical_call_candidate).
- do_spells: `src/skills.c:277` (lexical_call_candidate).
- do_spells: `src/skills.c:285` (lexical_call_candidate).
- do_spells: `src/skills.c:294` (lexical_call_candidate).
- do_spells: `src/skills.c:304` (lexical_call_candidate).
- do_spells: `src/skills.c:310` (lexical_call_candidate).
- do_spells: `src/skills.c:362` (lexical_call_candidate).
- do_skills: `src/skills.c:397` (lexical_call_candidate).
- do_skills: `src/skills.c:405` (lexical_call_candidate).
- do_skills: `src/skills.c:414` (lexical_call_candidate).
- do_skills: `src/skills.c:424` (lexical_call_candidate).
- do_skills: `src/skills.c:430` (lexical_call_candidate).
- do_skills: `src/skills.c:479` (lexical_call_candidate).
- list_group_costs: `src/skills.c:504` (lexical_call_candidate).
- list_group_costs: `src/skills.c:517` (lexical_call_candidate).
- list_group_costs: `src/skills.c:519` (lexical_call_candidate).
- list_group_costs: `src/skills.c:523` (lexical_call_candidate).
- list_group_costs: `src/skills.c:524` (lexical_call_candidate).
- list_group_costs: `src/skills.c:529` (lexical_call_candidate).
- list_group_costs: `src/skills.c:543` (lexical_call_candidate).
- list_group_costs: `src/skills.c:545` (lexical_call_candidate).
- list_group_costs: `src/skills.c:549` (lexical_call_candidate).
- list_group_costs: `src/skills.c:550` (lexical_call_candidate).
- list_group_costs: `src/skills.c:553` (lexical_call_candidate).
- list_group_costs: `src/skills.c:556` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:572` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:584` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:586` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:590` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:591` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:596` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:608` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:610` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:614` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:615` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:618` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:621` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:687` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:697` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:703` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:711` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:717` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:731` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:738` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:746` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:751` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:759` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:767` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:774` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:790` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:798` (lexical_call_candidate).
- do_groups: `src/skills.c:855` (lexical_call_candidate).
- do_groups: `src/skills.c:857` (lexical_call_candidate).
- do_groups: `src/skills.c:861` (lexical_call_candidate).
- do_groups: `src/skills.c:863` (lexical_call_candidate).
- do_groups: `src/skills.c:874` (lexical_call_candidate).
- do_groups: `src/skills.c:876` (lexical_call_candidate).
- do_groups: `src/skills.c:879` (lexical_call_candidate).
- do_groups: `src/skills.c:888` (lexical_call_candidate).
- do_groups: `src/skills.c:889` (lexical_call_candidate).
- do_groups: `src/skills.c:899` (lexical_call_candidate).
- do_groups: `src/skills.c:901` (lexical_call_candidate).
- do_groups: `src/skills.c:904` (lexical_call_candidate).
- check_improve: `src/skills.c:941` (lexical_call_candidate).
- check_improve: `src/skills.c:955` (lexical_call_candidate).
- spec_patrolman: `src/special.c:288` (lexical_call_candidate).
- advance_level: `src/update.c:111` (lexical_call_candidate).
- gain_exp: `src/update.c:129` (lexical_call_candidate).
- gain_condition: `src/update.c:350` (lexical_call_candidate).
- gain_condition: `src/update.c:354` (lexical_call_candidate).
- gain_condition: `src/update.c:359` (lexical_call_candidate).
- weather_update: `src/update.c:595` (lexical_call_candidate).
- char_update: `src/update.c:693` (lexical_call_candidate).
- char_update: `src/update.c:726` (lexical_call_candidate).
- char_update: `src/update.c:727` (lexical_call_candidate).
- char_update: `src/update.c:752` (lexical_call_candidate).
- char_update: `src/update.c:782` (lexical_call_candidate).
- char_update: `src/update.c:804` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2107` (declaration_or_dispatch_reference).

Dependencies: `write_to_buffer`, `strlen`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.send_to_char.if.001` | 2339 | `if ( txt != NULL && ch->desc != NULL )` |  | pending |
| `comm.send_to_char.and.001` | 2339 | `&& ch->desc != NULL )` |  | pending |
| `comm.send_to_char.return.001` | 2341 | `return;` |  | pending |

## page_to_char

[Source line 2347](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2347); ends at line 2366. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_replay: `src/act_comm.c:265` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:229` (lexical_call_candidate).
- do_help: `src/act_info.c:1805` (lexical_call_candidate).
- do_whois: `src/act_info.c:1884` (lexical_call_candidate).
- do_who: `src/act_info.c:2077` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1921` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1962` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1988` (lexical_call_candidate).
- do_sockets: `src/act_wiz.c:4081` (lexical_call_candidate).
- ban_site: `src/ban.c:174` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3639` (lexical_call_candidate).
- do_play: `src/music.c:285` (lexical_call_candidate).
- parse_note: `src/note.c:608` (lexical_call_candidate).
- parse_note: `src/note.c:644` (lexical_call_candidate).
- do_spells: `src/skills.c:371` (lexical_call_candidate).
- do_skills: `src/skills.c:488` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2108` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `defined`, `alloc_mem`, `strlen`, `strcpy`, `show_string`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.page_to_char.if.001` | 2349 | `if ( txt == NULL \|\| ch->desc == NULL)` |  | pending |
| `comm.page_to_char.or.001` | 2349 | `\|\| ch->desc == NULL)` |  | pending |
| `comm.page_to_char.return.001` | 2350 | `return;` |  | pending |
| `comm.page_to_char.if.002` | 2352 | `if (ch->lines == 0 )` |  | pending |
| `comm.page_to_char.return.002` | 2355 | `return;` |  | pending |
| `comm.page_to_char.if.003` | 2358 | `if defined(macintosh)` |  | pending |

## show_string

[Source line 2370](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2370); ends at line 2421. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_unix: `src/comm.c:766` (lexical_call_candidate).
- page_to_char: `src/comm.c:2364` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2103` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `free_mem`, `strlen`, `write_to_buffer`, `isspace`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.show_string.if.001` | 2379 | `if (buf[0] != '\0')` |  | pending |
| `comm.show_string.if.002` | 2381 | `if (d->showstr_head)` |  | pending |
| `comm.show_string.return.001` | 2387 | `return;` |  | pending |
| `comm.show_string.if.003` | 2390 | `if (d->character)` |  | pending |
| `comm.show_string.for.001` | 2395 | `for (scan = buffer; ; scan++, d->showstr_point++)` |  | pending |
| `comm.show_string.if.004` | 2397 | `if (((*scan = *d->showstr_point) == '\n' \|\| *scan == '\r') 	    && (toggle = -toggle) < 0)` |  | pending |
| `comm.show_string.or.001` | 2397 | `\|\| *scan == '\r')` |  | pending |
| `comm.show_string.and.001` | 2398 | `&& (toggle = -toggle) < 0)` |  | pending |
| `comm.show_string.if.005` | 2401 | `if (!*scan \|\| (show_lines > 0 && lines >= show_lines))` |  | pending |
| `comm.show_string.or.002` | 2401 | `\|\| (show_lines > 0 && lines >= show_lines))` |  | pending |
| `comm.show_string.and.002` | 2401 | `&& lines >= show_lines))` |  | pending |
| `comm.show_string.for.002` | 2405 | `for (chk = d->showstr_point; isspace(*chk); chk++)` |  | pending |
| `comm.show_string.if.006` | 2407 | `if (!*chk)` |  | pending |
| `comm.show_string.if.007` | 2409 | `if (d->showstr_head)` |  | pending |
| `comm.show_string.return.002` | 2417 | `return;` |  | pending |
| `comm.show_string.return.003` | 2420 | `return;` |  | pending |

## fix_sex

[Source line 2425](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2425); ends at line 2429. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):


Dependencies: `IS_NPC`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.fix_sex.if.001` | 2427 | `if (ch->sex < 0 \|\| ch->sex > 2)` |  | pending |
| `comm.fix_sex.or.001` | 2427 | `\|\| ch->sex > 2)` |  | pending |
| `comm.fix_sex.ternary.001` | 2428 | `? 0 : ch->pcdata->true_sex;` |  | pending |

## act_new

[Source line 2431](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2431); ends at line 2559. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_auction: `src/act_comm.c:318` (lexical_call_candidate).
- do_gossip: `src/act_comm.c:373` (lexical_call_candidate).
- do_grats: `src/act_comm.c:428` (lexical_call_candidate).
- do_quote: `src/act_comm.c:483` (lexical_call_candidate).
- do_question: `src/act_comm.c:538` (lexical_call_candidate).
- do_answer: `src/act_comm.c:593` (lexical_call_candidate).
- do_music: `src/act_comm.c:649` (lexical_call_candidate).
- do_clantalk: `src/act_comm.c:701` (lexical_call_candidate).
- do_immtalk: `src/act_comm.c:731` (lexical_call_candidate).
- do_immtalk: `src/act_comm.c:738` (lexical_call_candidate).
- do_tell: `src/act_comm.c:894` (lexical_call_candidate).
- do_reply: `src/act_comm.c:938` (lexical_call_candidate).
- do_reply: `src/act_comm.c:952` (lexical_call_candidate).
- do_reply: `src/act_comm.c:957` (lexical_call_candidate).
- do_reply: `src/act_comm.c:965` (lexical_call_candidate).
- do_reply: `src/act_comm.c:966` (lexical_call_candidate).
- do_group: `src/act_comm.c:1747` (lexical_call_candidate).
- do_group: `src/act_comm.c:1759` (lexical_call_candidate).
- do_group: `src/act_comm.c:1767` (lexical_call_candidate).
- do_group: `src/act_comm.c:1769` (lexical_call_candidate).
- do_group: `src/act_comm.c:1771` (lexical_call_candidate).
- do_group: `src/act_comm.c:1777` (lexical_call_candidate).
- do_group: `src/act_comm.c:1778` (lexical_call_candidate).
- do_group: `src/act_comm.c:1779` (lexical_call_candidate).
- do_gtell: `src/act_comm.c:1927` (lexical_call_candidate).
- do_stand: `src/act_move.c:898` (lexical_call_candidate).
- do_stand: `src/act_move.c:919` (lexical_call_candidate).
- do_stand: `src/act_move.c:924` (lexical_call_candidate).
- do_stand: `src/act_move.c:929` (lexical_call_candidate).
- do_rest: `src/act_move.c:1010` (lexical_call_candidate).
- do_rest: `src/act_move.c:1033` (lexical_call_candidate).
- do_rest: `src/act_move.c:1039` (lexical_call_candidate).
- do_rest: `src/act_move.c:1045` (lexical_call_candidate).
- do_sit: `src/act_move.c:1145` (lexical_call_candidate).
- do_sit: `src/act_move.c:1167` (lexical_call_candidate).
- do_sit: `src/act_move.c:1172` (lexical_call_candidate).
- do_sit: `src/act_move.c:1177` (lexical_call_candidate).
- do_sleep: `src/act_move.c:1272` (lexical_call_candidate).
- do_wake: `src/act_move.c:1328` (lexical_call_candidate).
- wiznet: `src/act_wiz.c:170` (lexical_call_candidate).
- do_protect: `src/act_wiz.c:2082` (lexical_call_candidate).
- do_protect: `src/act_wiz.c:2088` (lexical_call_candidate).
- song_update: `src/music.c:94` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:1842` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:2111` (declaration_or_dispatch_reference).

Dependencies: `bug`, `PERS`, `URANGE`, `can_see_obj`, `one_argument`, `UPPER`, `write_to_buffer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.act_new.if.001` | 2451 | `if ( format == NULL \|\| format[0] == '\0' )` |  | pending |
| `comm.act_new.or.001` | 2451 | `\|\| format[0] == '\0' )` |  | pending |
| `comm.act_new.return.001` | 2452 | `return;` |  | pending |
| `comm.act_new.if.002` | 2455 | `if (ch == NULL \|\| ch->in_room == NULL)` |  | pending |
| `comm.act_new.or.002` | 2455 | `\|\| ch->in_room == NULL)` |  | pending |
| `comm.act_new.return.002` | 2456 | `return;` |  | pending |
| `comm.act_new.if.003` | 2459 | `if ( type == TO_VICT )` |  | pending |
| `comm.act_new.if.004` | 2461 | `if ( vch == NULL )` |  | pending |
| `comm.act_new.return.003` | 2464 | `return;` |  | pending |
| `comm.act_new.if.005` | 2467 | `if (vch->in_room == NULL)` |  | pending |
| `comm.act_new.return.004` | 2468 | `return;` |  | pending |
| `comm.act_new.for.001` | 2473 | `for ( ; to != NULL; to = to->next_in_room )` |  | pending |
| `comm.act_new.if.006` | 2475 | `if ( to->desc == NULL \|\| to->position < min_pos )` |  | pending |
| `comm.act_new.or.003` | 2475 | `\|\| to->position < min_pos )` |  | pending |
| `comm.act_new.continue.001` | 2476 | `continue;` |  | pending |
| `comm.act_new.if.007` | 2478 | `if ( (type == TO_CHAR) && to != ch )` |  | pending |
| `comm.act_new.and.001` | 2478 | `&& to != ch )` |  | pending |
| `comm.act_new.continue.002` | 2479 | `continue;` |  | pending |
| `comm.act_new.if.008` | 2480 | `if ( type == TO_VICT && ( to != vch \|\| to == ch ) )` |  | pending |
| `comm.act_new.and.002` | 2480 | `&& ( to != vch \|\| to == ch ) )` |  | pending |
| `comm.act_new.or.004` | 2480 | `\|\| to == ch ) )` |  | pending |
| `comm.act_new.continue.003` | 2481 | `continue;` |  | pending |
| `comm.act_new.if.009` | 2482 | `if ( type == TO_ROOM && to == ch )` |  | pending |
| `comm.act_new.and.003` | 2482 | `&& to == ch )` |  | pending |
| `comm.act_new.continue.004` | 2483 | `continue;` |  | pending |
| `comm.act_new.if.010` | 2484 | `if ( type == TO_NOTVICT && (to == ch \|\| to == vch) )` |  | pending |
| `comm.act_new.and.004` | 2484 | `&& (to == ch \|\| to == vch) )` |  | pending |
| `comm.act_new.or.005` | 2484 | `\|\| to == vch) )` |  | pending |
| `comm.act_new.continue.005` | 2485 | `continue;` |  | pending |
| `comm.act_new.while.001` | 2489 | `while ( *str != '\0' )` |  | pending |
| `comm.act_new.if.011` | 2491 | `if ( *str != '$' )` |  | pending |
| `comm.act_new.continue.006` | 2494 | `continue;` |  | pending |
| `comm.act_new.if.012` | 2498 | `if ( arg2 == NULL && *str >= 'A' && *str <= 'Z' )` |  | pending |
| `comm.act_new.and.005` | 2498 | `&& *str >= 'A' && *str <= 'Z' )` |  | pending |
| `comm.act_new.and.006` | 2498 | `&& *str <= 'Z' )` |  | pending |
| `comm.act_new.switch.001` | 2505 | `switch ( *str )` |  | pending |
| `comm.act_new.default.001` | 2507 | `default:  bug( "Act: bad code %d.", *str );` |  | pending |
| `comm.act_new.break.001` | 2508 | `break;` |  | pending |
| `comm.act_new.case.001` | 2510 | `case 't': i = (char *) arg1;` |  | pending |
| `comm.act_new.break.002` | 2510 | `break;` |  | pending |
| `comm.act_new.case.002` | 2511 | `case 'T': i = (char *) arg2;` |  | pending |
| `comm.act_new.break.003` | 2511 | `break;` |  | pending |
| `comm.act_new.case.003` | 2512 | `case 'n': i = PERS( ch,  to  );` |  | pending |
| `comm.act_new.break.004` | 2512 | `break;` |  | pending |
| `comm.act_new.case.004` | 2513 | `case 'N': i = PERS( vch, to  );` |  | pending |
| `comm.act_new.break.005` | 2513 | `break;` |  | pending |
| `comm.act_new.case.005` | 2514 | `case 'e': i = he_she  [URANGE(0, ch  ->sex, 2)];` |  | pending |
| `comm.act_new.break.006` | 2514 | `break;` |  | pending |
| `comm.act_new.case.006` | 2515 | `case 'E': i = he_she  [URANGE(0, vch ->sex, 2)];` |  | pending |
| `comm.act_new.break.007` | 2515 | `break;` |  | pending |
| `comm.act_new.case.007` | 2516 | `case 'm': i = him_her [URANGE(0, ch  ->sex, 2)];` |  | pending |
| `comm.act_new.break.008` | 2516 | `break;` |  | pending |
| `comm.act_new.case.008` | 2517 | `case 'M': i = him_her [URANGE(0, vch ->sex, 2)];` |  | pending |
| `comm.act_new.break.009` | 2517 | `break;` |  | pending |
| `comm.act_new.case.009` | 2518 | `case 's': i = his_her [URANGE(0, ch  ->sex, 2)];` |  | pending |
| `comm.act_new.break.010` | 2518 | `break;` |  | pending |
| `comm.act_new.case.010` | 2519 | `case 'S': i = his_her [URANGE(0, vch ->sex, 2)];` |  | pending |
| `comm.act_new.break.011` | 2519 | `break;` |  | pending |
| `comm.act_new.case.011` | 2521 | `case 'p':` |  | pending |
| `comm.act_new.ternary.001` | 2523 | `? obj1->short_descr` |  | pending |
| `comm.act_new.break.012` | 2525 | `break;` |  | pending |
| `comm.act_new.case.012` | 2527 | `case 'P':` |  | pending |
| `comm.act_new.ternary.002` | 2529 | `? obj2->short_descr` |  | pending |
| `comm.act_new.break.013` | 2531 | `break;` |  | pending |
| `comm.act_new.case.013` | 2533 | `case 'd':` |  | pending |
| `comm.act_new.if.013` | 2534 | `if ( arg2 == NULL \|\| ((char *) arg2)[0] == '\0' )` |  | pending |
| `comm.act_new.or.006` | 2534 | `\|\| ((char *) arg2)[0] == '\0' )` |  | pending |
| `comm.act_new.break.014` | 2543 | `break;` |  | pending |
| `comm.act_new.while.002` | 2548 | `while ( ( *point = *i ) != '\0' )` |  | pending |
| `comm.act_new.return.005` | 2558 | `return;` |  | pending |

## gettimeofday

[Source line 2567](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2567); ends at line 2571. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- main: `src/comm.c:365` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:505` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:642` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:665` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:817` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:847` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/comm.c:131` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/comm.c:149` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/comm.c:175` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/comm.c:197` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/comm.c:205` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/comm.c:231` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/comm.c:262` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/comm.c:283` (declaration_or_dispatch_reference).

Dependencies: `time`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `comm.gettimeofday.entry` | 2567 | `Straight-line entry` |  | pending |

## Preprocessor and macro inventory

- Line 46: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 47: `#include <types.h>` — pending configuration/reachability review.
- Line 48: `#else` — pending configuration/reachability review.
- Line 49: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 50: `#include <sys/time.h>` — pending configuration/reachability review.
- Line 51: `#endif` — pending configuration/reachability review.
- Line 53: `#include <ctype.h>` — pending configuration/reachability review.
- Line 54: `#include <errno.h>` — pending configuration/reachability review.
- Line 55: `#include <stdio.h>` — pending configuration/reachability review.
- Line 56: `#include <string.h>` — pending configuration/reachability review.
- Line 57: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 58: `#include <time.h>` — pending configuration/reachability review.
- Line 60: `#include "merc.h"` — pending configuration/reachability review.
- Line 61: `#include "interp.h"` — pending configuration/reachability review.
- Line 62: `#include "recycle.h"` — pending configuration/reachability review.
- Line 63: `#include "tables.h"` — pending configuration/reachability review.
- Line 68: `#if defined(sun)` — pending configuration/reachability review.
- Line 69: `#undef MALLOC_DEBUG` — pending configuration/reachability review.
- Line 70: `#endif` — pending configuration/reachability review.
- Line 72: `#if defined(MALLOC_DEBUG)` — pending configuration/reachability review.
- Line 73: `#include <malloc.h>` — pending configuration/reachability review.
- Line 76: `#endif` — pending configuration/reachability review.
- Line 85: `#if defined(apollo)` — pending configuration/reachability review.
- Line 86: `#define __attribute(x)` — pending configuration/reachability review.
- Line 87: `#endif` — pending configuration/reachability review.
- Line 89: `#if defined(unix)` — pending configuration/reachability review.
- Line 90: `#include <signal.h>` — pending configuration/reachability review.
- Line 91: `#endif` — pending configuration/reachability review.
- Line 93: `#if defined(apollo)` — pending configuration/reachability review.
- Line 94: `#undef __attribute` — pending configuration/reachability review.
- Line 95: `#endif` — pending configuration/reachability review.
- Line 102: `#if	defined(macintosh) || defined(MSDOS)` — pending configuration/reachability review.
- Line 106: `#endif` — pending configuration/reachability review.
- Line 108: `#if	defined(unix)` — pending configuration/reachability review.
- Line 109: `#include <fcntl.h>` — pending configuration/reachability review.
- Line 110: `#include <netdb.h>` — pending configuration/reachability review.
- Line 111: `#include <netinet/in.h>` — pending configuration/reachability review.
- Line 112: `#include <sys/socket.h>` — pending configuration/reachability review.
- Line 113: `#include "telnet.h"` — pending configuration/reachability review.
- Line 117: `#endif` — pending configuration/reachability review.
- Line 124: `#if	defined(_AIX)` — pending configuration/reachability review.
- Line 125: `#include <sys/select.h>` — pending configuration/reachability review.
- Line 136: `#endif` — pending configuration/reachability review.
- Line 138: `#if	defined(apollo)` — pending configuration/reachability review.
- Line 139: `#include <unistd.h>` — pending configuration/reachability review.
- Line 141: `#endif` — pending configuration/reachability review.
- Line 143: `#if	defined(__hpux)` — pending configuration/reachability review.
- Line 154: `#endif` — pending configuration/reachability review.
- Line 156: `#if	defined(interactive)` — pending configuration/reachability review.
- Line 157: `#include <net/errno.h>` — pending configuration/reachability review.
- Line 158: `#include <sys/fnctl.h>` — pending configuration/reachability review.
- Line 159: `#endif` — pending configuration/reachability review.
- Line 161: `#if	defined(linux)` — pending configuration/reachability review.
- Line 181: `#endif` — pending configuration/reachability review.
- Line 183: `#if	defined(macintosh)` — pending configuration/reachability review.
- Line 184: `#include <console.h>` — pending configuration/reachability review.
- Line 185: `#include <fcntl.h>` — pending configuration/reachability review.
- Line 186: `#include <unix.h>` — pending configuration/reachability review.
- Line 192: `#if	!defined(isascii)` — pending configuration/reachability review.
- Line 193: `#define	isascii(c)		( (c) < 0200 )` — pending configuration/reachability review.
- Line 194: `#endif` — pending configuration/reachability review.
- Line 198: `#endif` — pending configuration/reachability review.
- Line 200: `#if	defined(MIPS_OS)` — pending configuration/reachability review.
- Line 202: `#endif` — pending configuration/reachability review.
- Line 204: `#if	defined(MSDOS)` — pending configuration/reachability review.
- Line 207: `#endif` — pending configuration/reachability review.
- Line 209: `#if	defined(NeXT)` — pending configuration/reachability review.
- Line 212: `#if	!defined(htons)` — pending configuration/reachability review.
- Line 214: `#endif` — pending configuration/reachability review.
- Line 215: `#if	!defined(ntohl)` — pending configuration/reachability review.
- Line 217: `#endif` — pending configuration/reachability review.
- Line 222: `#endif` — pending configuration/reachability review.
- Line 224: `#if	defined(sequent)` — pending configuration/reachability review.
- Line 232: `#if	!defined(htons)` — pending configuration/reachability review.
- Line 234: `#endif` — pending configuration/reachability review.
- Line 236: `#if	!defined(ntohl)` — pending configuration/reachability review.
- Line 238: `#endif` — pending configuration/reachability review.
- Line 246: `#endif` — pending configuration/reachability review.
- Line 249: `#if defined(sun)` — pending configuration/reachability review.
- Line 261: `#if !defined(__SVR4)` — pending configuration/reachability review.
- Line 264: `#if defined(SYSV)` — pending configuration/reachability review.
- Line 267: `#else` — pending configuration/reachability review.
- Line 270: `#endif` — pending configuration/reachability review.
- Line 271: `#endif` — pending configuration/reachability review.
- Line 274: `#endif` — pending configuration/reachability review.
- Line 276: `#if defined(ultrix)` — pending configuration/reachability review.
- Line 292: `#endif` — pending configuration/reachability review.
- Line 314: `#if defined(macintosh) || defined(MSDOS)` — pending configuration/reachability review.
- Line 318: `#endif` — pending configuration/reachability review.
- Line 320: `#if defined(unix)` — pending configuration/reachability review.
- Line 326: `#endif` — pending configuration/reachability review.
- Line 351: `#if defined(unix)` — pending configuration/reachability review.
- Line 353: `#endif` — pending configuration/reachability review.
- Line 358: `#if defined(MALLOC_DEBUG)` — pending configuration/reachability review.
- Line 360: `#endif` — pending configuration/reachability review.
- Line 372: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 377: `#endif` — pending configuration/reachability review.
- Line 409: `#if defined(macintosh) || defined(MSDOS)` — pending configuration/reachability review.
- Line 413: `#endif` — pending configuration/reachability review.
- Line 415: `#if defined(unix)` — pending configuration/reachability review.
- Line 422: `#endif` — pending configuration/reachability review.
- Line 434: `#if defined(unix)` — pending configuration/reachability review.
- Line 456: `#if defined(SO_DONTLINGER) && !defined(SYSV)` — pending configuration/reachability review.
- Line 471: `#endif` — pending configuration/reachability review.
- Line 494: `#endif` — pending configuration/reachability review.
- Line 498: `#if defined(macintosh) || defined(MSDOS)` — pending configuration/reachability review.
- Line 545: `#if defined(MSDOS)` — pending configuration/reachability review.
- Line 547: `#endif` — pending configuration/reachability review.
- Line 624: `#if defined(MSDOS)` — pending configuration/reachability review.
- Line 626: `#endif` — pending configuration/reachability review.
- Line 637: `#if defined(MSDOS)` — pending configuration/reachability review.
- Line 639: `#endif` — pending configuration/reachability review.
- Line 654: `#endif` — pending configuration/reachability review.
- Line 658: `#if defined(unix)` — pending configuration/reachability review.
- Line 677: `#if defined(MALLOC_DEBUG)` — pending configuration/reachability review.
- Line 680: `#endif` — pending configuration/reachability review.
- Line 853: `#endif` — pending configuration/reachability review.
- Line 857: `#if defined(unix)` — pending configuration/reachability review.
- Line 875: `#if !defined(FNDELAY)` — pending configuration/reachability review.
- Line 876: `#define FNDELAY O_NDELAY` — pending configuration/reachability review.
- Line 877: `#endif` — pending configuration/reachability review.
- Line 958: `#endif` — pending configuration/reachability review.
- Line 1024: `#if defined(MSDOS) || defined(macintosh)` — pending configuration/reachability review.
- Line 1026: `#endif` — pending configuration/reachability review.
- Line 1052: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 1066: `#endif` — pending configuration/reachability review.
- Line 1068: `#if defined(MSDOS) || defined(unix)` — pending configuration/reachability review.
- Line 1094: `#endif` — pending configuration/reachability review.
- Line 1520: `#if defined(macintosh) || defined(MSDOS)` — pending configuration/reachability review.
- Line 1523: `#endif` — pending configuration/reachability review.
- Line 1648: `#if defined(unix)` — pending configuration/reachability review.
- Line 1650: `#endif` — pending configuration/reachability review.
- Line 1752: `#if defined(unix)` — pending configuration/reachability review.
- Line 1754: `#endif` — pending configuration/reachability review.
- Line 1783: `#if defined(unix)` — pending configuration/reachability review.
- Line 1785: `#endif` — pending configuration/reachability review.
- Line 2173: `#if defined(MSDOS)` — pending configuration/reachability review.
- Line 2176: `#endif` — pending configuration/reachability review.
- Line 2178: `#if defined(macintosh) || defined(unix)` — pending configuration/reachability review.
- Line 2181: `#endif` — pending configuration/reachability review.
- Line 2358: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 2360: `#else` — pending configuration/reachability review.
- Line 2365: `#endif` — pending configuration/reachability review.
- Line 2566: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 2572: `#endif` — pending configuration/reachability review.

## Static tables

- `echo_off_str` at line 103 — pending entry/termination review.
- `echo_on_str` at line 104 — pending entry/termination review.
- `go_ahead_str` at line 105 — pending entry/termination review.
- `echo_off_str` at line 114 — pending entry/termination review.
- `echo_on_str` at line 115 — pending entry/termination review.
- `go_ahead_str` at line 116 — pending entry/termination review.
- `dir_name` at line 1327 — pending entry/termination review.
- `he_she` at line 2434 — pending entry/termination review.
- `him_her` at line 2435 — pending entry/termination review.
- `his_her` at line 2436 — pending entry/termination review.

## Commented code candidates

