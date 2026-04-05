# Kravspecifikation för projekt: **Lynx**

Av Oscar Hellgren Te23A Ebersteinska Gymnasium 

## 1. Innehålls förtekning
1. <a href="#1-innehålls-förtekning">Innehålls förtekning</a>
2. <a href="#2-bakgrund">Bakgrund</a>
3. <a href="#3-beskrivning">Beskrivning</a>
4. <a href="#4-målgrupp">Målgrupp</a>
5. <a href="#5-funktionella-krav">Funktionella krav</a>
6. <a href="#6-tekniska-val">Tekniska val</a>



## 2. Bakgrund

### 2.1 Idé 1
Allting började med att jag Vibe koda med Claude. Då försökte jag först framställa ett program för krypterad chattrum som jag kunde använda med mina vänner. Programet var mest utsed till att vara en rolig grej. Eftersom att det mest var ett roligt mini-project beslöt jag mig för att implementera kommandon som gav mig möjlighet att göra harmlösa spratt på min kompis dator (ex skaka muspekaren).


### 2.2 Idé 2
Jag tyckte prank biten var kul att jag slopa hela chatt idén. Istället kom jag på att jag ville göra ett program som gav mig en bakväg in i flera av mina vänners datorer och erbjöd mig att utföra spratt. Jag började försöka utveckla mitt nya projekt med Claude. Men Claude vägra hjälpa mig utveckla min idé. Claude förklara för mig att det jag ville göra kallades för en RAT vilket generellt är oetiskt och klassas i nästan alla fall som skadlig programvara.


### 2.3 Vad är en RAT?
Jag kan börja med att säga vad RAT står för då namnet ger en ganska tydlig bild över vad det är för något. RAT står för **R**emote **A**ccess **T**rojan. Alltså låter någon från fjärran komma åt och styra en dator med hjälp av ett trojan program. Ett trojan program är som i berättelsen om trojanska hästen, något som ser ut som ett bra sak på utsidan men i verkligheten kan göra hemska saker. Ett RAT program är ett program som maskerar sig för att vara ett hedligt program men som i bakgrunden kan exekvera kod, övervaka användaren, stjäla inloggnings uppgifter/lösenord/koder men också mycket mer saker. Den data den samlar skickas till den som står för programmet. 




## 3. Beskrivning

### 3.1 Övergripande
Min RAT består av flera delar. Dessa beskrivs nedan. Tillsammans bildar de ett system som tillåter mig skämtas lite med mina kompisar och är utvecklat ur ett forsknings perspektiv samt för att utveckla mina kunskaper om cyber säkerhet, nätverks infrastruktur och hur man driver ett större programerings projekt.


### 3.2 Server program ("Offer")
Server programet är det program som "offret" har blivit injecerat med. Dens huvudsakliga uppgifter är annonsering, gå att ansluta till, hantera bra/dåliga anslutningar och sedan utföra de spratten jag vill implementera.

Annonseringen är att programmet ropar ut på nätet "Jag är här". Rent praktiskt kommer den att sända dator namnet (hostname) på broadcast ip addressen. Denna utsändning kan fångas upp av admin programet och visar mig vilket "offer" som just nu är aktivt och går att ansluta till. Dock låter denna metod att fler människor än mig kan läsa det. Vilket innebär en säkerhetsrisk för "offret".

Jag är inte ett fan av säkerhetsrisker därför för att hantera farliga anslutningar tar programmet automatiskt hand om det. Därför ska programet ha en dedikerad funktion för detta.

Dessutom kommer det som kan exekveras vara förutbestämt för att förhindra skadlig användning.

Jag vill skydda "offret" så mycket som möjligt från främande.


### 3.3 Klient program (Jag/admin)
Admin/klient programet är det programet som hittar och kopplar upp mot offer datorn. Programets gränssnitt ska vara som CLI baserat (likna linux terminalen) för att vara lätt att använda samt det ser coolt ut.


### 3.4 Krypterings modul
För att skydda "offret" mer vill jag också utveckla min egna krypterings algoritm för att kunna dela krypterade nycklar som ingen kan läsa eller veta vilka de är. (Om jag hinner)


### 3.5 Injektions program (Trojan)
Detta program ansvarar för att injecera server ṕrogramet. Tanken är att trojan programet ska vara ett program som på ytan ser ut att bara vara ett spel eller liknande. Men i själva verket läggs server filen i mappen för de program som automatiskt startar.


### 3.6 Varför är min RAT etisk? (Sammanfattning)
Varför är just min RAT mer etisk än andra? Svaret: Den är inte etisk. Detta program är per definition skadlig programvara. Men det behöver inte betyda att den inte är utformad för att vara skadlig, permanent eller i syfte av att förstöra. Ja, den kommer vara irriterande och ja den kommer vara svår att hitta och oskadliggöra själv. Men den är just bara det, irriterande och inte permanent. Detta projekt är endast utvecklat i forsknings syfte.




## 4. Målgrupp
Folk som vill lära sig mer om hur sådant här fungerar och också har ett intresse för programering och nätverk.




## 5. Funktionella krav
### 5.1 Server program ("Offer")
1. Annonsera sig själv. 
2. Sätta upp en server som en klient kan ansluta till
3. Kunna se ifall inkommande anslutningar är dåliga och då släppa kontakten och stänga ned programet för denna körning.
4. Skicka beskrivande debug i terminalen
5. Programet ska kunna ta bort sig själv när jag vill. (Self destruct)


### 5.2 Klient program (Jag/admin)
1. Ha ett command line gränssnitt är funktionellt men även estestiskt
2. Kunna upptäcka "offren" och sortera ut ev. rest
3. Ansluta till dem och kunna skicka komandon.


### 5.3 Krypterings modul
1. Kunna kryptera lösenord men också kunna göra det på ett effektivt sätt


### 5.4 Injektions program (Trojan)
1. En vacker framsida och hemsk baksida.
2. Flytta fil till rätt mapp.




## 6. Tekniska val
### 6.1 Översikt
1. använder python för att det är det språk jag kan bäst. Jag använder socket modulen för att hantera nätverksbiten.

### 6.2 Server program ("Offer")
1. Annonserar sig själv med UDP packet på broadcast ip addressen, UDP för att de är snabba och det spelar ingen roll om de kommer fram eller ej. 
2. Använder TCP för att packeten ska komma fram


### 6.3 Klient program (Jag/admin)
1. Valde lätt gränssnit för att det är coolt och man kan få det ganska snyggt