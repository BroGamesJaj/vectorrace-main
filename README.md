# VectorRace

A játék célja a virtuális autó legmesszebbre juttatása (legtöbb mérési pont megfelelő sorrendben történő keresztezése) adott lépésszám alatt.  
A játékosnak ehhez egy robot vezetőt kell készíteni, ami az autóról és a pályáról szerzett információ alapján módosítja az aktuális sebességvektort.    
A sebességvektor módosítása sorok és oszlopok mentén is -1..+1 közé eső egész szám lehet [-1, 0, +1].  
Az érzékelők olvasási lehetőségeinek száma lépésciklusonként korlátozott.
  
## Indítás

### Előfeltételek
- Python 3.8 (minimum)
- csomagkezelő (pl. PIP)
- PIL (pillow)
- numpy
- matplotlib
- PyYAML
- (datetime, os, sys)

### Működtetés
#### Verseny szimuláció
A verseny szimulációját a ```main.py``` file végzi, melynek parancssori paraméterei:  
1. TracksFolder/TF: Pálya leíró YAML fájlokat tartalmazó mappa
2. TrackName/TN: A pályaleíró YAML fájl neve, kiterjesztéssel  (opcionális)
3. DriversFolder/DF: Vezetők (```DriverBase``` leszármazottak) implementációit tartalmazó mappa
4. LogsFolder/LF: Futtatási (.log) és mozgáspálya (.coords) naplók célmappája
5. LogType/LT: Készítendő napló típusok: ```None```/```Events```/```Coords```/```Both``` 
6. VisualizationType/VT: Eredmény vizualizáció típusa: ```None```/```Animated```/```Still```  
  
Amennyiben a pálya leírókat tartalmazó mappában több pálya leíró is található, ki kell választani a használandót. Ez történhet a ```TrackName``` paraméter megadásával, vagy futtatás közbeni választással.  
  
Verseny indítási példa:
```python main.py TF:Tracks TN:Track_1.yml DF:Drivers LF:Logs LT:None VT:Still```  

#### Verseny utólagos megtekintés
Verseny szimulációk eredményei önállóan is megjeleníthetők a ```visualization.py``` fájl segítségével, melynek parancssori paraméterei:
1. TracksFolder/TF: Pálya leíró YAML fájlokat tartalmazó mappa  
2. LogsFolder/LF: Mozgáspálya (Coords) naplókat tartalmazó mappa
3. LogName/LN: A betöltendő koordináta naplófájl neve, kiterjesztéssel (opcionális)
3. VisualizationType/VT: Eredmény vizualizáció típusa: ```Animated```/```Still```/```Continuous```/```Repeat:X```  
Ahol a *Continous* folyamatos, a *Repeat* pedig X-szer ismételt animáció lejátszást jelent
   
Amennyiben a naplókat tartalmazó mappában több napló is található, ki kell választani a használandót.  Ez történhet a LogName paraméter megadásával, vagy futtatás közbeni választással.  
  
Vizualizáció indítási példa: ```python visualization.py TF:Tracks LF:Logs LN:track01_20231214_075231.coords VT:Animated```  

### Pálya leírás
A leíró YAML fájl szerkezete:
```yaml
image_file: Tracks\track_1.png
name: Square
down_sample: 5
start:
  from: { X: 270, Y: 450 }
  to: { X: 270, Y: 499 }
  direction: { X: 1, Y: 0 }
splits:
  - split 1:
      from: { X: 540, Y: 450 }
      to: { X: 540, Y: 499 }
  - split 2:
      from: { X: 540, Y: 165 }
      to: { X: 540, Y: 214 }
  - split 3:
      from: { X: 210, Y: 165 }
      to: { X: 210, Y: 214 }
  - split 4:
      from: { X: 150, Y: 340 }
      to: { X: 199, Y: 340 }
```

A pályaleíróban megadott **RGB** (3x8 bit) képen **fehér háttér előtt fekete út** található.  
Az utat keresztbe átszelő vonalak:
- start (zöld): startvonal szakasz végpontokkal megadva és a kötelező haladási irány
- splits (kék): az érintendő mérési pontok, az érintés sorrendjében 
  
### Vezetők (Drivers)
A tesztelendő vezető példányokat a ```main.py``` script ```DriversFolder:``` indítási paraméterében meghatározott mappába kell másolni.  
**Egy versenyben több autó (vezető) is részt vehet, azoknak egymásra semmilyen hatása nincs!**

A vezetőnek az autó sebességvektorát módosító döntése (```_think```) és az autó sebességvektorának módosítása (```update```) azért vannak szétválasztva, mert a sebesség módosítást a döntés külön szálban futtatása és esetleges megszakítása (timeout) esetén is végre kell hajtani. 
  
### A verseny vége
Egy verseny addig tart, míg az előírt számú autó mozgató iteráció le nem fut, vagy míg az összes autó inaktív (nem-aktív) státuszba nem kerül.
Ez akkor történik:
- amennyiben ez lehetséges: az autó falnak ütközik (lelép az útról)
- amennyiben az út elhagyása engedélyezett: az autó lelép a térképről
- megadott számú egymást követő mozgató lépésen keresztül 0 a sebességvektorának hossza
- a vezető megadott számú (összesen, nem feltétlenül egymást követő) esetben kezeletlen kivételt vált ki

A verseny két módban futtatható:
- engedélyezett a pálya elhagyása, ekkor az autó üzemképes és irányítható marad a pályán kívül is, azonban a sebessége maximalizálásra kerül. (a térkép elhagyása azonnali kizárást eredményez)
- nem engedélyezett a pálya elhagyása, ekkor a falnak ütközéskor az autó sebessége 0-ra csökken és néhány iterációra mozgásképtelen lesz (újraindítás)
  
A bejárt útvonalakat az autók tárolják, ezeket a ```Visualizer``` osztály képes a pályarajzon megjeleníteni.  
  
A verseny végeredménye az autók (vezetők) teljesítmény alapú sorbarendezéséve alakul ki.  
A teljesítményt meghatározó rendezési szempontok:
1. a megtett út (keresztezett részidő mérőpontok száma)
2. a megtételhez szükséges idő
3. a legnagyobb sebesség

A legnagyobb sebesség és első elérési ideje szerinti rendezettségi lista alapján kiegészítő pontok szerezhetők. 

## A versenyfeladat
A játékos feladata tehát, hogy olyan program komponenst készítsen, amely az elérhető autó és pálya érzékelők által szolgáltatott adatok alapján meghatározza az autó sebességvektorának sor és oszlop irányú relatív módosítását (módosító vektor). Szem előtt tartva, hogy a gyorsulás/lassulás, kanyarodás műveletek az autó orientációja szerint más irányú módosító vektorokat, más (sor, oszlop) módosításokat jelentenek.  

Az elkészítendő robot vezetőt a ```DriverBase``` osztályból örököltetett saját osztály készítésével kell előállítani, melyben a szükséges számításokat a  
```def _think(self, car_sensor: SensorBase, track_sensor: SensorBase):```  
örökölt metódus felülírásával (override) kell elvégezni. Ezt a metódust a keretrendszer a megfelelő helyen és időben automatikusan hívja.  
  
A sebességvektor módosítását (a módosító vektor sor, oszlop koordinátáit) ```DriverBase``` osztályból örökölt ```self.relative_speed_change``` publikus adattagban kell elhelyezni.  
**A számítások eredménye: a sebességvektor változása, a VEKTOR végpontjának relatív elmozdulása, a módosító vektor végpontjának (sor, oszlop) koordinátái.**  
Az új sebességvektor a korábbi sebességvektor és az módosító sebességvektor összege lesz.
  
A sebességmódosítás számítására minden lépésciklusban korlátozott idő áll rendelkezésre, gondolkodási időtúllépés esetén az autó kiesik a versenyből.

A módosító vektor alapértelemezett értéke ```self.relative_speed_change = (0, 0)```, vagyis vezetői döntési hiba esetén a sebességvektor változatlan marad (az autó sebessége és iránya nem változik).

### A munka során felhasználható eszközök
#### Adattárolás
A vezető ősosztály (```DriverBase```) ```storage``` publikus adattagja (```self.storage```) egy olyan tároló, amelyben nevesített értékek tárolhatók a módosítási lépések között.
A tároló használata:
- olvasás: ```self.storage.get(<az érték neve>, <alapértelmezett érték (ha a név még nincs a tárolóban)>)```
- írás: ```self.storage.set(<az érték beve>, <tárolandó új érték>)```
  
A tároló használatára példa:
- olvasás: ```self.storage.get("first_run", True)```
- írás: ```self.storage.set("first_run", False)```

Az objektumorinetált programozásban jártas programozók használhatnak:
- adattárolásra a saját vezető osztály példány adattagjait 
- a megoldás struktúrálására példány metódusokat és/vagy egyéb saját osztályok példányait
  
**Globális változók és metódusok készítése TILOS!!!**
  
#### Érzékelők
Az feladat megoldásához két érzékelő típus használható, a konkrét típusokat az aktuális feladat tartalmazza:
- ```CarSensor``` - az autó állapotát lekérdezőeszköz 
  - get_iteration() -> int - megadja az aktuális autó mozgató lépés számát 
  - get_position() -> (sor, oszlop) - megadja az autó aktuális abszolút helyzetét
  - get_speed() -> (sor, oszlop) - megadja az autó aktuális sebességét
  - get_speed_vector_length() -> float - megadja az aktuális sebességet (a sebességvektor hosszát)
  - is_restarting() -> bool - megadja, hogy az autó megállás/újraindítás alatt van-e (pályaelhagyási kísérlet miatti büntetés)
- Pálya érzékelő
  - ```SensorBase``` ősosztály - az innen örökölt metódusok használata nem korlátozott
    - get_track_size() -> (sor, oszlop) - visszaadja a térkép méretét pixelben 
    - get_start_direction() -> (sor, oszlop)  - visszaadja a kötelező elindulási irányt, vagyis az elinduláshoz szükséges sebesség módosítót
    - can_scan() -> bool - visszaadja, hogy az értékelés képes-e további érzékelésre (korlátozott számú érzékelés esetén)
  - ```PointSensor``` - Csak pályapontokat vizsgál, hogy a vizsgált pont a pályán van-e
    - is_point_on_track(point) -> PointOnTrackResult - megadja, hogy a pont a pályán van-e (KORLÁTOZOTT)
    - is_point_on_map(point) -> PointOnMapResult - megmondja, hogy a pont a térképen van-e (KORLÁTOZOTT)
  - ```PathSensorBase``` - ```PointSensor``` osztályból származtatott absztrakt osztály, a pályapontok mellett pályautakat is vizsgál
    - a ```PointSensor``` funkcióit örökli
    - is_path_homogeneous(start_point, end_point) -> PathCheckResult - megvizsgálja, hogy a kezdő és végpontok a pályán vannak-e illetve hogy a kettő közötti út meddig azonos a kezdőponttal  (KORLÁTOZOTT)
    - ```LineOfSightSensor``` - a vizsgált út az autótól induló egyenes.
    - ```LineSensor``` - a vizsgált út a bármely két pont közötti egyenes.

*A felhasználható érzékelők pontos típusát a konkrét versenyfeladat tartalmazza!*

#### Érzékelési eredmények
Az egyes érzékelő metódusok az alábbi osztályokba tartozó eredmények egy-egy példányát adhatják vissza.  

Pályapont vizsgálat esetén az eredmény típus:
- (```PointOnTrackResult```) publikus komponensei:
  + coordinate: tuple - a vizsgált koordináta (sor, oszlop)
  + is_on_track: bool - a koordináta a pályán van?
- (```PointOnMapResult```) publikus komponensei:
  + coordinate: tuple - a vizsgált koordináta (sor, oszlop)
  + is_on_map: bool - a koordináta a térképen van?

Pályaút vizsgálat esetén az eredmény típus (```PathCheckResult```) publikus komponensei:
+ start_coordinate: tuple - az út kezdőpontjának koordinátái (sor, oszlop)
+ end_coordinate: tuple - az út végpontjának koordinátái (sor, oszlop)
+ path: list of tuples - az út pontjainak koordinátái (sor, oszlop) a kezdőponttól a végpontig  
az utat a ```PathSensorBase``` osztály ```_get_path(self, r0, c0, r1, c1)``` metódusa állítja elő.
+ is_start_on_track: bool - a kezdőpont a pályán van-e?
+ is_end_on_track: bool - a végpont a pályán van-e?
+ last_on_track: tuple - az út utolsó olyan pontjának koordinátája, amelynek típusa megegyezik a kezdőpontéval

### Vezető példa
  
A Drivers/Examples mappában két példa is található a vezető implementációra.  
Ugyan egyik sem oldja meg a feladatot hatékonyan, a programozási eszközök felhasználásának módja jól látható bennük, így a saját fejelesztések jó alapjául szolgálhatnak.

```
import math

from Model.DriverBase import DriverBase
from Model.Sensors.CarSensor import CarSensor
from Model.Sensors.LineSensor import LineSensor


class TestDriver(DriverBase):

    def _think(self, car_sensor: CarSensor, track_sensor: LineSensor):
        # default inputs
        pos_y, pos_x = car_sensor.get_position()
        speed_y, speed_x = car_sensor.get_speed()
        speed_vector_length = car_sensor.get_speed_vector_length()
        iteration = car_sensor.get_iteration()

        # custom values from the storage to local variables
        is_first_run = self.storage.get("first_run", True)
        total_length = self.storage.get("total_length", 0)

        # use local variables
        total_length += math.sqrt(speed_y ** 2 + speed_x ** 2)
        if is_first_run:
            print("Track size: {0}".format(track_sensor.get_track_size()))

        # update custom values in the storage
        self.storage.set("first_run", False)
        self.storage.set("total_length", total_length)

        # set output, default in each call: (0, 0)
        # for now, as a test, continuous acceleration in start direction
        self.relative_speed_change = track_sensor.get_start_direction()

        next_position = (
            pos_y + speed_y + self.relative_speed_change[0],
            pos_x + speed_x + self.relative_speed_change[1]
        )

        # test sensor read limit (sensor returns -1 if read limit reached)
        while track_sensor.can_scan():
            # sensor returns: PointOnTrackResult object
            # PointOnTrackResult.is_on_track: bool - is coordinate on track
            sensor_value = track_sensor.is_point_on_track(next_position)
            print(
                iteration,
                pos_y, pos_x,
                total_length,
                speed_y, speed_x, speed_vector_length,
                sensor_value
            )

            if sensor_value.is_on_track:
                # move forward
                pass
            else:
                # turn
                pass

```
