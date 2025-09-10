import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class Crawler:
    def __init__(self, target, max_pages=30, timeout=6):
        self.target = target.rstrip("/")
        parsed = urlparse(self.target)
        self.base_netloc = parsed.netloc
        self.scheme = parsed.scheme
        self.max_pages = max_pages
        self.timeout = timeout
        self.visited = set()

    def same_domain(self, url):
        try:
            p = urlparse(url)
            return p.netloc == self.base_netloc or p.netloc == ""
        except:
            return False

    def get_soup(self, url):
        try:
            resp = requests.get(url, timeout=self.timeout)
            return resp, BeautifulSoup(resp.text, "lxml")
        except Exception as e:
            return None, None

    def extract_forms(self, soup):
        forms = []
        for f in soup.find_all("form"):
            form = {}
            form['action'] = f.get("action")
            form['method'] = f.get("method", "get").lower()
            inputs = []
            for inp in f.find_all(["input", "textarea", "select"]):
                name = inp.get("name")
                itype = inp.get("type", "text")
                value = inp.get("value", "")
                inputs.append({"name": name, "type": itype, "value": value})
            form['inputs'] = inputs
            forms.append(form)
        return forms

    def crawl(self):
        to_visit = [self.target]
        results = []
        while to_visit and len(self.visited) < self.max_pages:
            url = to_visit.pop(0)
            if url in self.visited:
                continue
            resp, soup = self.get_soup(url)
            self.visited.add(url)
            if not soup:
                continue
            # extract forms
            forms = self.extract_forms(soup)
            results.append({"url": url, "forms": forms})

            # find links
            for a in soup.find_all("a", href=True):
                href = a['href']
                full = urljoin(url, href)
                if self.same_domain(full) and full not in self.visited:
                    if full.startswith(self.scheme):
                        to_visit.append(full)
            time.sleep(0.2)
        return results
