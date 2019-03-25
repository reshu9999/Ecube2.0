def get_aetos_proxy(domain, country):
    '''
    Missing Proxy
    Czech
    Hungary
    Finland
    Thailand
    Israel
    Malaysia
    Iceland
    Costa Rica
    Luxembourg
    Phillippines
    '''
    proxy_mapper = {
        "Taiwan": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6841"
        },
        "Vietnam": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6842"
        },
        "Indonesia": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6836"
        },
        "Canada": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6834"
        },
        "Colombia": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6831"
        },
        "Puerto Rico": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6815"
        },
        "Tokyo": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6837"
        },
        "Japan": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6837"
        },
        "Netherlands": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6825"
        },
        "Switzerland": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6822"
        },
        "United States": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6848"
        },
        "Turkey": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6840"
        },
        "Denmark": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6821"
        },
        "Argentina": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6832"
        },
        "New Zealand": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6816"
        },
        "Brazil": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6823"
        },
        "Austria": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6849"
        },
        "Hong Kong": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6835"
        },
        "London(UK)": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6811"
        },
        "Newcastle(UK)": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6811"
        },
        "United Kingdom": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6811"
        },
        "Mexico": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6819"
        },
        "Spain": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6828"
        },
        "Australia": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6810"
        },
        "Sweden": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6829"
        },
        "Kazakhstan": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6860"
        },
        "Singapore": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6818"
        },
        "Russia": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6843"
        },
        "Peru": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6830"
        },
        "China": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6814"
        },
        "Belgium": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6845"
        },
        "Korea, Republic": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6838"
        },
        "portugal": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6827"
        },
        "France": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6812"
        },
        "SouthAfrica": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6850"
        },
        "South Africa": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6850"
        },
        "Italy": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6824"
        },
        "Egypt": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6846"
        },
        "Germany": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6813"
        },
        "Poland": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6844"
        },
        "Philippines": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6839"
        },
        "Ireland": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6820"
        },
        "India": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6817"
        },
        "Norway": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6826"
        },
        "United Arab Emirates": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6851"
        },
        "Chile": {
            "UserName": "11297",
            "IP": "world.nohodo.com",
            "Password": "NEyRG2",
            "port": "6833"
        }
    }

    return proxy_mapper.get(country)


def get_nohodo_proxy(domain, country):
    import random
    proxy_csv = """
world.nohodo.com,6810,10172,Jq4wtJ,High,,,Australia,,Nohodo
world.nohodo.com,6849,10172,Jq4wtJ,High,,,Austria,,Nohodo
world.nohodo.com,6814,10172,Jq4wtJ,High,,,China,,Nohodo
world.nohodo.com,6813,10172,Jq4wtJ,High,,,Germany,,Nohodo
world.nohodo.com,6837,10172,Jq4wtJ,High,,,Japan,,Nohodo
world.nohodo.com,6844,10172,Jq4wtJ,High,,,Poland,,Nohodo
world.nohodo.com,6818,10172,Jq4wtJ,High,,,Singapore,,Nohodo
world.nohodo.com,6811,10172,Jq4wtJ,High,,,UK,,Nohodo
"""
    return [{'IP': p[0], 'port': p[1], 'UserName': p[2], 'Password': p[3], 'proxyCountry': p[7]}
            for p in [line.split(',') for line in proxy_csv.split('\n') if line]][random.randint(0, 7)]


def get_user_agent(domain):
    return 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'


def hotel_data_save_checker(hotel_data):
    checks = [
        # Properties from Parent
        lambda d: 'index' in d,
        lambda d: 'city' in d,
        lambda d: 'checkIn' in d,
        lambda d: 'checkOut' in d,
    
        # Crawler Output
        lambda d: 'htmls' in d,
        lambda d: 'hotelName' in d,
        lambda d: 'roomTypes' in d,
    
        # Meta Data
        lambda d: 'meta' in d,
        lambda d: 'requestId' in d['meta'],
        lambda d: 'subRequestId' in d['meta'],
        lambda d: 'requestRunId' in d['meta'],
        lambda d: 'startDT' in d['meta'],
        lambda d: 'endDT' in d['meta'],
    ]

    for check in checks:
        if not check(hotel_data):
            raise Exception('Hotel Data Check Failed')

    return hotel_data
