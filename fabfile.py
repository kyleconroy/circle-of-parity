from fabric.api import task, local
import requests


def scrape_game_info(url, folder):
    local("mkdir -p data/{}".format(folder))
    urls = [url.format(year) for year in xrange(1869, 2011)]
    results = [requests.get(u) for u in urls]
    for year, resp in enumerate(results, start=1869):
        if resp.ok:
            with open("data/{0}/{0}_{1}.txt".format(folder, year), "w") as f:
                f.write(resp.content)
        else:
            print "Error retrieving {}".format(resp.url)


@task
def download():
    pass


@task
def scrape():
    base_uri = "http://homepages.cae.wisc.edu/~dwilson/rfsc/history/howell/"
    scrape_game_info(base_uri + "cf{}tms.txt", "teams")
    scrape_game_info(base_uri + "cf{}gms.txt", "scores")


@task
def analyze():
    pass

@task
def report():
    pass
