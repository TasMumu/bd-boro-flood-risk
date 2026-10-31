"""Reference metadata from Crossref and DataCite, by DOI, so that author lists, years and pages
come from the registries. Entries without a DOI are given by hand.
Output: paper/references.json. usage: python src/fetch_references.py"""
import json
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "paper" / "references.json"
UA = {"User-Agent": "boro-flood-paper-references"}
DOIS = {
    "ahmed2017": "10.3390/s17102347", "dey2021": "10.1016/j.ijdrr.2021.102247", "mondal2021": "10.3329/jesnr.v12i1-2.52007",
    "khan2012": "10.3329/jesnr.v5i1.11581", "rashid2018": "10.3329/brj.v21i1.37360", "kamruzzaman2018": "10.13189/ujar.2018.060106",
    "hossain2023": "10.3390/su152416873", "ahmed2024": "10.1002/fes3.70028", "baishakhy2023": "10.1016/j.heliyon.2023.e14011",
    "kamruzzaman2024": "10.1007/s00704-024-05270-5", "banerjee2010": "10.1080/13600818.2010.505681", "asada2005": "10.4157/grj.78.783",
    "rahman2025": "10.1016/j.ijdrr.2025.105401", "guiteras2015": "10.1257/aer.p20151095", "amin2015": "10.3390/su7010898",
    "sarker2014": "10.1016/j.eap.2014.11.004", "hasan2016": "10.1142/s2010007816500081", "rahman2017": "10.1186/s40066-017-0089-5",
    "dasgupta2017": "10.1017/age.2017.14", "lesk2016": "10.1038/nature16467", "li2025": "10.1126/sciadv.adx7799", "cui2020": "10.1086/709859",
    "obembe2021": "10.1371/journal.pone.0252067", "wei2023": "10.1038/s41893-023-01152-2", "blanc2016": "10.1175/jamc-d-15-0214.1",
    "uddin2019": "10.3390/rs11131581", "rahman2020a": "10.3390/agriculture10040131", "rahman2020b": "10.1007/s13753-020-00305-7",
    "qamer2023": "10.1038/s41598-023-30347-y", "singha2019": "10.1038/s41597-019-0036-3", "shew2019": "10.3390/rs11101235",
    "mosleh2014": "10.3390/rs6031938", "pekel2016": "10.1038/nature20584", "mosleh2016": "10.5424/sjar/2016143-8347",
    "alam2019": "10.1109/igarss.2019.8899084", "saisana2005": "10.1111/j.1467-985X.2005.00350.x", "tate2012": "10.1007/s11069-012-0152-2",
    "hinkel2011": "10.1016/j.gloenvcha.2010.08.002", "anselin1995": "10.1111/j.1538-4632.1995.tb00338.x", "conley1999": "10.1016/s0304-4076(98)00084-0",
    "driscoll1998": "10.1162/003465398557825", "cameron2008": "10.1162/rest.90.3.414", "mackinnon2017": "10.1002/jae.2508",
    "mackinnon2018": "10.1111/ectj.12107", "mackinnon2020": "10.1016/j.jeconom.2020.04.024", "conley2011": "10.1162/REST_a_00049",
    "abadie2021": "10.1257/jel.20191450", "hsiang2016": "10.1146/annurev-resource-100815-095343", "blanc2017": "10.1093/reep/rex016", "auffhammer2013": "10.1093/reep/ret016",
    "santos2006": "10.1162/rest.88.4.641", "benjamini1995": "10.1111/j.2517-6161.1995.tb02031.x", "bairagi2021": "10.1016/j.foodpol.2021.102183",
    "islam2021": "10.22434/ifamr2019.0190", "didan2021": "10.5067/MODIS/MOD13Q1.061", "zanaga2022": "10.5281/zenodo.7254221",
    "munozsabater2021": "10.5194/essd-13-4349-2021", "torres2012": "10.1016/j.rse.2011.05.028", "gorelick2017": "10.1016/j.rse.2017.06.031",
    "jagadish2007": "10.1093/jxb/erm003", "twele2016": "10.1080/01431161.2016.1192304", "moran1950": "10.1093/biomet/37.1-2.17",
    "mumu2026b": "10.5281/zenodo.23795046",
}
MANUAL = {
    "mumu2026a": dict(type="report", authors=[{"family": "Mumu", "given": "Tasnim Ahmad"}, {"family": "Karim", "given": "Rezaul"}], year="2026a",
                      title="An open, tested data engineering framework for integrating official crop statistics with satellite and climate data: district-level Boro rice in Bangladesh",
                      publisher="Manuscript submitted to Environmental Modelling & Software"),
    "bbs2026": dict(type="report", authors=[{"family": "Bangladesh Bureau of Statistics", "given": ""}], year=2026,
                    title="Yearbook of Agricultural Statistics-2025 (37th series)",
                    publisher="Statistics and Informatics Division, Ministry of Planning, Dhaka"),
    "gadm2022": dict(type="dataset", authors=[{"family": "GADM", "given": ""}], year=2022,
                     title="Database of Global Administrative Areas, version 4.1", publisher="https://gadm.org"),
    "oecd2008": dict(type="book", authors=[{"family": "OECD", "given": ""}, {"family": "European Commission Joint Research Centre", "given": ""}],
                     year=2008, title="Handbook on Constructing Composite Indicators: Methodology and User Guide",
                     publisher="OECD Publishing, Paris", doi="10.1787/9789264043466-en"),
    "hassan2019": dict(type="report", authors=[{"family": "Hassan", "given": "S. M. Kamrul"}], year=2019,
                       title="Impacts of flooding on the rice production of Bangladesh: a panel data study",
                       publisher="Thesis, Colorado State University. https://mountainscholar.org/handle/10217/197396"),
}


def get(url):
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))
        except Exception:
            time.sleep(3)
    raise RuntimeError(url)


def crossref(doi):
    m = get(f"https://api.crossref.org/works/{doi}")["message"]
    return dict(type=m.get("type"), doi=doi,
                authors=[{"family": a.get("family") or a.get("name", ""), "given": a.get("given", "")} for a in m.get("author", [])],
                year=((m.get("published-print") or m.get("issued") or {}).get("date-parts") or [[None]])[0][0],
                title=": ".join(x for x in [(m.get("title") or [""])[0], (m.get("subtitle") or [""])[0]] if x),
                container=(m.get("container-title") or [""])[0], volume=m.get("volume"), issue=m.get("issue"),
                pages=m.get("article-number") or m.get("page"), publisher=m.get("publisher"))


def datacite(doi):
    a = get(f"https://api.datacite.org/dois/{doi}")["data"]["attributes"]
    au = [{"family": (c.get("familyName") or c.get("name", "").split(",")[0]).strip(), "given": (c.get("givenName") or "").strip()} for c in a["creators"]]
    pub = a.get("publisher")
    return dict(type=a["types"].get("resourceTypeGeneral", "Dataset").lower(), doi=doi, authors=au, year=a["publicationYear"],
                title=a["titles"][0]["title"], publisher=pub if isinstance(pub, str) else (pub or {}).get("name"))


# Registry titles that need correcting
TITLE_FIX = {"hasan2016": "Assessment of climate change impacts on Aman and Boro rice yields in Bangladesh",
             "alam2019": "Boro rice yield estimation model using MODIS NDVI data for Bangladesh",
             "moran1950": "Notes on continuous stochastic phenomena"}


def tidy(name):
    """Names sent to the registry in capitals: JEFF becomes Jeff, while initials stay as they are."""
    return " ".join(t.title() if t.isupper() and len(t) > 2 and "." not in t else t for t in name.split())


refs = dict(MANUAL)
for key, doi in DOIS.items():
    try:
        refs[key] = crossref(doi)
    except RuntimeError:
        refs[key] = datacite(doi)
    refs[key]["authors"] = [dict(family=tidy(a["family"]), given=tidy(a["given"])) for a in refs[key]["authors"]]
    refs[key]["title"] = TITLE_FIX.get(key, refs[key]["title"])
    print(f"{key:18s} {refs[key]['year']}  {', '.join(a['family'] for a in refs[key]['authors'][:3])}")
refs["mumu2026b"]["year"] = "2026b"
refs["santos2006"]["authors"][0] = dict(family="Santos Silva", given="J. M. C.")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(refs, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(refs), "references")
