-- Detailed Episode watchlog.
"SELECT * FROM watchlog W INNER JOIN episode E on E.id == W.media_id INNER JOIN show S on S.id == E.show_id order by watched_at DESC;"

-- Detailed Episode watch counts.
"SELECT E.season, E.number, E.title, S.title, W.media_id, count(W.media_id) AS watched FROM watchlog W INNER JOIN episode E on E.id == W.media_id INNER JOIN show S on S.id == E.show_id GROUP BY W.media_id order by watched DESC;"
