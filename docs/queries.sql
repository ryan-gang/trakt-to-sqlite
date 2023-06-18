-- Detailed Episode watchlog.
"SELECT * FROM watchlog W INNER JOIN episode E on E.id == W.media_id INNER JOIN show S on S.id == E.show_id order by watched_at DESC;"

-- Detailed Episode watch counts.
"SELECT E.season, E.number, E.title, S.title, W.media_id, count(W.media_id) AS watched FROM watchlog W INNER JOIN episode E on E.id == W.media_id INNER JOIN show S on S.id == E.show_id GROUP BY W.media_id order by watched DESC;"

-- Cleaner Episode watchlog.
SELECT S.title as show, S.year, E.season, E.number as episode, E.title, date(watched_at) as date, time(watched_at) as time FROM watchlog W INNER JOIN episode E on E.id == W.media_id INNER JOIN show S on S.id == E.show_id order by watched_at DESC;
