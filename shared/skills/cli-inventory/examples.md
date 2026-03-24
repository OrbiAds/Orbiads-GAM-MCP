# Examples

## List all ad units

```bash
$ orbiads inventory ad-units --json
[{"id": "12345", "name": "Homepage_Leaderboard", "sizes": ["728x90"], "status": "ACTIVE"}, {"id": "12346", "name": "Homepage_MPU", "sizes": ["300x250"], "status": "ACTIVE"}]
```

## Search ad units by name

```bash
$ orbiads inventory ad-units --search "homepage" --json
[{"id": "12345", "name": "Homepage_Leaderboard", "sizes": ["728x90"], "status": "ACTIVE"}]
```

## List targeting keys

```bash
$ orbiads inventory keys --json
[{"name": "section", "values": ["sport", "news", "tech"]}, {"name": "device", "values": ["desktop", "mobile", "tablet"]}]
```

## List placements

```bash
$ orbiads inventory placements --json
[{"id": "98765", "name": "ROS_Standard", "adUnitIds": ["12345", "12346"]}]
```
