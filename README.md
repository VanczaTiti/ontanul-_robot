# Öntanuló robot projekt

Egy kosarazó robotot építek és modellezek, majd evolucios algoritmussal megkeresek olyan bemeneteket, melyekkel a robot pontosan a megadott távolságra dobja a labdát. Célom a megfelelő bemeneteket megtalálásához szükséges dobások minimalizálása.
Ehhez genetikus algoritmust, bakteriális algoritmust és neurális hálót készítettem. Mivel a projekt célja ezen algoritmusok mélyebb megismerése, csupán numpy és math csomagokat használok.

A projekt célja, személyes fejlődésem, a mesteréges intelligencia alkalmazásában, python programozásban, és hardwear készítésben.
Az evolúciós algoritmusok, és a neurális hálózat programozásához Kóczy T. László, Tikk Domonkos, Botzheim János (2007): Intelligens rendszerek c. könyv 10. és 11. fejezetében leírtakra támaszkodtam. <br/>
A könyv itt olvasható: http://www.inf.u-szeged.hu/~dombi/lib/downloads/school/resources/intsys/Intrsz.pdf

### A robot felépítése:

A robot soros porton keresztül kommunikál a számítógéppel. A robot bemenete egy szöggyorsulás görbe dt időközönkénti értékei, kimenete a visszaesett golyó távolsága a dobás helyétől.

A robot alapját egy ferde lap adja, melyet egy keret vesz körül, hogy a golyó le ne essen. Ezen a ferde lapon helyezkedik el a dobó kar, melyet egy szervómotor hajt meg. Minden dobás azonos pozícióból indul. A kar a számítógéptől kapott szögsebesség-görbét követve remélhetőleg eldobja a golyót. Egy előre meghatározott vonalon (célvonal) a robot megméri a visszaeső golyó pozícióját, ebből határozható meg a dobás pontossága. Sikertelen dobásnak tekintek minden olyan esetet, melynél a golyó nem halad át a célvonalon, ezeket a dobásokat nagyon pontatlannak tekinti a robot.

A robot vezérlését egy arduni nano végzi. A motor egy Dynamixel AX-12A típusú szervo. A pozíció méréséhez egy TOF-Time Of Flight lézeres távolságmérőt alkalmazok, mivel ezek a szenzorok nagyon gyrövid időn belül képesek mérni, ami fontos a vonalon áthaladó golyó pozíciójának meghatározásához. 

A robot egyenlőre nem készült el. A lézeres távolságmérő nem jelenik meg a I2C eszközök között, valamint a szervó hafduplex kommunikációjához szükség van egy bufferre. 

### A dobás egyszerű modellje:

A dobas szimulációját a "dobas.py" fileban valósítottam meg. <br/>
A modellezett robot felépítését leegyszerüsítettem, néhány változtatható paraméterre. <br/>
A golyó pontszerűnek tekintem, a surlódástól eltekintek.<br/>
A golyó pályáját korlátozó keretet elhagytam, és az alapot síkot "B" dőlésszöggel jellemeztem.<br/>
A dobókart egy L alakú karnak tekintem melyet hosszával ("L"), és a kar végének sugáriránnyal bezárt szögével ("A") jellemeztem.<br/>
Paraméternek tekintem még a cél távolságot.

A dobókar pozitív irányba forog. A felvett koordinátarendszer origólya a forgástengely, x tengely vízszintes, jobbra pozitív, y tengely erre merőleges a síkra illeszkedik és felfelé pozitív.

A "dobas.py" legfontosabb függvénye a "hibafv(sebességgörbe)" függvény, ami egy egy a sebesség-görbéből, visszatér a céltól cm-ben számított hiba négyzetével.

A tesztelés során használt paraméterek: cél=-20 cm, L=5cm, A=80°, cos(B)=0,05.

### Genetikus algoritmus:

A genetikus algoritmust a "genetikus.py" fileban valósítottam meg.<br/>
Az algoritmus addig fut amíg lesz 10 olyan egyed mely dobástávolsága a céltávolság 0,1 cm es környezetén belül van.
Az algoritmus az Intelligens rendszerek (lásd feljebb) 10. fejezetében leírtakat követi. <br/>
Mutációt, keresztezést és visszahelyettesítést alkalmazok 1 populáción. A kiválasztás minden esetben rulett kerék módszerrel töténik.

A paraméterek megfelelő beállítása után az algoritmusnak átlagosan 195 dobásra van szüksége, hogy találjon 10 pontos egyedet, azaz 10 olyan szögsebeség-görbét melynél dobástávolság a céltávolság 0,1 cm es környezetén belül van. Azonban a szükséges dobások szórása jelentős 114, azaz az átlag több mint fele, ami miatt gyakori a 300 fölötti érték is.

### Bakteriális algoritmus:

A bakteriális algoritmust a "bakteriális.py" fileban valósítottam meg.
Az algoritmus , a genetikus algoritmushoz hasonlóan, addig fut amíg lesz 10 pontos egyed, és az Intelligens rendszerek 10. fejezetében leírtakat követi.

Bakteriális mutációt és génátadást alkalmazok 1 populáción. Génátadásnál a polpulációt pontosság szerint 2 részre osztom, és a jobbik félből sorsolom a forrás míg a rosszabbikból a cél egyedet.

Két probléma merült fel ennél az algoritmusnál.  <br/>
Az első problémát a sikertelen dobások okozták. Ha egy szögsebességgörbe esetén a golyó nem fölfelé repül el (sikertelen), akkor a modell visszatérő értéke +1m, azaz olyan mintha +1 m-re repülne a golyó, ami nagyon messze van a céltól (-20 cm). Könnyen belátható, hogy ilyen bemenet esetén a fitness gradiense nullvektor, így az egyed sem mutáció, sem génátadás útján nem fejlődik. Ezt úgy oldottam meg, hogy az új egyedek mind képesek legyenek eldobni a golyót. Azaz egy új egyed esetén addig próbálgatok véletlenszerű szögsebbeség-görbéket míg az egyiknek sikerül eldobnia a golyót. Ehhez a lépéshez szükséges dobások számát neurális hálóval csökkentettem, melyről lejjebb írok.<br/>
A második probblémát a fitness függvény egy lokális minimuma okozza. Ha egy egyed épp az előtt dobja el a golyót, hogy a dobókar az x-tengellyel  180°-ot zárjon be, és a dobás sebessége elenyésző, akkor az egyed beragad. Ennek oka, hogy egy a célhoz közelebbi dobáshoz korábban, és erősebben kéne eldobnia a golyót, azonban ha korábban dobja el elenyésző sebességgel akkor messzebb kerül a céltól, míg ha nagyobb sebességgel próbálja eldobni a golyót akkor a kar túlmehet a 180°-on mely esetben a dobás sikertelen lesz. Ezeket az egyedeket nehezebb elkerülni, a problémát úgy oldottam meg, hogy minden generáció esetén a legpontatlanabb n egyedet lecserélem.

A bakteriális algoritmusnak a genetikusnál lényegesen több, átlagosan 790 dobásra van szüksége, hogy találjon 10 pontos egyedet, azonban megvannak az előnyei. Míg a genetikus algoritmus által adott 10 megoldás egymáshoz nagyon hasonló, addig a bakteriális algoritmus egymástól jobban eltérő, megoldásokat határoz meg. A megkívánt pontosság, vagy a dobástávolság növelésével a bakteriális algoritmus hátránya jelentősen csökken. Az algoritmus szórása is kisebb 166 azaz az átlag nagyjából 20%-a, tehát a futásidő jobban becsülhtő.

### Neurális háló alkalmazása:

A neurális hálót a "halo.py" fileban valósítottam meg. A háló többrétegű perceptron, bemeneti rétege 8, kimeneti rétege 1,  három rejtett rétege 20-20-10 neuronból áll, az aktivációs függvény minden esetben szigmoid. A súlymátrixokat (W1, W2..) és torzítási vektorokat (B1, B2...) .csv filokból olvasom be.

A véletlen szerű dobások 17%-a sikeres, így a olyan új egyedek generálásához mely biztosan sikeresek átlagosan 5,88 dobás szükséges. Betanítottam egy neurális hálót, ami 96%-as biztonsággal el tudja dönteni hogy egy szöggyorsulás-görbe sikeres-e. Ha a neurális hálóval előtesztelem akkor biztosan sikeres új egyed generálásához átlagosan 1,20 dobás szükséges. (1/(17%*96% /(17%*96%+83%*4%)))

### Neurális háló tanítása:

A tanításhoz szükséges adatokat a "data_maker.py" program készíti el és menti el a  "data.csv" fileban. A file első 8 oszlopa a szögsebesség-görbét írja le míg a 9.oszlopa a 1 ha a dobás sikeres, 0 ha sikertelen. Az adatokban nagyon erős túlsúlyban lenne a 0 kimenet, ami miatt a betanított háló a felé hajolna. Hogy ezt elkerüljem a filba felváltva sikeres és sikertelen dobások adatait írom be.

A neurális háló tanítását a "neuralis_halo.py" fileban valósítottam meg.
Az algoritmus, az Intelligens rendszerek 11. fejezetében leírtakat követi.<br/>
Backpropagation-höz szükségs gradienst numerikusan közelítem, e miatt a program futásideje jelentősen nagyobb mintha ezt analitikusan számítanám.<br/>
A tanításhoz 200 000 elemes adatsort alkalmaztam, melyet 1000-es csoportonként vizsgálok a számítás gyorsítása érdekében. Az adatsoron összesen 50 szer megy végig az algorizmus, a súlyokat és torzításokat a gradiens "lr" szeresével változtatja minden csoport vizsgálása után. Lr értékét futás közben csökkentem 5-től  0,05-ig. A súlymátrixokat (W1, W2..) és torzítási vektorokat (B1, B2...) .csv filokba mentem el.

### A projekt jelenlegi állapota:

Eredeti célkitűzések:<br/>
A robot nem készült el.<br/>
Egyszerű szimuláció elkészült.<br/>
A genetikus algoritmus elkészült.<br/>

Új célok:<br/>
Bakteriális algoritmus elkészült.<br/>
Neurális háló elkészült.<br/>

Feltételezve, hogy az elkészülő robot 10 másodpercenként tud 1-et dobni, és azonos bemenetre mindig azonos kimenetet ad, átlagogas 30 perces futásidővel találna 10 pontos egyedet. 10 másodpercenkénti dobás felfételezhető, azonban a dobások pontos megismételhetősége már nem.

### A projekt Folytatása:

Robot megépítése.

Komplexitás csökkentése.<br/>
A mosteni probléma szándékosan túl komplex, hogy lássam ezt hogyan tudol evolúciós algoritmussal megoldani, azonban ha gyorsan tanuló robotot szeretnék érdemes minimumra csökkenteni a komplexitást. Jelenleg 8 illetve 10 paraméterből állő bemeneteket alkalmazok egy szögyorsulás görbe leírására. Az eldobott golyó leírható az eldobás pillanatában a golyó sebességével, és a dobókar szögével. Mivel az elrepülő golyó 2 paraméterel leírható, megfelelően megválasztott 2 bemeneti paraméter elegendő. Pl. szöggyorsulás és gyorsulás időtartama

A valóságot jobban közelítő szimuláció készítése physics engine alkalmazásával. És a neurális háló helyett ezt használni előteszteléshez. Vagy neural netwok könyvtárak használatával pontosabbá tenni a hálót.

A valós robot pontatlanságának szimulálása, és olyan algoritmus készítése, mely képes ezt kezelni.






