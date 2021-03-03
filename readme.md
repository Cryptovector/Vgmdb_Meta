
-ID can be Barcode or Catalog Number<br/>
![Catalog Number](IMG_20210303_042458.jpg?raw=true)
![Barcode](IMG_20210303_042514.jpg?raw=true)
-CD [Optional] Must be stated if there is more than one CD in Album<br/>
-D Destination for Rename and Tagging<br/>
-AA Loads Album Art (You must install Pillow for Album Artworks)<br/>
-M Loads Metadata<br/>
-S Search in Database (for Album)<br/>

Example:

Vgmdb.py -ID 4534530127365 -CD 2 -D "D:\NEWMEDIA\Musik\Collection\[OST] [FLAC] The Promised Neverland S1-2 OST\CD 2" -AA -M<br/>
Vgmdb.py -ID 4534530127365 -S<br/>
Vgmdb.py -ID SVWC-70521~2 -S<br/>

NOTE:

TRACKS MUST BE IN CHRONOLOGICAL NAMING ORDER:

Example:

RIGHT:

01 Track.flac<br/>
02 Track.flac<br/>
03 Track.flac<br/>

---------

Track01.flac<br/>
Track02.flac<br/>
Track03.flac<br/>


WRONG:

11 Track01.flac<br/>
10 Track02.flac<br/>
09 Track03.flac<br/>
