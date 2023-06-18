SQLite doesn't have a timestamp datatype. 
It can be either stored as ISO8601 strings, julian day numbers or unix time.
In this project we are gonna write them as strings, with a structure like : `YYYY-MM-DDTHH:MM:SS.SSSZ`

Ref : https://www.sqlite.org/datatype3.html, https://www.sqlite.org/lang_datefunc.html