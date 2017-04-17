-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table Player(
    id serial primary key,
    name varchar(50)
);


create table Matches(
    id serial primary key,
    winner_id int,
    looser_id int
    );

create view Matches_won as
SELECT player.id,player.name,count(matches.winner_id) as win
from player left join matches on player.id = matches.winner_id
group by player.id
order by win desc;

create view matches_total as
SELECT player.id,player.name,count(matches.id) as matches
from player left join matches on player.id = matches.winner_id or player.id = matches.looser_id
group by player.id;
