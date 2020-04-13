import math

from bs4 import BeautifulSoup as BSoup
from tabula import convert_into

import csv
import requests
from datetime import datetime, date

# ERROR CODES
#
# E01-1 - no mean price data for surrounding cities (from)
# E01-2 - no mean price data for surrounding cities (to)
# E02 - could not find data specified cities

session = requests.session()

codes_url = "https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm"
codes_r = session.get(codes_url)
codes_soup = BSoup(codes_r.content, 'html5lib')

raw_data = []
overall_mean_variances = [0.046935368, 0.349271934, 0.015730188, 0.104964831, 0.219331373, 0.066125376, -0.13580952, 0.040763284, 0.247060446, 0.298777508, 0.165885977, -0.293639191]
overall_stdev_variances = [0.48164962, 0.626318344, 0.511550704, 0.454368646, 0.393383854, 0.42043275, 0.244046188, 0.580217736, 0.654213661, 0.712783114, 0.459309131, 0.263116568]

opinions = ['Wait, if possible', 'Strongly advised to wait', 'Looks good']

opinions_options = {
    'Thunderstorm': opinions[0],
    'Tornado': opinions[1],
}

months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }

city_codes = {'Aarhus': ['AAR'], 'Abadan': ['ABD'], 'Abeche': ['AEH'], 'Aberdeen': ['ABZ', 'ABR'], 'Abidjan': ['ABJ'], 'Abilene': ['ABI'], 'Abu Dhabi': ['AUH'], 'Abuja': ['ABV'], 'Abu Rudeis': ['AUE'], 'Abu Simbel': ['ABS'], 'Acapulco': ['ACA'], 'Accra': ['ACC'], 'Adana': ['ADA'], 'Addis Ababa': ['ADD'], 'Adelaide': ['ADL'], 'Aden': ['ADE'], 'Adiyaman': ['ADF'], 'Adler/Sochi': ['AER'], 'Agades': ['AJY'], 'Agadir': ['AGA'], 'Agana': ['SUM'], 'Aggeneys': ['AGZ'], 'Aguadilla': ['BQN'], 'Aguascaliente': ['AGU'], 'Ahmedabad': ['AMD'], 'Aiyura': ['AYU'], 'Ajaccio': ['AJA'], 'Akita': ['AXT'], 'Akron': ['CAK'], 'Akrotiri': ['AKT'], 'Al Ain': ['AAN'], 'Al Arish': ['AAC'], 'Albany': ['ALH', 'ABY', 'ALB'], 'Albi': ['LBI'], 'Alborg': ['AAL'], 'Albuquerque': ['ABQ'], 'Albury': ['ABX'], 'Alderney': ['ACI'], 'Aleppo': ['ALP'], 'Alesund': ['AES'], 'Alexander Bay': ['ALJ'], 'Alexandria': ['HBH', 'ALY', 'ESF'], 'Alfujairah': ['FJR'], 'Alghero Sassari': ['AHO'], 'Algiers, Houari Boumediene Airport': ['ALG'], 'Al Hoceima': ['AHU'], 'Alicante': ['ALC'], 'Alice Springs': ['ASP'], 'Alldays': ['ADY'], 'Allentown': ['ABE'], 'Almaty': ['ALA'], 'Almeria': ['LEI'], 'Alta': ['ALF'], 'Altay': ['AAT'], 'Altenrhein': ['ACH'], 'Altoona': ['AOO'], 'Altus': ['AXS'], 'Amami': ['ASJ'], 'Amarillo': ['AMA'], 'Amazon Bay': ['AZB'], 'Amman': ['AMM', 'ADJ'], 'Amritsar': ['ATQ'], 'Amsterdam': ['AMS'], 'Anand': ['QNB'], 'Anchorage': ['ANC'], 'Ancona': ['AOI'], 'Andorra La Vella': ['ALV'], 'Anguilla': ['AXA'], 'Anjouan': ['AJN'], 'Ankara': ['ANK', 'ESB'], 'Annaba': ['AAE'], 'Ann Arbor': ['ARB'], 'Annecy': ['NCY'], 'Anniston': ['ANB'], 'Antalya': ['AYT'], 'Antananarivo': ['TNR'], 'Antigua, V.C. Bird International': ['ANU'], 'Antwerp': ['ANR'], 'Aomori': ['AOJ'], 'Apia': ['APW'], 'Appelton/Neenah/Menasha': ['ATW'], 'Aqaba': ['AQJ'], 'Aracaju': ['AJU'], 'Arkhangelsk': ['ARH'], 'Arusha': ['ARK'], 'Araxos': ['GPA'], 'Arlit': ['RLT'], 'Arrecife/Lanzarote': ['ACE'], 'Aruba': ['AUA'], 'Asheville': ['AVL'], 'Ashgabat': ['ASB'], 'Asmara': ['ASM'], 'Aspen,': ['ASE'], 'Assiut': ['ATZ'], 'Astana': ['TSE'], 'Asuncion': ['ASU'], 'Aswan': ['ASW'], 'Athens': ['ATH', 'AHN', 'ATO'], 'Athens, Hellinikon Airport': ['HEW'], 'Atlanta': ['ATL'], 'Atlantic City': ['ACY'], 'Attawapiskat, NT': ['YAT'], 'Auckland': ['AKL'], 'Augsburg': ['AGB'], 'Augusta': ['AGS', 'AUG'], 'Aurillac': ['AUR'], 'Austin': ['AUS'], 'Ayawasi': ['AYW'], 'Ayers Rock': ['AYQ'], 'Ayr': ['AYR'], 'Badajoz': ['BJZ'], 'Bagdad': ['BGW'], 'Bagdogra': ['IXB'], 'Bahamas': ['NAS'], 'Bahawalpur': ['BHV'], 'Bahrain': ['BAH'], 'Bakersfield': ['BFL'], 'Baku': ['BAK'], 'Ballina': ['BNK'], 'Baltimore': ['BWI'], 'Bamaga': ['ABM'], 'Bamako': ['BKO'], 'Bambari': ['BBY'], 'Bandar Seri Begawan': ['BWN'], 'Bandung': ['BDO'], 'Bangalore': ['BLR'], 'Bangassou': ['BGU'], 'Bangkok, Don Muang': ['DMK'], 'Bangkok, Suvarnabhumi International': ['BKK'], 'Bangor': ['BGR'], 'Bangui': ['BGF'], 'Banjul': ['BJL'], 'Bannu': ['BNP'], 'Barcelona': ['BCN', 'BLA'], 'Bardufoss': ['BDU'], 'Bari': ['BRI'], 'Barisal': ['BZL'], 'Baroda': ['BDQ'], 'Barra': ['BRR'], 'Barranquilla': ['BAQ'], 'Basel': ['BSL'], 'Basel/Mulhouse': ['EAP'], 'Basra, Basrah': ['BSR'], 'Basse': ['PTP'], 'Basseterre': ['SKB'], 'Bastia': ['BIA'], 'Baton Rouge': ['BTR'], 'Bayreuth': ['BYU'], 'Beaumont/Pt. Arthur': ['BPT'], 'Beckley': ['BKW'], 'Beef Island': ['EIS'], 'Beijing': ['PEK', 'NAY'], 'Beira': ['BEW'], 'Beirut': ['BEY'], 'Belem': ['BEL'], 'Belfast': ['BHD', 'BFS'], 'Belgaum': ['IXG'], 'Belgrad': ['BEG'], 'Belize City': ['BZE'], 'Bellingham': ['BLI'], 'Belo Horizonte': ['CNF'], 'Bemidji': ['BJI'], 'Benbecula': ['BEB'], 'Benghazi': ['BEN'], 'Benguela': ['BUG'], 'Benton Harbour': ['BEH'], 'Berberati': ['BBT'], 'Bergamo/Milan': ['BGY'], 'Bergen': ['BGO'], 'Bergerac': ['EGC'], 'Berlin': ['BER'], 'Berlin, Schoenefeld': ['SXF'], 'Berlin, Tegel': ['TXL'], 'Berlin, Tempelhof': ['THF'], 'Bermuda': ['BDA'], 'Berne, Bern': ['BRN'], 'Berne, Railway Service': ['ZDJ'], 'Bethel': ['BET'], 'Bhopal': ['BHO'], 'Bhubaneswar': ['BBI'], 'Biarritz': ['BIQ'], 'Bilbao': ['BIO'], 'Billings': ['BIL'], 'Billund': ['BLL'], 'Bintulu': ['BTU'], 'Biraro': ['IRO'], 'Birmingham': ['BHX', 'BHM'], 'Bishkek': ['FRU'], 'Bismarck': ['BIS'], 'Bissau': ['BXO'], 'Blackpool': ['BLK'], 'Blackwater': ['BLT'], 'Blantyre': ['BLZ'], 'Blenheim': ['BHE'], 'Bloemfontein': ['BFN'], 'Bloomington': ['BMI', 'BMG'], 'Bluefield': ['BLF'], 'Boa Vista': ['BVB'], 'Bobo/Dioulasso': ['BOY'], 'Bodo': ['BOO'], 'Bodrum': ['BJV'], 'Bogota': ['BOG'], 'Boise': ['BOI'], 'Bologna': ['BLQ'], 'Bombay': ['BOM'], 'Bonaire': ['BON'], 'Bonaventure, PQ': ['YVB'], 'Bora Bora': ['BOB'], 'Bordeaux': ['BOD'], 'Borrego Springs': ['BXS'], 'Boston': ['BOS'], 'Bouake': ['BYK'], 'Bourgas/Burgas': ['BOJ'], 'Bournemouth': ['BOH'], 'Bowen': ['ZBO'], 'Bozeman': ['BZN'], 'Bradford/Warren': ['BFD'], 'Brainerd': ['BRD'], 'Brampton Island': ['BMP'], 'Brasilia': ['BSB'], 'Bratislava': ['BTS'], 'Brazzaville': ['BZV'], 'Bremen': ['BRE'], 'Brescia, Montichiari': ['VBS'], 'Brest': ['BES'], 'Bria': ['BIV'], 'Bridgeport': ['BDR'], 'Bridgetown': ['BGI'], 'Brindisi': ['BDS'], 'Brisbane': ['BNE'], 'Bristol': ['BRS'], 'Broennoeysund': ['BNN'], 'Broken Hill': ['BHQ'], 'Brookings': ['BKX'], 'Broome': ['BME'], 'Brunswick': ['BQK'], 'Brussels': ['BRU'], 'Bucaramanga': ['BGA'], 'Bucharest': ['BUH', 'OTP'], 'Budapest': ['BUD'], 'Buenos Aires': ['BUE'], 'Buenos Aires, Ezeiza International Airport': ['EZE'], 'Buenos Aires, Jorge Newbery': ['AEP'], 'Buffalo Range': ['BFO'], 'Buffalo/Niagara Falls': ['BUF'], 'Bujumbura': ['BJM'], 'Bulawayo': ['BUQ'], 'Bullhead City': ['BHC'], 'Bundaberg': ['BDB'], 'Burbank': ['BUR'], 'Burlington IA': ['BRL'], 'Burlington': ['BTV'], 'Burnie': ['BWT'], 'Butte': ['BTM'], 'Cabinda': ['CAB'], 'Cagliari': ['CAG'], 'Cairns': ['CNS'], 'Cairo': ['CAI'], 'Calama': ['CJC'], 'Calcutta': ['CCU'], 'Calgary': ['YYC'], 'Cali': ['CLO'], 'Calicut': ['CCJ'], 'Calvi': ['CLY'], 'Cambridge Bay': ['YCB'], 'Cambrigde': ['CBG'], 'Campbeltown': ['CAL'], 'Campo Grande': ['CGR'], 'Canberra': ['CBR'], 'Cancun': ['CUN'], 'Cannes – Mandelieu Airport': ['CEQ'], 'Canouan': ['CIW'], 'Cape Town': ['CPT'], 'Caracas': ['CCS'], 'Cardiff': ['CWL'], 'Carlsbad': ['CLD'], 'Carnarvon': ['CVQ'], 'Carnot': ['CRF'], 'Carson City': ['CSN'], 'Casablanca': ['CAS'], 'Casablanca, Mohamed V': ['CMN'], 'Casa de Campo': ['LRM'], 'Casino': ['CSI'], 'Casper': ['CPR'], 'Castaway': ['CST'], 'Cartagena': ['CTG'], 'Castries': ['SLU'], 'Catania': ['CTA'], 'Cayenne': ['CAY'], 'Cottbus': ['CBU'], 'Cebu City': ['CEB'], 'Cedar City': ['CDC'], 'Cedar Rapids IA': ['CID'], 'Ceduna': ['CED'], 'Cessnock': ['CES'], 'Chabarovsk': ['KHV'], 'Chambery': ['CMF'], 'Champaign': ['CMI'], 'Chandigarh': ['IXC'], 'Changchun': ['CGQ'], 'Chania': ['CHQ'], 'Chaoyang, Beijing': ['CHG'], 'Charleston': ['CHS', 'CRW'], 'Charlotte': ['CLT'], 'Charlottesville': ['CHO'], 'Charters Towers': ['CXT'], 'Chattanooga': ['CHA'], 'Chengdu': ['CTU'], 'Chennai': ['MAA'], 'Cheyenne': ['CYS'], 'Chiang Mai': ['CNX'], 'Chiba City': ['QCB'], 'Chicago': ['MDW', 'ORD', 'CHI'], 'Chichen Itza': ['CZA'], 'Chico': ['CIC'], 'Chihuahua': ['CUU'], 'Chios': ['JKH'], 'Chipata': ['CIP'], 'Chisinau': ['KIV'], 'Chita': ['HTA'], 'Sapporo': ['CTS', 'SPK', 'OKD', 'CTS'], 'Chitral': ['CJL'], 'Chittagong': ['CGP'], 'Chongqing': ['CKG'], 'Christchurch': ['CHC'], 'Chub Cay': ['CCZ'], 'Churchill': ['YYQ'], 'Cienfuegos': ['CFG'], 'Cincinnati': ['CVG'], 'Ciudad Del Carmen': ['CME'], 'Ciudad Guayana': ['CGU'], 'Ciudad Juarez': ['CJS'], 'Ciudad Obregon': ['CEN'], 'Ciudad Victoria': ['CVM'], 'Clarksburg': ['CKB'], 'Clermont': ['CMQ'], 'Clermont Ferrand': ['CFE'], 'Cleveland': ['BKL', 'CLE'], 'Cochabamba': ['CBB'], 'Cochin': ['COK'], 'Cody/Powell/Yellowstone': ['COD'], 'Coffmann Cove': ['KCC'], 'Coffs Harbour': ['CFS'], 'Coimbatore': ['CJB'], 'Colima': ['CLQ'], 'College Station/Bryan': ['CLL'], 'Collinsville': ['KCE'], 'Cologne': ['CGN'], 'Colombo': ['CMB'], 'Colorado Springs': ['COS'], 'Columbia': ['CAE'], 'Columbus': ['CSG', 'CMH'], 'Conakry': ['CKY'], 'Concord': ['CCR', 'CON'], 'Constantine': ['CZL'], 'Constanta': ['CND'], 'Coober Pedy': ['CPD'], 'Cooktown': ['CTN'], 'Cooma': ['OOM'], 'Copenhagen': ['CPH'], 'Cordoba': ['COR', 'ODB'], 'Cordova': ['CDV'], 'Corfu': ['CFU'], 'Cork': ['ORK'], 'Corpus Christi': ['CRP'], 'Cotonou': ['COO'], 'Coventry': ['CVT'], 'Cozmel': ['CZM'], 'Craig': ['CGA'], 'Crescent City': ['CEC'], 'Cuiaba': ['CGB'], 'Culiacan': ['CUL'], 'Curacao': ['CUR'], 'Curitiba': ['CWB'], 'Cuyo': ['CYU'], 'Dakar': ['DKR'], 'Dalaman': ['DLM'], 'Dalby': ['DBY'], 'Dalian': ['DLC'], 'Dallas': ['DAL'], 'Dallas/Ft. Worth': ['DFW'], 'Daloa': ['DJO'], 'Damascus, International': ['DAM'], 'Dammam, King Fahad International': ['DMM'], 'Danville': ['DAN'], 'Dar es Salam': ['DAR'], 'Darwin': ['DRW'], 'Daydream Island': ['DDI'], 'Dayton': ['DAY'], 'Daytona Beach': ['DAB'], 'Decatur': ['DEC'], 'Deer Lake/Corner Brook': ['YDF'], 'Delhi': ['DEL'], 'Den Haag': ['HAG'], 'Denizli': ['DNZ'], 'Denpasar/Bali': ['DPS'], 'Denver': ['DEN'], 'Dera Ismail Khan': ['DSK'], 'Derby': ['DRB'], 'Derry': ['LDY'], 'Des Moines': ['DSM'], 'Detroit': ['DET', 'DTW', 'DTT'], 'Devils Lake': ['DVL'], 'Devonport': ['DPO'], 'Dhahran': ['DHA'], 'Dhaka': ['DAC'], 'Dili': ['DIL'], 'Dillingham': ['DLG'], 'Dinard': ['DNR'], 'Disneyland Paris': ['DLP'], 'Djerba': ['DJE'], 'Djibouti': ['JIB'], 'Dodoma': ['DOD'], 'Doha': ['DOH'], 'Doncaster/Sheffield, Robin Hood International Airport': ['DSA'], 'Donegal': ['CFN'], 'Dortmund': ['DTM'], 'Dothan': ['DHN'], 'Douala': ['DLA'], 'Dresden': ['DRS'], 'Dubai': ['DXB'], 'Dubbo': ['DBO'], 'Dublin': ['DUB'], 'Dubois': ['DUJ'], 'Dubrovnik': ['DBV'], 'Dubuque IA': ['DBQ'], 'Duesseldorf': ['DUS'], 'Duluth': ['DLH'], 'Dundee': ['DND'], 'Dunedin': ['DUD'], 'Dunk Island': ['DKI'], 'Durango': ['DRO'], 'Durban': ['DUR'], 'Dushanbe': ['DYU'], 'Dutch Harbor': ['DUT'], 'Dysart': ['DYA'], 'Dzaoudzi': ['DZA'], 'East London': ['ELS'], 'Easter Island': ['IPC'], 'Eau Clarie': ['EAU'], 'Edinburgh': ['EDI'], 'Edmonton': ['YEA'], 'Edmonton, International': ['YEG'], 'Edmonton, Municipal': ['YXD'], 'Egilsstadir': ['EGS'], 'Eindhoven': ['EIN'], 'Samana': ['AZS'], 'Elba Island, Marina Di Campo': ['EBA'], 'Elat': ['ETH'], 'Elat, Ovula': ['VDA'], 'Elkhart': ['EKI'], 'Elko': ['EKO'], 'Ellisras': ['ELL'], 'El Minya': ['EMY'], 'Elmira': ['ELM'], 'El Paso': ['ELP'], 'Ely': ['ELY'], 'Emerald': ['EDR', 'EMD'], 'Enontekioe': ['ENF'], 'Entebbe': ['EBB'], 'Erfurt': ['ERF'], 'Erie': ['ERI'], 'Eriwan': ['EVN'], 'Erzincan': ['ERC'], 'Erzurum': ['ERZ'], 'Esbjerg': ['EBJ'], 'Escanaba': ['ESC'], 'Esperance': ['EPR'], 'Eugene': ['EUG'], 'Eureka': ['ACV'], 'Evansville': ['EVV'], 'Evenes': ['EVE'], 'Exeter': ['EXT'], 'Fairbanks': ['FAI'], 'Fair Isle': ['FIE'], 'Faisalabad': ['LYP'], 'Fargo': ['FAR'], 'Farmington': ['FMN'], 'Faro': ['FAO'], 'Faroer': ['FAE'], 'Fayetteville': ['FYV'], 'Fayetteville/Ft. Bragg': ['FAY'], 'Fes': ['FEZ'], 'Figari': ['FSC'], 'Flagstaff': ['FLG'], 'Flin Flon': ['YFO'], 'Flint': ['FNT'], 'Florence': ['FLR', 'FLO'], 'Florianopolis': ['FLN'], 'Floro': ['FRO'], 'Fort Albert': ['YFA'], 'Fortaleza': ['FOR'], 'Fort de France': ['FDF'], 'Fort Dodge IA': ['FOD'], 'Fort Huachuca/Sierra Vista': ['FHU'], 'Fort Lauderdale/Hollywood': ['FLL'], 'Fort McMurray': ['YMM'], 'Fort Myers, Metropolitan Area': ['FMY'], 'Fort Myers, Southwest Florida Reg': ['RSW'], 'Fort Riley': ['FRI'], 'Fort Smith': ['YSM', 'FSM'], 'Fort St. John': ['YXJ'], 'Fort Walton Beach': ['VPS'], 'Fort Wayne': ['FWA'], 'Fort Worth': ['DFW'], 'Foula': ['FOU'], 'Francistown': ['FRW'], 'Frankfurt/Main': ['FRA'], 'Frankfurt/Hahn': ['HHN'], 'Franklin/Oil City': ['FKL'], 'Fredericton': ['YFC'], 'Freeport': ['FPO'], 'Freetown': ['FNA'], 'Frejus': ['FRJ'], 'Fresno': ['FAT'], 'Friedrichshafen': ['FDH'], 'Fuerteventura': ['FUE'], 'Fujairah, International Airport': ['FJR'], 'Fukuoka': ['FUK'], 'Fukushima': ['FKS'], 'Funchal': ['FNC'], 'Futuna': ['FUT'], 'Gaborone': ['GBE'], 'Gadsden': ['GAD'], 'Gainesville': ['GNV'], 'Galway': ['GWY'], 'Gander': ['YQX'], 'Garoua': ['GOU'], 'Gaza City': ['GZA'], 'Gaziantep': ['GZT'], 'Gdansk': ['GDN'], 'Geelong': ['GEX'], 'Geneva': ['GVA'], 'Genoa': ['GOA'], 'George': ['GRJ'], 'Georgetown': ['GEO'], 'Geraldton': ['GET'], 'Gerona': ['GRO'], 'Ghent': ['GNE'], 'Gibraltar': ['GIB'], 'Gilette': ['GCC'], 'Gilgit': ['GIL'], 'Gillam': ['YGX'], 'Gladstone': ['GLT'], 'Glasgow, Prestwick': ['PIK'], 'Glasgow': ['GLA', 'GGW'], 'Glendive': ['GDV'], 'Goa': ['GOI'], 'Goiania, Santa Genoveva Airport': ['GYN'], 'Gold Coast': ['OOL'], 'Goondiwindi': ['GOO'], 'Goose Bay': ['YYR'], 'Gorna': ['GOZ'], 'Gothenburg': ['GOT'], 'Gove': ['GOV'], 'Govenors Harbour': ['GHB'], 'Granada': ['GRX'], 'Grand Bahama International': ['FPO'], 'Grand Canyon': ['GCN'], 'Grand Cayman': ['GCM'], 'Grand Forks': ['GFK'], 'Grand Junction': ['GJT'], 'Grand Rapids': ['GRR', 'GPZ'], 'Graz': ['GRZ'], 'Great Falls': ['GTF'], 'Great Keppel Island': ['GKL'], 'Green Bay': ['GRB'], 'Greenbrier/Lewisburg': ['LWB'], 'Greensboro/Winston Salem': ['GSO'], 'Greenville': ['GLH', 'PGV'], 'Greenville/Spartanburg': ['GSP'], 'Grenada': ['GND'], 'Grenoble': ['GNB'], 'Griffith': ['GFF'], 'Groningen': ['GRQ'], 'Groote Eylandt': ['GTE'], 'Groton/New London': ['GON'], 'Guadalajara': ['GDL'], 'Guadalcanal': ['GSI'], 'Guam': ['GUM'], 'Guangzhou': ['CAN'], 'Sao Paulo': ['GRU', 'SAO', 'CGH', 'GRU', 'VCP'], 'Guatemala City': ['GUA'], 'Guayaquil': ['GYE'], 'Guernsey': ['GCI'], 'Guettin': ['GTI'], 'Gulfport/Biloxi': ['GPT'], 'Guilin': ['KWL'], 'Gulu': ['ULU'], 'Gunnison/Crested Butte': ['GUC'], 'Guwahati': ['GAU'], 'Gwadar': ['GWD'], 'Gweru': ['GWE'], 'Gympie': ['GYP'], 'Hachijo Jima': ['HAC'], 'Hagåtña': ['GUM'], 'Haifa': ['HFA'], 'Haines': ['HNS'], 'Hakodate': ['HKD'], 'Halifax International': ['YHZ'], 'Hall Beach': ['YUX'], 'Hamburg': ['HAM'], 'Hamilton': ['HLT', 'YHM', 'HLZ'], 'Hamilton Island': ['HTI'], 'Hammerfest': ['HFT'], 'Hancock': ['CMX'], 'Hangchow': ['HGH'], 'Hannover': ['HAJ'], 'Hanoi': ['HAN'], 'Harare': ['HRE'], 'Harbin': ['HRB'], 'Harlingen/South Padre Island': ['HRL'], 'Harrington Harbour, PQ': ['YHR'], 'Harrisburg': ['HAR', 'MDT'], 'Hartford': ['BDL'], 'Hatyai': ['HDY'], 'Haugesund': ['HAU'], 'Havana': ['HAV'], 'Havre': ['HVR'], 'Hayman Island': ['HIS'], 'Helena': ['HLN'], 'Helsingborg': ['JHE'], 'Helsinki': ['HEL'], 'Heraklion': ['HER'], 'Hermosillo': ['HMO'], 'Hervey Bay': ['HVB'], 'Hibbing': ['HIB'], 'Hickory': ['HKY'], 'Hilo': ['ITO'], 'Hilton Head Island': ['HHH'], 'Hinchinbrook Island': ['HNK'], 'Hiroshima International': ['HIJ'], 'Ho Chi Minh City': ['SGN'], 'Hobart': ['HBA'], 'Hof': ['HOQ'], 'Holguin': ['HOG'], 'Home Hill': ['HMH'], 'Homer': ['HOM'], 'Hong Kong': ['HKG', 'ZJK'], 'Honiara Henderson International': ['HIR'], 'Honolulu': ['HNL'], 'Hoonah': ['HNH'], 'Horta': ['HOR'], 'Houston': ['HOU'], 'Houston, TX': ['IAH'], 'Huahine': ['HUH'], 'Huatulco': ['HUX'], 'Hue': ['HUI'], 'Humberside': ['HUY'], 'Huntington': ['HTS'], 'Huntsville': ['HSV'], 'Hurghada International': ['HRG'], 'Huron': ['HON'], 'Hwange National Park': ['HWN'], 'Hyannis': ['HYA'], 'Hydaburg': ['HYG'], 'Hyderabad': ['HYD', 'HDD'], 'Ibiza': ['IBZ'], 'Idaho Falls': ['IDA'], 'Iguazu, Cataratas': ['IGR'], 'Ile des Pins': ['ILP'], 'Ile Ouen': ['IOU'], 'Iliamna': ['ILI'], 'Imperial': ['IPL'], 'Incercargill': ['IVC'], 'Incheon, Incheon International Airport': ['ICN'], 'Indianapolis': ['IND'], 'Ingham': ['IGH'], 'Innisfail': ['IFL'], 'Innsbruck': ['INN'], 'International Falls': ['INL'], 'Inuvik': ['YEV'], 'Invercargill': ['IVC'], 'Inverness': ['INV'], 'Inykern': ['IYK'], 'Iqaluit': ['YFB'], 'Iquitos': ['IQT'], 'Irkutsk': ['IKT'], 'Ishigaki': ['ISG'], 'Islamabad': ['ISB'], 'Islay': ['ILY'], 'Isle of Man': ['IOM'], 'Istanbul': ['IST', 'SAW'], 'Ithaca/Cortland': ['ITH'], 'Ivalo': ['IVL'], 'Ixtapa/Zihuatenejo': ['ZIH'], 'Izmir': ['IZM', 'ADB'], 'Jackson Hole': ['JAC', 'JAC'], 'Jackson': ['JXN', 'JAN', 'HKS', 'MKL'], 'Jackson, \xa0MN': ['MJQ'], 'Jacksonville': ['LRF', 'NZC', 'NIP', 'JAX', 'CRG', 'IJX', 'OAJ', 'JKV'], 'Jacmel': ['JAK'], 'Jacobabad': ['JAG'], 'Jacobina': ['JCM'], 'Jacquinot Bay': ['JAQ'], 'Jaffna': ['JAF'], 'Jagdalpur': ['JGB'], 'Jaipur': ['JAI'], 'Jaisalmer': ['JSA'], 'Jakarta': ['HLP', 'JKT', 'CGK'], 'Jalalabad': ['JAA'], 'Jalandhar': ['JLR'], 'Jalapa': ['JAL'], 'Jales': ['JLS'], 'Jaluit Island': ['UIT'], 'Jamba': ['JMB'], 'Jambi': ['DJB'], 'Jambol': ['JAM'], 'Jamestown': ['JMS', 'JHW'], 'Jammu': ['IXJ'], 'Jamnagar': ['JGA'], 'Jamshedpur': ['IXW'], 'Janakpur': ['JKR'], 'Jandakot': ['JAD'], 'Janesville': ['JVL'], 'Januaria': ['JNA'], 'Jaque': ['JQE'], 'Jatai': ['JTI'], 'Jauja': ['JAU'], 'Jayapura': ['DJJ'], 'Jeddah': ['JED'], 'Jefferson City': ['JEF'], 'Jeremie': ['JEE'], 'Jerez de la Frontera/Cadiz': ['XRY'], 'Jersey': ['JER'], 'Jerusalem': ['JRS'], 'Jessore': ['JSR'], 'Jeypore': ['PYB'], "Ji'an": ['JGS'], 'Jiamusi': ['JMU'], 'Jiayuguan': ['JGN'], 'Jijel': ['GJL'], 'Jijiga': ['JIJ'], 'Jilin': ['JIL'], 'Jimma': ['JIM'], 'Jinan': ['TNA'], 'Jingdezhen': ['JDZ'], 'Jinghong': ['JHG'], 'Jining': ['JNG'], 'Jinja': ['JIN'], 'Jinjiang': ['JJN'], 'Jinka': ['BCO'], 'Jinzhou': ['JNZ'], 'Jipijapa': ['JIP'], 'Jiri': ['JIR'], 'Jiujiang': ['JIU'], 'Jiwani': ['JIW'], 'Joacaba': ['JCB'], 'Joao Pessoa': ['JPA'], 'Jodhpur': ['JDH'], 'Jönköping': ['JKG'], 'Joensuu': ['JOE'], 'Johannesburg': ['JNB'], 'Johnson City': ['BGM'], 'Johnston Island': ['JON'], 'Johnstown': ['JST'], 'Johor Bahru': ['JHB'], 'Joinville': ['JOI'], 'Jolo': ['JOL'], 'Jomsom': ['JMO'], 'Jonesboro': ['JBR'], 'Joplin': ['JLN'], 'Jorhat': ['JRH'], 'Jos': ['JOS'], 'Jose De San Martin': ['JSM'], 'Jouf': ['AJF'], 'Juanjui': ['JJI'], 'Juba': ['JUB'], 'Juist': ['JUI'], 'Juiz De Fora': ['JDF'], 'Jujuy': ['JUJ'], 'Julia Creek': ['JCK'], 'Juliaca': ['JUL'], 'Jumla': ['JUM'], 'Jundah': ['JUN'], 'Juneau': ['JNU'], 'Junin': ['JNI'], 'Juticalpa': ['JUT'], 'Jwaneng': ['JWA'], 'Jyväskylä': ['JYV'], 'Kabul': ['KBL'], 'Kagoshima': ['KOJ'], 'Kahramanmaras': ['KCM'], 'Kahului': ['OGG'], 'Kajaani': ['KAJ'], 'Kalamata': ['KLX'], 'Kalamazoo/Battle Creek': ['AZO'], 'Kalgoorlie': ['KGI'], 'Kaliningrad': ['KGD'], 'Kalispell': ['FCA'], 'Kalmar': ['KLR'], 'Kamloops, BC': ['YKA'], 'Kamuela': ['MUE'], 'Kano': ['KAN'], 'Kanpur': ['KNU'], 'Kansas City': ['MCI'], 'Kaohsiung International': ['KHH'], 'Kapalua West': ['JHM'], 'Karachi': ['KHI'], 'Karlsruhe': ['FKB'], 'Karlstad': ['KSD'], 'Karpathos': ['AOK'], 'Karratha': ['KTA'], 'Kars': ['KYS'], 'Karumba': ['KRB'], 'Karup': ['KRP'], 'Kaschechawan, PQ': ['ZKE'], 'Kassala': ['KSL'], 'Katherine': ['KTR'], 'Kathmandu': ['KTM'], 'Katima Mulilo/Mpacha': ['MPA'], 'Kauhajoki': ['KHJ'], 'Kaunakakai': ['MKK'], 'Kavalla': ['KVA'], 'Kayseri': ['ASR'], 'Kazan': ['KZN'], 'Keetmanshoop': ['KMP'], 'Kelowna, BC': ['YLW'], 'Kemi/Tornio': ['KEM'], 'Kenai': ['ENA'], 'Kent': ['MSE'], 'Kerry County': ['KIR'], 'Ketchikan': ['KTN'], 'Key West': ['EYW'], 'Khamis Mushayat': ['AHB'], 'Kharga': ['UVL'], 'Kharkov': ['HRK'], 'Khartoum': ['KRT'], 'Khuzdar': ['KDD'], 'Kiel': ['KEL'], 'Kiev': ['KBP', 'IEV'], 'Kigali': ['KGL'], 'Kilimadjaro': ['JRO'], 'Killeem': ['ILE'], 'Kimberley': ['KIM'], 'King Island': ['KNS'], 'King Salomon': ['AKN'], 'Kingscote': ['KGC'], 'Kingston': ['KIN', 'ISO'], 'Kingstown': ['SVD'], 'Kinshasa': ['FIH'], 'Kiritimati': ['CXI'], 'Kirkenes': ['KKN'], 'Kirkuk': ['KIK'], 'Kirkwall': ['KOI'], 'Kiruna': ['KRN'], 'Kisangani': ['FKI'], 'Kittilä': ['KTT'], 'Kitwe': ['KIW'], 'Klagenfurt': ['KLU'], 'Klamath Fall': ['LMT'], 'Klawock': ['KLW'], 'Kleinsee': ['KLZ'], 'Knock': ['NOC'], 'Knoxville': ['TYS'], 'Kobe': ['UKB'], 'Kochi': ['KCZ'], 'Köln, Köln/Bonn': ['CGN'], 'Kodiak': ['ADQ'], 'Kohat': ['OHT'], 'Kokkola/Pietarsaari': ['KOK'], 'Kolkata': ['CCU'], 'Komatsu': ['KMQ'], 'Kona': ['KOA'], 'Konya': ['KYA'], 'Korhogo': ['HGO'], 'Kos': ['KGS'], 'Kota Kinabalu': ['BKI'], 'Kotzbue': ['OTZ'], 'Kowanyama': ['KWM'], 'Krakow': ['KRK'], 'Kristiansand': ['KRS'], 'Kristianstad': ['KID'], 'Kristiansund': ['KSU'], 'Kuala Lumpur': ['KUL', 'SZB'], 'Kuantan': ['KUA'], 'Kuching': ['KCH'], 'Kumamoto': ['KMJ'], 'Kununurra': ['KNX'], 'Kuopio': ['KUO'], 'Kushiro': ['KUH'], 'Kuujjuaq': ['YVP'], 'Kuujjuarapik': ['YGW'], 'Kuusamo': ['KAO'], 'Kuwait': ['KWI'], 'Kyoto': ['UKY'], 'Labe': ['LEK'], 'Labouchere Bay': ['WLB'], 'Labuan': ['LBU'], 'Lac Brochet, MB': ['XLB'], 'La Coruna': ['LCG'], 'La Crosse': ['LSE'], 'Lae': ['LAE'], 'La Rochelle': ['LRH'], 'Lafayette': ['LAF'], 'Lafayette, La': ['LFT'], 'Lagos': ['LOS'], 'La Grande': ['YGL'], 'Lahore': ['LHE'], 'Lake Charles': ['LCH'], 'Lake Havasu City': ['HII'], 'Lake Tahoe': ['TVL'], 'Lakselv': ['LKL'], 'Lambarene': ['LBQ'], 'Lamezia Terme': ['SUF'], 'Lampedusa': ['LMP'], 'Lanai City': ['LNY'], 'Lancaster': ['LNS'], "Land's End": ['LEQ'], 'Langkawi': ['LGK'], 'Lannion': ['LAI'], 'Lanseria': ['HLA'], 'Lansing': ['LAN'], 'La Paz': ['LPB', 'LAP'], 'Lappeenranta': ['LPP'], 'Laramie': ['LAR'], 'Laredo': ['LRD'], 'Larnaca': ['LCA'], 'Las Palmas': ['LPA'], 'Las Vegas': ['LAS'], 'Latrobe': ['LBE'], 'Launceston': ['LST'], 'Laurel/Hattisburg': ['PIB'], 'Laverton': ['LVO'], 'Lawton': ['LAW'], 'Lazaro Cardenas': ['LZC'], 'Leaf Rapids': ['YLR'], 'Learmouth': ['LEA'], 'Lebanon': ['LEB'], 'Leeds/Bradford': ['LBA'], 'Leinster': ['LER'], 'Leipzig': ['LEJ'], 'Lelystad': ['LEY'], 'Leon': ['BJX'], 'Leonora': ['LNO'], 'Lerwick/Tingwall': ['LWK'], 'Lewiston': ['LWS'], 'Lewistown': ['LWT'], 'Lexington': ['LEX'], 'Libreville': ['LBV'], 'Lidkoeping': ['LDK'], 'Liege': ['LGG'], 'Lifou': ['LIF'], 'Lihue': ['LIH'], 'Lille': ['LIL'], 'Lilongwe': ['LLW'], 'Lima': ['LIM'], 'Limassol': ['QLI'], 'Limoges': ['LIG'], 'Lincoln': ['LNK'], 'Lindeman Island': ['LDC'], 'Linz': ['LNZ'], 'Lisala': ['LIQ'], 'Lisbon': ['LIS'], 'Lismore': ['LSY'], 'Little Rock': ['LIT'], 'Liverpool': ['LPL'], 'Lizard Island': ['LZR'], 'Ljubljana': ['LJU'], 'Lockhart River': ['IRG'], 'Lome': ['LFW'], 'London': ['YXU', 'LCY', 'LGW', 'LHR', 'LTN', 'STN'], 'London Metropolitan Area': ['LON'], 'Londonderry': ['LDY'], 'Long Beach': ['LGB'], 'Long Island': ['LIJ'], 'Long Island, Islip': ['ISP'], 'Longreach': ['LRE'], 'Longview/Kilgore': ['GGG'], 'Longyearbyen': ['LYR'], 'Loreto': ['LTO'], 'Lorient': ['LRT'], 'Los Angeles': ['LAX'], 'Los Cabos': ['SJD'], 'Los Mochis': ['LMM'], 'Los Rodeos': ['TFN'], 'Losinj': ['LSZ'], 'Lourdes/Tarbes': ['LDE'], 'Louisville': ['SDF'], 'Luanda': ['LAD'], 'Lubbock': ['LBB'], 'Lucknow': ['LKO'], 'Luederitz': ['LUD'], 'Luga': ['MLA'], 'Lugano': ['LUG'], 'Lulea': ['LLA'], 'Lumbumbashi': ['FBM'], 'Lusaka': ['LUN'], 'Lusisiki': ['LUJ'], 'Luxembourg': ['LUX'], 'Luxi': ['LUM'], 'Luxor': ['LXR'], 'Lvov': ['LWO'], 'Lydd': ['LYX'], 'Lynchburg': ['LYH'], 'Lyon': ['LYS'], 'Lyons': ['LYO'], 'Maastricht/Aachen': ['MST'], 'Macapa': ['MCP'], 'Macau': ['MFM'], 'Maceio': ['MCZ'], 'Mackay': ['MKY'], 'Macon': ['MCN'], 'Mactan Island': ['NOP'], 'Madinah': ['MED'], 'Madison': ['MSN'], 'Madras': ['MAA'], 'Madrid': ['MAD'], 'Mahe': ['SEZ'], 'Mahon': ['MAH'], 'Maitland': ['MTL'], 'Majunga': ['MJN'], 'Makung': ['MZG'], 'Malabo': ['SSG'], 'Malaga': ['AGP'], 'Malatya': ['MLX'], 'Male': ['MLE'], 'Malindi': ['MYD'], 'Malmo': ['MMA', 'MMX'], 'Man': ['MJC'], 'Managua': ['MGA'], 'Manaus': ['MAO'], 'Manchester': ['MAN', 'MHT'], 'Mandalay': ['MDL'], 'Manguna': ['MFO'], 'Manihi': ['XMH'], 'Manila': ['MNL'], 'Manzanillo': ['ZLO'], 'Manzini': ['MTS'], 'Maputo': ['MPM'], 'Mar del Plata': ['MDQ'], 'Maracaibo': ['MAR'], 'Maradi': ['MFQ'], 'Maras': ['KCM'], 'Marathon': ['MTH'], 'Mardin': ['MQM'], 'Mare': ['MEE'], 'Margate': ['MGH'], 'Margerita': ['PMV'], 'Maribor': ['MBX'], 'Mariehamn': ['MHQ'], 'Maroua': ['MVR'], 'Marquette': ['MQT'], 'Marrakesh': ['RAK'], 'Marsa Alam': ['RMF'], 'Marsa Matrah': ['MUH'], 'Marseille': ['MRS'], 'Marsh Harbour': ['MHH'], "Martha's Vineyard": ['MVY'], 'Martinsburg': ['MRB'], 'Maryborough': ['MBH'], 'Maseru': ['MSU'], 'Mason City IA': ['MCW'], 'Masvingo': ['MVZ'], 'Matsumoto, Nagano': ['MMJ'], 'Matsuyama': ['MYJ'], 'Mattoon': ['MTO'], 'Maun': ['MUB'], 'Maupiti': ['MAU'], 'Mauritius': ['MRU'], 'Mayaguez': ['MAZ'], 'Mazatlan': ['MZT'], 'McAllen': ['MFE'], 'Medan': ['MES', 'KNO'], 'Medellin': ['MDE'], 'Medford': ['MFR'], 'Medina': ['MED'], 'Meekatharra': ['MKR'], 'Melbourne': ['MEL', 'MLB'], 'Melville Hall': ['DOM'], 'Memphis': ['MEM'], 'Mendoza': ['MDZ'], 'Manado': ['MDC'], 'Merced': ['MCE'], 'Merida': ['MID'], 'Meridian': ['MEI'], 'Merimbula': ['MIM'], 'Messina': ['MEZ'], 'Metlakatla': ['MTM'], 'Metz': ['MZM'], 'Metz/Nancy Metz': ['ETZ'], 'Mexicali': ['MXL'], 'Mexico City': ['MEX', 'AZP', 'MEX', 'NLU'], 'Mfuwe': ['MFU'], 'Miami': ['MIA'], 'Mianwali': ['MWD'], 'Middlemount': ['MMM'], 'Midland/Odessa': ['MAF'], 'Midway Island': ['MDY'], 'Mikkeli': ['MIK'], 'Milan': ['MIL', 'LIN', 'MXP', 'BGY'], 'Mildura': ['MQL'], 'Miles City': ['MLS'], 'Milford Sound': ['MFN'], 'Milwaukee': ['MKE'], 'Minatitlan': ['MTT'], 'Mineralnye Vody': ['MRV'], 'Minneapolis': ['MSP'], 'Minot': ['MOT'], 'Minsk, International': ['MSQ'], 'Miri': ['MYY'], 'Mirpur': ['QML'], 'Missula': ['MSO'], 'Mitchell': ['MHE'], 'Miyako Jima': ['MMY'], 'Miyazaki': ['KMI'], 'Mkambati': ['MBM'], 'Moanda': ['MFF'], 'Mobile': ['MOB'], 'Modesto': ['MOD'], 'Moenjodaro': ['MJD'], 'Mogadishu': ['MGQ'], 'Mokuti': ['OKU'], 'Moline/Quad Cities': ['MLI'], 'Mombasa': ['MBA'], 'Monastir': ['MIR'], 'Moncton': ['YQM'], 'Monroe': ['MLU'], 'Monrovia': ['MLW', 'ROB'], 'Montego Bay': ['MBJ'], 'Montenegro': ['QGF'], 'Monterey': ['MRY'], 'Monterrey': ['MTY', 'NTR'], 'Montevideo': ['MVD'], 'Montgomery': ['MGM'], 'Montpellier': ['MPL'], 'Montreal': ['YMQ', 'YUL', 'YMX'], 'Montrose/Tellruide': ['MTJ'], 'Moorea': ['MOZ'], 'Moranbah': ['MOV'], 'Moree': ['MRZ'], 'Morelia': ['MLM'], 'Morgantown': ['MGW'], 'Morioka, Hanamaki': ['HNA'], 'Moroni': ['HAH'], 'Moruya': ['MYA'], 'Moscow': ['MOW', 'DME', 'SVO', 'VKO'], 'Moses Lake': ['MWH'], 'Mossel Bay': ['MZY'], 'Mostar': ['OMO'], 'Mosul': ['OSM'], 'Mouila': ['MJL'], 'Moundou': ['MQQ'], 'Mount Cook': ['GTN'], 'Mount Gambier': ['MGB'], 'Mount Magnet': ['MMG'], 'Mt. Isa': ['ISA'], 'Mt. McKinley': ['MCL'], 'Muenchen': ['MUC'], 'Muenster/Osnabrueck': ['FMO'], 'Mulhouse': ['MLH'], 'Multan': ['MUX'], 'Murcia': ['MJV'], 'Murmansk': ['MMK'], 'Mus': ['MSR'], 'Muscat': ['MCT'], 'Muscle Shoals': ['MSL'], 'Muskegon': ['MKG'], 'Muzaffarabad': ['MFG'], 'Mvengue': ['MVB'], 'Mykonos': ['JMK'], 'Myrtle Beach': ['MYR', 'CRE'], 'Mysore': ['MYQ'], 'Mytilene': ['MJT'], 'Mzamba': ['MZF'], 'Nadi': ['NAN'], 'Nagasaki': ['NGS'], 'Nagoya': ['NGO'], 'Nagpur': ['NAG'], 'Nairobi': ['NBO'], 'Nakhichevan': ['NAJ'], 'Nakhon Si Thammarat': ['NST'], 'Nancy': ['ENC'], 'Nanisivik': ['YSR'], 'Nanning': ['NNG'], 'Nantes': ['NTE'], 'Nantucket': ['ACK'], 'Naples': ['NAP', 'APF'], 'Narrabri': ['NAA'], 'Narrandera': ['NRA'], 'Narsarsuaq': ['UAK'], 'Nashville': ['BNA'], 'Nassau': ['NAS'], 'Natal': ['NAT'], 'Nausori': ['SUV'], 'Nawab Shah': ['WNS'], 'Naxos': ['JNX'], "N'Djamena": ['NDJ'], "N'Dola": ['NLA'], 'Nelson': ['NSN'], 'Nelspruit': ['NLP', 'MQP'], 'Nevis': ['NEV'], 'New Bern': ['EWN'], 'New Haven': ['HVN'], 'New Orleans, La': ['MSY'], 'Newquay': ['NQY'], 'New Valley': ['UVL'], 'New York': ['JFK', 'LGA', 'EWR', 'NYC'], 'Newburgh': ['SWF'], 'Newcastle': ['BEO', 'NTL', 'NCL', 'NCS'], 'Newman': ['ZNE'], 'Newport News/Williamsburg': ['PHF'], "N'Gaoundere": ['NGE'], 'Niagara Falls International': ['IAG'], 'Niamey': ['NIM'], 'Nice': ['NCE'], 'Nicosia': ['NIC'], 'Nikolaev': ['NLV'], 'Niigata': ['KIJ'], 'Nimes': ['FNI'], 'Nis': ['INI'], 'Nizhny Novgorod': ['GOJ'], 'Nome': ['OME'], 'Noosa': ['NSA'], 'Norfolk Island': ['NLK'], 'Norfolk/Virginia Beach': ['ORF'], 'Norman Wells': ['YVQ'], 'Norrkoeping': ['NRK'], 'North Bend': ['OTH'], 'North Eleuthera': ['ELH'], 'Norwich': ['NWI'], 'Nottingham': ['EMA'], 'Nouadhibou': ['NDB'], 'Nouakchott': ['NKC'], 'Noumea': ['NOU'], 'Novi Sad': ['QND'], 'Novosibirsk': ['OVB'], 'Nürnberg': ['NUE'], 'Nuevo Laredo': ['NLD'], "Nuku'alofa": ['TBU'], 'Oakland': ['OAK'], 'Oaxaca': ['OAX'], 'Odense': ['ODE'], 'Odessa': ['ODS'], 'Oerebro': ['ORB'], 'Ohrid': ['OHD'], 'Oita': ['OIT'], 'Okayama': ['OKJ'], 'Okinawa, Ryukyo Island': ['OKA'], 'Oklahoma City': ['OKC'], 'Olbia': ['OLB'], 'Olympic Dam': ['OLP'], 'Omaha': ['OMA'], 'Ondangwa': ['OND'], 'Ontario': ['ONT'], 'Oran': ['ORN'], 'Orange': ['OAG'], 'Orange County': ['SNA'], 'Oranjemund': ['OMD'], 'Oranjestad': ['AUA'], 'Orkney': ['KOI'], 'Orlando Metropolitan Area': ['ORL'], 'Orlando': ['MCO'], 'Orpheus Island': ['ORS'], 'Osaka, Metropolitan Area': ['OSA'], 'Osaka': ['ITM', 'KIX'], 'Oshkosh': ['OSH'], 'Osijek': ['OSI'], 'Oslo': ['OSL', 'FBU', 'TRF'], 'Ottawa': ['YOW'], 'Ouadda': ['ODA'], 'Ouarzazate': ['OZZ'], 'Oudtshoorn': ['OUH'], 'Ouagadougou': ['OUA'], 'Oujda': ['OUD'], 'Oulu': ['OUL'], 'Out Skerries': ['OUK'], 'Oviedo': ['OVD'], 'Owensboro': ['OWB'], 'Oxnard': ['OXR'], 'Oyem': ['UVE'], 'Paderborn/Lippstadt': ['PAD'], 'Paducah': ['PAH'], 'Page/Lake Powell': ['PGA'], 'Pago Pago': ['PPG'], 'Pakersburg': ['PKB'], 'Palermo': ['PMO'], 'Palma de Mallorca': ['PMI'], 'Palmas': ['PMW'], 'Palmdale/Lancaster': ['PMD'], 'Palmerston North': ['PMR'], 'Palm Springs': ['PSP'], 'Panama City': ['PTY', 'PFN'], 'Panjgur': ['PJG'], 'Pantelleria': ['PNL'], 'Papeete': ['PPT'], 'Paphos': ['PFO'], 'Paraburdoo': ['PBO'], 'Paramaribo': ['PBM'], 'Paris': ['PAR', 'CDG', 'LBG', 'ORY'], 'Paro': ['PBH'], 'Pasco': ['PSC'], 'Pasni': ['PSI'], 'Patna': ['PAT'], 'Pattaya': ['PYX'], 'Pau': ['PUF'], 'Pellston': ['PLN'], 'Penang International': ['PEN'], 'Pendelton': ['PDT'], 'Pensacola': ['PNS'], 'Peoria/Bloomington': ['PIA'], 'Pereira': ['PEI'], 'Perpignan': ['PGF'], 'Perth International': ['PER'], 'Perugia': ['PEG'], 'Pescara': ['PSR'], 'Peshawar': ['PEW'], 'Petersburg': ['PSG'], 'Phalaborwa': ['PHW'], 'Philadelphia': ['PHL'], 'Phnom Penh': ['PNH'], 'Phoenix': ['PHX'], 'Phuket': ['HKT'], 'Pierre': ['PIR'], 'Pietermaritzburg': ['PZB'], 'Pietersburg': ['PTG'], 'Pilanesberg/Sun City': ['NTY'], 'Pisa': ['PSA'], 'Pittsburgh International Airport': ['PIT'], 'Plattsburgh': ['PLB'], 'Plettenberg Bay': ['PBZ'], 'Pocatello': ['PIH'], 'Podgorica': ['TGD'], 'Pohnpei': ['PNI'], 'Pointe a Pitre': ['PTP'], 'Pointe Noire': ['PNR'], 'Poitiers': ['PIS'], 'Ponce': ['PSE'], 'Ponta Delgada': ['PDL'], 'Pori': ['POR'], 'Port Angeles': ['CLM'], 'Port au Prince': ['PAP'], 'Port Augusta': ['PUG'], 'Port Elizabeth': ['PLZ'], 'Port Gentil': ['POG'], 'Port Harcourt': ['PHC'], 'Port Hedland': ['PHE'], 'Portland': ['PTJ', 'PWM'], 'Portland International': ['PDX'], 'Port Lincoln': ['PLO'], 'Port Macquarie': ['PQQ'], 'Port Menier, PQ': ['YPN'], 'Port Moresby': ['POM'], 'Porto': ['OPO'], 'Porto Alegre': ['POA'], 'Port of Spain': ['POS'], 'Port Said': ['PSD'], 'Porto Santo': ['PXO'], 'Porto Velho': ['PVH'], 'Port Vila': ['VLI'], 'Poughkeepsie': ['POU'], 'Poznan, Lawica': ['POZ'], 'Prague': ['PRG'], 'Praia': ['RAI'], 'Presque Island': ['PQI'], 'Pretoria': ['PRY'], 'Preveza/Lefkas': ['PVK'], 'Prince George': ['YXS'], 'Prince Rupert/Digby Island': ['YPR'], 'Pristina': ['PRN'], 'Prosperpine': ['PPP'], 'Providence': ['PVD'], 'Prudhoe Bay': ['SCC'], 'Puebla': ['PBC'], 'Pueblo': ['PUB'], 'Puerto Escondido': ['PXM'], 'Puerto Ordaz': ['PZO'], 'Puerto Plata': ['POP'], 'Puerto Vallarta': ['PVR'], 'Pukatawagan': ['XPK'], 'Pula': ['PUY'], 'Pullman': ['PUW'], 'Pune': ['PNQ'], 'Punta Arenas': ['PUQ'], 'Punta Cana': ['PUJ'], 'Pu San': ['PUS'], 'Pyongyang': ['FNJ'], 'Quebec': ['YQB'], 'Queenstown': ['UEE', 'ZQN'], 'Quetta': ['UET'], 'Qingdao': ['TAO'], 'Quimper': ['UIP'], 'Quincy': ['UIN'], 'Quito': ['UIO'], 'Rabat': ['RBA'], 'Rahim Yar Khan': ['RYK'], 'Raiatea': ['RFP'], 'Rainbow Lake, AB': ['YOP'], 'Rajkot': ['RAJ'], 'Raleigh/Durham': ['RDU'], 'Ranchi': ['IXR'], 'Rangiroa': ['RGI'], 'Rangoon': ['RGN'], 'Rapid City': ['RAP'], 'Rarotonga': ['RAR'], 'Ras al Khaymah': ['RKT'], 'Rawala Kot': ['RAZ'], 'Rawalpindi': ['RWP'], 'Reading': ['RDG'], 'Recife': ['REC'], 'Redding': ['RDD'], 'Redmond': ['RDM'], 'Reggio Calabria': ['REG'], 'Regina': ['YQR'], 'Reina Sofia': ['TFS'], 'Rennes': ['RNS'], 'Reno': ['RNO'], 'Resolute Bay': ['YRB'], 'Reus': ['REU'], 'Reykjavik': ['REK', 'KEF'], 'Rhinelander': ['RHI'], 'Rhodos': ['RHO'], 'Richards Bay': ['RCB'], 'Richmond': ['RIC'], 'Riga': ['RIX'], 'Rijeka': ['RJK'], 'Rimini': ['RMI'], 'Rio Branco': ['RBR'], 'Rio de Janeiro': ['GIG', 'SDU', 'RIO'], 'Riyadh': ['RUH'], 'Roanne': ['RNE'], 'Roanoke': ['ROA'], 'Roatan': ['RTB'], 'Rochester': ['RST', 'ROC'], 'Rock Sound': ['RSD'], 'Rock Springs': ['RKS'], 'Rockford': ['RFD'], 'Rockhampton': ['ROK'], 'Rockland': ['RKD'], 'Rocky Mount': ['RWI'], 'Rodez': ['RDZ'], 'Rodrigues Island': ['RRG'], 'Roenne': ['RNN'], 'Rome': ['ROM', 'CIA', 'FCO'], 'Ronneby': ['RNB'], 'Rosario': ['ROS'], 'Rostov': ['RVI', 'ROV'], 'Rotorua': ['ROT'], 'Rotterdam': ['RTM'], 'Rovaniemi': ['RVN'], 'Rundu': ['NDU'], 'Ruse': ['ROU'], 'Saarbruecken': ['SCN'], 'Sacramento': ['SMF'], 'Sado Shima': ['SDS'], 'Saginaw/Bay City/Midland': ['MBS'], 'Saidu Sharif': ['SDT'], 'Saigon': ['SGN'], 'Saint Brieuc': ['SBK'], 'Saint Denis': ['RUN'], 'Saint John': ['YSJ'], 'Saipan': ['SPN'], 'Sal': ['SID'], 'Salalah': ['SLL'], 'Salem': ['SLE'], 'Salinas': ['SNS', 'SNC'], 'Salisbury': ['SAY', 'SBY'], 'Saloniki': ['SKG'], 'Salta, Gen Belgrano': ['SLA'], 'Salt Lake City': ['SLC'], 'Salvador': ['SSA'], 'Salzburg': ['SZG'], 'Samara': ['KUF'], 'Samarkand': ['SKD'], 'Samos': ['SMI'], 'Samsun': ['SZF'], 'San Andres': ['ADZ'], 'San Angelo': ['SJT'], 'San Antonio': ['SAT'], 'San Carlos de Bariloche': ['BRC'], 'San Diego': ['SAN'], 'San Francisco': ['SFO'], 'San Jose Cabo': ['SJD'], 'San Jose': ['SJO', 'SJC'], 'San Juan': ['SJU'], 'San Luis Obisco': ['SBP'], 'San Luis Potosi': ['SLP'], 'San Pedro': ['SPY'], 'San Pedro Sula': ['SAP'], 'San Salvador': ['ZSA', 'SAL'], 'San Sebastian': ['EAS'], 'Sanaa': ['SAH'], 'Sandspit': ['YZP'], 'Santa Ana': ['SNA'], 'Santa Barbara': ['SBA'], 'Santa Cruz de la Palma': ['SPC'], 'Santa Cruz de la Sierra': ['SRZ'], 'Santa Katarina': ['SKV'], 'Santa Maria': ['SMA', 'SMX'], 'Santander': ['SDR'], 'Santa Rosa': ['STS', 'SRB', 'SRA', 'RSA'], 'Santa Rosa, Copan': ['SDH'], 'Santa Rosalia': ['SSL', 'SRL'], 'Santiago': ['SCU'], 'Santiago de Chile': ['SCL'], 'Santiago de Compostela': ['SCQ'], 'Santo': ['SON'], 'Santo Domingo': ['SDQ'], 'Sao Luis': ['SLZ'], 'Sao Tome': ['TMS'], 'Sarajevo': ['SJJ'], 'Saransk': ['SKX'], 'Sarasota/Bradenton': ['SRQ'], 'Saskatoon': ['YXE'], 'Sassandra': ['ZSS'], 'Savannah': ['SAV'], 'Savonlinna': ['SVL'], 'Scarborough': ['TAB'], 'Scone': ['NSO'], 'Scottsdale': ['SCF'], 'Seattle/Tacoma': ['SEA'], 'Sehba': ['SEB'], 'Seinaejoki': ['SJY'], 'Selibi Phikwe': ['PKW'], 'Sendai': ['SDJ'], 'Seoul': ['ICN', 'SEL'], 'Sevilla': ['SVQ'], 'Sfax': ['SFA'], 'Shamattawa, MB': ['ZTM'], 'Shanghai': ['SHA', 'PVG'], 'Shannon': ['SNN'], 'Sharjah': ['SHJ'], 'Sharm El Sheikh': ['SSH'], 'Sheffield, City Airport': ['SZD'], 'Sheffield, Doncaster, Robin Hood International Airport': ['DSA'], 'Shenandoah Valley/Stauton': ['SHD'], 'Shenyang': ['SHE'], 'Shenzhen': ['SZX'], 'Sheridan': ['SHR'], 'Shreveport, La': ['SHV'], 'Shute Harbour': ['JHQ'], 'Sibu': ['SBW'], 'Sidney': ['SDY'], 'Silistra': ['SLS'], 'Simferopol': ['SIP'], 'Sindhri': ['MPD'], 'Singapore': ['SIN', 'QPG', 'XSP'], 'Singleton': ['SIX'], 'Sioux City IA': ['SUX'], 'Sioux Falls': ['FSD'], 'Sishen': ['SIS'], 'Sitka': ['SIT'], 'Sivas': ['VAS'], 'Siwa': ['SEW'], 'Skagway': ['SGY'], 'Skardu': ['KDU'], 'Skiathos': ['JSI'], 'Skopje': ['SKP'], 'Skrydstrup': ['SKS'], 'Skukuza': ['SZK'], 'Sligo': ['SXL'], 'Smithers': ['YYD'], 'Sodankylae': ['SOT'], 'Soenderborg': ['SGD'], 'Soendre Stroemfjord': ['SFJ'], 'Sofia': ['SOF'], 'Sogndal': ['SOG'], 'Southampton': ['SOU'], 'South Bend': ['SBN'], 'South Indian Lake, MB': ['XSI'], 'South Molle Island': ['SOI'], 'Southend': ['SEN'], 'Split': ['SPU'], 'Spokane': ['GEG'], 'Springbok': ['SBU'], 'Springfield': ['SPI', 'SGF'], 'Srinagar': ['SXR'], 'St. Augustin, PQ': ['YIF'], 'St. Croix': ['STX'], 'St. Etienne': ['EBU'], 'St. George': ['SGU'], "St. John's": ['YYT'], 'St. Kitts': ['SKB'], 'St. Louis': ['STL'], 'St. Lucia Hewanorra': ['UVF'], 'St. Lucia Vigle': ['SLU'], 'St. Marteen': ['SXM'], 'St. Martin': ['SFG'], 'St. Petersburg': ['LED'], 'St. Pierre, NF': ['FSP'], 'St. Thomas': ['STT'], 'St. Vincent': ['SVD'], 'Stansted': ['STN'], 'State College/Belefonte': ['SCE'], 'Stavanger': ['SVG'], 'Steamboat Springs': ['HDN'], 'Stettin': ['SZZ'], 'Stockholm Metropolitan Area': ['STO'], 'Stockholm': ['ARN', 'BMA'], 'Stockton': ['SCK'], 'Stornway': ['SYY'], 'Strasbourg': ['SXB'], 'Streaky Bay': ['KBY'], 'Stuttgart': ['STR'], 'Sui': ['SUL'], 'Sukkur': ['SKZ'], 'Sumburgh': ['LSI'], 'Sun Valley': ['SUN'], 'Sundsvall': ['SDL'], 'Sunshine Coast': ['MCY'], 'Surabaya': ['SUB'], 'Surat': ['STV'], 'Suva': ['SUV'], 'Swakopmund': ['SWP'], 'Sydney': ['SYD'], 'Sylhet': ['ZYL'], 'Syracuse': ['SYR'], 'Tabuk': ['TUU'], 'Taif': ['TIF'], 'Taipei': ['TPE', 'TAY'], 'Taiyuan': ['TYN'], 'Takamatsu': ['TAK'], 'Talkeetna': ['TKA'], 'Tallahassee': ['TLH'], 'Tallinn': ['QUF', 'TLL'], 'Tampa': ['TPA'], 'Tampere': ['TMP'], 'Tampico': ['TAM'], 'Tamworth': ['TMW'], 'Tangier': ['TNG'], 'Taree': ['TRO'], 'Targovishte': ['TGV'], 'Tashkent': ['TAS'], 'Tawau': ['TWU'], 'Tbilisi': ['TBS'], 'Te Anau': ['TEU'], 'Teesside, Durham Tees Valley': ['MME'], 'Tegucigalpa': ['TGU'], 'Tehran': ['THR'], 'Tekirdag': ['TEQ'], 'Tel Aviv': ['TLV'], 'Telluride': ['TEX'], 'Temora': ['TEM'], 'Tenerife': ['TCI', 'TFS', 'TFN'], 'Tennant Creek': ['TCA'], 'Terceira': ['TER'], 'Teresina': ['THE'], 'Termez': ['TMZ'], 'Terrace': ['YXT'], 'Terre Haute': ['HUF'], 'Texarkana': ['TXK'], "Thaba'Nchu": ['TCU'], 'The Pas': ['YQD'], 'Thessaloniki': ['SKG'], 'Thief River Falls': ['TVF'], 'Thira': ['JTR'], 'Thiruvananthapuram': ['TRV'], 'Thisted': ['TED'], 'Thompson': ['YTH'], 'Thorne Bay': ['KTB'], 'Thunder Bay': ['YQT'], 'Thursday Island': ['TIS'], 'Tianjin': ['TSN'], 'Tijuana': ['TIJ'], 'Tioman': ['TOD'], 'Tirana': ['TIA'], 'Tiruchirapally': ['TRZ'], 'Tivat': ['TIV'], 'Tobago': ['TAB'], 'Tokushima': ['TKS'], 'Tokyo': ['TYO', 'HND', 'NRT'], 'Toledo': ['TOL'], 'Tom Price': ['TPR'], 'Toowoomba': ['TWB'], 'Toronto': ['YTZ', 'YYZ', 'YTO'], 'Tortola': ['TOV'], 'Touho': ['TOU'], 'Toulouse': ['TLS'], 'Townsville': ['TSV'], 'Toyama': ['TOY'], 'Trabzon': ['TZX'], 'Trapani': ['TPS'], 'Traverse City': ['TVC'], 'Treasure Cay': ['TCB'], 'Trenton/Princeton': ['TTN'], 'Treviso': ['TSF'], 'Tri': ['TRI'], 'Trieste': ['TRS'], 'Tripoli': ['TIP'], 'Tromsoe': ['TOS'], 'Trondheim': ['TRD'], 'Tsumeb': ['TSB'], 'Tucson': ['TUS'], 'Tulepo': ['TUP'], 'Tulsa': ['TUL'], 'Tunis': ['TUN'], 'Turbat': ['TUK'], 'Turin': ['TRN'], 'Turku': ['TKU'], 'Tuscaloosa': ['TCL'], 'Tuxtla Gutierrez': ['TGZ'], 'Twin Falls': ['TWF'], 'Tyler': ['TYR'], 'Ua Huka': ['UAH'], 'Ua Pou': ['UAP'], 'Ube': ['UBJ'], 'Uberaba': ['UBA'], 'Uberlandia': ['UDI'], 'Ubon Ratchathani': ['UBP'], 'Udaipur': ['UDR'], 'Uden': ['UDE'], 'Udon Thani': ['UTH'], 'Ufa': ['UFA'], 'Uherske Hradiste': ['UHE'], 'Uige': ['UGO'], 'Ujung Pandang': ['UPG'], 'Ukhta': ['UCT'], 'Ukiah': ['UKI'], 'Ulaanbaatar': ['ULN'], 'Ulan': ['UUD'], 'Ulanhot': ['HLH'], 'Ulei': ['ULB'], 'Ulsan': ['USN'], 'Ulundi': ['ULD'], 'Umea': ['UME'], 'Umiujaq': ['YUD'], 'Umtata': ['UTT'], 'Unalakleet': ['UNK'], 'Union Island': ['UNI'], 'Unst': ['UNT'], 'Upala': ['UPL'], 'Upernavik': ['JUV'], 'Upington': ['UTN'], 'Upolu Point': ['UPP'], 'Uranium City': ['YBE'], 'Urgench': ['UGC'], 'Uriman': ['URM'], 'Urmiehm': ['OMH'], 'Uruapan': ['UPN'], 'Urubupunga': ['URB'], 'Uruguaiana': ['URG'], 'Urumqi': ['URC'], 'Uruzgan': ['URZ'], 'Ushuaia': ['USH'], 'Utapao': ['UTP'], 'Utica': ['UCA'], 'Utila': ['UII'], 'Uummannaq': ['UMD'], 'Uzhgorod': ['UDJ'], 'Vaasa': ['VAA'], 'Vaexjoe': ['VXO'], 'Vail': ['EGE'], "Val d'Or": ['YVO'], 'Valdez': ['VDZ'], 'Valdosta': ['VLD'], 'Valencia': ['VLC', 'VLN'], 'Valladolid': ['VLL'], 'Valparaiso': ['VAP'], 'Valverde': ['VDE'], 'Van': ['VAN'], 'Vancouver': ['YVR'], 'Varadero': ['VRA'], 'Varanasi': ['VNS'], 'Varkaus': ['VRK'], 'Varna': ['VAR'], 'Vasteras': ['VST'], 'Velikiye Luki': ['VLU'], 'Venice': ['VCE'], 'Veracruz': ['VER'], 'Vernal': ['VEL'], 'Vero Beach/Ft. Pierce': ['VRB'], 'Verona': ['VBS', 'VRN'], 'Victoria': ['YYJ'], 'Victoria Falls': ['VFA'], 'Vidin': ['VID'], 'Vientiane': ['VTE'], 'Vigo': ['VGO'], 'Villahermosa': ['VSA'], 'Vilnius': ['VNO'], 'Virgin Gorda': ['VIJ'], 'Visalia': ['VIS'], 'Visby': ['VBY'], 'Vitoria': ['VIT', 'VIX'], 'Vryheid': ['VYD'], 'Wabush': ['YWK'], 'Waco': ['ACT'], 'Wagga': ['WGA'], 'Walla Walla': ['ALW'], 'Wallis': ['WLS'], 'Walvis Bay': ['WVB'], 'Warrnambool': ['WMB'], 'Warsaw': ['WAW'], 'Washington DC': ['BWI', 'IAD', 'DCA', 'WAS'], 'Waterloo IA': ['ALO'], 'Watertown': ['ATY'], 'Wausau/Stevens Point': ['CWA'], 'Weipa': ['WEI'], 'Welkom': ['WEL'], 'Wellington': ['WLG'], 'Wenatchee': ['EAT'], 'West Palm Beach': ['PBI'], 'West Yellowstone': ['WYS'], 'Westerland, Sylt Airport': ['GWT'], 'Whakatane': ['WHK'], 'Whale Cove, NT': ['YXN'], 'Whangarei': ['WRE'], 'White Plains': ['HPN'], 'Whitehorse': ['YXY'], 'Whitsunday Resort': ['HAP'], 'Whyalla': ['WYA'], 'Wichita Falls': ['SPS'], 'Wichita': ['ICT'], 'Wick': ['WIC'], 'Wickham': ['WHM'], 'Wien': ['VIE'], 'Wiesbaden, Air Base': ['WIE'], 'Wilkes Barre/Scranton': ['AVP'], 'Williamsport': ['IPT'], 'Williston': ['ISL'], 'Wilmington': ['ILM'], 'Wilna': ['VNO'], 'Wiluna': ['WUN'], 'Windhoek': ['ERS', 'WDH'], 'Windsor Ontario': ['YQG'], 'Winnipeg International': ['YWG'], 'Wolf Point': ['OLF'], 'Wollongong': ['WOL'], 'Woomera': ['UMR'], 'Worcester': ['ORH'], 'Worland': ['WRL'], 'Wrangell': ['WRG'], 'Wuhan': ['WUH'], 'Wyndham': ['WYN'], 'Xiamen': ['XMN'], "Xi'an": ['XIY'], 'Yakima': ['YKM'], 'Yakutat': ['YAK'], 'Yakutsk': ['YKS'], 'Yamagata, Junmachi': ['GAJ'], 'Yamoussoukro': ['ASK'], 'Yanbu': ['YNB'], 'Yangon': ['RGN'], 'Yaounde': ['YAO'], 'Yellowknife': ['YZF'], 'Yekaterinburg': ['SVX'], 'Yichang': ['YIH'], 'Yokohama': ['YOK'], 'Yuma': ['YUM'], 'Zacatecas': ['ZCL'], 'Zadar': ['ZAD'], 'Zagreb': ['ZAG'], 'Zakynthos': ['ZTH'], 'Zaragoza': ['ZAZ'], 'Zhob': ['PZH'], 'Zinder': ['ZND'], 'Zouerate': ['OUZ'], 'Zurich': ['ZRH']}

# Helper functioon to sort cities by distance
def sort_distance(e):
    if 'distance' in e:
        return e['distance']

    return 10000

# Gets all cities in the specified around the given city
def get_airports_near(city, distance):
    url = "https://www.distance24.org/route.json?stops=" + city
    r = session.get(url)

    soup = BSoup(r.content, 'html5lib')

    json = r.json()

    cities = []

    nearby_cities = json['stops'][0]['nearByCities'] # Gets names of nearby cities
    nearby_cities.sort(key = sort_distance) # Sorts by distance from given city

    for city in nearby_cities:
        if 'distance' in city:
            if city['distance'] < distance: # Only adds cities below the threshold
                cities.append(city['city'])
        else:
            cities.append(city['city'])

    return cities

def get_flight_data(depart, arrival):
    url = "https://www.faredetective.com/faredetective/chart_data"
    r = session.post(url, data={'arrival': arrival, 'departure': depart})

    #print("Departure: " + depart)
    #print("Arrival: " + arrival)

    chart_data = r.json()['chart_data']

    temp_data = [depart, arrival, {}, {}] # Initializing data entry

    price = 0
    month_count = 0
    temp_month_count = 0
    month = ""

    for i in range(len(chart_data)): # For every month data
        item = chart_data[i] # All relevant info

        info = item['year'].split("\n")
        info.append(item['price'])

        if not month:  # First month data
            month = info[0]
            year = int(info[1])
        elif info[0] != month:  # When you get to the next month (some months have multiple data points)
            temp_data[2][months[month]] = price / temp_month_count # Sets months price to the average of each data point

            # Reset info for next month
            price = 0
            temp_month_count = 0
            month_count += 1
            month = info[0]

        temp_month_count += 1
        price += float(info[2])

        if i == len(chart_data) - 1: # Last month
            temp_data[2][months[month]] = price / temp_month_count # Sets months price to the average of each data point
            month_count += 1

    if month_count > 0: # If any data at all
        prices = temp_data[2]

        for key, price in prices.items(): # For every month's price
            key2 = key + 1 if key < 12 else 1  # Ensures that Dec to Jan gets calculated (wraps around to 1 if at the end of the list)

            if key2 in prices:  # If two consecutive months have data points
                price2 = prices[key2]

                difference = (price2 - price) / price

                #if difference > 10:
                    #difference -= difference - 10

                temp_data[3][key] = difference  # Calculates change in price

        return temp_data

    return False

# Get current weather data for a city
def get_weather_data(city):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=0d0edf5fecdbdc3efe2e67eedf441aae&units=imperial"

    r = session.get(url)

    json = r.json()

    if 'weather' in json:
        return {
            'main': json['weather'][0]['main'],
            'temp': round(json['main']['temp']),
            'icon': json['weather'][0]['icon']
        }

    return False

# Gets all airport codes for a city
def get_all_codes(cities):
    total_codes = []

    for city in cities:
        if city in city_codes:
            total_codes += city_codes[city]

    return total_codes

# Averages the prices and variances. Commenting would be a pain but trust me it works
def get_stats(surrounding_data, flight_data):
    mean_prices = {}
    mean_variances = {}
    prices_counts = {}
    variances_counts = {}
    stdev_variances = {}
    stdev_totals = {}
    stdev_counts = {}

    for route in surrounding_data:
        for i, price in route[-2].items():
            if i in mean_prices:
                mean_prices[i] += price
                prices_counts[i] += 1
            else:
                mean_prices[i] = price
                prices_counts[i] = 1

        for i, variance in route[-1].items():
            if i in mean_variances:
                mean_variances[i] += variance
                variances_counts[i] += 1
            else:
                mean_variances[i] = variance
                variances_counts[i] = 1

    for i, variance in flight_data[-1].items():
        if i in mean_variances:
            mean_variances[i] += variance
            variances_counts[i] += 1
        else:
            mean_variances[i] = variance
            variances_counts[i] = 1

    for i, variance in mean_variances.items():
        variance /= variances_counts[i]

    for i, price in mean_prices.items():
        price /= prices_counts[i]

    # Substitutes the overall variance if not is found
    for x in range(len(overall_mean_variances)):
        if x + 1 not in mean_variances:
            mean_variances[x + 1] = overall_mean_variances[x]

    for route in surrounding_data:
        for i, variance in route[-1].items():
            if i in stdev_totals:
                stdev_totals[i] += math.pow(variance - mean_variances[i], 2)
                stdev_counts[i] += 1
            else:
                stdev_totals[i] = math.pow(variance - mean_variances[i], 2)
                stdev_counts[i] = 1

    # Calculate the standard deviations
    for i, stdev_total in stdev_totals.items():
        if stdev_counts[i] > 1:
            stdev_variances[i] = math.sqrt(stdev_total / (stdev_counts[i] - 1))

    # Substitutes the overall standard deviation if not is found
    for x in range(len(overall_stdev_variances)):
        if x + 1 not in stdev_variances:
            stdev_variances[x + 1] = overall_stdev_variances[x]

    return mean_prices, mean_variances, stdev_variances

# Give our opinion on if the price is good enough to buy
def determine_opinion(upswing, weather_from, weather_to):
    # Highest level threats
    if weather_from['main'] in opinions_options:
        return opinions_options[weather_from['main']]

    if weather_to['main'] in opinions_options:
        return opinions_options[weather_to['main']]

    if upswing:
        return opinions[0]

    return opinions[2]

def get_final_data(depart, arrival, sample_size_cap, distance_cap):
    return_data = {}

    depart_code = ''
    arrival_code = ''

    output = []

    if depart in city_codes and arrival in city_codes: # If function found correct IATA codes from city names
        depart_code = city_codes[depart][0]
        arrival_code = city_codes[arrival][0]

        route_data = get_flight_data(depart_code, arrival_code) # Gets the user's requested flight data

        if not route_data: # If nothing is found by using the codes, use the cities names instead
            route_data = get_flight_data(depart, arrival)
    else:
        route_data = get_flight_data(depart, arrival) # Try to get flight data by city name instead of IATA codes

    if route_data: # Finally, if some flight data was found
        price_from = 0
        price_to = 0

        predicted_price = 0
        lower_bound = 0
        upper_bound = 0

        surrounding_flights_data = []

        # Gets codes of nearby cities
        cities1 = get_all_codes(get_airports_near(depart, distance_cap))[:sample_size_cap]
        cities2 = get_all_codes(get_airports_near(arrival, distance_cap))[:sample_size_cap]

        # Gathers all flight data for nearby cities
        for city1 in cities1:
            for city2 in cities2:
                if city1 != city2:
                    result = get_flight_data(city1, city2)

                    if result:
                        surrounding_flights_data.append(result)

        # Gets the mean price and variances of the flights of surrounding cities, and also the standard deviations of each months' variance
        mean_prices, mean_variances, stdev_variances = get_stats(surrounding_flights_data, route_data)

        today = date.today()
        month_index = date.today().month # An index of 3 means from March to April

        # Instead of a single trendline, this uses a linear trend from month to month (15th to 15th)
        if today.day < 15:
            month_index = month_index - 1 if month_index > 1 else 12

        predicted_variance = mean_variances[month_index]

        # Based on the progress through the cycle (middle of each month), it picks the months
        month_from = list(months.keys())[month_index - 1]
        month_to = list(months.keys())[month_index]

        if month_index in route_data[2]:
            price_from = route_data[2][month_index]
        elif month_index in mean_prices: # Uses average price from nearby cities if nothing is found
            price_from = mean_prices[month_index]
        else:
            return_data['success'] = False
            return_data['error_message'] = 'Not enough data available (E01-1)'

            return return_data

        if month_index + 1 in route_data[2]:
            price_to = route_data[2][month_index + 1]
        elif month_index + 1 in mean_prices: # Uses average price from nearby cities if nothing is found
            price_to = mean_prices[month_index + 1]
        else:
            return_data['success'] = False
            return_data['error_message'] = 'Not enough data available (E01-2)'

            return return_data

        # Calculates progress into the cycle
        days_into_cycle = (today - date(2020, month_index, 15)).days

        # Gets the standard deviation from the correct month
        stdev = stdev_variances[month_index]

        # Generates a confidence interval for the predicted price
        predicted_price = round(price_from * (1 + (days_into_cycle * predicted_variance) / 30), 2)
        bound1 = round(price_from * (1 + (days_into_cycle * (predicted_variance - stdev)) / 30), 2)
        bound2 = upper_bound = round(price_from * (1 + (days_into_cycle * (predicted_variance + stdev)) / 30), 2)

        if bound1 > bound2:
            lower_bound = bound2
            upper_bound = bound1
        else:
            lower_bound = bound1
            upper_bound = bound2

        weather_from = get_weather_data(depart)
        weather_to = get_weather_data(arrival)

        # Outputs to console
        output.append(depart + ": " + str(cities1))
        output.append(arrival + ': ' + str(cities2) + '\n')

        output.append("Route variances: " + str(stdev_variances) + '\n')

        output.append(month_from + ": $" + str(price_from))
        output.append(month_to + ": $" + str(price_to))
        output.append('Days: ' + str(days_into_cycle) + '/30 \n')

        output.append("Predicted values: ")
        output.append('\tVariance: ' + str(predicted_variance))
        output.append('\tStandard Deviation: ' + str(stdev))
        output.append('\tPrice: $' + str(predicted_price))

        output.append('\n' + str(weather_from))
        output.append(str(weather_to))

        # Formats return data
        return_data['success'] = True
        return_data['cities'] = (depart, arrival)
        return_data['confidence_interval'] = {
            'lower_bound': '{:.2f}'.format(lower_bound if lower_bound > 0 else 0),
            'predicted_price': '{:.2f}'.format(predicted_price),
            'upper_bound': '{:.2f}'.format(upper_bound)
        }
        return_data['weather'] = {
            'from': weather_from,
            'to': weather_to
        }
        return_data['opinion'] = determine_opinion(predicted_variance < 0 and days_into_cycle < 25, weather_from, weather_to)
    else:
        return_data['success'] = False
        return_data['error_message'] = 'Could not find data on specified cities (E02)'

        return return_data

    print('\n' + '\n'.join(output) + '\n')

    return return_data