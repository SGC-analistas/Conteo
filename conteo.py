# /**
#  * @author Emmanuel Castillo
#  * @email ecastillot@unal.edu.co / ecastillo@sgc.gov.co
#  * @create date 2021-07-24 07:02:45
#  * @modify date 2021-07-24 07:02:45
#  * @desc [description]
#  */

import sys
php_query_path = "/home/ecastillo/repositories/php_queries"
sys.path.insert(0,php_query_path)

from query import Query
import numpy as np
import pandas as pd
import argparse
# def conteo_radial()


class Conteo(Query):
    def __init__(self,MySQLdb_dict):
        """
        Class to counting events according his type.

        Parameters:
        -----------
        MySQLdb_dict: dict
            MySQLdb_dict= {'host':host, 'user':user, 'passwd':passwd, 'db': db}
        """

        Query.__init__(self,MySQLdb_dict,"events")
                

    def _get_stats(self,df):
        '''
        From DataFrame, It returns a stats dictionary 
        '''
        df_obj = df.select_dtypes(['object'])
        df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

        if self.users != None:
            df["picker"] = df["picker"].apply(lambda x: x.split("@")[0])
            df = df[df["picker"].isin(self.users)]
            

        eq = df[(df["type"] == "earthquake") | \
                (df["type"] == "unset")]
        not_loc = df[df["type"]=='not locatable']
        outside = df[df["type"]=='outside of network interest']
        volcanic = df[df["type"]=='volcanic_eruption']

        mag = np.arange(*self.mag_range)
        eq_m = eq.groupby(pd.cut(eq["magnitude"],mag))
        counts = eq_m.count()["magnitude"]

        stats = {"earthquake":{"len":len(eq),"interval":counts},
                "not_locatable":{"len":len(not_loc)},
                "outside_of_network_interest":{"len":len(outside)},
                "volcanic":{"len":len(volcanic)}     }
        
        return stats

    def radial(self,lat, lon, radious, 
                    starttime, endtime,
                    mag_range, depth_range,
                    users=None):
        """
        Parameters:
        -----------
        lat: float
            latitude
        lon: float 
            longitude
        radious: float
            radious
        initial_date: str
            initial date in the next format : YYYYMMDDTHHMMSS
        final_date: str 
            final date in the next format : YYYYMMDDTHHMMSS
        mag: range
            (start,end,interval)
        depth: range
            (start,end)
        users: list
            Name of the users
        """


        self.mag_range = mag_range
        self.users = users

        starttime = starttime.replace("T"," ")
        endtime = endtime.replace("T"," ")
        data = self.radial_SQLquery(lat, lon, radious, 
                    starttime, endtime, 
                    min_mag=mag_range[0], max_mag=mag_range[1],
                    min_prof=depth_range[0], max_prof=depth_range[1])

        stats = self._get_stats(data)

        return stats
    
    def simple(self,starttime, endtime,
                    mag_range, depth_range,
                    users=None):
        """
        Parameters:
        -----------
        initial_date: str
            initial date in the next format : YYYYMMDDTHHMMSS
        final_date: str 
            final date in the next format : YYYYMMDDTHHMMSS
        mag: range
            (start,end,interval)
        depth: range
            (start,end)
        users: list
            Name of the users
        """
        
        self.mag_range = mag_range
        self.users = users

        starttime = starttime.replace("T"," ")
        endtime = endtime.replace("T"," ")
        data = self.simple_SQLquery(starttime, endtime, 
                    min_mag=mag_range[0], max_mag=mag_range[1],
                    min_prof=depth_range[0], max_prof=depth_range[1])
        stats = self._get_stats(data)
        return stats


def read_args():
    prefix = "+"
    ini_msg = "#"*120

    parser = argparse.ArgumentParser("Conteo de eventos. ",prefix_chars=prefix,
                        usage=f'Conteo de eventos.')

    parser.add_argument(prefix+"s",prefix*2+"start",
                        type=str,
                        metavar='',
                        help="Fecha inicial en formato 'yyyymmddThhmmss'", required = True)

    parser.add_argument(prefix+"e",prefix*2+"end",
                        type=str,
                        metavar='',
                        help="Fecha final en formato 'yyyymmddThhmmss'", required = True)

    parser.add_argument(prefix+"m",prefix*2+"mag",
                        type=float,
                        nargs='+',
                        metavar='',
                        help="Rango e intervalo de magnitud, ej: 0 10 1 ", required = True)

    parser.add_argument(prefix+"d",prefix*2+"depth",
                        type=float,
                        nargs='+',
                        metavar='',
                        help="Profundidad mínima", required = True)

    parser.add_argument(prefix+"r",prefix*2+"radial",
                        default=None,
                        nargs='+',
                        metavar='',
                        help="Se debe especificar: lat lon  r. Ejemplo: 6.81 -73.17 120")

    parser.add_argument(prefix+"u",prefix*2+"users",
                        default=None,
                        nargs='+',
                        metavar='',
                        help="Usuario. ej: ecastillo")

    parser.add_argument(prefix+"mysqldb",prefix*2+"mysqldb",
                        default=None,
                        nargs='+',
                        metavar='',
                        help="Se debe especificar: host user passwd db. Ejemplo: 10.100.100.232 consulta consulta seiscomp3")
    
    args = parser.parse_args()
    # vars_args = vars(args)
    return args


if __name__ == "__main__":
    print("SIMPLE: python conteo.py +s 20210101T000000 +e 20210801T000000 +m 0 10 1 +d 0 200 +u ecastillo")
    print("RADIAL: python conteo.py +s 20210101T000000 +e 20210801T000000 +m 0 10 1 +d 0 200 +r 6.81 -73.17 120 +u ecastillo")
    
    args = read_args()

    if args.mysqldb != None:
        MySQLdb_dict= {'host':args.mysqldb[0], 'user':args.mysqldb[1],
            'passwd':args.mysqldb[2], 'db': args.mysqldb[3]}
    else:
        host = "10.100.100.232"
        user="consulta"
        passwd="consulta"
        db="seiscomp3"
        MySQLdb_dict= {'host':host, 'user':user, 'passwd':passwd, 'db': db}

    conteo = Conteo(MySQLdb_dict)
    if args.radial != None:
        stats = conteo.radial(lat=args.radial[0],lon=args.radial[1],radious=args.radial[2],
                      starttime=args.start, endtime=args.end,
                      mag_range= args.mag,
                      depth_range=args.depth,users=args.users)
    else: 
        stats = conteo.simple(starttime=args.start, endtime=args.end,
                      mag_range= args.mag,
                      depth_range=args.depth,users=args.users)

    print(stats)

    
    # MySQLdb_dict= {'host':"10.100.100.232", 'user':"consulta", 
    #                 'passwd':"consulta", 'db': "seiscomp3"}
    # conteo = Conteo(MySQLdb_dict)
    # # conteo.radial(6.81,-73.17,120,
    # #                 "20191201T000000",
    # #                 "20191202T000000",
    # #                 mag_range=(0,10,0.5),
    # #                 depth_range=(-10,300))
    # simple = conteo.simple(  "20191201T000000",
    #                 "20191202T000000",
    #                 mag_range=(0,10,0.5),
    #                 depth_range=(-10,300))
    # print(simple)