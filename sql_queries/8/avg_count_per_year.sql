WITH RECURSIVE
    children AS (
        -- Wybierz początkowy węzeł na poziomie 1
        SELECT id, parent_id, lvl, text
        FROM fsaps_correspondent_correspondent_kind
        WHERE lvl = 1                -- Znajdź węzły na poziomie 1
          AND id in (101, 20, 10, 2) -- Wybierz konkretny węzeł

        UNION ALL

        -- Znajdź dzieci węzła na poziomie 1
        SELECT t.id, t.parent_id, t.lvl, t.text
        FROM fsaps_correspondent_correspondent_kind t
                 INNER JOIN children c ON t.parent_id = c.id),
    payments AS (
        -- Twoje istniejące zapytanie
        SELECT correspondent_id, date_part('year', date) AS rok_wplaty, COUNT(id) AS liczba_wplat
        FROM fsaps_payment_payment
        WHERE date BETWEEN '#A#-01-01' AND '#B#-12-31'
          AND correspondent_id IN (SELECT correspondent_id
                                   FROM fsaps_correspondent_correspondent
                                   WHERE kind_id IN (SELECT id FROM children))
        GROUP BY correspondent_id, rok_wplaty)
-- Połączenie obu części za pomocą złączenia
SELECT rok_wplaty, AVG(liczba_wplat) AS srednia_liczba_wplat, sum(liczba_wplat) as laczna_liczba_wplat
FROM (
         -- Unia wyników z mojego zapytania rekurencyjnego i Twojego zapytania

         SELECT rok_wplaty, liczba_wplat
         FROM payments) AS merged_data
GROUP BY rok_wplaty;
