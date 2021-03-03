
-ID can be Barcode or Catalog Number
![Catalog Number](IMG_20210303_042458.jpg?raw=true)
![Barcode](IMG_20210303_042514.jpg?raw=true)
-CD [Optional] Must be stated if there is more than one CD in Album
-D Destination for Rename and Tagging
-AA Loads Album Art (You must install Pillow for Album Artworks)
-M Loads Metadata
-S Search in Database (for Album)

Example

Vgmdb.py -ID 4534530127365 -CD 2 -D "D:\NEWMEDIA\Musik\Collection\[OST] [FLAC] The Promised Neverland S1-2 OST\CD 2" -AA -M
Vgmdb.py -ID 4534530127365 -S
Vgmdb.py -ID SVWC-70521~2 -S

NOTE:

TRACKS MUST BE IN CHRONOLOGICAL NAMING ORDER:

Example:

RIGHT:

01 Track.flac
02 Track.flac
03 Track.flac

---------

Track01.flac
Track02.flac
Track03.flac


WRONG: 

11 Track01.flac
10 Track02.flac
09 Track03.flac