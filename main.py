from modules.webscraper import WebScrapper

if __name__ == "__main__":
    
    while True:
        uf = input("-> UF: ").upper()
        city = input("-> City: ").upper()
        
        if uf and city :
            break
        
        print("You need to inform UF and city!")
    
    web_scrapper = WebScrapper(state=uf, city=city)
    result = web_scrapper.get_cnpj_and_infos()
    
    print(result)