DROP TABLE IF EXISTS Rulings_by_Set;
DROP TABLE IF EXISTS Cards_by_Set;
DROP TABLE IF EXISTS Words_by_Set;

CREATE TABLE 'Rulings_by_Set' AS
SELECT Sets.name, dtable.date_released, avg(rcount) as Rulings_per_card, sum(rcount) as Total_rulings
FROM (SELECT Cards.name, Cards.date_released, Cards.oracle_id, Cards.setname_id, count(DISTINCT ruling_text) as rcount 
	FROM Cards LEFT JOIN Rulings on Cards.oracle_id = Rulings.oracle_id 
	GROUP BY Cards.oracle_id, setname_id) as dtable
JOIN Sets on dtable.setname_id = Sets.id
WHERE Sets.set_type = 'core' or Sets.set_type = 'expansion'
GROUP BY Sets.id
ORDER BY date_released;

CREATE TABLE 'Cards_by_Set' AS
SELECT Sets.name, count(mytable.oracle_id) as Cards_per_set
FROM (SELECT DISTINCT oracle_id, setname_id FROM Cards) as mytable
JOIN Sets on mytable.setname_id = Sets.id
WHERE Sets.set_type = 'core' or Sets.set_type = 'expansion'
GROUP BY Sets.name;

CREATE TABLE 'Words_by_Set' AS
SELECT setname_id, Sets.name, date_released, avg(word_count)as Words_per_Card, sum(word_count) as Total_Words_in_Set
FROM (SELECT DISTINCT Cards.name, word_count, date_released, setname_id FROM Cards)
JOIN Sets on setname_id = Sets.id
WHERE Sets.set_type = 'core' or Sets.set_type = 'expansion'
GROUP BY setname_id
ORDER BY date_released;

SELECT Rulings_by_Set.name, Rulings_by_Set.date_released, Rulings_per_card, Total_rulings, Cards_per_set, Words_per_Card, Total_Words_in_Set 
FROM Rulings_by_Set
JOIN Cards_by_Set on Rulings_by_Set.name = Cards_by_Set.name
JOIN Words_by_Set on Words_by_Set.name = Cards_by_Set.name;