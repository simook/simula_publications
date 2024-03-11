import time
from playwright.sync_api import sync_playwright
from urllib.parse import urlencode

class Publication(object):
    def __init__(self, publication) -> None:
        self._publication = publication
    
    def __str__(self) -> str:
        return f'{self.authors}\n{self.title}\n{self.journal}\n'

    @property
    def title(self):
        return str(self._publication.locator('.wp-block-simula-preview__title').inner_text())
    
    @property
    def authors(self):
        return str(self._publication.locator('.wp-block-simula-preview__meta.meta-one').inner_text())
    
    @property
    def journal(self):
        return str(self._publication.locator('.wp-block-simula-preview__meta.meta-two').inner_text())
    
    @property
    def url(self):
        href = self._publication.locator('.wp-block-simula-preview__link').get_attribute('href')
        return f'https://www.simula.no{href}'

class Simula(object):
    """ The Simula.no website is a React website (based on Next.js). 
        It currently does not have an API for obtaining publications.
        This library uses a headless browser to provide a programatic interface
        for obtaining the publications that have been published by Simula. 
    """
    def __init__(self):
        self._p = sync_playwright()
        self.playwright = self._p.start()
        self.browser = self.playwright.chromium.launch()

    def __del__(self):
        self.browser.close()        
        self._p.__exit__()

    def publications(self, params={}):
        """ Return a list of publications.
        """
        page = self.browser.new_page()
        url = f'https://www.simula.no/publications/?page=1&{urlencode(params)}'
        visited = []

        while url is not None:
            page.goto(url)
            pubs = page.locator('.publications')
            while not pubs.is_visible():
                # wait for the nextjs framework to render the results
                time.sleep(.1)
            
            for publication in pubs.locator('.publications__publication').all():
                try:
                    yield Publication(publication)
                except Exception as e:
                    print(e)
                    yield None
            
            visited.append(url)
            url = None
            for paginator in page.locator('.ais-Pagination-link').all():
                href = paginator.get_attribute('href')
                if href is None:
                    continue
                if href not in visited:
                    url = href

        page.close()