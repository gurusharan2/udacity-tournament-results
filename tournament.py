#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    db.commit()
    db.close()
    """Remove all the match records from the database."""


def deletePlayers():
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM Player")
    db.commit()
    db.close()
    """Remove all the player records from the database."""


def countPlayers():
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) from player")
    result = c.fetchall()
    db.commit()
    db.close()
    return result[0][0]
    """Returns the number of players currently registered."""


def registerPlayer(name):
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO Player(name) VALUES (%s)", (name,))
    db.commit()
    db.close()
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT matches_won.id,matches_won.name,matches_won.win,matches_total.matches from matches_won,matches_total where matches_won.id =matches_total.id order by win desc")
    result = []
    for a in c.fetchall():
        result.append(a)
    db.commit()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute(
        "INSERT INTO Matches(winner_id,looser_id) VALUES (%s,%s)", (winner, loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM matches_won;")
    rows = c.fetchall()
    db.close()
    i = 0
    result = []
    while i < len(rows):
        playerAid = rows[i][0]
        playerAname = rows[i][1]
        playerBid = rows[i+1][0]
        playerBname = rows[i+1][1]
        result.append((playerAid, playerAname, playerBid, playerBname))
        i = i+2

    return result

print swissPairings()
