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

