from modules.webscraper import WebScrapper

if __name__ == "__main__":
    
    counter = 1
    result = []
    
    while True:
        uf = input("-> UF: ").upper()
        city = input("-> City: ").upper()
        page_number = int(input("-> Page numeber: "))
        
        if uf and city and page_number and page_number > 0:
            break
        
        print("You need to inform UF, city and how many pages you wish to scrap!")
    
    web_scrapper = WebScrapper(state=uf, city=city)
    
    while counter <= page_number:
        result.append(web_scrapper.get_cnpj_and_infos(counter))
        print(result)
        
        counter += 1