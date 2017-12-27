# 索引

● base_article => SELECT

```
DROP INDEX IF EXISTS guid_url_title_pubtime_source_reprinted_area_id ON `base_article`;

CREATE INDEX guid_url_title_pubtime_source_reprinted_area_id ON `base_article` (`guid`, `url`, `title`, `pubtime`, `source`, `reprinted`, `area_id`);

```

● base_article => WHERE

```
DROP INDEX IF EXISTS pubtime_guid ON `base_article`;

CREATE INDEX pubtime_guid ON `base_article`(`pubtime`, `guid`);

```

● yqj_article => SELECT

```
DROP INDEX IF EXISTS base_article ON `yqj_article`;

CREATE INDEX base_article ON yqj_article(`base_article`);

```

● base_articlecategory => WHERE

```
DROP INDEX IF EXISTS name_level ON `base_articlecategory`;

CREATE INDEX name_level ON `base_articlecategory`(`name`, `level`);

```

● base_area => SELECT

```
DROP INDEX IF EXISTS name ON `base_area`;

CREATE INDEX name ON `base_area`(`name`);

```

● base_inspection => SELECT

```
DROP INDEX IF EXISTS guid_product_title_pubtime_source_qualitied_url_level ON `base_inspection`;

CREATE INDEX guid_product_title_pubtime_source_qualitied_url_level ON  `base_inspection`(`guid`, `product`, `title`, `pubtime`, `source`, `qualitied`, `url`, `level`);
```
