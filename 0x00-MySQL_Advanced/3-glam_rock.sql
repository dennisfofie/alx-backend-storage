-- script to lists all brands with glam rock as their style

SELECT band_name, (IFNULL(split, 2023) - formed) AS lifespan FROM metal_bands  WHERE style LIKE "%Glam rock%" ORDER By lifespan DESC;