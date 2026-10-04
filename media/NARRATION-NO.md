# Norsk hovedmanus

## 1 · Spørsmålet

Hva betyr det egentlig å eie en digital tjeneste? Ikke bare å betale en
leverandør. Ikke bare å ha en innlogging. Men å kunne se kildekoden, forstå
identiteten, ta en verifiserbar sikkerhetskopi og faktisk flytte tjenesten når
du trenger det.

Vi bygget derfor en komplett, liten demonstrator på noen få fokuserte dager.
Den er åpen kildekode, kjører lokalt med syntetiske data og er laget for å
svare på ett konkret spørsmål: Kan tjenesten forlate mål A og fungere på mål B
uten at vi bare lover at det skal gå?

## 2 · Hva løsningen består av

Demoen har en liten notattjeneste, PostgreSQL for data, Keycloak for ekte OIDC-
identitet, rollebasert tilgang, en strukturert auditlogg og en kryptert Restic-
sikkerhetskopi. Alt er versjonert. Containerbilder er låst til bestemte
digest-verdier, og Python-avhengighetene er låst med hashverdier.

Det betyr ikke at dette er en ferdig bedriftsplattform. Det betyr at alle
viktige deler av demonstrasjonen kan inspiseres, bygges og testes av andre.

## 3 · Identitet som faktisk avviser

En sikkerhetstest er ikke bare en vellykket innlogging. Vi kontrollerte også
det som skal stoppes. En forespørsel uten token ble avvist. Et token laget for
feil mottaker ble avvist. En vanlig bruker fikk ikke åpne administratorens
auditoversikt. Og en konto som fortsatt måtte registrere TOTP, fikk ikke hoppe
over det steget.

Samtidig fungerte gyldig bruker- og administratortilgang. Auditloggen lagret
handling, resultat, mål og en kort hash av identiteten—ikke passord, bearer-
token eller teksten i notatet.

## 4 · Selve flyttingen

Først opprettet vi to helt fiktive poster på mål A. Deretter stoppet og startet
vi A for å bevise at dataene overlevde vanlig drift. Antall poster og en
deterministisk SHA-256-fingeravtrykk var identisk før og etter.

Så eksporterte vi PostgreSQL-dataene. Eksporten fikk en kontrollsum, ble lagt i
et kryptert Restic-repository og kontrollert med Restics egen integritetstest.

Deretter kom det viktigste punktet: applikasjonen og databasen på mål A ble
stoppet før mål B fikk bli godkjent. Sikkerhetskopien ble gjenopprettet, lastet
inn i en separat database på B og testet med de samme tilgangskontrollene.

Resultatet var to av to poster og nøyaktig samme innholdshash. Den komplette
applikasjons- og dataflyttingen tok 24,843 sekunder i denne lille testen.
Backupdelen tok 6,457 sekunder. Samplet samlet toppminne var omtrent 665 MiB.

Dette er målinger fra én liten syntetisk demo på én vert. De er ikke et løfte
om kapasitet, oppetid eller ytelse i produksjon.

## 5 · Det vi bevisst ikke skjuler

Identitetstjenesten var felles under flyttingen. Vi har derfor ikke kalt dette
en målt identitetsmigrering. En virkelig flytting av identitet krever blant
annet ny utsteder, nøkkelrotasjon, klientendringer og vanligvis ny registrering
av sterk autentisering.

Keycloak kjører også i utviklingsmodus med et lite innebygd lager. Demoen har
ikke høy tilgjengelighet, offentlig TLS, produksjonsovervåkning eller
sertifisering. Den skal lære bort og bevise en begrenset prosess—ikke skjule
veien fra demonstrasjon til drift.

Det samme gjelder fysisk teknologi. RFID-kort, fingeravtrykkslesere, WebAuthn-
nøkler og andre adgangskomponenter kan vurderes som senere oppgraderinger. Vi
har ikke bestilt, integrert eller testet et fysisk kort i denne leveransen.

## 6 · Hvorfor åpen kildekode

Når kildekoden er åpen, er ikke verdien en hemmelig ZIP-fil. Verdien ligger i å
forstå miljøet, integrere det mot virksomhetens systemer, velge riktige
sikkerhetsgrenser og øve på gjenoppretting før det haster.

Du kan klone prosjektet fra både GitHub og GitLab, lese alle filene og kjøre
hele testen selv. Hemmelighetene genereres lokalt og legges aldri i Git. Når
testen er ferdig, er alle democontainere stoppet, mens de små øvingsvolumene kan
beholdes til neste gjennomgang.

## 7 · Hvordan dette kan brukes

En bedrift med egne teknikere kan bruke rammen til intern opplæring og bygge
videre selv. En bedrift som vil ha støtte, kan velge hvor vår kompetanse skal
inn: vurdering, sikker arkitektur, integrasjon, dokumentasjon, en full
overlevering eller videre forvaltning.

Mange ganger er den beste og mest bærekraftige løsningen å oppgradere den delen
som faktisk er utdatert, ikke å kaste alt. Du kan skaffe den maskinvaren som
passer. Vi kan hjelpe med de digitale integrasjonene, testene og en trygg vei
videre.

## 8 · Avslutning

Dette prosjektet viser ikke at alle skyløsninger er enkle. Det viser at eierskap
kan gjøres konkret: kilde du kan lese, data du kan eksportere, backup du kan
kontrollere og en flytting du kan gjenta.

Se den åpne kildekoden. Les det maskinlesbare beviset. Kjør den lille demoen
selv. Og hvis du vil gjøre prinsippet virkelig i din virksomhet, ta kontakt med
IntentForce.
