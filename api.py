from backend import json
import urllib.request
import socket


def collected_servers():
    """
    Get server link from www.radio-browser.info

    :return: List sontaining all avaiable server for requests
    """
    try:
        hosts = []
        ips = socket.getaddrinfo('all.api.radio-browser.info', 80, 0, 0, socket.IPPROTO_TCP)
        for ip_tupple in ips:
            ip = ip_tupple[4][0]
            host_addr = socket.gethostbyaddr(ip)
            if host_addr[0] not in hosts:
                hosts.append(host_addr[0])

        hosts.sort()
        return list(map(lambda x: "https://" + x, hosts))

    except Exception as e:
        print("COLLECT_SERVERS Unable to download from api url: ", e)
        pass


def collect_country_info(term):
    """
    First step for a searcha based on countries. Get names of all the available countries

    :param term: "name", "iso_3166_1" or "stationcount" as terms
    :return: list of countries, abreviations of the countries or number of stations in every country
    """

    url = collected_servers()

    for server in url:
        try:
            req = urllib.request.Request(f"{server}/json/countries")
            response = urllib.request.urlopen(req)
            data = response.read()
            response.close()

            countries_info = json.loads(data)
            country_info_list = [country_name[term] for country_name in countries_info]
            return country_info_list

        except Exception as e:
            print("COLLECT_COUNTRY_INFO Unable to download from api url: ", e)
            pass


def search_by_country(term, country):
    """
    Get all available radio stations from a selected country

    :param term: "name", "url", "stationuuid", "codec", "bitrate", "description", "tags", "countrycode" or "homepage"
    :param country: Country name, can be obtained from de function: collect_country_info()
    :return: List of names, urls or the selected term from the selected country
    """

    url = collected_servers()

    for server in url:
        try:
            count = country.replace(" ", "_")
            req = urllib.request.Request(f"{server}/json/stations/bycountry/{count}")
            response = urllib.request.urlopen(req)
            data = response.read()
            response.close()

            stations_by_country_info = json.loads(data)
            stations_by_country_list = [station[term] for station in stations_by_country_info]
            return stations_by_country_list

        except Exception as e:
            print("SEARCH_BY_COUNTRY Unable to download from api url: ", e)
            pass


def search_by_tag(term, tag):
    """
    Get all the radio station marked with the selected tag (NO EXACT SEARCH)

    :param term: "name", "url", "stationuuid", "codec", "bitrate", "description", "tags", "countrycode" or "homepage"
    :param tag: selected tag for searching on the api
    :return: a list of the stations asigned to the selected tag
    """

    url = collected_servers()

    for server in url:
        try:
            req = urllib.request.Request(f"{server}/json/stations/bytag/{tag}")
            response = urllib.request.urlopen(req)
            data = response.read()
            response.close()

            stations_by_tag_info = json.loads(data)
            stations_by_tag_list = [station[term] for station in stations_by_tag_info]
            return stations_by_tag_list

        except Exception as e:
            print("SEARCH_BY_TAG Unable to download from api url: ", e)
            pass


def search_by_name(term, name):
    """
    Get all the radio station marked with the selected name (NO EXACT SEARCH)

    :param term: "name", "url", "stationuuid", "codec", "bitrate", "description", "tags", "countrycode" or "homepage"
    :param name: selected name for searching on the api
    :return: a list of the stations asigned to the selected tag
    """

    url = collected_servers()

    for server in url:
        try:
            req = urllib.request.Request(f"{server}/json/stations/byname/{name}")
            response = urllib.request.urlopen(req)
            data = response.read()
            response.close()

            stations_by_name_info = json.loads(data)
            stations_by_name_list = [station[term] for station in stations_by_name_info]
            return stations_by_name_list

        except Exception as e:
            print("SEARCH_BY_NAME Unable to download from api url: ", e)
            pass


""" EXAMPLES """
"""
print(collected_servers())

print(collect_country_info("name"))
print(collect_country_info("iso_3166_1"))
print(collect_country_info("stationcount"))

print(search_by_country("name", "The_Netherlands"))
print(search_by_country("url", "The_Netherlands"))

# print(search_by_tag('name', 'rock'))
# print(search_by_tag('url', "rock"))

print(search_by_name('name', 'slam'))
print(search_by_name('url', 'slam'))
"""