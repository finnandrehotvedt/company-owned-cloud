# Norsk kortfilm · under 3 minutter

Hva betyr det å eie en digital tjeneste? Vi ville ikke svare med et slagord,
men med en test.

På noen få fokuserte dager bygget vi en komplett liten demonstrator med åpen
kildekode: en notattjeneste, PostgreSQL, ekte Keycloak OIDC, roller, en
innholdsminimert auditlogg og kryptert Restic-backup.

Først testet vi identiteten. Gyldig bruker og administrator fungerte. Manglende
token, feil audience, utilstrekkelig rolle og en konto som fortsatt måtte
registrere TOTP, ble avvist.

Så la vi to syntetiske poster på mål A. Etter en full omstart hadde vi fortsatt
samme antall og samme SHA-256-fingeravtrykk.

Dataene ble eksportert, kontrollsummert og lagret i en kryptert backup. Deretter
stoppet vi både appen og databasen på A før B fikk bli godkjent. På B
gjenopprettet vi databasen, kjørte tilgangstestene og sammenlignet staten.

To av to poster. Nøyaktig samme innholdshash. Backupdelen tok 6,457 sekunder,
og hele applikasjons- og dataflyttingen tok 24,843 sekunder. Samplet toppminne
var omtrent 665 MiB.

Dette er en liten målt demo—ikke en produksjonsplattform eller et
kapasitetsløfte. Identitetstjenesten var felles og ble ikke migrert. Fysiske
RFID- eller fingeravtrykkskort ble heller ikke bestilt eller testet; det er bare
eksempler på mulige senere oppgraderinger.

Hele kildekoden og de maskinlesbare resultatene ligger åpent på GitHub og
GitLab. Du kan kjøre øvelsen selv, lære av den og bygge videre. Eller du kan
bestemme hvor IntentForce skal hjelpe: integrasjon, sikkerhet, opplæring,
overlevering eller videre drift.

Eierskap blir virkelig når du kan lese kilden, kontrollere backupen og bevise
at tjenesten kan flyttes.
