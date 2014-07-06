rebate_info
===========


API that gives access to energy efficiency incentive information

[http://rebates.jaytarlecki.com/](http://rebates.jaytarlecki.com/)

##About
This is an API that attempts to provide detailed information on utility-based energy efficiency rebate programs, resolved down to the zipcode.  The intent here, is that a user posts a zipcode in a URL, and the response is a structured packet of data (.json format) that gives info about 

1. the utility companies and energy types they provide, currently limited to electric and gas
2. the rebate programs that utility companies participate in (if any)
3. the building sectors that the rebate program services
4. and the rebate-eligible technologies that the program covers

The data is not limited to these items above, but this is the initial scope of the project.  The application is set up in such a way that the "better" or more current data could be annexed to the program by 1) expanding the administrative interface for users to take custody of the data or 2) simply bulk uploading more current data to any of the table, as more robust or accurate data presents itself.


##Background
Whether it is LED lighting, a new boiler, or a premium efficiency motor, efficient equipment consumes less energy.  However, the most energy efficient products on the market are often too cost prohibitive to entice the end-user to make a purchase.  Sure, a small business owner could buy a new HVAC system for their building and potentially save a lot of money in the years to come; unfortunately, the building owner often does not realize his return on investment until after the tenth year of operation.  Efficient gear may save a ton of money on utility bills, but its too difficult to lay out all that money for something that does not provide a more immediate return.  Thus, in order to buy down the first cost of these efficiency upgrades, the utility rebate program was born.  The grids in the U.S. are under such pressure (logistically, environmentally, and quantitatively) that is more cost effective for the utility companies to subsidize their consumers efficiency upgrades rather than spend the money on the generation/distribution of their own commodity (energy).  For the utilities, it is basically a forced market-transformation strategy.  The success of these rebate programs is evident in their annually increasing funding in every state.   I believe that better access to this information would be very useful to both the vendors who sell efficient products, as well as the consumers who want to find the best way to spend their capital improvement budgets.  

In my previous job, I created a few database-driven web applications that would calculate utility-based incentives for specific energy efficiency upgrades to buildings (Chillers, VFDs, Water Source Heat Pumps, etc.).  I realized that the development of the applications was a bit of a waste of time.  Why? Both end-users of energy and vendors who sell the efficient gear just want the data available to them, not necessarily a website dreamed up to help facilitate their access to the data.  Its a lot of wasted time and energy when someone could just provide the service delivery of structured data returns, so the user can organize and collate the output of the data however they like.

##Data
Note: A lot of this data I had to scrub

####Zipcodes
- **WHAT:**	    A listing of zipcodes and some related geographic information
- **WHERE:** 	http://www.unitedstateszipcodes.org/zip-code-database/
- **WHY:**	    Needed for geographic indexing of information
- **HOW:**	    csv imported into postgreSQL database

####ZipUtilities
- **WHAT:** 	Listing of gas and electric utilities resolved down to the zipcode level.
- **WHERE:** 	http://en.openei.org/datasets/node/899
- **WHY:**	    Indexes utility companies down to the zipcode level. Generally, there is more than one utility company for each zipcode, so there is typically more than one answer per zipcode.  I actually normalized the 'utilities' out of the zipcodes making them unique in their own table, with a foreign key in the "ziputilities" table point there.   This shrinks down the dataset and makes it more flexible overall (less to manage!)
- **HOW:**	csv parsed and imported into postgreSQL database

####RebatePrograms
- **WHAT:** 	A listing of rebate programs, with a number of external relationships to help categorize the program.  Each record comes with some overview information about the program eligibility and requirements.
- **WHERE:** 	http://en.openei.org/wiki/Rebate_Programs
- **WHY:**	For this API, a utility may (or may not) offer Rebate Programs for eligible technologies.  The API will show the utility     companies that provide service for the user's zipcode, and what rebate programs those utility companies subscribe to (if any).
- **HOW:**	    I could right a novel about this one, but I will try to keep it short.  I selected a portion of pertinent data from the dataset mentioned above.  It was a "flat file" collection of csv files that needed some normalization in order to make the data more usable and actionable.  In analyzing the data, I realized that there was a lot of repetition that could be broken out into seperate tables.  I actually uploaded the raw data to a single SQL table, then wrote a parser in procedural sql in order to normalize the entire dataset.  The data was normalized as follows: 

######Many-to-many relationships
- **Sectors**:		The building sectors that the rebate programs services eg) Agricultural, Commercial, Industrial, etc.
- **Technologies**:	A listing of rebate-eligible technologies for which the rebate programs provide incentives, eg) Boilers, Chillers, Lighting Controls/Sensors, etc.  I actually created a parent table "TechnologyCategories" to help bucket the technologies into specific categories, there is a foreign key inside "Technologies" pointed to the parent table.
- **FundingTypes**:	There are only two fundingtypes which are defined as follows 1) Energy Efficiency Incentive Programs: permanently REDUCING demand on the grid and 2) Renewable Energy Incentive Programs: permanently REMOVING demand on the grid.  Although the database is heavily skewed toward the former, I thought it would be informative to keep these partitioned when I normalized the dataset.
- **Utilities**:  	I actually created this dataset myself by [miserably] parsing through all the rebate program and utility websites.  The bulk of work for this app was in here.  This is when development of this application started to suck.

######One-to-many relationships
- **FundingSources**:	This is a short list of who finances the rebate, eg) Local, Utility, Federal, etc.  This application focuses strictly on the "Utility" funding source.
- **ProgramAdmins**: 	Although some utility companies do self-adminster their own rebate programs, many opt to outsource the management of their programs to a third party vendor.  This particular foreign key does not come into play much in this app, but I thought it might be nice to see what Program Administrators controlled what utility jurisdictions. 
- **States**:			This is simply the consolidation of states, pulled out of the "RebatePrograms" table.   Utility companies may span states, but as part of regulations, utility companies are overseen by the states that they operate in by a public utility commission or related authority.  Thus, each utility-based rebate program operates differently in each state.  In order to resolve the API back to geographic info (zipcodes), it became pertinent to have an explicit tie to state for each rebate program. I foreigned keyed that data to its own table here.

That covers the basics of the data model. If you are familiar with django, then please refer to the models.py for a complete listing of the data model.  If there are any questions, please send me and email.  I'll just be glad to know you are interested.


## How to run
If you are familiar with python/django then you can just grab the code and go
python manage.py syncdb
python manage.py runserver
If you want to put some data into the app, just navigate to the default django admin interface. I have not put any work into the administrative interface at this time, and do not intend to unless this application needs active management.  For now, its an exploration into webservices using Tastypie! 


##How to use
Basically, a user can query whatever they want as I have created .json returns for almsot every relevant table.  The URL would take the following form:

    http://localhost:8000/api/<table_resource>/?<filter_name>=<filter>

Schemas for each table can be found as follows:

    http://localhost:8000/api/<table_resource>/schema/

The nuts-and-bolts of the application is the query onto the "ZipUtilities" resource.  Now, it may not be named properly, but adding a zip filter into the URL will give all the 'utilities' related to the 'zipcode', along with all the 'rebateprograms' associated with each 'utility'

Example)
Sending a request to a Philly zipcode:

    http://localhost:8000/api/ziputilities/?zipcode=19104
    

Would render this response:

        {
          "meta": {
            "limit": 20, 
            "next": null, 
            "offset": 0, 
            "previous": null, 
            "total_count": 3
          }, 
          "objects": [
            {
              "energytype": {
                "code": "E", 
                "energy": "ELECTRIC", 
                "modifieddate": "2014-05-05", 
                "resource_uri": "/api/energytypes/2/"
              }, 
              "modifieddate": "2014-05-05", 
              "overlap": 1.0, 
              "resource_uri": "/api/ziputilities/156692/", 
              "utility": {
                "modifieddate": "2014-03-11", 
                "rebateprograms": [
                  {
                    "modifieddate": "2014-05-04", 
                    "name": "PECO Energy (Electric) - Non-Residential Energy Efficiency Rebate Program (Pennsylvania)", 
                    "programbudget": "", 
                    "programcaveats": "", 
                    "programenddatestring": "5/31/2013", 
                    "programstartdatestring": "", 
                    "programyearenddate": null, 
                    "programyearstartdate": null, 
                    "rebateprogramtechnologies": [
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/12228/", 
                        "technology": {
                          "name": "Groud Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/13068/", 
                        "technology": {
                          "name": "Air Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/13908/", 
                        "technology": {
                          "name": "Water Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/14705/", 
                        "technology": {
                          "name": "LED"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/15473/", 
                        "technology": {
                          "name": "Linear Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/16241/", 
                        "technology": {
                          "name": "Compact Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17009/", 
                        "technology": {
                          "name": "HID"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17777/", 
                        "technology": {
                          "name": "Induction"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/18545/", 
                        "technology": {
                          "name": "Performance"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/19313/", 
                        "technology": {
                          "name": "Cold Cathode"
                        }
                      }
                    ], 
                    "resource_uri": "/api/rebateprograms/1413/", 
                    "temppayoutstring": "Unitary and Split Air Conditioning Systems and Air Source Heat Pumps: $25-$45/tonChillers: $10-$40/tonGround Source Heat Pumps: $40/tonHotel Occupancy Sensors: $20-$40Energy Management Control System: $0.10/sq. ft. or $0.21/sq. ft.Fluorescent Lamps: $1-$9Lamp Removal: $7.50-$12.50/lamp removedLighting Fixtures: $15-$50Lighting Controls/Sensors: $0.10-$0.12/Watts ControlledLED Exit Sign: $25LEDs: $15Exterior Lighting: $45-$120/fixtureTraffic Lights: $48-$52/fixtureMotors: $8-$475/motorVFDs: $40-$500Refrigeration Measures: $4-$70Freezer: $150 or $400Ice Makers: $100-$500Other Food Service: $30-$150Custom Incentives: $0.08 or $0.12/kWh", 
                    "tempprojectsizestring": "", 
                    "temprequirementsstring": "Unitary and Split Air Conditioning Systems and Air Source Heat Pumps: 15 SEER or 10.2-12 EER/TBD IEER depending on size<br />Air-Cooled Chillers: 1.04 kW/ton-IPLV<br />Ground Source Heat Pumps: EER 17", 
                    "website": "https://www.peco.com/Savings/ProgramsandRebates/Business/Pages/default.aspx"
                  }, 
                  {
                    "modifieddate": "2014-05-04", 
                    "name": "PECO Energy (Electric)- Residential Energy Efficiency Rebate Program (Pennsylvania)", 
                    "programbudget": "", 
                    "programcaveats": "", 
                    "programenddatestring": "12/31/2012", 
                    "programstartdatestring": "", 
                    "programyearenddate": null, 
                    "programyearstartdate": null, 
                    "rebateprogramtechnologies": [
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/12229/", 
                        "technology": {
                          "name": "Groud Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/13069/", 
                        "technology": {
                          "name": "Air Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/13909/", 
                        "technology": {
                          "name": "Water Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/14706/", 
                        "technology": {
                          "name": "LED"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/15474/", 
                        "technology": {
                          "name": "Linear Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/16242/", 
                        "technology": {
                          "name": "Compact Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17010/", 
                        "technology": {
                          "name": "HID"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17778/", 
                        "technology": {
                          "name": "Induction"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/18546/", 
                        "technology": {
                          "name": "Performance"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/19314/", 
                        "technology": {
                          "name": "Cold Cathode"
                        }
                      }
                    ], 
                    "resource_uri": "/api/rebateprograms/1414/", 
                    "temppayoutstring": "Central A/C: $300<br />Air-Source Heat Pump: $325-$400<br />Geothermal Heat Pump: $217/ton<br />Heat Pump Water Heater: $300<br />Gas Furnace (replacing Electric Base Board or Electric Furnace): $1,000<br />Gas Furnace (replacing Electric Heat Pump): $550<br />Gas Water Heater (replacing Electric Hot Water Heater): $250<br /> LED/CFL Bulbs: Discounted<br />Storage Tank Electric Water Heater: $25<br />Room Air Conditioner: $25<br />Refrigerator: $25<br />Clothes Washer: $25<br />Refrigerator/Freezer Recycling: $15", 
                    "tempprojectsizestring": "", 
                    "temprequirementsstring": "ENERGY STAR Most Efficient refrigerators and clothes washers, and ENERGY STAR room air conditionersAir Source Heat Pump: minimum 15 SEERGeothermal Heat Pump: minimum coefficient of performance of 3.3Heat Pump Water heater minimum 2.0 EFElectric Water Heater: minimum .93 EFNatural Gas Boiler: 85% AFUENatural Gas Furnace: 90% AFUE", 
                    "website": "https://www.peco.com/Savings/ProgramsandRebates/Residential/Pages/default.aspx"
                  }, 
                  {
                    "modifieddate": "2014-05-04", 
                    "name": "PECO Energy (Gas) - Heating Efficiency Rebate Program (Pennsylvania)", 
                    "programbudget": "", 
                    "programcaveats": "Must be replacing existing equipment.", 
                    "programenddatestring": "", 
                    "programstartdatestring": "", 
                    "programyearenddate": null, 
                    "programyearstartdate": null, 
                    "rebateprogramtechnologies": [], 
                    "resource_uri": "/api/rebateprograms/1415/", 
                    "temppayoutstring": "High Efficiency Boiler/Furnace: $300<br />Natural Gas Storage Tank Water Heater: $50", 
                    "tempprojectsizestring": "", 
                    "temprequirementsstring": "Furnaces/Boilers/Water Heaters: must be ENERGY STAR qualified<br />Water Heaters: Business Customers not eligible<br />Furnaces: Must have a 90% or greater AFUE rating<br />Boilers: Must have an 85% or greater AFUE rating<br />Storage Tank Water Heaters: Must have an EF of 0.67 or greater<br />", 
                    "website": "https://www.peco.com/Savings/ProgramsandRebates/Residential/PECOSmartGasEfficiencyUpgrade/Pages/Overview.aspx"
                  }
                ], 
                "resource_uri": "/api/utilities/4209/", 
                "utilityname": "PECO"
              }, 
              "utilitytype": {
                "code": "IOU", 
                "description": "INVESTOR OWNED", 
                "modifieddate": "2014-05-05", 
                "resource_uri": "/api/utilitytypes/4/"
              }, 
              "zipcode": "19104"
            }, 
            {
              "energytype": {
                "code": "G", 
                "energy": "GAS", 
                "modifieddate": "2014-05-05", 
                "resource_uri": "/api/energytypes/3/"
              }, 
              "modifieddate": "2014-05-05", 
              "overlap": 1.0, 
              "resource_uri": "/api/ziputilities/159479/", 
              "utility": {
                "modifieddate": "2014-03-11", 
                "rebateprograms": [
                  {
                    "modifieddate": "2014-05-04", 
                    "name": "Philadelphia Gas Works - Commercial and Industrial EnergySense Retrofit Program (Pennsylvania)", 
                    "programbudget": "", 
                    "programcaveats": "", 
                    "programenddatestring": "9/1/2015", 
                    "programstartdatestring": "", 
                    "programyearenddate": null, 
                    "programyearstartdate": null, 
                    "rebateprogramtechnologies": [], 
                    "resource_uri": "/api/rebateprograms/1450/", 
                    "temppayoutstring": "Varies Widely", 
                    "tempprojectsizestring": "", 
                    "temprequirementsstring": "Retrofits must reduce gas consumption", 
                    "website": "https://www.pgworks.com/index.aspx?NID=403"
                  }, 
                  {
                    "modifieddate": "2014-05-04", 
                    "name": "Philadelphia Gas Works - Residential EnergySense Program (Pennsylvania)", 
                    "programbudget": "", 
                    "programcaveats": "Low Income Retrofit: Must be enrolled in PGWÃ¢â‚¬â„¢s Customer Responsibility Program.", 
                    "programenddatestring": "9/1/2015", 
                    "programstartdatestring": "4/1/2011", 
                    "programyearenddate": null, 
                    "programyearstartdate": null, 
                    "rebateprogramtechnologies": [
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/14723/", 
                        "technology": {
                          "name": "LED"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/15491/", 
                        "technology": {
                          "name": "Linear Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/16259/", 
                        "technology": {
                          "name": "Compact Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17027/", 
                        "technology": {
                          "name": "HID"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17795/", 
                        "technology": {
                          "name": "Induction"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/18563/", 
                        "technology": {
                          "name": "Performance"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/19331/", 
                        "technology": {
                          "name": "Cold Cathode"
                        }
                      }
                    ], 
                    "resource_uri": "/api/rebateprograms/1451/", 
                    "temppayoutstring": "Low Income Retrofit Audit: Free weatherization, CFLs, window upgrades, heating and hot water energy saving measures<br />Boiler: $2,000 rebate check<br />Furnace: $500 Visa Prepaid Card<br />Programmable Thermostat: $30", 
                    "tempprojectsizestring": "", 
                    "temprequirementsstring": "Boiler and Furnace: AFUE 94% or greater", 
                    "website": "https://www.pgworks.com/index.aspx?nid=334"
                  }
                ], 
                "resource_uri": "/api/utilities/3887/", 
                "utilityname": "PGW"
              }, 
              "utilitytype": {
                "code": "MUNI", 
                "description": "MUNICIPAL", 
                "modifieddate": "2014-05-05", 
                "resource_uri": "/api/utilitytypes/5/"
              }, 
              "zipcode": "19104"
            }, 
            {
              "energytype": {
                "code": "G", 
                "energy": "GAS", 
                "modifieddate": "2014-05-05", 
                "resource_uri": "/api/energytypes/3/"
              }, 
              "modifieddate": "2014-05-05", 
              "overlap": 1.0, 
              "resource_uri": "/api/ziputilities/195337/", 
              "utility": {
                "modifieddate": "2014-03-11", 
                "rebateprograms": [
                  {
                    "modifieddate": "2014-05-04", 
                    "name": "PECO Energy (Electric) - Non-Residential Energy Efficiency Rebate Program (Pennsylvania)", 
                    "programbudget": "", 
                    "programcaveats": "", 
                    "programenddatestring": "5/31/2013", 
                    "programstartdatestring": "", 
                    "programyearenddate": null, 
                    "programyearstartdate": null, 
                    "rebateprogramtechnologies": [
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/12228/", 
                        "technology": {
                          "name": "Groud Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/13068/", 
                        "technology": {
                          "name": "Air Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/13908/", 
                        "technology": {
                          "name": "Water Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/14705/", 
                        "technology": {
                          "name": "LED"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/15473/", 
                        "technology": {
                          "name": "Linear Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/16241/", 
                        "technology": {
                          "name": "Compact Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17009/", 
                        "technology": {
                          "name": "HID"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17777/", 
                        "technology": {
                          "name": "Induction"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/18545/", 
                        "technology": {
                          "name": "Performance"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/19313/", 
                        "technology": {
                          "name": "Cold Cathode"
                        }
                      }
                    ], 
                    "resource_uri": "/api/rebateprograms/1413/", 
                    "temppayoutstring": "Unitary and Split Air Conditioning Systems and Air Source Heat Pumps: $25-$45/tonChillers: $10-$40/tonGround Source Heat Pumps: $40/tonHotel Occupancy Sensors: $20-$40Energy Management Control System: $0.10/sq. ft. or $0.21/sq. ft.Fluorescent Lamps: $1-$9Lamp Removal: $7.50-$12.50/lamp removedLighting Fixtures: $15-$50Lighting Controls/Sensors: $0.10-$0.12/Watts ControlledLED Exit Sign: $25LEDs: $15Exterior Lighting: $45-$120/fixtureTraffic Lights: $48-$52/fixtureMotors: $8-$475/motorVFDs: $40-$500Refrigeration Measures: $4-$70Freezer: $150 or $400Ice Makers: $100-$500Other Food Service: $30-$150Custom Incentives: $0.08 or $0.12/kWh", 
                    "tempprojectsizestring": "", 
                    "temprequirementsstring": "Unitary and Split Air Conditioning Systems and Air Source Heat Pumps: 15 SEER or 10.2-12 EER/TBD IEER depending on size<br />Air-Cooled Chillers: 1.04 kW/ton-IPLV<br />Ground Source Heat Pumps: EER 17", 
                    "website": "https://www.peco.com/Savings/ProgramsandRebates/Business/Pages/default.aspx"
                  }, 
                  {
                    "modifieddate": "2014-05-04", 
                    "name": "PECO Energy (Electric)- Residential Energy Efficiency Rebate Program (Pennsylvania)", 
                    "programbudget": "", 
                    "programcaveats": "", 
                    "programenddatestring": "12/31/2012", 
                    "programstartdatestring": "", 
                    "programyearenddate": null, 
                    "programyearstartdate": null, 
                    "rebateprogramtechnologies": [
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/12229/", 
                        "technology": {
                          "name": "Groud Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/13069/", 
                        "technology": {
                          "name": "Air Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/13909/", 
                        "technology": {
                          "name": "Water Source Heat Pumps"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/14706/", 
                        "technology": {
                          "name": "LED"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/15474/", 
                        "technology": {
                          "name": "Linear Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/16242/", 
                        "technology": {
                          "name": "Compact Fluorescent"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17010/", 
                        "technology": {
                          "name": "HID"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/17778/", 
                        "technology": {
                          "name": "Induction"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/18546/", 
                        "technology": {
                          "name": "Performance"
                        }
                      }, 
                      {
                        "application_url": "NULL", 
                        "caps": "NULL", 
                        "directory_url": "NULL", 
                        "modifieddate": "2014-05-06", 
                        "payout_overview": "NULL", 
                        "resource_uri": "/api/rebateprogramtechnologies/19314/", 
                        "technology": {
                          "name": "Cold Cathode"
                        }
                      }
                    ], 
                    "resource_uri": "/api/rebateprograms/1414/", 
                    "temppayoutstring": "Central A/C: $300<br />Air-Source Heat Pump: $325-$400<br />Geothermal Heat Pump: $217/ton<br />Heat Pump Water Heater: $300<br />Gas Furnace (replacing Electric Base Board or Electric Furnace): $1,000<br />Gas Furnace (replacing Electric Heat Pump): $550<br />Gas Water Heater (replacing Electric Hot Water Heater): $250<br /> LED/CFL Bulbs: Discounted<br />Storage Tank Electric Water Heater: $25<br />Room Air Conditioner: $25<br />Refrigerator: $25<br />Clothes Washer: $25<br />Refrigerator/Freezer Recycling: $15", 
                    "tempprojectsizestring": "", 
                    "temprequirementsstring": "ENERGY STAR Most Efficient refrigerators and clothes washers, and ENERGY STAR room air conditionersAir Source Heat Pump: minimum 15 SEERGeothermal Heat Pump: minimum coefficient of performance of 3.3Heat Pump Water heater minimum 2.0 EFElectric Water Heater: minimum .93 EFNatural Gas Boiler: 85% AFUENatural Gas Furnace: 90% AFUE", 
                    "website": "https://www.peco.com/Savings/ProgramsandRebates/Residential/Pages/default.aspx"
                  }, 
                  {
                    "modifieddate": "2014-05-04", 
                    "name": "PECO Energy (Gas) - Heating Efficiency Rebate Program (Pennsylvania)", 
                    "programbudget": "", 
                    "programcaveats": "Must be replacing existing equipment.", 
                    "programenddatestring": "", 
                    "programstartdatestring": "", 
                    "programyearenddate": null, 
                    "programyearstartdate": null, 
                    "rebateprogramtechnologies": [], 
                    "resource_uri": "/api/rebateprograms/1415/", 
                    "temppayoutstring": "High Efficiency Boiler/Furnace: $300<br />Natural Gas Storage Tank Water Heater: $50", 
                    "tempprojectsizestring": "", 
                    "temprequirementsstring": "Furnaces/Boilers/Water Heaters: must be ENERGY STAR qualified<br />Water Heaters: Business Customers not eligible<br />Furnaces: Must have a 90% or greater AFUE rating<br />Boilers: Must have an 85% or greater AFUE rating<br />Storage Tank Water Heaters: Must have an EF of 0.67 or greater<br />", 
                    "website": "https://www.peco.com/Savings/ProgramsandRebates/Residential/PECOSmartGasEfficiencyUpgrade/Pages/Overview.aspx"
                  }
                ], 
                "resource_uri": "/api/utilities/4209/", 
                "utilityname": "PECO"
              }, 
              "utilitytype": {
                "code": "IOU", 
                "description": "INVESTOR OWNED", 
                "modifieddate": "2014-05-05", 
                "resource_uri": "/api/utilitytypes/4/"
              }, 
              "zipcode": "19104"
            }
          ]
        }


Feel free to explore, but that the main component of this API. The data has a lot of flexibility and opportunity for expansion.


##Credits
**Thanks to the following platforms, their documentation, and the communities that support them**
* Python
* Django
* South
* Tastypie

**Thanks to the following data outlets that made this possible**
* USPS
* OpenEI
* DSIRE
* me

Uncopyright Jay Tarlecki 2014

