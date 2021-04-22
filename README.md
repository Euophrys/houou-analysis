# houou-analysis
 Scripts for analysing Houou replays. Results can usually be found on [my blog](https://pathofhouou.blogspot.com/), if they're interesting. My past analysis scripts can be found at my [phoenix-logs](https://github.com/Euophrys/phoenix-logs/tree/develop/analysis) fork.

I'm making a new repo because this one will contain breaking changes. Tiles are now from 0 to 33 instead of 0 to 37 (no separate storage for aka). Hands are now Counters instead of lists.

This breaks the old shanten code, but enables the new shanten code in the spine_shanten folder to work. This shanten code is about nine times faster on a fresh hand and much much faster for progressive hands. The code was ported to Python from [spinesheath's C# repo](https://github.com/spinesheath/Spines.Mahjong/tree/master/Analysis).

To get the replays, use [ApplySci's phoenix-logs repo](https://github.com/ApplySci/phoenix-logs), or download some of the databases from [this Google Drive folder](https://drive.google.com/drive/u/0/folders/1danHelDPYF2YP9Er2HhJCemlVQN25nb_). For a reference of the Tenhou log format, see [here](https://github.com/ApplySci/tenhou-log#log-format).