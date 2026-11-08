## Esimerkki: product ja sprint backlog GitHub Projectsilla

Tähän repositorioon on tehty esimerkkinä backlogit boilerplaten todo-sovellukselle sellaisina kuin ne voisivat olla kesken sprinttiä 2. Katso esimerkistä mallia oman ryhmäsi backlogeihin. Miniprojektin vaatimukset backlogeille löytyvät [arvosteluperusteista](https://studies.cs.helsinki.fi/ohtu/miniprojektin_arvosteluperusteet). Esimerkin backlogit ja niiden yhteys kurssin teoriaan esitellään myös kurssimateriaalin osassa 2: [Esimerkki: backlogit GitHub Projectsilla](https://studies.cs.helsinki.fi/ohtu/osa2/#esimerkki-backlogit-github-projectsilla).

### Linkit

- [Tyhjä backlog-pohja](https://github.com/orgs/ohjelmistotuotanto-hy/projects/2), jonka voi kopioida omaksi projektiksi (ks. [käyttöönotto](#valmis-pohja-kopioi-ja-ota-käyttöön))
- [Esimerkkiprojekti](https://github.com/orgs/ohjelmistotuotanto-hy/projects/1)
  - [Product backlog](https://github.com/orgs/ohjelmistotuotanto-hy/projects/1/views/1): kaikki user storyt prioriteettijärjestyksessä
  - [Sprint 1 backlog](https://github.com/orgs/ohjelmistotuotanto-hy/projects/1/views/2): valmis sprintti, kaikki taskit Done-tilassa
  - [Sprint 2 backlog](https://github.com/orgs/ohjelmistotuotanto-hy/projects/1/views/3): käynnissä oleva sprintti
  - [Sprint 1 burnup](https://github.com/orgs/ohjelmistotuotanto-hy/projects/1/insights/3) ja [Sprint 2 burnup](https://github.com/orgs/ohjelmistotuotanto-hy/projects/1/insights/4): sprinttikohtaiset burnup-kaaviot (ks. [miksi kaaviot näyttävät oudoilta](#miksi-esimerkin-burnup-kaaviot-näyttävät-oudoilta))
- [Issuet](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues?q=is%3Aissue): jokainen user story ja taski on oma issuensa
  - [User storyt](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues?q=is%3Aissue+label%3A%22user+story%22)
  - [Taskit](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues?q=is%3Aissue+label%3Atask)

### Mitä esimerkistä kannattaa katsoa

**Product backlog** on DEEP:

- storyt ovat prioriteettijärjestyksessä, tärkein ylimpänä
- ylimmät storyt on kuvattu tarkasti ja niille on kirjattu hyväksymiskriteerit, esim. [#3](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues/3)
- mitä alempana story on, sitä karkeampi se saa olla, esim. [#38](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues/38) tarkennetaan asiakkaan kanssa vasta myöhemmin
- storyja ei estimoida, sillä miniprojektissa sitä ei vaadita
- backlogista näkyy jokaisen storyn status ja sprintti, johon se on otettu

**Sprint backlog:**

- sprinttiin valitut storyt on jaettu teknisen tason taskeiksi. Taskit ovat storyn _sub-issueita_, esim. story [#22](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues/22) ja sen taskit
- jokaisella taskilla on status (Todo, In Progress, Done) ja tekijä (Assignees)
- sprinttiin kuuluu myös taskeja, jotka eivät liity mihinkään storyyn, esim. CI:n konfigurointi [#41](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues/41) ja retrospektiivi [#44](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues/44)

**Hyväksymiskriteerit:**

- sprintin 1 storyissa hyväksymiskriteerit on kirjattu issueen tekstinä, esim. [#8](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues/8)
- sprintistä 2 alkaen hyväksymiskriteerit kirjoitetaan Robot Framework -testeiksi, ja issuessa on linkki testitiedostoon, esim. [#17](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/issues/17) → [todos.robot](src/story_tests/todos.robot)

### Valmis pohja: kopioi ja ota käyttöön

Valmis tyhjä pohja on [Miniprojekti – backlog-template](https://github.com/orgs/ohjelmistotuotanto-hy/projects/2). Siinä on valmiina:

- kentät _Sprint_ (Sprint 1–4) ja _Tyyppi_ (User story / Task)
- näkymät _Product backlog_ ja _Sprint 1–4 backlog_
- burnup-kaaviot _Sprint 1–4 burnup_

Pohjan käyttöönotto:

1. Avaa [pohja](https://github.com/orgs/ohjelmistotuotanto-hy/projects/2) ja valitse oikean yläkulman _..._ → _Make a copy_.
2. Valitse omistajaksi ryhmän repositorion omistaja (käyttäjä tai organisaatio) ja anna projektille nimi. Kopioon tulevat kentät, näkymät ja kaaviot, mutta ei sisältöä.
3. Vaihda kopion asetuksista (_..._ → _Settings_) _Visibility_ arvoon _Public_.
4. Linkitä projekti ryhmän repositorioon: repositorion _Projects_-välilehti → _Link a project_.
5. Laita projektin _Workflows_-asetuksista päälle _Auto-add to project_ ryhmän repositoriolle, niin uudet issuet tulevat projektiin automaattisesti.
6. Kirjatkaa storyt ja taskit issueina ja asettakaa niille projektissa kentät _Tyyppi_ ja _Sprint_. Näkymät ja kaaviot suodattavat _Tyyppi_-kentän perusteella, joten labeleita ei tarvita.

Alla oleva ohje kertoo, miten sama rakennetaan alusta asti itse. Sitä kannattaa lukea myös pohjaa käyttäessä, sillä siinä selitetään, mitä kukin osa tekee.

### Ohje: näin teette backlogit omalle projektillenne

#### 1. Luo projekti

1. Mene GitHubissa ryhmänne repositorioon ja avaa välilehti _Projects_ → _New project_
2. Valitse pohjaksi _Table_ ja anna projektille nimi
3. Avaa projektin asetukset (oikean yläkulman _..._ → _Settings_) ja vaihda _Visibility_ arvoon _Public_. **Backlogien tulee olla koko maailman luettavissa.**
4. Jos loit projektin jostain muualta kuin repositoriosta, linkitä se repositorioon: repositorion _Projects_-välilehti → _Link a project_

#### 2. Lisää tarvittavat kentät ja labelit

1. Lisää projektiin kenttä _Sprint_: taulukon otsikkorivin _+_ → _New field_ → tyypiksi _Single select_ ja vaihtoehdoiksi _Sprint 1_, _Sprint 2_, _Sprint 3_ ja _Sprint 4_. Myös tyyppi _Iteration_ käy.
2. Tarkista, että _Status_-kentässä on vaihtoehdot _Todo_, _In Progress_ ja _Done_. Voit lisätä myös muita tiloja, esim. _Testing_.
3. Luo repositorioon labelit `user story` ja `task`: _Issues_ → _Labels_ → _New label_. Labelien avulla storyt ja taskit on helppo erottaa toisistaan näkymissä.

#### 3. Kirjaa user storyt

1. Luo jokaisesta user storysta issue, jolle annat labelin `user story`. Otsikoksi tulee story, esim. _Käyttäjänä voin lisätä uuden todon_.
2. Kirjaa issueen hyväksymiskriteerit. Sprintistä 2 alkaen kriteerit kirjoitetaan Robot-testeiksi, ja issueen laitetaan linkki testitiedostoon.
3. Lisää issue projektiin (issuen oikea sivupalkki → _Projects_). Vaihtoehtoisesti voit lisätä kaikki issuet automaattisesti: projektin _..._ → _Workflows_ → _Auto-add to project_.
4. Järjestä storyt prioriteettijärjestykseen raahaamalla rivejä taulukossa.

#### 4. Tee product backlog -näkymä

1. Nimeä projektin oletusnäkymä uudelleen nimelle _Product backlog_ (tuplaklikkaa välilehden nimeä).
2. Kirjoita näkymän suodatinkenttään `label:"user story"`, jolloin näkymässä näkyvät vain storyt.
3. Lisää sarakkeiksi _Status_, _Sprint_ ja _Sub-issues progress_.
4. Tallenna näkymä (_Save_).

#### 5. Sprintin suunnittelu ja sprint backlog

1. Merkitse sprinttiin valituille storyille _Sprint_-kenttään oikea sprintti.
2. Pilko storyt taskeiksi: avaa storyn issue ja valitse _Create sub-issue_. Anna taskille label `task` ja aseta sen _Sprint_-kenttä. Storyyn kuulumattomat taskit, kuten CI:n konfigurointi, luodaan tavallisina issueina.
3. Luo uusi näkymä _New view_ → _Board_ ja nimeä se esim. _Sprint 1 backlog_.
4. Kirjoita suodattimeksi `sprint:"Sprint 1" label:task`. Board ryhmittelee kortit _Status_-kentän mukaan sarakkeisiin.
5. Laita näkymän asetuksista (_View_ → _Fields_) näkyviin _Assignees_ ja _Parent issue_, jolloin kortista näkee tekijän ja storyn.
6. Tee jokaiselle sprintille oma näkymänsä.

#### 6. Sprintin aikana

- Kun aloitat taskin, merkitse itsesi sen tekijäksi (_Assignees_) ja siirrä kortti sarakkeeseen _In Progress_.
- Kun taski on valmis, sulje issue. Kortti siirtyy automaattisesti _Done_-sarakkeeseen, jos projektin workflow _Item closed_ on päällä (oletuksena on).
- Story merkitään valmiiksi vasta, kun se on toteutettu _definition of donen_ mukaisesti.
- Seuraa sprintin etenemistä sprintin burnup-kaaviosta, ks. seuraava kohta.

#### 7. Sprinttikohtainen burnup-kaavio

GitHub Projects piirtää burnup-kaavion valmiiksi suljettujen issueiden perusteella. Projektin oletuskaavio sisältää kaikki issuet, joten jokaiselle sprintille kannattaa tehdä oma kaavionsa:

1. Avaa projektin _Insights_-välilehti (projektin oikea yläkulma) ja valitse vasemmasta palkista _New chart_.
2. Uusi kaavio on oletuksena pylväskaavio. Muuta se burnupiksi: _Configure_ → _Layout_: _Stacked area_ ja _X-axis_: _Time_. Tallenna (_Save_).
3. Kirjoita kaavion suodatinkenttään `sprint:"Sprint 1" label:task`, jolloin kaavio laskee vain sprintin taskit, ja tallenna (_Save_).
4. Nimeä kaavio esim. _Sprint 1 burnup_ klikkaamalla kynä-ikonia nimen vieressä.
5. Seuraavan sprintin kaavion saa helpoimmin kopioimalla: kaavion nimen vieressä oleva _..._ → _Duplicate chart_. Vaihda kopioon suodatin (`sprint:"Sprint 2" label:task`) ja nimi.
6. Kaavion aikaväliä voi rajata yläpuolen napeilla (_2 weeks_, _1 month_, ...) tai valikosta _Custom range_, esim. sprintin alku- ja loppupäivään.

Kaavio näyttää ajan funktiona, kuinka monta taskia sprintissä on kaikkiaan ja kuinka moni niistä on valmis. Kun taskeja suljetaan pitkin sprinttiä, valmiiden käyrä nousee kohti kokonaismäärää. Jos käyrä pysyy pitkään tasaisena ja nousee vasta sprintin lopussa, taskit ovat todennäköisesti liian isoja tai niitä ei suljeta sitä mukaa kuin ne valmistuvat.

Kaavio perustuu issueiden avaamis- ja sulkemisajankohtiin, joten se näyttää järkevältä vain, jos taskit oikeasti suljetaan silloin, kun ne valmistuvat.

##### Miksi esimerkin burnup-kaaviot näyttävät oudoilta

Esimerkin kaavioissa molemmat käyrät pysyvät nollassa koko aikavälin ja nousevat aivan oikeassa reunassa yhdellä kertaa lopulliseen arvoonsa. Sprintin 1 kaaviossa kumpikin käyrä nousee 16:een, sprintin 2 kaaviossa kokonaismäärä nousee 13:een ja valmiiden määrä 6:een.

Syy on se, että esimerkkiprojektin kaikki issuet luotiin skriptillä muutaman minuutin aikana 29.10.2026, ja valmiiksi merkityt taskit suljettiin heti luomisen jälkeen. GitHubin näkökulmasta kummankin sprintin kaikki taskit siis syntyivät ja valmistuivat samana päivänä, eikä kaaviolla ole mitään historiaa näytettävänä. Sprint-kentän arvolla ei ole vaikutusta siihen, mihin ajankohtaan taski kaaviossa sijoittuu.

Oikeassa projektissa kaavio näyttäisi toiselta:

- kokonaismäärän käyrä nousee sprintin suunnittelussa, kun taskit luodaan, ja myöhemmin pienin askelin, jos taskeja lisätään kesken sprintin
- valmiiden käyrä nousee portaittain sitä mukaa kuin taskeja suljetaan
- sprintin lopussa käyrät ovat lähellä toisiaan, jos sprinttiin valitut taskit saatiin valmiiksi
- käyrien välinen ero kertoo milloin tahansa, paljonko työtä on vielä jäljellä

#### 8. Linkitä backlogit README:hen

Lisää README:hen linkit product backlogiin ja sprint backlogeihin. Tarkista kirjautumattomana (esim. selaimen incognito-ikkunassa), että linkit toimivat.
