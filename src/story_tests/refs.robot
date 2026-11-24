*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References


*** Test Cases ***

No references displayed when nothing in database
    Go To  ${HOME_URL}
    Get Title  ==  References
    Get Text  h1  ==  0 references
    Get Text  body  *=  No references yet


Book references that are in database are also displayed
    Go To  http://${SERVER}/seed_db
    Go To  ${HOME_URL}
    Get Text  h1  ==  4 references
    Get Element Count  .reference  ==  4
    Get Text  body  *=  Clean Code: A Handbook of Agile Software Craftsmanship
    Get Text  body  *=  Robert C. Martin
    Get Text  body  *=  \\cite{Martin08}
    Get Text  body  *=  \\cite{Gamma94}
    Get Text  body  *=  \\cite{Fowler99}
    Get Text  body  *=  \\cite{Thomas19}


User can add a new book reference
    Go To  http://${SERVER}/references/new
    Fill Text  input[name="key"]  Knuth97
    Fill Text  input[name="author"]  Donald E. Knuth
    Fill Text  input[name="title"]  The Art of Computer Programming
    Fill Text  input[name="year"]  1997
    Fill Text  input[name="publisher"]  Addison-Wesley
    Fill Text  input[name="pages"]  1-10
    Click  button[type="submit"]
    Get Text  h1  ==  1 reference
    Get Text  body  *=  \\cite{Knuth97}
    Get Text  body  *=  The Art of Computer Programming


User can add a new article reference
    Go To  http://${SERVER}/references/new
    Select Options By  select[name="reference_type"]  value  article
    Fill Text  input[name="key"]  Dijkstra68
    Fill Text  input[name="author"]  Edsger W. Dijkstra
    Fill Text  input[name="title"]  Go To Statement Considered Harmful
    Fill Text  input[name="year"]  1968
    Fill Text  input[name="journal"]  Communications of the ACM
    Fill Text  input[name="pages"]  147-148
    Click  button[type="submit"]
    Get Text  h1  ==  1 reference
    Get Text  .reference .reference-type  ==  ARTICLE
    Get Text  .reference h2  ==  Go To Statement Considered Harmful
    Get Text  .reference .citation-key  ==  \\cite{Dijkstra68}
    Get Text  .reference .metadata  *=  Author
    Get Text  .reference .metadata  *=  Edsger W. Dijkstra
    Get Text  .reference .metadata  *=  Year
    Get Text  .reference .metadata  *=  1968
    Get Text  .reference .metadata  *=  Journal
    Get Text  .reference .metadata  *=  Communications of the ACM
    Get Text  .reference .metadata  *=  Pages
    Get Text  .reference .metadata  *=  147-148


User can edit a reference
    Go To  http://${SERVER}/seed_db
    Go To  ${HOME_URL}
    Hover  .reference >> nth=0
    Click  .edit-reference >> nth=0
    Get Text  h1  ==  Edit book reference
    Get Property  input[name="key"]  value  ==  Martin08
    Fill Text  input[name="title"]  Clean Code (2nd Edition)
    Fill Text  input[name="year"]  2009
    Click  button[type="submit"]
    Get Text  h1  ==  4 references
    Get Text  body  *=  Clean Code (2nd Edition)
    Get Text  body  *=  2009


