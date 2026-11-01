# src/telnet.h

Role: header. Disposition: **pending**. SHA-256: `15064d41929b45d5c313897692c64fa2755c2e57c8e915a1db52e6a18f231f09`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## Preprocessor and macro inventory

- Line 12: `#ifndef _arpa_telnet_h` — pending configuration/reachability review.
- Line 13: `#define _arpa_telnet_h` — pending configuration/reachability review.
- Line 15: `#define	IAC	255		/* interpret as command: */` — pending configuration/reachability review.
- Line 16: `#define	DONT	254		/* you are not to use option */` — pending configuration/reachability review.
- Line 17: `#define	DO	253		/* please, you use option */` — pending configuration/reachability review.
- Line 18: `#define	WONT	252		/* I won't use option */` — pending configuration/reachability review.
- Line 19: `#define	WILL	251		/* I will use option */` — pending configuration/reachability review.
- Line 20: `#define	SB	250		/* interpret as subnegotiation */` — pending configuration/reachability review.
- Line 21: `#define	GA	249		/* you may reverse the line */` — pending configuration/reachability review.
- Line 22: `#define	EL	248		/* erase the current line */` — pending configuration/reachability review.
- Line 23: `#define	EC	247		/* erase the current character */` — pending configuration/reachability review.
- Line 24: `#define	AYT	246		/* are you there */` — pending configuration/reachability review.
- Line 25: `#define	AO	245		/* abort output--but let prog finish */` — pending configuration/reachability review.
- Line 26: `#define	IP	244		/* interrupt process--permanently */` — pending configuration/reachability review.
- Line 27: `#define	BREAK	243		/* break */` — pending configuration/reachability review.
- Line 28: `#define	DM	242		/* data mark--for connect. cleaning */` — pending configuration/reachability review.
- Line 29: `#define	NOP	241		/* nop */` — pending configuration/reachability review.
- Line 30: `#define	SE	240		/* end sub negotiation */` — pending configuration/reachability review.
- Line 31: `#define EOR     239             /* end of record (transparent mode) */` — pending configuration/reachability review.
- Line 33: `#define SYNCH	242		/* for telfunc calls */` — pending configuration/reachability review.
- Line 35: `#ifdef TELCMDS` — pending configuration/reachability review.
- Line 40: `#endif` — pending configuration/reachability review.
- Line 43: `#define TELOPT_BINARY	0	/* 8-bit data path */` — pending configuration/reachability review.
- Line 44: `#define TELOPT_ECHO	1	/* echo */` — pending configuration/reachability review.
- Line 45: `#define	TELOPT_RCP	2	/* prepare to reconnect */` — pending configuration/reachability review.
- Line 46: `#define	TELOPT_SGA	3	/* suppress go ahead */` — pending configuration/reachability review.
- Line 47: `#define	TELOPT_NAMS	4	/* approximate message size */` — pending configuration/reachability review.
- Line 48: `#define	TELOPT_STATUS	5	/* give status */` — pending configuration/reachability review.
- Line 49: `#define	TELOPT_TM	6	/* timing mark */` — pending configuration/reachability review.
- Line 50: `#define	TELOPT_RCTE	7	/* remote controlled transmission and echo */` — pending configuration/reachability review.
- Line 51: `#define TELOPT_NAOL 	8	/* negotiate about output line width */` — pending configuration/reachability review.
- Line 52: `#define TELOPT_NAOP 	9	/* negotiate about output page size */` — pending configuration/reachability review.
- Line 53: `#define TELOPT_NAOCRD	10	/* negotiate about CR disposition */` — pending configuration/reachability review.
- Line 54: `#define TELOPT_NAOHTS	11	/* negotiate about horizontal tabstops */` — pending configuration/reachability review.
- Line 55: `#define TELOPT_NAOHTD	12	/* negotiate about horizontal tab disposition */` — pending configuration/reachability review.
- Line 56: `#define TELOPT_NAOFFD	13	/* negotiate about formfeed disposition */` — pending configuration/reachability review.
- Line 57: `#define TELOPT_NAOVTS	14	/* negotiate about vertical tab stops */` — pending configuration/reachability review.
- Line 58: `#define TELOPT_NAOVTD	15	/* negotiate about vertical tab disposition */` — pending configuration/reachability review.
- Line 59: `#define TELOPT_NAOLFD	16	/* negotiate about output LF disposition */` — pending configuration/reachability review.
- Line 60: `#define TELOPT_XASCII	17	/* extended ascic character set */` — pending configuration/reachability review.
- Line 61: `#define	TELOPT_LOGOUT	18	/* force logout */` — pending configuration/reachability review.
- Line 62: `#define	TELOPT_BM	19	/* byte macro */` — pending configuration/reachability review.
- Line 63: `#define	TELOPT_DET	20	/* data entry terminal */` — pending configuration/reachability review.
- Line 64: `#define	TELOPT_SUPDUP	21	/* supdup protocol */` — pending configuration/reachability review.
- Line 65: `#define	TELOPT_SUPDUPOUTPUT 22	/* supdup output */` — pending configuration/reachability review.
- Line 66: `#define	TELOPT_SNDLOC	23	/* send location */` — pending configuration/reachability review.
- Line 67: `#define	TELOPT_TTYPE	24	/* terminal type */` — pending configuration/reachability review.
- Line 68: `#define	TELOPT_EOR	25	/* end or record */` — pending configuration/reachability review.
- Line 69: `#define TELOPT_EXOPL	255	/* extended-options-list */` — pending configuration/reachability review.
- Line 71: `#ifdef TELOPTS` — pending configuration/reachability review.
- Line 72: `#define	NTELOPTS	(1+TELOPT_EOR)` — pending configuration/reachability review.
- Line 81: `#endif` — pending configuration/reachability review.
- Line 84: `#define	TELQUAL_IS	0	/* option is... */` — pending configuration/reachability review.
- Line 85: `#define	TELQUAL_SEND	1	/* send option */` — pending configuration/reachability review.
- Line 87: `#endif /*!_arpa_telnet_h*/` — pending configuration/reachability review.

## Static tables

- `telcmds` at line 36 — pending entry/termination review.
- `telopts` at line 73 — pending entry/termination review.

## Commented code candidates

