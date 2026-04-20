IF OBJECT_ID('dbo.players', 'U') IS NOT NULL
    DROP TABLE dbo.players;
GO

CREATE TABLE dbo.players (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    age INT NOT NULL,
    position VARCHAR(80) NOT NULL,
    number INT NOT NULL,
    first_club VARCHAR(120) NOT NULL,
    current_club VARCHAR(120) NOT NULL
);
GO

INSERT INTO dbo.players (name, age, position, number, first_club, current_club) VALUES
('buffon', 47, 'Goalkeeper', 1, 'Parma', 'Retired'),
('maldini', 56, 'Defender', 3, 'AC Milan', 'Retired'),
('totti', 49, 'Forward', 10, 'AS Roma', 'Retired'),
('delpiero', 51, 'Forward', 10, 'Padova', 'Retired'),
('pirlo', 46, 'Midfielder', 21, 'Brescia', 'Retired'),
('chiellini', 41, 'Defender', 3, 'Livorno', 'Los Angeles FC'),
('bonucci', 39, 'Defender', 19, 'Inter', 'Fenerbahce'),
('verratti', 33, 'Midfielder', 7, 'Pescara', 'Al Arabi'),
('barella', 29, 'Midfielder', 23, 'Cagliari', 'Inter'),
('donnarumma', 27, 'Goalkeeper', 1, 'AC Milan', 'Paris Saint-Germain');
GO
