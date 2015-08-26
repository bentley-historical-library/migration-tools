Open Refine
===========

<famname>
---------

Before anything else, you'll need to find any <persname> texts that have accidentally found their way into the <famname> text. These change in the EAD! This regex seems to get you part of the way there: ^[A-Za-z]+\,[^,]*$

You'll also need to check for and delete duplicates from the original CSV. These usually appear when a source hasn't been filled out, and you can find them by doing a custom facet on blanks. Of course, if there isn't a duplicate for a row when you filter this way, add the proper source.

  1. Create new column WORKING based on column ORIGINAL by filling 404 rows with grel:value
  
We don't want to mess with the originals (or at least we want to have these for reference).
  
  2. Text transform on 380 cells in column WORKING: grel:value.replace(/\.$/, '')
  
Gets rid of any ending periods. We weren't consistent about this, plus ArchivesSpace handles this when it creates the sort name. Plus, these aren't actually included in LCNAF, I think they're a MARC thing.
  
  3. Text transform on 1 cells in column WORKING: grel:value.replace('â€™', "'")
  
Character encoding issues, which we found just by looking and which we are handling on a case-by-case basis. Hopefully we didn't miss any.
  
  4. Text transform on 1 cells in column WORKING: grel:value.replace('Ã©', 'é')
  
See above.
  
  5. Text transform on 1 cells in column WORKING: grel:value.replace('Family (William Montague Ferry family)', '(Family: Ferry, William Montague, 1796-1867)')
  
Handles exceptions, again case-by-case. We found these by filtering the WORKING column looking for strings with an open parenthesis in it. Hopefully we didn't miss any.
  
  6. Text transform on 1 cells in column WORKING: grel:value.replace('Woodruff Family Papers', 'Woodruff (Family)')
  
See above.
  
  7. Text transform on 401 cells in column WORKING: grel:value.replace(/ Family| family/, ' (Family)')
  
Formats the family part according to RDA, which superceded AACR2.
  
  8. Text transform on 404 cells in column Family Name: grel:cells['WORKING'].value.split(' (')[0]
  
Throws the family name in the Family Name column.
  
  9. Text transform on 404 cells in column Qualifier: grel:'(' + cells['WORKING'].value.split(' (')[1]
  
Throws the qualifier in the Qualifier column.

  10. Remove column WORKING
  
Removes the WORKING column we created at the beginning.

  11. Fill down 1 cells in column Source
  
Makes sure we aren't missing any sources. These are required in ArchivesSpace.

We're done!

<corpname>
----------

Before anything else, you'll need to find any <persname> texts that have accidentally found their way into the <famname> text. These change in the EAD! This regex gets you part of the way there: ^[A-Za-z]+\,[^,]*$

After that, I filtered on things like Company and Inc as well as and and &, starred those rows, and then filtered by no stars on the column I had already filtered on the above regex.

You'll also need to look for <geogname> mistakes.

You'll also need to check for and delete duplicates from the original CSV. These usually appear when a source hasn't been filled out, and you can find them by doing a custom facet on blanks. Of course, if there isn't a duplicate for a row when you filter this way, add the proper source.

  1. Text transform on 8 cells in column Source: grel:value.replace('AACR2', 'aacr2').replace('lchaf', 'lcnaf').replace('local', 'Local sources')
  
This brings all the sources into the appropriate controlled vocabulary.

  2. Create new column WORKING based on column ORIGINAL by filling 5694 rows with grel:value
  
We don't want to mess with the originals (or at least we want to have these for reference).

  3. Text transform on 3787 cells in column WORKING: grel:value.replace(/\.$/, '')
  
Gets rid of any ending periods. We weren't consistent about this, plus ArchivesSpace handles this when it creates the sort name. Plus, these aren't actually included in LCNAF, I think they're a MARC thing.
  
  4. Text transform on 1 cells in column WORKING: grel:value.replace('â€™', "'")
  
Character encoding issues, which we found just by looking and which we are handling on a case-by-case basis. Hopefully we didn't miss any.
  
  5. 
  
See above.

We're done!

<persname>
----------
