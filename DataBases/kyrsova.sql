---------------------------------Створення таблиць
CREATE TABLE clubs (
    club_id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    team INT NOT NULL,
    description VARCHAR(300)
);

CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
	latitude NUMERIC(9,6) NOT NULL,
	longitude NUMERIC(10,6) NOT NULL
);

CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    team INT NOT NULL,
    name VARCHAR(64) NOT NULL,
    position VARCHAR(64),
    is_main BOOLEAN NOT NULL
);

CREATE TABLE distances (
    distance_id SERIAL PRIMARY KEY,
    team int NOT NULL,
    stadium int NOT NULL,
    distance int NOT NULL
);

CREATE TABLE stadiums (
    stadium_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    capacity INT NOT NULL,
	latitude NUMERIC(9,6) NOT NULL,
	longitude NUMERIC(10,6) NOT NULL
);

CREATE TABLE games (
    game_id SERIAL PRIMARY KEY,
    start TIMESTAMP,
	stadium INT NOT NULL,
    team_1 INT NOT NULL,
    team_2 INT NOT NULL
);

CREATE TABLE substitutes (
    substitute_id SERIAL PRIMARY KEY,
    game INT NOT NULL,
    orig_pl INT NOT NULL,
    sub_pl INT NOT NULL,
    time TIME 
);

CREATE TABLE game_results (
    game_id int PRIMARY KEY,
    team_1 int NOT NULL,
    team_2 int NOT NULL,
	team_2_gls int,
	team_1_gls int 
);

CREATE TABLE goals (
    goal_id SERIAL PRIMARY KEY,
    game INT NOT NULL,
	team INT NOT NULL,
    scorer INT NOT NULL
);

CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    game INT NOT NULL,
    stadium INT NOT NULL,
    place INT NOT NULL,
);

CREATE OR REPLACE PROCEDURE calculate_distance(team_id_own INT, stadium_id_own INT)
LANGUAGE plpgsql AS $$
DECLARE
    team_lat numeric(9, 6);
    team_lon numeric(10, 6);
    stadium_lat numeric(9, 6);
    stadium_lon numeric(10, 6);
    my_distance float;
    R double precision := 6371; 
BEGIN
    SELECT latitude, longitude INTO team_lat, team_lon
    FROM teams
    WHERE team_id = team_id_own;

    SELECT latitude, longitude INTO stadium_lat, stadium_lon
    FROM stadiums
    WHERE stadium_id = stadium_id_own;
    
    my_distance := R * 2 * ASIN(SQRT(
        POWER(SIN((team_lat - stadium_lat) * PI() / 180 / 2), 2) + 
        COS(team_lat * PI() / 180) * COS(stadium_lat * PI() / 180) * 
        POWER(SIN((team_lon - stadium_lon) * PI() / 180 / 2), 2)
    ));
    my_distance := ROUND(my_distance);

    INSERT INTO distances (team, stadium, distance)
    VALUES (team_id_own, stadium_id_own, my_distance);
    RAISE NOTICE 'Distance = % ', my_distance;
END;
$$;

------------------------------------------------Створення звязків

ALTER TABLE clubs
ADD CONSTRAINT fk_team FOREIGN KEY (team) REFERENCES teams(team_id);

ALTER TABLE teams
ADD CONSTRAINT fk_club FOREIGN KEY (club) REFERENCES clubs(club_id);

ALTER TABLE players
ADD CONSTRAINT fk_team FOREIGN KEY (team) REFERENCES teams(team_id);

ALTER TABLE distances
ADD CONSTRAINT fk_stadium FOREIGN KEY (stadium) REFERENCES stadiums(stadium_id);

ALTER TABLE distances
ADD CONSTRAINT fk_team FOREIGN KEY (team) REFERENCES teams(team_id);

ALTER TABLE games
ADD CONSTRAINT fk_stadium FOREIGN KEY (stadium) REFERENCES stadiums(stadium_id);

ALTER TABLE games
ADD CONSTRAINT fk_team1 FOREIGN KEY (team_1) REFERENCES teams(team_id);

ALTER TABLE games
ADD CONSTRAINT fk_team2 FOREIGN KEY (team_2) REFERENCES teams(team_id);

ALTER TABLE substitutes
ADD CONSTRAINT fk_game FOREIGN KEY (game) REFERENCES games(game_id);

ALTER TABLE substitutes
ADD CONSTRAINT fk_orig_pl FOREIGN KEY (orig_pl) REFERENCES players(player_id);

ALTER TABLE substitutes
ADD CONSTRAINT fk_sub_pl FOREIGN KEY (sub_pl) REFERENCES players(player_id);

ALTER TABLE goals
ADD CONSTRAINT fk_game FOREIGN KEY (game) REFERENCES games(game_id);

ALTER TABLE goals
ADD CONSTRAINT fk_team FOREIGN KEY (team) REFERENCES teams(team_id);

ALTER TABLE goals
ADD CONSTRAINT fk_scorer FOREIGN KEY (scorer) REFERENCES players(player_id);

ALTER TABLE game_results
ADD CONSTRAINT fk_game FOREIGN KEY (game_id) REFERENCES games(game_id);

ALTER TABLE game_results
ADD CONSTRAINT fk_team1 FOREIGN KEY (team_1) REFERENCES teams(team_id);

ALTER TABLE game_results
ADD CONSTRAINT fk_team2 FOREIGN KEY (team_2) REFERENCES teams(team_id);

ALTER TABLE tickets
ADD CONSTRAINT fk_game FOREIGN KEY (game) REFERENCES games(game_id);

ALTER TABLE tickets
ADD CONSTRAINT fk_stadium FOREIGN KEY (stadium) REFERENCES stadiums(stadium_id);

----------------------------------Забезпечення цілісності

ALTER TABLE clubs
ADD CONSTRAINT uniq_team UNIQUE(team); 

CREATE OR REPLACE FUNCTION player_limit()
RETURNS TRIGGER 
AS $$
BEGIN
    IF 
		(SELECT COUNT(*) FROM players WHERE team = NEW.team) >= 15 
	THEN
        RAISE EXCEPTION 'Team % already has 15 players.', NEW.team;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_player_limit
BEFORE INSERT OR UPDATE ON players
FOR EACH ROW
EXECUTE FUNCTION player_limit();

CREATE OR REPLACE FUNCTION main_players_limit()
RETURNS TRIGGER 
AS $$
BEGIN
    IF NEW.is_main THEN
        IF (SELECT COUNT(*) FROM players WHERE team = NEW.team AND is_main = TRUE) >= 11 THEN
            RAISE EXCEPTION 'Team % already has 11 main players.', NEW.team;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_main_player_limit
BEFORE INSERT OR UPDATE ON players
FOR EACH ROW
EXECUTE FUNCTION main_player_limit();

ALTER TABLE teams
ADD CONSTRAINT check_position CHECK (position IN ('goalkeeper', 'defender', 'midfielder', 'attacker'));

CREATE OR REPLACE FUNCTION goalkeeper_limit()
RETURNS TRIGGER 
AS $$
BEGIN
    IF NEW.position = 'goalkeeper' THEN
        IF (SELECT COUNT(*) FROM players WHERE team = NEW.team AND position = 'goalkeeper') >= 1 THEN
            RAISE EXCEPTION 'Team % already has a goalkeeper.', NEW.team;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_goalkeeper_limit
BEFORE INSERT OR UPDATE ON players
FOR EACH ROW
EXECUTE FUNCTION goalkeeper_limit();

CREATE OR REPLACE PROCEDURE game_results(game_id_own INT, team_1_own INT, team_2_own INT)
LANGUAGE plpgsql
AS $$
DECLARE
    team_1_goals INT;
    team_2_goals INT;
BEGIN
    SELECT COUNT(*) INTO team_1_goals
    FROM goals
    WHERE game = game_id_own AND team = team_1_own;

    SELECT COUNT(*) INTO team_2_goals
    FROM goals
    WHERE game = game_id_own AND team = team_2_own;

    UPDATE game_results
    SET team_2_gls = team_2_goals,
        team_1_gls = team_1_goals
    WHERE game_id = game_id_own AND team_2 = team_2_own AND team_1 = team_1_own;

    RAISE NOTICE 'Game %: Team 1 (% goals), Team 2 (% goals)', game_id_own, team_1_goals, team_2_goals;
END;
$$;

CREATE OR REPLACE FUNCTION count_tickets()
RETURNS TRIGGER 
AS $$
BEGIN
	IF
	(SELECT COUNT(*) FROM tickets WHERE stadium = NEW.stadium AND game = NEW.game) >= 
	(SELECT capacity FROM stadiums WHERE stadium_id = NEW.stadium)
	THEN
	RAISE EXCEPTION 'All tickets are sold, capacity for stadium % ', NEW.stadium;
    END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql

CREATE TRIGGER check_num_tickets
BEFORE INSERT OR UPDATE ON tickets
FOR EACH ROW
EXECUTE FUNCTION count_tickets();

ALTER TABLE tickets
ADD CONSTRAINT uniq_place UNIQUE(game, stadium, place);

-------------------------------- -----Заповнення таблиць

INSERT INTO teams (name, latitude, longitude)
VALUES
		( 'Dynamo Kyiv', 50.4501, 30.5323),
		( 'Red Devils', 53.4631, -2.2913),
		( 'Barca', 41.3809, 2.1228);

INSERT INTO clubs (name, team, description)
VALUES	
		('Dynamo', 7, 'український футбольний клуб з міста Києва'),
		('Manchester United ', 8, 'англійський футбольний клуб з осідком в Олд-Траффорд, районі метрополійного Манчестера.'),
		('Barcelona', 9, 'футбольний клуб з Барселони, Каталонія, Іспанія.');

INSERT INTO players (team, name, position, is_main)
VALUES
		(7, 'Vasia', 'goalkeeper', 'TRUE'),
		(7, 'Vitia', 'defender', 'TRUE'),
		(7, 'Yra', 'defender', 'TRUE'),
		(7, 'Sasha', 'defender', 'TRUE'),
		(7, 'Nikita', 'defender', 'TRUE'),
		(7, 'Max', 'midfielder', 'TRUE'),
		(7, 'Artem', 'midfielder', 'TRUE'),
		(7, 'Jenya', 'midfielder', 'TRUE'),
		(7, 'Yarik', 'attacker', 'TRUE'),
		(7, 'Stas', 'attacker', 'TRUE'),
		(7, 'Vitaliy', 'attacker', 'TRUE'),
		(7, 'Vlad', 'attacker', 'FALSE'),
		(7, 'Nazar', 'attacker', 'FALSE'),
		(7, 'Mihail', 'midfielder', 'FALSE'),
		(7, 'Roma', 'defender', 'FALSE'),
		(8, 'Colocol', 'goalkeeper', 'TRUE'),
		(8, 'Pypok', 'defender', 'TRUE'),
		(8, 'Banka', 'defender', 'TRUE'),
		(8, 'Shnyrok', 'defender', 'TRUE'),
		(8, 'Tubik', 'midfielder', 'TRUE'),
		(8, 'Chypik', 'midfielder', 'TRUE'),
		(8, 'Korzina', 'midfielder', 'TRUE'),
		(8, 'Gorshok', 'midfielder', 'TRUE'),
		(8, 'Modni', 'attacker', 'TRUE'),
		(8, 'Krytoi', 'attacker', 'TRUE'),
		(8, 'Boba', 'attacker', 'TRUE'),
		(8, 'Bomba', 'defender', 'FALSE'),
		(8, 'Kykyha', 'attacker', 'FALSE'),
		(8, 'Koka', 'attacker', 'FALSE'),
		(8, 'Konopel', 'defender', 'FALSE'),
		(9, 'Oliver', 'goalkeeper', 'TRUE'),
		(9, 'Jordj', 'defender', 'TRUE'),
		(9, 'Garik', 'defender', 'TRUE'),
		(9, 'Dgeycob', 'defender', 'TRUE'),
		(9, 'Noy', 'defender', 'TRUE'),
		(9, 'Jeck', 'midfielder', 'TRUE'),
		(9, 'Charli', 'midfielder', 'TRUE'),
		(9, 'Tomas', 'midfielder', 'TRUE'),
		(9, 'Oskar', 'midfielder', 'TRUE'),
		(9, 'Viliam', 'attacker', 'TRUE'),
		(9, 'Podik', 'attacker', 'TRUE'),
		(9, 'Svetlana', 'midfielder', 'FALSE'),
		(9, 'Apteka', 'defender', 'FALSE'),
		(9, 'Dengi', 'attacker', 'FALSE'),
		(9, 'Sobaka', 'attacker', 'FALSE');

INSERT INTO stadiums ( name, capacity, latitude, longitude)
VALUES
		('Maracana', 10, -22.9127, -43.2302),
		('Barnabeu', 7, 40.4531, -3.6883),
		('Metlif', 9, 40.8128, -73.8343);
		
INSERT INTO games ( start, stadium, team_1, team_2)
VALUES
		('2024-12-20 14:30:00', 1, 8, 9),
		('2024-12-21 12:40:00', 2, 8, 7),
		('2024-12-22 16:00:00', 3, 9, 7);

INSERT INTO game_results ( game_id, team_1, team_2)
VALUES
		(1, 8, 9),
		(2, 8, 7),
		(3, 9, 7);

INSERT INTO goals ( game, team, scorer)
VALUES
		(1, 8, 17),
		(1, 8, 17),
		(1, 9, 34),
		(2, 8, 18),
		(2, 7, 3),
		(3, 9, 36),
		(3, 7, 5),
		(3, 7, 8);

INSERT INTO substitute ( game, orig_pl, sub_pl, time)
VALUES
		(1, 20, 28, '15:00:00'),
		(2, 10, 14, '14:30:00'),
		(3, 35, 43, '17:51:24');

INSERT INTO tickets ( game, stadium, place)
VALUES 
		(1, 1, 1),
		(1, 1, 2),
		(1, 1, 3),
		(1, 1, 4),
		(2, 2, 1),
		(2, 2, 2),
		(2, 2, 3),
		(2, 2, 4),
		(3, 3, 1),
		(3, 3, 2),
		(3, 3, 3),
		(3, 3, 4),
		(3, 3, 5),
		(3, 3, 6);
--------------------------------------Виконання завдань

--СПИСОК ЗАЯВЛЕНИХ ГРАВЦІВ КОМАНД
SELECT team, ARRAY_AGG(name) AS names, ARRAY_AGG(position) AS positions, ARRAY_AGG(is_main) AS is_main
FROM players 
GROUP BY team ;

--ІСТОРІЯ ІГОР
SELECT * FROM games
ORDER BY start ASC;

--ДАНІ ФУТБОЛЬНИХ КЛУБІВ. 
SELECT * FROM clubs

--БЛАНК КВИТКА
CREATE VIEW ticket_blank AS
SELECT * FROM tickets
WHERE 1 = 0

SELECT * FROM ticket_blank

--ПЕРЕЛІК ВІЛЬНИХ МІСЦЬ НА КОНКРЕТНУ ГРУ
CREATE OR REPLACE PROCEDURE free_placec(place_in_game INT)
LANGUAGE plpgsql
AS $$
DECLARE
stadium_for_game INT;
free_places INT;
BEGIN
SELECT stadium FROM games
WHERE game_id = place_in_game
INTO stadium_for_game;

SELECT 
(SELECT capacity FROM stadiums WHERE stadium_id = stadium_for_game) - 
(SELECT COUNT(*) FROM tickets WHERE game = place_in_game AND stadium = stadium_for_game) INTO free_places;

RAISE NOTICE 'Free places for game: %', free_places;
END;
$$;

CALL free_placec(1);

-- НАЙРЕЗУЛЬТАТИВНІШИЙ ГРАВЕЦЬ
SELECT scorer, COUNT(*) AS number_of_goals
FROM goals
GROUP BY scorer
ORDER BY number_of_goals DESC
LIMIT 1;

--КОМАНДА З НАЙБІЛЬШОЮ РІЗНИЦЕЮ ГОЛІВ
SELECT team, MAX(goal_diff) AS max_diff
FROM (
    SELECT 
        team_1 AS team,
        (team_1_gls - team_2_gls) AS goal_diff
    FROM game_results
    UNION ALL
    SELECT 
        team_2 AS team,
        (team_2_gls - team_1_gls) AS goal_diff
    FROM game_results
) AS all_results
GROUP BY team
ORDER BY max_diff DESC
LIMIT 1;