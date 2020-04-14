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

city_codes = {'aarhus': ['AAR'], 'abadan': ['ABD'], 'abeche': ['AEH'], 'aberdeen': ['ABZ', 'ABR'], 'abidjan': ['ABJ'], 'abilene': ['ABI'], 'abu dhabi': ['AUH'], 'abuja': ['ABV'], 'abu rudeis': ['AUE'], 'abu simbel': ['ABS'], 'acapulco': ['ACA'], 'accra': ['ACC'], 'adana': ['ADA'], 'addis ababa': ['ADD'], 'adelaide': ['ADL'], 'aden': ['ADE'], 'adiyaman': ['ADF'], 'adler/sochi': ['AER'], 'agades': ['AJY'], 'agadir': ['AGA'], 'agana': ['SUM'], 'aggeneys': ['AGZ'], 'aguadilla': ['BQN'], 'aguascaliente': ['AGU'], 'ahmedabad': ['AMD'], 'aiyura': ['AYU'], 'ajaccio': ['AJA'], 'akita': ['AXT'], 'akron': ['CAK'], 'akrotiri': ['AKT'], 'al ain': ['AAN'], 'al arish': ['AAC'], 'albany': ['ALH', 'ABY', 'ALB'], 'albi': ['LBI'], 'alborg': ['AAL'], 'albuquerque': ['ABQ'], 'albury': ['ABX'], 'alderney': ['ACI'], 'aleppo': ['ALP'], 'alesund': ['AES'], 'alexander bay': ['ALJ'], 'alexandria': ['HBH', 'ALY', 'ESF'], 'alfujairah': ['FJR'], 'alghero sassari': ['AHO'], 'algiers, houari boumediene airport': ['ALG'], 'al hoceima': ['AHU'], 'alicante': ['ALC'], 'alice springs': ['ASP'], 'alldays': ['ADY'], 'allentown': ['ABE'], 'almaty': ['ALA'], 'almeria': ['LEI'], 'alta': ['ALF'], 'altay': ['AAT'], 'altenrhein': ['ACH'], 'altoona': ['AOO'], 'altus': ['AXS'], 'amami': ['ASJ'], 'amarillo': ['AMA'], 'amazon bay': ['AZB'], 'amman': ['AMM', 'ADJ'], 'amritsar': ['ATQ'], 'amsterdam': ['AMS'], 'anand': ['QNB'], 'anchorage': ['ANC'], 'ancona': ['AOI'], 'andorra la vella': ['ALV'], 'anguilla': ['AXA'], 'anjouan': ['AJN'], 'ankara': ['ANK', 'ESB'], 'annaba': ['AAE'], 'ann arbor': ['ARB'], 'annecy': ['NCY'], 'anniston': ['ANB'], 'antalya': ['AYT'], 'antananarivo': ['TNR'], 'antigua, v.c. bird international': ['ANU'], 'antwerp': ['ANR'], 'aomori': ['AOJ'], 'apia': ['APW'], 'appelton/neenah/menasha': ['ATW'], 'aqaba': ['AQJ'], 'aracaju': ['AJU'], 'arkhangelsk': ['ARH'], 'arusha': ['ARK'], 'araxos': ['GPA'], 'arlit': ['RLT'], 'arrecife/lanzarote': ['ACE'], 'aruba': ['AUA'], 'asheville': ['AVL'], 'ashgabat': ['ASB'], 'asmara': ['ASM'], 'aspen,': ['ASE'], 'assiut': ['ATZ'], 'astana': ['TSE'], 'asuncion': ['ASU'], 'aswan': ['ASW'], 'athens': ['ATH', 'AHN', 'ATO'], 'athens, hellinikon airport': ['HEW'], 'atlanta': ['ATL'], 'atlantic city': ['ACY'], 'attawapiskat, nt': ['YAT'], 'auckland': ['AKL'], 'augsburg': ['AGB'], 'augusta': ['AGS', 'AUG'], 'aurillac': ['AUR'], 'austin': ['AUS'], 'ayawasi': ['AYW'], 'ayers rock': ['AYQ'], 'ayr': ['AYR'], 'badajoz': ['BJZ'], 'bagdad': ['BGW'], 'bagdogra': ['IXB'], 'bahamas': ['NAS'], 'bahawalpur': ['BHV'], 'bahrain': ['BAH'], 'bakersfield': ['BFL'], 'baku': ['BAK'], 'ballina': ['BNK'], 'baltimore': ['BWI'], 'bamaga': ['ABM'], 'bamako': ['BKO'], 'bambari': ['BBY'], 'bandar seri begawan': ['BWN'], 'bandung': ['BDO'], 'bangalore': ['BLR'], 'bangassou': ['BGU'], 'bangkok, don muang': ['DMK'], 'bangkok, suvarnabhumi international': ['BKK'], 'bangor': ['BGR'], 'bangui': ['BGF'], 'banjul': ['BJL'], 'bannu': ['BNP'], 'barcelona': ['BCN', 'BLA'], 'bardufoss': ['BDU'], 'bari': ['BRI'], 'barisal': ['BZL'], 'baroda': ['BDQ'], 'barra': ['BRR'], 'barranquilla': ['BAQ'], 'basel': ['BSL'], 'basel/mulhouse': ['EAP'], 'basra, basrah': ['BSR'], 'basse': ['PTP'], 'basseterre': ['SKB'], 'bastia': ['BIA'], 'baton rouge': ['BTR'], 'bayreuth': ['BYU'], 'beaumont/pt. arthur': ['BPT'], 'beckley': ['BKW'], 'beef island': ['EIS'], 'beijing': ['PEK', 'NAY'], 'beira': ['BEW'], 'beirut': ['BEY'], 'belem': ['BEL'], 'belfast': ['BHD', 'BFS'], 'belgaum': ['IXG'], 'belgrad': ['BEG'], 'belize city': ['BZE'], 'bellingham': ['BLI'], 'belo horizonte': ['CNF'], 'bemidji': ['BJI'], 'benbecula': ['BEB'], 'benghazi': ['BEN'], 'benguela': ['BUG'], 'benton harbour': ['BEH'], 'berberati': ['BBT'], 'bergamo/milan': ['BGY'], 'bergen': ['BGO'], 'bergerac': ['EGC'], 'berlin': ['BER'], 'berlin, schoenefeld': ['SXF'], 'berlin, tegel': ['TXL'], 'berlin, tempelhof': ['THF'], 'bermuda': ['BDA'], 'berne, bern': ['BRN'], 'berne, railway service': ['ZDJ'], 'bethel': ['BET'], 'bhopal': ['BHO'], 'bhubaneswar': ['BBI'], 'biarritz': ['BIQ'], 'bilbao': ['BIO'], 'billings': ['BIL'], 'billund': ['BLL'], 'bintulu': ['BTU'], 'biraro': ['IRO'], 'birmingham': ['BHX', 'BHM'], 'bishkek': ['FRU'], 'bismarck': ['BIS'], 'bissau': ['BXO'], 'blackpool': ['BLK'], 'blackwater': ['BLT'], 'blantyre': ['BLZ'], 'blenheim': ['BHE'], 'bloemfontein': ['BFN'], 'bloomington': ['BMI', 'BMG'], 'bluefield': ['BLF'], 'boa vista': ['BVB'], 'bobo/dioulasso': ['BOY'], 'bodo': ['BOO'], 'bodrum': ['BJV'], 'bogota': ['BOG'], 'boise': ['BOI'], 'bologna': ['BLQ'], 'bombay': ['BOM'], 'bonaire': ['BON'], 'bonaventure, pq': ['YVB'], 'bora bora': ['BOB'], 'bordeaux': ['BOD'], 'borrego springs': ['BXS'], 'boston': ['BOS'], 'bouake': ['BYK'], 'bourgas/burgas': ['BOJ'], 'bournemouth': ['BOH'], 'bowen': ['ZBO'], 'bozeman': ['BZN'], 'bradford/warren': ['BFD'], 'brainerd': ['BRD'], 'brampton island': ['BMP'], 'brasilia': ['BSB'], 'bratislava': ['BTS'], 'brazzaville': ['BZV'], 'bremen': ['BRE'], 'brescia, montichiari': ['VBS'], 'brest': ['BES'], 'bria': ['BIV'], 'bridgeport': ['BDR'], 'bridgetown': ['BGI'], 'brindisi': ['BDS'], 'brisbane': ['BNE'], 'bristol': ['BRS'], 'broennoeysund': ['BNN'], 'broken hill': ['BHQ'], 'brookings': ['BKX'], 'broome': ['BME'], 'brunswick': ['BQK'], 'brussels': ['BRU'], 'bucaramanga': ['BGA'], 'bucharest': ['BUH', 'OTP'], 'budapest': ['BUD'], 'buenos aires': ['BUE'], 'buenos aires, ezeiza international airport': ['EZE'], 'buenos aires, jorge newbery': ['AEP'], 'buffalo range': ['BFO'], 'buffalo/niagara falls': ['BUF'], 'bujumbura': ['BJM'], 'bulawayo': ['BUQ'], 'bullhead city': ['BHC'], 'bundaberg': ['BDB'], 'burbank': ['BUR'], 'burlington ia': ['BRL'], 'burlington': ['BTV'], 'burnie': ['BWT'], 'butte': ['BTM'], 'cabinda': ['CAB'], 'cagliari': ['CAG'], 'cairns': ['CNS'], 'cairo': ['CAI'], 'calama': ['CJC'], 'calcutta': ['CCU'], 'calgary': ['YYC'], 'cali': ['CLO'], 'calicut': ['CCJ'], 'calvi': ['CLY'], 'cambridge bay': ['YCB'], 'cambrigde': ['CBG'], 'campbeltown': ['CAL'], 'campo grande': ['CGR'], 'canberra': ['CBR'], 'cancun': ['CUN'], 'cannes – mandelieu airport': ['CEQ'], 'canouan': ['CIW'], 'cape town': ['CPT'], 'caracas': ['CCS'], 'cardiff': ['CWL'], 'carlsbad': ['CLD'], 'carnarvon': ['CVQ'], 'carnot': ['CRF'], 'carson city': ['CSN'], 'casablanca': ['CAS'], 'casablanca, mohamed v': ['CMN'], 'casa de campo': ['LRM'], 'casino': ['CSI'], 'casper': ['CPR'], 'castaway': ['CST'], 'cartagena': ['CTG'], 'castries': ['SLU'], 'catania': ['CTA'], 'cayenne': ['CAY'], 'cottbus': ['CBU'], 'cebu city': ['CEB'], 'cedar city': ['CDC'], 'cedar rapids ia': ['CID'], 'ceduna': ['CED'], 'cessnock': ['CES'], 'chabarovsk': ['KHV'], 'chambery': ['CMF'], 'champaign': ['CMI'], 'chandigarh': ['IXC'], 'changchun': ['CGQ'], 'chania': ['CHQ'], 'chaoyang, beijing': ['CHG'], 'charleston': ['CHS', 'CRW'], 'charlotte': ['CLT'], 'charlottesville': ['CHO'], 'charters towers': ['CXT'], 'chattanooga': ['CHA'], 'chengdu': ['CTU'], 'chennai': ['MAA'], 'cheyenne': ['CYS'], 'chiang mai': ['CNX'], 'chiba city': ['QCB'], 'chicago': ['MDW', 'ORD', 'CHI'], 'chichen itza': ['CZA'], 'chico': ['CIC'], 'chihuahua': ['CUU'], 'chios': ['JKH'], 'chipata': ['CIP'], 'chisinau': ['KIV'], 'chita': ['HTA'], 'sapporo': ['CTS', 'SPK', 'OKD', 'CTS'], 'chitral': ['CJL'], 'chittagong': ['CGP'], 'chongqing': ['CKG'], 'christchurch': ['CHC'], 'chub cay': ['CCZ'], 'churchill': ['YYQ'], 'cienfuegos': ['CFG'], 'cincinnati': ['CVG'], 'ciudad del carmen': ['CME'], 'ciudad guayana': ['CGU'], 'ciudad juarez': ['CJS'], 'ciudad obregon': ['CEN'], 'ciudad victoria': ['CVM'], 'clarksburg': ['CKB'], 'clermont': ['CMQ'], 'clermont ferrand': ['CFE'], 'cleveland': ['BKL', 'CLE'], 'cochabamba': ['CBB'], 'cochin': ['COK'], 'cody/powell/yellowstone': ['COD'], 'coffmann cove': ['KCC'], 'coffs harbour': ['CFS'], 'coimbatore': ['CJB'], 'colima': ['CLQ'], 'college station/bryan': ['CLL'], 'collinsville': ['KCE'], 'cologne': ['CGN'], 'colombo': ['CMB'], 'colorado springs': ['COS'], 'columbia': ['CAE'], 'columbus': ['CSG', 'CMH'], 'conakry': ['CKY'], 'concord': ['CCR', 'CON'], 'constantine': ['CZL'], 'constanta': ['CND'], 'coober pedy': ['CPD'], 'cooktown': ['CTN'], 'cooma': ['OOM'], 'copenhagen': ['CPH'], 'cordoba': ['COR', 'ODB'], 'cordova': ['CDV'], 'corfu': ['CFU'], 'cork': ['ORK'], 'corpus christi': ['CRP'], 'cotonou': ['COO'], 'coventry': ['CVT'], 'cozmel': ['CZM'], 'craig': ['CGA'], 'crescent city': ['CEC'], 'cuiaba': ['CGB'], 'culiacan': ['CUL'], 'curacao': ['CUR'], 'curitiba': ['CWB'], 'cuyo': ['CYU'], 'dakar': ['DKR'], 'dalaman': ['DLM'], 'dalby': ['DBY'], 'dalian': ['DLC'], 'dallas': ['DAL'], 'dallas/ft. worth': ['DFW'], 'daloa': ['DJO'], 'damascus, international': ['DAM'], 'dammam, king fahad international': ['DMM'], 'danville': ['DAN'], 'dar es salam': ['DAR'], 'darwin': ['DRW'], 'daydream island': ['DDI'], 'dayton': ['DAY'], 'daytona beach': ['DAB'], 'decatur': ['DEC'], 'deer lake/corner brook': ['YDF'], 'delhi': ['DEL'], 'den haag': ['HAG'], 'denizli': ['DNZ'], 'denpasar/bali': ['DPS'], 'denver': ['DEN'], 'dera ismail khan': ['DSK'], 'derby': ['DRB'], 'derry': ['LDY'], 'des moines': ['DSM'], 'detroit': ['DET', 'DTW', 'DTT'], 'devils lake': ['DVL'], 'devonport': ['DPO'], 'dhahran': ['DHA'], 'dhaka': ['DAC'], 'dili': ['DIL'], 'dillingham': ['DLG'], 'dinard': ['DNR'], 'disneyland paris': ['DLP'], 'djerba': ['DJE'], 'djibouti': ['JIB'], 'dodoma': ['DOD'], 'doha': ['DOH'], 'doncaster/sheffield, robin hood international airport': ['DSA'], 'donegal': ['CFN'], 'dortmund': ['DTM'], 'dothan': ['DHN'], 'douala': ['DLA'], 'dresden': ['DRS'], 'dubai': ['DXB'], 'dubbo': ['DBO'], 'dublin': ['DUB'], 'dubois': ['DUJ'], 'dubrovnik': ['DBV'], 'dubuque ia': ['DBQ'], 'duesseldorf': ['DUS'], 'duluth': ['DLH'], 'dundee': ['DND'], 'dunedin': ['DUD'], 'dunk island': ['DKI'], 'durango': ['DRO'], 'durban': ['DUR'], 'dushanbe': ['DYU'], 'dutch harbor': ['DUT'], 'dysart': ['DYA'], 'dzaoudzi': ['DZA'], 'east london': ['ELS'], 'easter island': ['IPC'], 'eau clarie': ['EAU'], 'edinburgh': ['EDI'], 'edmonton': ['YEA'], 'edmonton, international': ['YEG'], 'edmonton, municipal': ['YXD'], 'egilsstadir': ['EGS'], 'eindhoven': ['EIN'], 'samana': ['AZS'], 'elba island, marina di campo': ['EBA'], 'elat': ['ETH'], 'elat, ovula': ['VDA'], 'elkhart': ['EKI'], 'elko': ['EKO'], 'ellisras': ['ELL'], 'el minya': ['EMY'], 'elmira': ['ELM'], 'el paso': ['ELP'], 'ely': ['ELY'], 'emerald': ['EDR', 'EMD'], 'enontekioe': ['ENF'], 'entebbe': ['EBB'], 'erfurt': ['ERF'], 'erie': ['ERI'], 'eriwan': ['EVN'], 'erzincan': ['ERC'], 'erzurum': ['ERZ'], 'esbjerg': ['EBJ'], 'escanaba': ['ESC'], 'esperance': ['EPR'], 'eugene': ['EUG'], 'eureka': ['ACV'], 'evansville': ['EVV'], 'evenes': ['EVE'], 'exeter': ['EXT'], 'fairbanks': ['FAI'], 'fair isle': ['FIE'], 'faisalabad': ['LYP'], 'fargo': ['FAR'], 'farmington': ['FMN'], 'faro': ['FAO'], 'faroer': ['FAE'], 'fayetteville': ['FYV'], 'fayetteville/ft. bragg': ['FAY'], 'fes': ['FEZ'], 'figari': ['FSC'], 'flagstaff': ['FLG'], 'flin flon': ['YFO'], 'flint': ['FNT'], 'florence': ['FLR', 'FLO'], 'florianopolis': ['FLN'], 'floro': ['FRO'], 'fort albert': ['YFA'], 'fortaleza': ['FOR'], 'fort de france': ['FDF'], 'fort dodge ia': ['FOD'], 'fort huachuca/sierra vista': ['FHU'], 'fort lauderdale/hollywood': ['FLL'], 'fort mcmurray': ['YMM'], 'fort myers, metropolitan area': ['FMY'], 'fort myers, southwest florida reg': ['RSW'], 'fort riley': ['FRI'], 'fort smith': ['YSM', 'FSM'], 'fort st. john': ['YXJ'], 'fort walton beach': ['VPS'], 'fort wayne': ['FWA'], 'fort worth': ['DFW'], 'foula': ['FOU'], 'francistown': ['FRW'], 'frankfurt/main': ['FRA'], 'frankfurt/hahn': ['HHN'], 'franklin/oil city': ['FKL'], 'fredericton': ['YFC'], 'freeport': ['FPO'], 'freetown': ['FNA'], 'frejus': ['FRJ'], 'fresno': ['FAT'], 'friedrichshafen': ['FDH'], 'fuerteventura': ['FUE'], 'fujairah, international airport': ['FJR'], 'fukuoka': ['FUK'], 'fukushima': ['FKS'], 'funchal': ['FNC'], 'futuna': ['FUT'], 'gaborone': ['GBE'], 'gadsden': ['GAD'], 'gainesville': ['GNV'], 'galway': ['GWY'], 'gander': ['YQX'], 'garoua': ['GOU'], 'gaza city': ['GZA'], 'gaziantep': ['GZT'], 'gdansk': ['GDN'], 'geelong': ['GEX'], 'geneva': ['GVA'], 'genoa': ['GOA'], 'george': ['GRJ'], 'georgetown': ['GEO'], 'geraldton': ['GET'], 'gerona': ['GRO'], 'ghent': ['GNE'], 'gibraltar': ['GIB'], 'gilette': ['GCC'], 'gilgit': ['GIL'], 'gillam': ['YGX'], 'gladstone': ['GLT'], 'glasgow, prestwick': ['PIK'], 'glasgow': ['GLA', 'GGW'], 'glendive': ['GDV'], 'goa': ['GOI'], 'goiania, santa genoveva airport': ['GYN'], 'gold coast': ['OOL'], 'goondiwindi': ['GOO'], 'goose bay': ['YYR'], 'gorna': ['GOZ'], 'gothenburg': ['GOT'], 'gove': ['GOV'], 'govenors harbour': ['GHB'], 'granada': ['GRX'], 'grand bahama international': ['FPO'], 'grand canyon': ['GCN'], 'grand cayman': ['GCM'], 'grand forks': ['GFK'], 'grand junction': ['GJT'], 'grand rapids': ['GRR', 'GPZ'], 'graz': ['GRZ'], 'great falls': ['GTF'], 'great keppel island': ['GKL'], 'green bay': ['GRB'], 'greenbrier/lewisburg': ['LWB'], 'greensboro/winston salem': ['GSO'], 'greenville': ['GLH', 'PGV'], 'greenville/spartanburg': ['GSP'], 'grenada': ['GND'], 'grenoble': ['GNB'], 'griffith': ['GFF'], 'groningen': ['GRQ'], 'groote eylandt': ['GTE'], 'groton/new london': ['GON'], 'guadalajara': ['GDL'], 'guadalcanal': ['GSI'], 'guam': ['GUM'], 'guangzhou': ['CAN'], 'sao paulo': ['GRU', 'SAO', 'CGH', 'GRU', 'VCP'], 'guatemala city': ['GUA'], 'guayaquil': ['GYE'], 'guernsey': ['GCI'], 'guettin': ['GTI'], 'gulfport/biloxi': ['GPT'], 'guilin': ['KWL'], 'gulu': ['ULU'], 'gunnison/crested butte': ['GUC'], 'guwahati': ['GAU'], 'gwadar': ['GWD'], 'gweru': ['GWE'], 'gympie': ['GYP'], 'hachijo jima': ['HAC'], 'hagåtña': ['GUM'], 'haifa': ['HFA'], 'haines': ['HNS'], 'hakodate': ['HKD'], 'halifax international': ['YHZ'], 'hall beach': ['YUX'], 'hamburg': ['HAM'], 'hamilton': ['HLT', 'YHM', 'HLZ'], 'hamilton island': ['HTI'], 'hammerfest': ['HFT'], 'hancock': ['CMX'], 'hangchow': ['HGH'], 'hannover': ['HAJ'], 'hanoi': ['HAN'], 'harare': ['HRE'], 'harbin': ['HRB'], 'harlingen/south padre island': ['HRL'], 'harrington harbour, pq': ['YHR'], 'harrisburg': ['HAR', 'MDT'], 'hartford': ['BDL'], 'hatyai': ['HDY'], 'haugesund': ['HAU'], 'havana': ['HAV'], 'havre': ['HVR'], 'hayman island': ['HIS'], 'helena': ['HLN'], 'helsingborg': ['JHE'], 'helsinki': ['HEL'], 'heraklion': ['HER'], 'hermosillo': ['HMO'], 'hervey bay': ['HVB'], 'hibbing': ['HIB'], 'hickory': ['HKY'], 'hilo': ['ITO'], 'hilton head island': ['HHH'], 'hinchinbrook island': ['HNK'], 'hiroshima international': ['HIJ'], 'ho chi minh city': ['SGN'], 'hobart': ['HBA'], 'hof': ['HOQ'], 'holguin': ['HOG'], 'home hill': ['HMH'], 'homer': ['HOM'], 'hong kong': ['HKG', 'ZJK'], 'honiara henderson international': ['HIR'], 'honolulu': ['HNL'], 'hoonah': ['HNH'], 'horta': ['HOR'], 'houston': ['HOU'], 'houston, tx': ['IAH'], 'huahine': ['HUH'], 'huatulco': ['HUX'], 'hue': ['HUI'], 'humberside': ['HUY'], 'huntington': ['HTS'], 'huntsville': ['HSV'], 'hurghada international': ['HRG'], 'huron': ['HON'], 'hwange national park': ['HWN'], 'hyannis': ['HYA'], 'hydaburg': ['HYG'], 'hyderabad': ['HYD', 'HDD'], 'ibiza': ['IBZ'], 'idaho falls': ['IDA'], 'iguazu, cataratas': ['IGR'], 'ile des pins': ['ILP'], 'ile ouen': ['IOU'], 'iliamna': ['ILI'], 'imperial': ['IPL'], 'incercargill': ['IVC'], 'incheon, incheon international airport': ['ICN'], 'indianapolis': ['IND'], 'ingham': ['IGH'], 'innisfail': ['IFL'], 'innsbruck': ['INN'], 'international falls': ['INL'], 'inuvik': ['YEV'], 'invercargill': ['IVC'], 'inverness': ['INV'], 'inykern': ['IYK'], 'iqaluit': ['YFB'], 'iquitos': ['IQT'], 'irkutsk': ['IKT'], 'ishigaki': ['ISG'], 'islamabad': ['ISB'], 'islay': ['ILY'], 'isle of man': ['IOM'], 'istanbul': ['IST', 'SAW'], 'ithaca/cortland': ['ITH'], 'ivalo': ['IVL'], 'ixtapa/zihuatenejo': ['ZIH'], 'izmir': ['IZM', 'ADB'], 'jackson hole': ['JAC', 'JAC'], 'jackson': ['JXN', 'JAN', 'HKS', 'MKL'], 'jackson, \xa0mn': ['MJQ'], 'jacksonville': ['LRF', 'NZC', 'NIP', 'JAX', 'CRG', 'IJX', 'OAJ', 'JKV'], 'jacmel': ['JAK'], 'jacobabad': ['JAG'], 'jacobina': ['JCM'], 'jacquinot bay': ['JAQ'], 'jaffna': ['JAF'], 'jagdalpur': ['JGB'], 'jaipur': ['JAI'], 'jaisalmer': ['JSA'], 'jakarta': ['HLP', 'JKT', 'CGK'], 'jalalabad': ['JAA'], 'jalandhar': ['JLR'], 'jalapa': ['JAL'], 'jales': ['JLS'], 'jaluit island': ['UIT'], 'jamba': ['JMB'], 'jambi': ['DJB'], 'jambol': ['JAM'], 'jamestown': ['JMS', 'JHW'], 'jammu': ['IXJ'], 'jamnagar': ['JGA'], 'jamshedpur': ['IXW'], 'janakpur': ['JKR'], 'jandakot': ['JAD'], 'janesville': ['JVL'], 'januaria': ['JNA'], 'jaque': ['JQE'], 'jatai': ['JTI'], 'jauja': ['JAU'], 'jayapura': ['DJJ'], 'jeddah': ['JED'], 'jefferson city': ['JEF'], 'jeremie': ['JEE'], 'jerez de la frontera/cadiz': ['XRY'], 'jersey': ['JER'], 'jerusalem': ['JRS'], 'jessore': ['JSR'], 'jeypore': ['PYB'], "ji'an": ['JGS'], 'jiamusi': ['JMU'], 'jiayuguan': ['JGN'], 'jijel': ['GJL'], 'jijiga': ['JIJ'], 'jilin': ['JIL'], 'jimma': ['JIM'], 'jinan': ['TNA'], 'jingdezhen': ['JDZ'], 'jinghong': ['JHG'], 'jining': ['JNG'], 'jinja': ['JIN'], 'jinjiang': ['JJN'], 'jinka': ['BCO'], 'jinzhou': ['JNZ'], 'jipijapa': ['JIP'], 'jiri': ['JIR'], 'jiujiang': ['JIU'], 'jiwani': ['JIW'], 'joacaba': ['JCB'], 'joao pessoa': ['JPA'], 'jodhpur': ['JDH'], 'jönköping': ['JKG'], 'joensuu': ['JOE'], 'johannesburg': ['JNB'], 'johnson city': ['BGM'], 'johnston island': ['JON'], 'johnstown': ['JST'], 'johor bahru': ['JHB'], 'joinville': ['JOI'], 'jolo': ['JOL'], 'jomsom': ['JMO'], 'jonesboro': ['JBR'], 'joplin': ['JLN'], 'jorhat': ['JRH'], 'jos': ['JOS'], 'jose de san martin': ['JSM'], 'jouf': ['AJF'], 'juanjui': ['JJI'], 'juba': ['JUB'], 'juist': ['JUI'], 'juiz de fora': ['JDF'], 'jujuy': ['JUJ'], 'julia creek': ['JCK'], 'juliaca': ['JUL'], 'jumla': ['JUM'], 'jundah': ['JUN'], 'juneau': ['JNU'], 'junin': ['JNI'], 'juticalpa': ['JUT'], 'jwaneng': ['JWA'], 'jyväskylä': ['JYV'], 'kabul': ['KBL'], 'kagoshima': ['KOJ'], 'kahramanmaras': ['KCM'], 'kahului': ['OGG'], 'kajaani': ['KAJ'], 'kalamata': ['KLX'], 'kalamazoo/battle creek': ['AZO'], 'kalgoorlie': ['KGI'], 'kaliningrad': ['KGD'], 'kalispell': ['FCA'], 'kalmar': ['KLR'], 'kamloops, bc': ['YKA'], 'kamuela': ['MUE'], 'kano': ['KAN'], 'kanpur': ['KNU'], 'kansas city': ['MCI'], 'kaohsiung international': ['KHH'], 'kapalua west': ['JHM'], 'karachi': ['KHI'], 'karlsruhe': ['FKB'], 'karlstad': ['KSD'], 'karpathos': ['AOK'], 'karratha': ['KTA'], 'kars': ['KYS'], 'karumba': ['KRB'], 'karup': ['KRP'], 'kaschechawan, pq': ['ZKE'], 'kassala': ['KSL'], 'katherine': ['KTR'], 'kathmandu': ['KTM'], 'katima mulilo/mpacha': ['MPA'], 'kauhajoki': ['KHJ'], 'kaunakakai': ['MKK'], 'kavalla': ['KVA'], 'kayseri': ['ASR'], 'kazan': ['KZN'], 'keetmanshoop': ['KMP'], 'kelowna, bc': ['YLW'], 'kemi/tornio': ['KEM'], 'kenai': ['ENA'], 'kent': ['MSE'], 'kerry county': ['KIR'], 'ketchikan': ['KTN'], 'key west': ['EYW'], 'khamis mushayat': ['AHB'], 'kharga': ['UVL'], 'kharkov': ['HRK'], 'khartoum': ['KRT'], 'khuzdar': ['KDD'], 'kiel': ['KEL'], 'kiev': ['KBP', 'IEV'], 'kigali': ['KGL'], 'kilimadjaro': ['JRO'], 'killeem': ['ILE'], 'kimberley': ['KIM'], 'king island': ['KNS'], 'king salomon': ['AKN'], 'kingscote': ['KGC'], 'kingston': ['KIN', 'ISO'], 'kingstown': ['SVD'], 'kinshasa': ['FIH'], 'kiritimati': ['CXI'], 'kirkenes': ['KKN'], 'kirkuk': ['KIK'], 'kirkwall': ['KOI'], 'kiruna': ['KRN'], 'kisangani': ['FKI'], 'kittilä': ['KTT'], 'kitwe': ['KIW'], 'klagenfurt': ['KLU'], 'klamath fall': ['LMT'], 'klawock': ['KLW'], 'kleinsee': ['KLZ'], 'knock': ['NOC'], 'knoxville': ['TYS'], 'kobe': ['UKB'], 'kochi': ['KCZ'], 'köln, köln/bonn': ['CGN'], 'kodiak': ['ADQ'], 'kohat': ['OHT'], 'kokkola/pietarsaari': ['KOK'], 'kolkata': ['CCU'], 'komatsu': ['KMQ'], 'kona': ['KOA'], 'konya': ['KYA'], 'korhogo': ['HGO'], 'kos': ['KGS'], 'kota kinabalu': ['BKI'], 'kotzbue': ['OTZ'], 'kowanyama': ['KWM'], 'krakow': ['KRK'], 'kristiansand': ['KRS'], 'kristianstad': ['KID'], 'kristiansund': ['KSU'], 'kuala lumpur': ['KUL', 'SZB'], 'kuantan': ['KUA'], 'kuching': ['KCH'], 'kumamoto': ['KMJ'], 'kununurra': ['KNX'], 'kuopio': ['KUO'], 'kushiro': ['KUH'], 'kuujjuaq': ['YVP'], 'kuujjuarapik': ['YGW'], 'kuusamo': ['KAO'], 'kuwait': ['KWI'], 'kyoto': ['UKY'], 'labe': ['LEK'], 'labouchere bay': ['WLB'], 'labuan': ['LBU'], 'lac brochet, mb': ['XLB'], 'la coruna': ['LCG'], 'la crosse': ['LSE'], 'lae': ['LAE'], 'la rochelle': ['LRH'], 'lafayette': ['LAF'], 'lafayette, la': ['LFT'], 'lagos': ['LOS'], 'la grande': ['YGL'], 'lahore': ['LHE'], 'lake charles': ['LCH'], 'lake havasu city': ['HII'], 'lake tahoe': ['TVL'], 'lakselv': ['LKL'], 'lambarene': ['LBQ'], 'lamezia terme': ['SUF'], 'lampedusa': ['LMP'], 'lanai city': ['LNY'], 'lancaster': ['LNS'], "land's end": ['LEQ'], 'langkawi': ['LGK'], 'lannion': ['LAI'], 'lanseria': ['HLA'], 'lansing': ['LAN'], 'la paz': ['LPB', 'LAP'], 'lappeenranta': ['LPP'], 'laramie': ['LAR'], 'laredo': ['LRD'], 'larnaca': ['LCA'], 'las palmas': ['LPA'], 'las vegas': ['LAS'], 'latrobe': ['LBE'], 'launceston': ['LST'], 'laurel/hattisburg': ['PIB'], 'laverton': ['LVO'], 'lawton': ['LAW'], 'lazaro cardenas': ['LZC'], 'leaf rapids': ['YLR'], 'learmouth': ['LEA'], 'lebanon': ['LEB'], 'leeds/bradford': ['LBA'], 'leinster': ['LER'], 'leipzig': ['LEJ'], 'lelystad': ['LEY'], 'leon': ['BJX'], 'leonora': ['LNO'], 'lerwick/tingwall': ['LWK'], 'lewiston': ['LWS'], 'lewistown': ['LWT'], 'lexington': ['LEX'], 'libreville': ['LBV'], 'lidkoeping': ['LDK'], 'liege': ['LGG'], 'lifou': ['LIF'], 'lihue': ['LIH'], 'lille': ['LIL'], 'lilongwe': ['LLW'], 'lima': ['LIM'], 'limassol': ['QLI'], 'limoges': ['LIG'], 'lincoln': ['LNK'], 'lindeman island': ['LDC'], 'linz': ['LNZ'], 'lisala': ['LIQ'], 'lisbon': ['LIS'], 'lismore': ['LSY'], 'little rock': ['LIT'], 'liverpool': ['LPL'], 'lizard island': ['LZR'], 'ljubljana': ['LJU'], 'lockhart river': ['IRG'], 'lome': ['LFW'], 'london': ['YXU', 'LCY', 'LGW', 'LHR', 'LTN', 'STN'], 'london metropolitan area': ['LON'], 'londonderry': ['LDY'], 'long beach': ['LGB'], 'long island': ['LIJ'], 'long island, islip': ['ISP'], 'longreach': ['LRE'], 'longview/kilgore': ['GGG'], 'longyearbyen': ['LYR'], 'loreto': ['LTO'], 'lorient': ['LRT'], 'los angeles': ['LAX'], 'los cabos': ['SJD'], 'los mochis': ['LMM'], 'los rodeos': ['TFN'], 'losinj': ['LSZ'], 'lourdes/tarbes': ['LDE'], 'louisville': ['SDF'], 'luanda': ['LAD'], 'lubbock': ['LBB'], 'lucknow': ['LKO'], 'luederitz': ['LUD'], 'luga': ['MLA'], 'lugano': ['LUG'], 'lulea': ['LLA'], 'lumbumbashi': ['FBM'], 'lusaka': ['LUN'], 'lusisiki': ['LUJ'], 'luxembourg': ['LUX'], 'luxi': ['LUM'], 'luxor': ['LXR'], 'lvov': ['LWO'], 'lydd': ['LYX'], 'lynchburg': ['LYH'], 'lyon': ['LYS'], 'lyons': ['LYO'], 'maastricht/aachen': ['MST'], 'macapa': ['MCP'], 'macau': ['MFM'], 'maceio': ['MCZ'], 'mackay': ['MKY'], 'macon': ['MCN'], 'mactan island': ['NOP'], 'madinah': ['MED'], 'madison': ['MSN'], 'madras': ['MAA'], 'madrid': ['MAD'], 'mahe': ['SEZ'], 'mahon': ['MAH'], 'maitland': ['MTL'], 'majunga': ['MJN'], 'makung': ['MZG'], 'malabo': ['SSG'], 'malaga': ['AGP'], 'malatya': ['MLX'], 'male': ['MLE'], 'malindi': ['MYD'], 'malmo': ['MMA', 'MMX'], 'man': ['MJC'], 'managua': ['MGA'], 'manaus': ['MAO'], 'manchester': ['MAN', 'MHT'], 'mandalay': ['MDL'], 'manguna': ['MFO'], 'manihi': ['XMH'], 'manila': ['MNL'], 'manzanillo': ['ZLO'], 'manzini': ['MTS'], 'maputo': ['MPM'], 'mar del plata': ['MDQ'], 'maracaibo': ['MAR'], 'maradi': ['MFQ'], 'maras': ['KCM'], 'marathon': ['MTH'], 'mardin': ['MQM'], 'mare': ['MEE'], 'margate': ['MGH'], 'margerita': ['PMV'], 'maribor': ['MBX'], 'mariehamn': ['MHQ'], 'maroua': ['MVR'], 'marquette': ['MQT'], 'marrakesh': ['RAK'], 'marsa alam': ['RMF'], 'marsa matrah': ['MUH'], 'marseille': ['MRS'], 'marsh harbour': ['MHH'], "martha's vineyard": ['MVY'], 'martinsburg': ['MRB'], 'maryborough': ['MBH'], 'maseru': ['MSU'], 'mason city ia': ['MCW'], 'masvingo': ['MVZ'], 'matsumoto, nagano': ['MMJ'], 'matsuyama': ['MYJ'], 'mattoon': ['MTO'], 'maun': ['MUB'], 'maupiti': ['MAU'], 'mauritius': ['MRU'], 'mayaguez': ['MAZ'], 'mazatlan': ['MZT'], 'mcallen': ['MFE'], 'medan': ['MES', 'KNO'], 'medellin': ['MDE'], 'medford': ['MFR'], 'medina': ['MED'], 'meekatharra': ['MKR'], 'melbourne': ['MEL', 'MLB'], 'melville hall': ['DOM'], 'memphis': ['MEM'], 'mendoza': ['MDZ'], 'manado': ['MDC'], 'merced': ['MCE'], 'merida': ['MID'], 'meridian': ['MEI'], 'merimbula': ['MIM'], 'messina': ['MEZ'], 'metlakatla': ['MTM'], 'metz': ['MZM'], 'metz/nancy metz': ['ETZ'], 'mexicali': ['MXL'], 'mexico city': ['MEX', 'AZP', 'MEX', 'NLU'], 'mfuwe': ['MFU'], 'miami': ['MIA'], 'mianwali': ['MWD'], 'middlemount': ['MMM'], 'midland/odessa': ['MAF'], 'midway island': ['MDY'], 'mikkeli': ['MIK'], 'milan': ['MIL', 'LIN', 'MXP', 'BGY'], 'mildura': ['MQL'], 'miles city': ['MLS'], 'milford sound': ['MFN'], 'milwaukee': ['MKE'], 'minatitlan': ['MTT'], 'mineralnye vody': ['MRV'], 'minneapolis': ['MSP'], 'minot': ['MOT'], 'minsk, international': ['MSQ'], 'miri': ['MYY'], 'mirpur': ['QML'], 'missula': ['MSO'], 'mitchell': ['MHE'], 'miyako jima': ['MMY'], 'miyazaki': ['KMI'], 'mkambati': ['MBM'], 'moanda': ['MFF'], 'mobile': ['MOB'], 'modesto': ['MOD'], 'moenjodaro': ['MJD'], 'mogadishu': ['MGQ'], 'mokuti': ['OKU'], 'moline/quad cities': ['MLI'], 'mombasa': ['MBA'], 'monastir': ['MIR'], 'moncton': ['YQM'], 'monroe': ['MLU'], 'monrovia': ['MLW', 'ROB'], 'montego bay': ['MBJ'], 'montenegro': ['QGF'], 'monterey': ['MRY'], 'monterrey': ['MTY', 'NTR'], 'montevideo': ['MVD'], 'montgomery': ['MGM'], 'montpellier': ['MPL'], 'montreal': ['YMQ', 'YUL', 'YMX'], 'montrose/tellruide': ['MTJ'], 'moorea': ['MOZ'], 'moranbah': ['MOV'], 'moree': ['MRZ'], 'morelia': ['MLM'], 'morgantown': ['MGW'], 'morioka, hanamaki': ['HNA'], 'moroni': ['HAH'], 'moruya': ['MYA'], 'moscow': ['MOW', 'DME', 'SVO', 'VKO'], 'moses lake': ['MWH'], 'mossel bay': ['MZY'], 'mostar': ['OMO'], 'mosul': ['OSM'], 'mouila': ['MJL'], 'moundou': ['MQQ'], 'mount cook': ['GTN'], 'mount gambier': ['MGB'], 'mount magnet': ['MMG'], 'mt. isa': ['ISA'], 'mt. mckinley': ['MCL'], 'muenchen': ['MUC'], 'muenster/osnabrueck': ['FMO'], 'mulhouse': ['MLH'], 'multan': ['MUX'], 'murcia': ['MJV'], 'murmansk': ['MMK'], 'mus': ['MSR'], 'muscat': ['MCT'], 'muscle shoals': ['MSL'], 'muskegon': ['MKG'], 'muzaffarabad': ['MFG'], 'mvengue': ['MVB'], 'mykonos': ['JMK'], 'myrtle beach': ['MYR', 'CRE'], 'mysore': ['MYQ'], 'mytilene': ['MJT'], 'mzamba': ['MZF'], 'nadi': ['NAN'], 'nagasaki': ['NGS'], 'nagoya': ['NGO'], 'nagpur': ['NAG'], 'nairobi': ['NBO'], 'nakhichevan': ['NAJ'], 'nakhon si thammarat': ['NST'], 'nancy': ['ENC'], 'nanisivik': ['YSR'], 'nanning': ['NNG'], 'nantes': ['NTE'], 'nantucket': ['ACK'], 'naples': ['NAP', 'APF'], 'narrabri': ['NAA'], 'narrandera': ['NRA'], 'narsarsuaq': ['UAK'], 'nashville': ['BNA'], 'nassau': ['NAS'], 'natal': ['NAT'], 'nausori': ['SUV'], 'nawab shah': ['WNS'], 'naxos': ['JNX'], "n'djamena": ['NDJ'], "n'dola": ['NLA'], 'nelson': ['NSN'], 'nelspruit': ['NLP', 'MQP'], 'nevis': ['NEV'], 'new bern': ['EWN'], 'new haven': ['HVN'], 'new orleans, la': ['MSY'], 'newquay': ['NQY'], 'new valley': ['UVL'], 'new york': ['JFK', 'LGA', 'EWR', 'NYC'], 'newburgh': ['SWF'], 'newcastle': ['BEO', 'NTL', 'NCL', 'NCS'], 'newman': ['ZNE'], 'newport news/williamsburg': ['PHF'], "n'gaoundere": ['NGE'], 'niagara falls international': ['IAG'], 'niamey': ['NIM'], 'nice': ['NCE'], 'nicosia': ['NIC'], 'nikolaev': ['NLV'], 'niigata': ['KIJ'], 'nimes': ['FNI'], 'nis': ['INI'], 'nizhny novgorod': ['GOJ'], 'nome': ['OME'], 'noosa': ['NSA'], 'norfolk island': ['NLK'], 'norfolk/virginia beach': ['ORF'], 'norman wells': ['YVQ'], 'norrkoeping': ['NRK'], 'north bend': ['OTH'], 'north eleuthera': ['ELH'], 'norwich': ['NWI'], 'nottingham': ['EMA'], 'nouadhibou': ['NDB'], 'nouakchott': ['NKC'], 'noumea': ['NOU'], 'novi sad': ['QND'], 'novosibirsk': ['OVB'], 'nürnberg': ['NUE'], 'nuevo laredo': ['NLD'], "nuku'alofa": ['TBU'], 'oakland': ['OAK'], 'oaxaca': ['OAX'], 'odense': ['ODE'], 'odessa': ['ODS'], 'oerebro': ['ORB'], 'ohrid': ['OHD'], 'oita': ['OIT'], 'okayama': ['OKJ'], 'okinawa, ryukyo island': ['OKA'], 'oklahoma city': ['OKC'], 'olbia': ['OLB'], 'olympic dam': ['OLP'], 'omaha': ['OMA'], 'ondangwa': ['OND'], 'ontario': ['ONT'], 'oran': ['ORN'], 'orange': ['OAG'], 'orange county': ['SNA'], 'oranjemund': ['OMD'], 'oranjestad': ['AUA'], 'orkney': ['KOI'], 'orlando metropolitan area': ['ORL'], 'orlando': ['MCO'], 'orpheus island': ['ORS'], 'osaka, metropolitan area': ['OSA'], 'osaka': ['ITM', 'KIX'], 'oshkosh': ['OSH'], 'osijek': ['OSI'], 'oslo': ['OSL', 'FBU', 'TRF'], 'ottawa': ['YOW'], 'ouadda': ['ODA'], 'ouarzazate': ['OZZ'], 'oudtshoorn': ['OUH'], 'ouagadougou': ['OUA'], 'oujda': ['OUD'], 'oulu': ['OUL'], 'out skerries': ['OUK'], 'oviedo': ['OVD'], 'owensboro': ['OWB'], 'oxnard': ['OXR'], 'oyem': ['UVE'], 'paderborn/lippstadt': ['PAD'], 'paducah': ['PAH'], 'page/lake powell': ['PGA'], 'pago pago': ['PPG'], 'pakersburg': ['PKB'], 'palermo': ['PMO'], 'palma de mallorca': ['PMI'], 'palmas': ['PMW'], 'palmdale/lancaster': ['PMD'], 'palmerston north': ['PMR'], 'palm springs': ['PSP'], 'panama city': ['PTY', 'PFN'], 'panjgur': ['PJG'], 'pantelleria': ['PNL'], 'papeete': ['PPT'], 'paphos': ['PFO'], 'paraburdoo': ['PBO'], 'paramaribo': ['PBM'], 'paris': ['PAR', 'CDG', 'LBG', 'ORY'], 'paro': ['PBH'], 'pasco': ['PSC'], 'pasni': ['PSI'], 'patna': ['PAT'], 'pattaya': ['PYX'], 'pau': ['PUF'], 'pellston': ['PLN'], 'penang international': ['PEN'], 'pendelton': ['PDT'], 'pensacola': ['PNS'], 'peoria/bloomington': ['PIA'], 'pereira': ['PEI'], 'perpignan': ['PGF'], 'perth international': ['PER'], 'perugia': ['PEG'], 'pescara': ['PSR'], 'peshawar': ['PEW'], 'petersburg': ['PSG'], 'phalaborwa': ['PHW'], 'philadelphia': ['PHL'], 'phnom penh': ['PNH'], 'phoenix': ['PHX'], 'phuket': ['HKT'], 'pierre': ['PIR'], 'pietermaritzburg': ['PZB'], 'pietersburg': ['PTG'], 'pilanesberg/sun city': ['NTY'], 'pisa': ['PSA'], 'pittsburgh international airport': ['PIT'], 'plattsburgh': ['PLB'], 'plettenberg bay': ['PBZ'], 'pocatello': ['PIH'], 'podgorica': ['TGD'], 'pohnpei': ['PNI'], 'pointe a pitre': ['PTP'], 'pointe noire': ['PNR'], 'poitiers': ['PIS'], 'ponce': ['PSE'], 'ponta delgada': ['PDL'], 'pori': ['POR'], 'port angeles': ['CLM'], 'port au prince': ['PAP'], 'port augusta': ['PUG'], 'port elizabeth': ['PLZ'], 'port gentil': ['POG'], 'port harcourt': ['PHC'], 'port hedland': ['PHE'], 'portland': ['PTJ', 'PWM'], 'portland international': ['PDX'], 'port lincoln': ['PLO'], 'port macquarie': ['PQQ'], 'port menier, pq': ['YPN'], 'port moresby': ['POM'], 'porto': ['OPO'], 'porto alegre': ['POA'], 'port of spain': ['POS'], 'port said': ['PSD'], 'porto santo': ['PXO'], 'porto velho': ['PVH'], 'port vila': ['VLI'], 'poughkeepsie': ['POU'], 'poznan, lawica': ['POZ'], 'prague': ['PRG'], 'praia': ['RAI'], 'presque island': ['PQI'], 'pretoria': ['PRY'], 'preveza/lefkas': ['PVK'], 'prince george': ['YXS'], 'prince rupert/digby island': ['YPR'], 'pristina': ['PRN'], 'prosperpine': ['PPP'], 'providence': ['PVD'], 'prudhoe bay': ['SCC'], 'puebla': ['PBC'], 'pueblo': ['PUB'], 'puerto escondido': ['PXM'], 'puerto ordaz': ['PZO'], 'puerto plata': ['POP'], 'puerto vallarta': ['PVR'], 'pukatawagan': ['XPK'], 'pula': ['PUY'], 'pullman': ['PUW'], 'pune': ['PNQ'], 'punta arenas': ['PUQ'], 'punta cana': ['PUJ'], 'pu san': ['PUS'], 'pyongyang': ['FNJ'], 'quebec': ['YQB'], 'queenstown': ['UEE', 'ZQN'], 'quetta': ['UET'], 'qingdao': ['TAO'], 'quimper': ['UIP'], 'quincy': ['UIN'], 'quito': ['UIO'], 'rabat': ['RBA'], 'rahim yar khan': ['RYK'], 'raiatea': ['RFP'], 'rainbow lake, ab': ['YOP'], 'rajkot': ['RAJ'], 'raleigh/durham': ['RDU'], 'ranchi': ['IXR'], 'rangiroa': ['RGI'], 'rangoon': ['RGN'], 'rapid city': ['RAP'], 'rarotonga': ['RAR'], 'ras al khaymah': ['RKT'], 'rawala kot': ['RAZ'], 'rawalpindi': ['RWP'], 'reading': ['RDG'], 'recife': ['REC'], 'redding': ['RDD'], 'redmond': ['RDM'], 'reggio calabria': ['REG'], 'regina': ['YQR'], 'reina sofia': ['TFS'], 'rennes': ['RNS'], 'reno': ['RNO'], 'resolute bay': ['YRB'], 'reus': ['REU'], 'reykjavik': ['REK', 'KEF'], 'rhinelander': ['RHI'], 'rhodos': ['RHO'], 'richards bay': ['RCB'], 'richmond': ['RIC'], 'riga': ['RIX'], 'rijeka': ['RJK'], 'rimini': ['RMI'], 'rio branco': ['RBR'], 'rio de janeiro': ['GIG', 'SDU', 'RIO'], 'riyadh': ['RUH'], 'roanne': ['RNE'], 'roanoke': ['ROA'], 'roatan': ['RTB'], 'rochester': ['RST', 'ROC'], 'rock sound': ['RSD'], 'rock springs': ['RKS'], 'rockford': ['RFD'], 'rockhampton': ['ROK'], 'rockland': ['RKD'], 'rocky mount': ['RWI'], 'rodez': ['RDZ'], 'rodrigues island': ['RRG'], 'roenne': ['RNN'], 'rome': ['ROM', 'CIA', 'FCO'], 'ronneby': ['RNB'], 'rosario': ['ROS'], 'rostov': ['RVI', 'ROV'], 'rotorua': ['ROT'], 'rotterdam': ['RTM'], 'rovaniemi': ['RVN'], 'rundu': ['NDU'], 'ruse': ['ROU'], 'saarbruecken': ['SCN'], 'sacramento': ['SMF'], 'sado shima': ['SDS'], 'saginaw/bay city/midland': ['MBS'], 'saidu sharif': ['SDT'], 'saigon': ['SGN'], 'saint brieuc': ['SBK'], 'saint denis': ['RUN'], 'saint john': ['YSJ'], 'saipan': ['SPN'], 'sal': ['SID'], 'salalah': ['SLL'], 'salem': ['SLE'], 'salinas': ['SNS', 'SNC'], 'salisbury': ['SAY', 'SBY'], 'saloniki': ['SKG'], 'salta, gen belgrano': ['SLA'], 'salt lake city': ['SLC'], 'salvador': ['SSA'], 'salzburg': ['SZG'], 'samara': ['KUF'], 'samarkand': ['SKD'], 'samos': ['SMI'], 'samsun': ['SZF'], 'san andres': ['ADZ'], 'san angelo': ['SJT'], 'san antonio': ['SAT'], 'san carlos de bariloche': ['BRC'], 'san diego': ['SAN'], 'san francisco': ['SFO'], 'san jose cabo': ['SJD'], 'san jose': ['SJO', 'SJC'], 'san juan': ['SJU'], 'san luis obisco': ['SBP'], 'san luis potosi': ['SLP'], 'san pedro': ['SPY'], 'san pedro sula': ['SAP'], 'san salvador': ['ZSA', 'SAL'], 'san sebastian': ['EAS'], 'sanaa': ['SAH'], 'sandspit': ['YZP'], 'santa ana': ['SNA'], 'santa barbara': ['SBA'], 'santa cruz de la palma': ['SPC'], 'santa cruz de la sierra': ['SRZ'], 'santa katarina': ['SKV'], 'santa maria': ['SMA', 'SMX'], 'santander': ['SDR'], 'santa rosa': ['STS', 'SRB', 'SRA', 'RSA'], 'santa rosa, copan': ['SDH'], 'santa rosalia': ['SSL', 'SRL'], 'santiago': ['SCU'], 'santiago de chile': ['SCL'], 'santiago de compostela': ['SCQ'], 'santo': ['SON'], 'santo domingo': ['SDQ'], 'sao luis': ['SLZ'], 'sao tome': ['TMS'], 'sarajevo': ['SJJ'], 'saransk': ['SKX'], 'sarasota/bradenton': ['SRQ'], 'saskatoon': ['YXE'], 'sassandra': ['ZSS'], 'savannah': ['SAV'], 'savonlinna': ['SVL'], 'scarborough': ['TAB'], 'scone': ['NSO'], 'scottsdale': ['SCF'], 'seattle/tacoma': ['SEA'], 'sehba': ['SEB'], 'seinaejoki': ['SJY'], 'selibi phikwe': ['PKW'], 'sendai': ['SDJ'], 'seoul': ['ICN', 'SEL'], 'sevilla': ['SVQ'], 'sfax': ['SFA'], 'shamattawa, mb': ['ZTM'], 'shanghai': ['SHA', 'PVG'], 'shannon': ['SNN'], 'sharjah': ['SHJ'], 'sharm el sheikh': ['SSH'], 'sheffield, city airport': ['SZD'], 'sheffield, doncaster, robin hood international airport': ['DSA'], 'shenandoah valley/stauton': ['SHD'], 'shenyang': ['SHE'], 'shenzhen': ['SZX'], 'sheridan': ['SHR'], 'shreveport, la': ['SHV'], 'shute harbour': ['JHQ'], 'sibu': ['SBW'], 'sidney': ['SDY'], 'silistra': ['SLS'], 'simferopol': ['SIP'], 'sindhri': ['MPD'], 'singapore': ['SIN', 'QPG', 'XSP'], 'singleton': ['SIX'], 'sioux city ia': ['SUX'], 'sioux falls': ['FSD'], 'sishen': ['SIS'], 'sitka': ['SIT'], 'sivas': ['VAS'], 'siwa': ['SEW'], 'skagway': ['SGY'], 'skardu': ['KDU'], 'skiathos': ['JSI'], 'skopje': ['SKP'], 'skrydstrup': ['SKS'], 'skukuza': ['SZK'], 'sligo': ['SXL'], 'smithers': ['YYD'], 'sodankylae': ['SOT'], 'soenderborg': ['SGD'], 'soendre stroemfjord': ['SFJ'], 'sofia': ['SOF'], 'sogndal': ['SOG'], 'southampton': ['SOU'], 'south bend': ['SBN'], 'south indian lake, mb': ['XSI'], 'south molle island': ['SOI'], 'southend': ['SEN'], 'split': ['SPU'], 'spokane': ['GEG'], 'springbok': ['SBU'], 'springfield': ['SPI', 'SGF'], 'srinagar': ['SXR'], 'st. augustin, pq': ['YIF'], 'st. croix': ['STX'], 'st. etienne': ['EBU'], 'st. george': ['SGU'], "st. john's": ['YYT'], 'st. kitts': ['SKB'], 'st. louis': ['STL'], 'st. lucia hewanorra': ['UVF'], 'st. lucia vigle': ['SLU'], 'st. marteen': ['SXM'], 'st. martin': ['SFG'], 'st. petersburg': ['LED'], 'st. pierre, nf': ['FSP'], 'st. thomas': ['STT'], 'st. vincent': ['SVD'], 'stansted': ['STN'], 'state college/belefonte': ['SCE'], 'stavanger': ['SVG'], 'steamboat springs': ['HDN'], 'stettin': ['SZZ'], 'stockholm metropolitan area': ['STO'], 'stockholm': ['ARN', 'BMA'], 'stockton': ['SCK'], 'stornway': ['SYY'], 'strasbourg': ['SXB'], 'streaky bay': ['KBY'], 'stuttgart': ['STR'], 'sui': ['SUL'], 'sukkur': ['SKZ'], 'sumburgh': ['LSI'], 'sun valley': ['SUN'], 'sundsvall': ['SDL'], 'sunshine coast': ['MCY'], 'surabaya': ['SUB'], 'surat': ['STV'], 'suva': ['SUV'], 'swakopmund': ['SWP'], 'sydney': ['SYD'], 'sylhet': ['ZYL'], 'syracuse': ['SYR'], 'tabuk': ['TUU'], 'taif': ['TIF'], 'taipei': ['TPE', 'TAY'], 'taiyuan': ['TYN'], 'takamatsu': ['TAK'], 'talkeetna': ['TKA'], 'tallahassee': ['TLH'], 'tallinn': ['QUF', 'TLL'], 'tampa': ['TPA'], 'tampere': ['TMP'], 'tampico': ['TAM'], 'tamworth': ['TMW'], 'tangier': ['TNG'], 'taree': ['TRO'], 'targovishte': ['TGV'], 'tashkent': ['TAS'], 'tawau': ['TWU'], 'tbilisi': ['TBS'], 'te anau': ['TEU'], 'teesside, durham tees valley': ['MME'], 'tegucigalpa': ['TGU'], 'tehran': ['THR'], 'tekirdag': ['TEQ'], 'tel aviv': ['TLV'], 'telluride': ['TEX'], 'temora': ['TEM'], 'tenerife': ['TCI', 'TFS', 'TFN'], 'tennant creek': ['TCA'], 'terceira': ['TER'], 'teresina': ['THE'], 'termez': ['TMZ'], 'terrace': ['YXT'], 'terre haute': ['HUF'], 'texarkana': ['TXK'], "thaba'nchu": ['TCU'], 'the pas': ['YQD'], 'thessaloniki': ['SKG'], 'thief river falls': ['TVF'], 'thira': ['JTR'], 'thiruvananthapuram': ['TRV'], 'thisted': ['TED'], 'thompson': ['YTH'], 'thorne bay': ['KTB'], 'thunder bay': ['YQT'], 'thursday island': ['TIS'], 'tianjin': ['TSN'], 'tijuana': ['TIJ'], 'tioman': ['TOD'], 'tirana': ['TIA'], 'tiruchirapally': ['TRZ'], 'tivat': ['TIV'], 'tobago': ['TAB'], 'tokushima': ['TKS'], 'tokyo': ['TYO', 'HND', 'NRT'], 'toledo': ['TOL'], 'tom price': ['TPR'], 'toowoomba': ['TWB'], 'toronto': ['YTZ', 'YYZ', 'YTO'], 'tortola': ['TOV'], 'touho': ['TOU'], 'toulouse': ['TLS'], 'townsville': ['TSV'], 'toyama': ['TOY'], 'trabzon': ['TZX'], 'trapani': ['TPS'], 'traverse city': ['TVC'], 'treasure cay': ['TCB'], 'trenton/princeton': ['TTN'], 'treviso': ['TSF'], 'tri': ['TRI'], 'trieste': ['TRS'], 'tripoli': ['TIP'], 'tromsoe': ['TOS'], 'trondheim': ['TRD'], 'tsumeb': ['TSB'], 'tucson': ['TUS'], 'tulepo': ['TUP'], 'tulsa': ['TUL'], 'tunis': ['TUN'], 'turbat': ['TUK'], 'turin': ['TRN'], 'turku': ['TKU'], 'tuscaloosa': ['TCL'], 'tuxtla gutierrez': ['TGZ'], 'twin falls': ['TWF'], 'tyler': ['TYR'], 'ua huka': ['UAH'], 'ua pou': ['UAP'], 'ube': ['UBJ'], 'uberaba': ['UBA'], 'uberlandia': ['UDI'], 'ubon ratchathani': ['UBP'], 'udaipur': ['UDR'], 'uden': ['UDE'], 'udon thani': ['UTH'], 'ufa': ['UFA'], 'uherske hradiste': ['UHE'], 'uige': ['UGO'], 'ujung pandang': ['UPG'], 'ukhta': ['UCT'], 'ukiah': ['UKI'], 'ulaanbaatar': ['ULN'], 'ulan': ['UUD'], 'ulanhot': ['HLH'], 'ulei': ['ULB'], 'ulsan': ['USN'], 'ulundi': ['ULD'], 'umea': ['UME'], 'umiujaq': ['YUD'], 'umtata': ['UTT'], 'unalakleet': ['UNK'], 'union island': ['UNI'], 'unst': ['UNT'], 'upala': ['UPL'], 'upernavik': ['JUV'], 'upington': ['UTN'], 'upolu point': ['UPP'], 'uranium city': ['YBE'], 'urgench': ['UGC'], 'uriman': ['URM'], 'urmiehm': ['OMH'], 'uruapan': ['UPN'], 'urubupunga': ['URB'], 'uruguaiana': ['URG'], 'urumqi': ['URC'], 'uruzgan': ['URZ'], 'ushuaia': ['USH'], 'utapao': ['UTP'], 'utica': ['UCA'], 'utila': ['UII'], 'uummannaq': ['UMD'], 'uzhgorod': ['UDJ'], 'vaasa': ['VAA'], 'vaexjoe': ['VXO'], 'vail': ['EGE'], "val d'or": ['YVO'], 'valdez': ['VDZ'], 'valdosta': ['VLD'], 'valencia': ['VLC', 'VLN'], 'valladolid': ['VLL'], 'valparaiso': ['VAP'], 'valverde': ['VDE'], 'van': ['VAN'], 'vancouver': ['YVR'], 'varadero': ['VRA'], 'varanasi': ['VNS'], 'varkaus': ['VRK'], 'varna': ['VAR'], 'vasteras': ['VST'], 'velikiye luki': ['VLU'], 'venice': ['VCE'], 'veracruz': ['VER'], 'vernal': ['VEL'], 'vero beach/ft. pierce': ['VRB'], 'verona': ['VBS', 'VRN'], 'victoria': ['YYJ'], 'victoria falls': ['VFA'], 'vidin': ['VID'], 'vientiane': ['VTE'], 'vigo': ['VGO'], 'villahermosa': ['VSA'], 'vilnius': ['VNO'], 'virgin gorda': ['VIJ'], 'visalia': ['VIS'], 'visby': ['VBY'], 'vitoria': ['VIT', 'VIX'], 'vryheid': ['VYD'], 'wabush': ['YWK'], 'waco': ['ACT'], 'wagga': ['WGA'], 'walla walla': ['ALW'], 'wallis': ['WLS'], 'walvis bay': ['WVB'], 'warrnambool': ['WMB'], 'warsaw': ['WAW'], 'washington dc': ['BWI', 'IAD', 'DCA', 'WAS'], 'waterloo ia': ['ALO'], 'watertown': ['ATY'], 'wausau/stevens point': ['CWA'], 'weipa': ['WEI'], 'welkom': ['WEL'], 'wellington': ['WLG'], 'wenatchee': ['EAT'], 'west palm beach': ['PBI'], 'west yellowstone': ['WYS'], 'westerland, sylt airport': ['GWT'], 'whakatane': ['WHK'], 'whale cove, nt': ['YXN'], 'whangarei': ['WRE'], 'white plains': ['HPN'], 'whitehorse': ['YXY'], 'whitsunday resort': ['HAP'], 'whyalla': ['WYA'], 'wichita falls': ['SPS'], 'wichita': ['ICT'], 'wick': ['WIC'], 'wickham': ['WHM'], 'wien': ['VIE'], 'wiesbaden, air base': ['WIE'], 'wilkes barre/scranton': ['AVP'], 'williamsport': ['IPT'], 'williston': ['ISL'], 'wilmington': ['ILM'], 'wilna': ['VNO'], 'wiluna': ['WUN'], 'windhoek': ['ERS', 'WDH'], 'windsor ontario': ['YQG'], 'winnipeg international': ['YWG'], 'wolf point': ['OLF'], 'wollongong': ['WOL'], 'woomera': ['UMR'], 'worcester': ['ORH'], 'worland': ['WRL'], 'wrangell': ['WRG'], 'wuhan': ['WUH'], 'wyndham': ['WYN'], 'xiamen': ['XMN'], "xi'an": ['XIY'], 'yakima': ['YKM'], 'yakutat': ['YAK'], 'yakutsk': ['YKS'], 'yamagata, junmachi': ['GAJ'], 'yamoussoukro': ['ASK'], 'yanbu': ['YNB'], 'yangon': ['RGN'], 'yaounde': ['YAO'], 'yellowknife': ['YZF'], 'yekaterinburg': ['SVX'], 'yichang': ['YIH'], 'yokohama': ['YOK'], 'yuma': ['YUM'], 'zacatecas': ['ZCL'], 'zadar': ['ZAD'], 'zagreb': ['ZAG'], 'zakynthos': ['ZTH'], 'zaragoza': ['ZAZ'], 'zhob': ['PZH'], 'zinder': ['ZND'], 'zouerate': ['OUZ'], 'zurich': ['ZRH']}

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
            'icon': json['weather'][0]['icon'],
            'desc': json['weather'][0]['description']
        }

    return False

# Gets all airport codes for a city
def get_all_codes(cities):
    total_codes = []

    for city in cities:
        city = city.lower()

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

    if 'extreme' in weather_from['desc'] or 'extreme' in weather_to['desc']:
        return opinions[0]

    if upswing:
        return opinions[0]

    return opinions[2]

def get_final_data(depart, arrival, sample_size_cap, distance_cap):
    return_data = {}

    depart_code = ''
    arrival_code = ''

    output = []

    if depart.lower() in city_codes and arrival.lower() in city_codes: # If function found correct IATA codes from city names
        depart_code = city_codes[depart.lower()][0]
        arrival_code = city_codes[arrival.lower()][0]

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