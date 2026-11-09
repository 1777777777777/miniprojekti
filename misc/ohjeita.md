## Muutamia vihjeitä projektin alkuun

Ihmisten välinen yhteistyö on suurin haaste ohjelmistojen kehittämiseen, ja erityisen haastavaa se on projektin alussa. Seuraavassa muutama vihje/checklist projektin käynnistämiseen.

- [ ] tehkää esittäytymiskierros
- [ ] luokaa jokin yhteinen kommunikaatiokanava, esim. Discordiin, Telegramiin, yms
> [!NOTE]
> Tutkimukseen osallistuvat:
> - [ ] kommunikaatiokanava Discord
> - [ ] luo uusi serveri miniprojektia varten
> - [ ] nimeä serveri tiiminne nimen mukaan
> - [ ] lisää [study-helper-bot](https://discord.com/oauth2/authorize?client_id=1568902809498423358&permissions=66560&integration_type=0&scope=bot+applications.commands) serverille
> - [ ] Botilla on komento `/status`, tarkista sen avulla että botti on toiminnassa
- [ ] jokainen liittyy kanavalle
- [ ] sopikaa yhteisistä työskentelyajoista
  - mahdollisimman monta tuntia viikossa
  - mielellään kampuksella paikan päällä, mutta jos se ei onnistu niin esim Discordin äänikanavalla
- [ ] luokaa projektillenne GitHub-repositorio
- [ ] luokaa alustava product ja sprint backlog
  - mielellään heti, jos se ei onnistu niin sopikaa että esim. kaksi teistä yhdessä hoitaa asian
- [ ] lisätkää repositorioon sovelluksen runko
  - runko voi olla esim Flask-sovellus jonka ainoa toiminnallisuus on etusivu, joka toteaa "Hello World"
  - mieluiten yhdessä, jos se ei onnistu niin sopikaa että esim. kaksi teistä yhdessä hoitaa asian
- [ ] sopikaa yhteisistä koodaus- ja versionhallintakäytänteistä
  - määritelkää definition of done
  - miettikää miten käytätte brancheja
- [ ] lisätkää Robot-testi, joka testaa että sovelluksen etusivu toimii, ja määritelkää GitHub Action, joka suorittaa testin
  - vastuulliseksi voi valita jälleen esim. kaksi ryhmäläistä
- [ ] Ota projektin tietokanta käyttöön
  - sovellus käyttää SQLitea, joka ei vaadi erillisen tietokantapalvelimen asentamista tai käynnistämistä, vaan tietokanta on yksittäinen tiedosto
  - luo projektin juureen `.env`-tiedosto, jossa määritellään ainakin seuraavat muuttujat:
    ```
    DATABASE_URL=sqlite:///database.db
    SECRET_KEY=jokinsalaisuus
    ```
  - aja komento `uv run python src/db_helper.py`, joka luo tietokantaan [src/schema.sql](../src/schema.sql):ssa määritellyt taulut
    - komento voidaan ajaa uudelleen aina kun taulujen rakennetta muutetaan, sillä se pudottaa olemassa olevat taulut ennen uusien luomista
  - tietokantatiedostoa (esim. `database.db`) ei lisätä versionhallintaan
  - vastuulliseksi voi valita esim. kaksi ryhmäläistä
- [ ] Vie sovellus OKD-klusterille
  - sovelluksen tulee toimia yliopiston OKD-klusterilla jo ensimmäisen sprintin lopussa (riittää, että boilerplate tai sprintin ensimmäinen story toimii siellä)
  - asentakaa `oc`-komentorivityökalu ja kirjautukaa klusteriin [tämän ohjeen](../OKD.md) mukaan. Klusteri näkyy vain yliopiston verkosta, eli Eduroamista tai HY:n VPN:n kautta
  - tehkää sovelluksen Docker-kuvasta julkinen ja muokatkaa `kustomization.yaml` omaan projektiinne sopivaksi ja luokaa tietokannan taulut klusterille [deployausohjeen](../DEPLOYMENT.md) mukaan
  - kun sovellus on kerran viety klusterille, sen versio päivittyy automaattisesti aina kun main-haaraan pushattu koodi läpäisee GitHub Actionsin testit
  - komento `oc apply -k .` on kuitenkin suoritettava itse, jos tiedostoa `kustomization.yaml`, hakemiston `manifests` tiedostoja tai tiedostoa `secret.env` muutetaan, ks. [Milloin deployaus tulee tehdä itse?](../DEPLOYMENT.md#milloin-deployaus-tulee-tehdä-itse)
  - lisätkää linkki klusterilla toimivaan sovellukseen README:hen
  - vastuulliseksi voi valita esim. kaksi ryhmäläistä
