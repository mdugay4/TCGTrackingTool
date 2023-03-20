    access_token = get_access_token()

    search_url = f'http://api.tcgplayer.com/catalog/products?'
    headers = {'Authorization': f'Bearer {access_token}'}


    res = requests.get(search_url, headers=headers)


    results = []

    offset = 100

    #totalItems 203750

    while offset < res.json()["totalItems"]:
        
        search_url = f'http://api.tcgplayer.com/catalog/products?limit=100&offset={offset}'
        headers = {'Authorization': f'Bearer {access_token}'}
        res = requests.get(search_url, headers=headers)

        for card in res.json()['results']:
            temp = card['name']
            results.append(temp)     

        print(offset)       # Track Progress 
        offset = offset + 100

    logging.basicConfig(filename='test.log', level=logging.DEBUG)
    logging.info(results)  # will print a message to the console

    # Note: This will take a while
