from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd

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
        # Adicionando opções para lidar com SSL e GPU
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

        # Adicionando opção para desativar interface gráfica (headless)
        options.add_argument('--headless')

        # Ajustando o tempo de espera para 30 segundos
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)

        # Lista para armazenar os resultados
        results = []

        for page in range(1, 99):
            # Usando o Selenium para obter a página
            url = f'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-sp/sao-paulo-e-regiao?pe=60000&ps=53100&doc=1&o={page}'
            driver.get(url)

            try:
                # Encontrando o elemento pelo ID usando XPath
                next_data_script = driver.find_element(By.XPATH, '//script[@id="__NEXT_DATA__"]')

                # Obtendo o texto do script
                html = next_data_script.get_attribute('innerHTML')

                # Imprimindo o conteúdo HTML (pode ser removido ou ajustado conforme necessário)
                print(f"HTML content for page {page}:\n{html}\n{'='*50}")

                # Convertendo HTML para JSON
                try:
                    html_json = json.loads(html)
                    cars = html_json.get('props', {}).get('pageProps', {}).get('ads', [])

                    for car in cars:
                        properties = car.get('properties', [])  # Use uma lista vazia como valor padrão se `properties` for None
                        extracted_properties = {
                            'Ano': None,
                            'Marca': None,
                            'Tipo de veículo': None,
                            'Quilometragem': None,
                            'Potência do motor': None,
                            'Combustível': None,
                            'Câmbio': None,
                            'Direção': None,
                            'Portas': None,
                        }
                        if properties:  # Verifique se `properties` não é uma lista vazia
                            for prop in properties:
                                if prop.get('label') in extracted_properties:
                                    extracted_properties[prop['label']] = prop.get('value')
                        try:
                            price = float(car.get('price', '0').replace('R$', '').replace('.', '').replace(',', '.'))
                        except ValueError:
                            price = 0  # Se a conversão falhar, definir o preço como 0
                        #filtro de leilao has_auction
                        #Kit GNV tmb elimina
                        #extra_key
                        if price > 0 and int(extracted_properties.get('Quilometragem', '0')) > 500 and int(extracted_properties.get('Ano', '0')) > 2000 :
                            results.append({
                                'title': car.get('title'),
                                'price': price,
                                'Ano': extracted_properties['Ano'],
                                'Marca': extracted_properties['Marca'],
                                'Tipo de veículo': extracted_properties['Tipo de veículo'],
                                'Quilometragem': extracted_properties['Quilometragem'],
                                'Potência do motor': extracted_properties['Potência do motor'],
                                'Combustível': extracted_properties['Combustível'],
                                'Câmbio': extracted_properties['Câmbio'],
                                'Direção': extracted_properties['Direção'],
                                'Portas': extracted_properties['Portas'],
                            })
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for page {page}: {e}")
            except Exception as e:
                print(f"Error retrieving data for page {page}: {e}")

        # Convertendo os resultados em um DataFrame do pandas
        df = pd.DataFrame(results)

        # Salvando o DataFrame em um arquivo Excel
        df.to_excel('resultados_carros2.xlsx', index=False)

        # Fechando o driver após a conclusão
        driver.quit()

# Exemplo de uso
if __name__ == "__main__":
    scraper = OlxCarsSelenium()
    scraper.scrape_olx()
