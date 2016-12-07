#! /naqfc/noscrub/Barry.Baker/anaconda2/bin/python
###for aitken replace the first line with /data/aqf/barryb/anaconda2/bin/python for the line above
#   To use this function you exectute as follows
#
# ./city_compare_aqs.py PATH/TO/ACONC PATH/TO/GRIDCRO LABEL CITY
#
# For a list of available cities please look at the end of the file
#
import sys
from glob import glob

import matplotlib.pyplot as plt
import verify

print "Name of Script: ", sys.argv[0]
print "ACONC FILE: ", sys.argv[1]
print "GRIDCRO2D FILE: ", sys.argv[2]
print "LABEL: ", sys.argv[3]
print "City Name: ", sys.argv[4]
print "OUTPUT FILENAME: ", sys.argv[5]

files = glob(sys.argv[1])
grid = sys.argv[2]

va = verify.verify_aqs(concpath=files, gridcro=grid, datapath='.', combine=True, neighbors=9)

names = va.df.MSA_Name.dropna().unique()
city = sys.argv[4]
name = ''
for i in names:
    if city.upper() in i.upper():
        name = i
params = va.df.groupby('MSA_Name').get_group(name).Species.unique()
for j in params:
    va.compare_param(param=j, timeseries=True, label=sys.argv[3], city=name, footer=False)
    plt.savefig(j + '_' + sys.argv[4] + sys.argv[5], dpi=100)
    plt.close()

'''
' Aberdeen, WA ', ' Adrian, MI ', ' Akron, OH ',
       ' Albany-Lebanon, OR ', ' Albany-Schenectady-Troy, NY ',
       ' Albuquerque, NM ', ' Allentown-Bethlehem-Easton, PA-NJ ',
       ' Altoona, PA ', ' Amarillo, TX ', ' Americus, GA ', ' Ames, IA ',
       ' Anderson, IN ', ' Anderson, SC ', ' Ann Arbor, MI ',
       ' Appleton, WI ', ' Ardmore, OK ', ' Arkadelphia, AR ',
       ' Asheville, NC ', ' Ashtabula, OH ', ' Athens, TN ',
       ' Athens-Clarke County, GA ',
       ' Atlanta-Sandy Springs-Marietta, GA ', ' Atlantic City, NJ ',
       ' Augusta-Richmond County, GA-SC ', ' Augusta-Waterville, ME ',
       ' Austin-Round Rock, TX ', ' Bakersfield, CA ',
       ' Baltimore-Towson, MD ', ' Bangor, ME ', ' Baraboo, WI ',
       ' Barnstable Town, MA ', ' Baton Rouge, LA ', ' Bay City, MI ',
       ' Beaumont-Port Arthur, TX ', ' Bellingham, WA ', ' Bend, OR ',
       ' Bennington, VT ', ' Berlin, NH-VT ', ' Birmingham-Hoover, AL ',
       ' Bishop, CA ', ' Bismarck, ND ',
       ' Blacksburg-Christiansburg-Radford, VA ', ' Bloomington, IN ',
       ' Bloomington-Normal, IL ', ' Boise City-Nampa, ID ',
       ' Boston-Cambridge-Quincy, MA-NH ', ' Boulder, CO ',
       ' Brainerd, MN ', ' Bridgeport-Stamford-Norwalk, CT ',
       ' Brigham City, UT ', ' Brownsville-Harlingen, TX ',
       ' Brunswick, GA ', ' Buffalo-Niagara Falls, NY ',
       ' Burlington-South Burlington, VT ', ' Cadillac, MI ',
       ' Cambridge, MD ', ' Canton-Massillon, OH ',
       ' Cape Coral-Fort Myers, FL ', ' Carlsbad-Artesia, NM ',
       ' Cedar Rapids, IA ', ' Chambersburg, PA ',
       ' Champaign-Urbana, IL ', ' Charlotte-Gastonia-Concord, NC-SC ',
       ' Charlottesville, VA ', ' Chattanooga, TN-GA ', ' Cheyenne, WY ',
       ' Chicago-Naperville-Joliet, IL-IN-WI ', ' Chico, CA ',
       ' Cincinnati-Middletown, OH-KY-IN ', ' City of The Dalles, OR ',
       ' Clarksville, TN-KY ', ' Cleveland, MS ',
       ' Cleveland-Elyria-Mentor, OH ', ' Clinton, IA ',
       " Coeur d'Alene, ID ", ' Colorado Springs, CO ', ' Columbia, MO ',
       ' Columbia, SC ', ' Columbus, GA-AL ', ' Columbus, IN ',
       ' Columbus, OH ', ' Concord, NH ', ' Corning, NY ',
       ' Corpus Christi, TX ', ' Corsicana, TX ',
       ' Dallas-Fort Worth-Arlington, TX ', ' Dalton, GA ',
       ' Daphne-Fairhope, AL ', ' Davenport-Moline-Rock Island, IA-IL ',
       ' Dayton, OH ', ' Decatur, AL ', ' Decatur, IL ',
       ' Deltona-Daytona Beach-Ormond Beach, FL ', ' Denver-Aurora, CO ',
       ' Des Moines, IA ', ' Detroit-Warren-Livonia, MI ',
       ' Dickinson, ND ', ' Dodge City, KS ', ' Dothan, AL ',
       ' Dover, DE ', ' DuBois, PA ', ' Duluth, MN-WI ', ' Durango, CO ',
       ' Durham, NC ', ' Dyersburg, TN ', ' Eagle Pass, TX ',
       ' East Stroudsburg, PA ', ' Effingham, IL ', ' El Centro, CA ',
       ' El Dorado, AR ', ' El Paso, TX ', ' Elizabethtown, KY ',
       ' Elkhart-Goshen, IN ', ' Ellensburg, WA ', ' Erie, PA ',
       ' Eugene-Springfield, OR ', ' Evanston, WY ', ' Evansville, IN-KY ',
       ' Fargo, ND-MN ', ' Farmington, NM ', ' Fayetteville, NC ',
       ' Fayetteville-Springdale-Rogers, AR-MO ', ' Flagstaff, AZ ',
       ' Flint, MI ', ' Florence, SC ', ' Florence-Muscle Shoals, AL ',
       ' Fond du Lac, WI ', ' Fort Collins-Loveland, CO ',
       ' Fort Smith, AR-OK ', ' Fort Walton Beach-Crestview-Destin, FL ',
       ' Fort Wayne, IN ', ' Fresno, CA ', ' Gadsden, AL ',
       ' Gainesville, FL ', ' Gettysburg, PA ', ' Gillette, WY ',
       ' Granbury, TX ', ' Grand Junction, CO ',
       ' Grand Rapids-Wyoming, MI ', ' Grants Pass, OR ', ' Greeley, CO ',
       ' Green Bay, WI ', ' Greensboro-High Point, NC ',
       ' Greenville, SC ', ' Gulfport-Biloxi, MS ',
       ' Hagerstown-Martinsburg, MD-WV ', ' Hanford-Corcoran, CA ',
       ' Harriman, TN ', ' Harrisburg-Carlisle, PA ', ' Harrison, AR ',
       ' Harrisonburg, VA ', ' Hartford-West Hartford-East Hartford, CT ',
       ' Helena, MT ', ' Hickory-Lenoir-Morganton, NC ', ' Hobbs, NM ',
       ' Homosassa Springs, FL ', ' Houma-Bayou Cane-Thibodaux, LA ',
       ' Houston-Sugar Land-Baytown, TX ',
       ' Huntington-Ashland, WV-KY-OH ', ' Huntsville, AL ',
       ' Idaho Falls, ID ', ' Indiana, PA ', ' Indianapolis, IN ',
       ' Iowa City, IA ', ' Ithaca, NY ', ' Jackson, MS ', ' Jackson, TN ',
       ' Jackson, WY-ID ', ' Jacksonville, FL ', ' Jefferson City, MO ',
       ' Johnstown, PA ', ' Joplin, MO ', ' Kalamazoo-Portage, MI ',
       ' Kalispell, MT ', ' Kansas City, MO-KS ', ' Keene, NH ',
       ' Kennewick-Richland-Pasco, WA ', ' Killeen-Temple-Fort Hood, TX ',
       ' Kingsport-Bristol-Bristol, TN-VA ', ' Klamath Falls, OR ',
       ' Knoxville, TN ', ' Kokomo, IN ', ' La Crosse, WI-MN ',
       ' La Grande, OR ', ' Laconia, NH ', ' Lafayette, IN ',
       ' Lafayette, LA ', ' Lake Charles, LA ', ' Lake City, FL ',
       ' Lake Havasu City-Kingman, AZ ', ' Lakeland, FL ',
       ' Lancaster, PA ', ' Lansing-East Lansing, MI ', ' Laramie, WY ',
       ' Laredo, TX ', ' Las Cruces, NM ', ' Las Vegas-Paradise, NV ',
       ' Lawrenceburg, TN ', ' Lawton, OK ', ' Lebanon, NH-VT ',
       ' Lewiston, ID-WA ', ' Lewiston-Auburn, ME ',
       ' Lexington-Fayette, KY ', ' Lima, OH ', ' Lincoln, NE ',
       ' Lincolnton, NC ', ' Little Rock-North Little Rock, AR ',
       ' Longview, TX ', ' Longview, WA ',
       ' Los Angeles-Long Beach-Santa Ana, CA ', ' Louisville, KY-IN ',
       ' Lubbock, TX ', ' Macon, GA ', ' Madera, CA ', ' Madison, WI ',
       ' Malone, NY ', ' Manchester-Nashua, NH ', ' Manitowoc, WI ',
       ' Marshall, MN ', ' Marshall, TX ', ' McAlester, OK ',
       ' McAllen-Edinburg-Mission, TX ', ' Medford, OR ',
       ' Memphis, TN-MS-AR ', ' Merced, CA ', ' Meridian, MS ',
       ' Miami, OK ', ' Miami-Fort Lauderdale-Miami Beach, FL ',
       ' Middlesborough, KY ', ' Milwaukee-Waukesha-West Allis, WI ',
       ' Minneapolis-St. Paul-Bloomington, MN-WI ', ' Mobile, AL ',
       ' Modesto, CA ', ' Monroe, LA ', ' Montgomery, AL ',
       ' Morehead City, NC ', ' Morgantown, WV ', ' Morristown, TN ',
       ' Moses Lake, WA ', ' Mount Vernon, IL ', ' Mount Vernon, OH ',
       ' Mount Vernon-Anacortes, WA ', ' Muskogee, OK ', ' Napa, CA ',
       ' Naples-Marco Island, FL ',
       ' Nashville-Davidson--Murfreesboro, TN ', ' New Castle, PA ',
       ' New Haven-Milford, CT ', ' New Orleans-Metairie-Kenner, LA ',
       ' New York-Northern New Jersey-Long Island, NY-NJ-PA ',
       ' Nogales, AZ ', ' Norwich-New London, CT ', ' Ocala, FL ',
       ' Odessa, TX ', ' Ogden-Clearfield, UT ', ' Oklahoma City, OK ',
       ' Olympia, WA ', ' Omaha-Council Bluffs, NE-IA ',
       ' Orlando-Kissimmee, FL ', ' Owensboro, KY ',
       ' Oxnard-Thousand Oaks-Ventura, CA ', ' Paducah, KY-IL ',
       ' Palm Bay-Melbourne-Titusville, FL ',
       ' Panama City-Lynn Haven, FL ',
       ' Parkersburg-Marietta-Vienna, WV-OH ', ' Pascagoula, MS ',
       ' Payson, AZ ', ' Pendleton-Hermiston, OR ',
       ' Pensacola-Ferry Pass-Brent, FL ', ' Peoria, IL ',
       ' Philadelphia-Camden-Wilmington, PA-NJ-DE-MD ',
       ' Phoenix Lake-Cedar Ridge, CA ', ' Phoenix-Mesa-Scottsdale, AZ ',
       ' Pittsburgh, PA ', ' Pittsfield, MA ', ' Pocatello, ID ',
       ' Ponca City, OK ', ' Port Angeles, WA ',
       ' Portland-South Portland-Biddeford, ME ',
       ' Portland-Vancouver-Beaverton, OR-WA ', ' Portsmouth, OH ',
       ' Poughkeepsie-Newburgh-Middletown, NY ', ' Prescott, AZ ',
       ' Prineville, OR ', ' Providence-New Bedford-Fall River, RI-MA ',
       ' Provo-Orem, UT ', ' Pullman, WA ', ' Quincy, IL-MO ',
       ' Raleigh-Cary, NC ', ' Rapid City, SD ', ' Reading, PA ',
       ' Red Bluff, CA ', ' Red Wing, MN ', ' Redding, CA ',
       ' Reno-Sparks, NV ', ' Richmond, VA ',
       ' Riverside-San Bernardino-Ontario, CA ', ' Riverton, WY ',
       ' Roanoke, VA ', ' Rochester, MN ', ' Rochester, NY ',
       ' Rock Springs, WY ', ' Rockford, IL ', ' Rocky Mount, NC ',
       ' Roseburg, OR ', ' Rutland, VT ',
       ' Sacramento--Arden-Arcade--Roseville, CA ', ' Salem, OR ',
       ' Salinas, CA ', ' Salisbury, NC ', ' Salt Lake City, UT ',
       ' San Antonio, TX ', ' San Diego-Carlsbad-San Marcos, CA ',
       ' San Francisco-Oakland-Fremont, CA ',
       ' San Jose-Sunnyvale-Santa Clara, CA ',
       ' San Luis Obispo-Paso Robles, CA ',
       ' Santa Barbara-Santa Maria, CA ', ' Santa Cruz-Watsonville, CA ',
       ' Santa Fe, NM ', ' Santa Rosa-Petaluma, CA ',
       ' Sarasota-Bradenton-Venice, FL ', ' Sault Ste. Marie, MI ',
       ' Savannah, GA ', ' Scranton--Wilkes-Barre, PA ', ' Seaford, DE ',
       ' Seattle-Tacoma-Bellevue, WA ', ' Sebring, FL ', ' Seneca, SC ',
       ' Sevierville, TN ', ' Shelton, WA ',
       ' Shreveport-Bossier City, LA ', ' Sierra Vista-Douglas, AZ ',
       ' Somerset, KY ', ' Somerset, PA ', ' South Bend-Mishawaka, IN-MI ',
       ' Spartanburg, SC ', ' Spokane, WA ', ' Springfield, IL ',
       ' Springfield, MA ', ' Springfield, MO ', ' Springfield, OH ',
       ' St. George, UT ', ' St. Joseph, MO-KS ', ' St. Louis, MO-IL ',
       ' St. Marys, PA ', ' State College, PA ', ' Stockton, CA ',
       ' Summerville, GA ', ' Syracuse, NY ', ' Tahlequah, OK ',
       ' Tallahassee, FL ', ' Tampa-St. Petersburg-Clearwater, FL ',
       ' Taos, NM ', ' Terre Haute, IN ', ' Texarkana, TX-Texarkana, AR ',
       ' Thomasville-Lexington, NC ', ' Toledo, OH ', ' Topeka, KS ',
       ' Torrington, CT ', ' Trenton-Ewing, NJ ',
       ' Truckee-Grass Valley, CA ', ' Tucson, AZ ', ' Tulsa, OK ',
       ' Tupelo, MS ', ' Tuscaloosa, AL ', ' Tyler, TX ', ' Ukiah, CA ',
       ' Utica-Rome, NY ', ' Valdosta, GA ', ' Vallejo-Fairfield, CA ',
       ' Victoria, TX ', ' Vincennes, IN ',
       ' Vineland-Millville-Bridgeton, NJ ',
       ' Virginia Beach-Norfolk-Newport News, VA-NC ',
       ' Visalia-Porterville, CA ', ' Wabash, IN ', ' Waco, TX ',
       ' Walla Walla, WA ', ' Walterboro, SC ', ' Warner Robins, GA ',
       ' Washington, OH ',
       ' Washington-Arlington-Alexandria, DC-VA-MD-WV ',
       ' Waterloo-Cedar Falls, IA ', ' Watertown-Fort Drum, NY ',
       ' Wausau, WI ', ' Weirton-Steubenville, WV-OH ', ' Wenatchee, WA ',
       ' Wheeling, WV-OH ', ' Whitewater, WI ', ' Wichita, KS ',
       ' Williamsport, PA ', ' Willimantic, CT ', ' Wilmington, NC ',
       ' Wilmington, OH ', ' Winchester, VA-WV ', ' Winston-Salem, NC ',
       ' Worcester, MA ', ' Yakima, WA ', ' York-Hanover, PA ',
       ' Youngstown-Warren-Boardman, OH-PA ', ' Yuba City, CA ',
       ' Yuma, AZ '
'''
