from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

class OlxCarsSelenium:
    def scrape_olx(self):
        # Configurando o Selenium
        service = Service()
        options = Options()

        # Desativando imagens para acelerar o carregamento da página
        chrome_prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", chrome_prefs)

        # Configurando o Selenium para agir como um navegador real
        options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(service=service, options=options)

        # Lista para armazenar os resultados
        results = []

        for page in range(1, 2):
            # Usando o Selenium para obter a página
            url = f'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rs?o={page}'
            driver.get(url)

            # Encontrando o elemento pelo ID usando XPath
            next_data_script = driver.find_element(By.XPATH, '//script[@id="__NEXT_DATA__"]')

            # Obtendo o texto do script
            html = next_data_script.get_attribute('innerHTML')

            # Imprimindo o conteúdo HTML (pode ser removido ou ajustado conforme necessário)
            print(f"HTML content for page {page}:\n{html}\n{'='*50}")

            # Convertendo HTML para JSON (se necessário)
            # Aqui você deve ajustar a lógica de extração de dados conforme necessário
            try:
                html_json = json.loads(html)
                cars = html_json.get('props').get('pageProps').get('ads')

                for car in cars:
                    price_str = car.get('price')
                    # Filtro: Incluir apenas carros com preços abaixo de R$ 50.000,00
                    if price_str is not None and float(price_str.replace('R$', '').replace('.', '').replace(',', '.')) < 50000:
                        results.append({
                            'title': car.get('title'),
                            'price': float(price_str.replace('R$', '').replace('.', '').replace(',', '.')),  # Corrigindo aqui
                            'location': car.get('location'),
                            'properties': car.get('properties')
                        })
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for page {page}: {e}")

        # Salvando os resultados em um arquivo JSON
        #with open('resultados.json', 'w', encoding='utf-8') as json_file:
         #   json.dump(results, json_file, ensure_ascii=False, indent=4)
        # Salvando os resultados em um arquivo JSON Lines
        with open('resultados.jsonl', 'w', encoding='utf-8') as jsonl_file:
            for car in results:
                jsonl_file.write(json.dumps(car, ensure_ascii=False) + '\n')

        # Fechando o driver após a conclusão
        driver.quit()

# Exemplo de uso
if __name__ == "__main__":
    scraper = OlxCarsSelenium()
    scraper.scrape_olx()
