import sqlite3
from typing import List
import logging

DB_FILE = "requirements.db"
NEEDS_FILE = "docs/requirements/needs.md"
FEATURES_FILE = "docs/requirements/features.md"

#### Needs

def getNeedCategories(connection: sqlite3.Connection) -> List[sqlite3.Row]:
    categories = connection.cursor()
    categories.execute("SELECT * FROM NeedCategory")
    return categories.fetchall()

def getNeedsForCategory(category: sqlite3.Row, connection: sqlite3.Connection) -> List[sqlite3.Row]:
    needs = connection.cursor()
    needs.execute('SELECT * FROM Need WHERE category=?', str(category['id']))
    return needs.fetchall()

def getMarkdownForNeed(need: sqlite3.Row) -> str:
    markdown = []
    markdown.append("### N{0}: {1}\n".format(need['id'], need['shortName']))
    markdown.append("{0}\n".format(need['description']))
    return '\n'.join(markdown)

def getMarkdownForNeedCategory(category: sqlite3.Row, connection: sqlite3.Connection) -> str:
    markdown = []
    markdown.append("## {0}\n".format(category['name']))
    needs = getNeedsForCategory(category, connection)
    for need in needs:
        markdown.append(getMarkdownForNeed(need))
    return '\n'.join(markdown)

def getMarkdownForNeedsFile(connection: sqlite3.Connection) -> str:
    markdown = []
    markdown.append("# Needs\n")
    needCategories = getNeedCategories(connection)
    for needCategory in needCategories:
        markdown.append(getMarkdownForNeedCategory(needCategory, connection))
    return '\n'.join(markdown)

def writeNeedsFile(needsFileName: str, connection: sqlite3.Connection):
    needsFile = open(needsFileName, "w")
    logging.info("Writing Needs file at %s", needsFileName)
    needsFile.write(getMarkdownForNeedsFile(connection))
    needsFile.close()

#### Features

def getFeatureCategories(connection: sqlite3.Connection) -> List[sqlite3.Row]:
    featureCategories = connection.cursor()
    featureCategories.execute("SELECT * FROM Need")
    return featureCategories.fetchall()

def getFeaturesForCategory(category: sqlite3.Row, connection: sqlite3.Connection) -> List[sqlite3.Row]:
    features = connection.cursor()
    features.execute("SELECT * FROM Feature WHERE need=?", str(category['id']))
    return features.fetchall()

def getMarkdownForFeature(feature: sqlite3.Row) -> str:
    markdown = []
    markdown.append("### F{0}: {1}\n".format(feature['id'], feature['shortName']))
    markdown.append("{0}\n".format(feature['description']))
    return '\n'.join(markdown)

def removePeriods(parts: List[str]) -> List[str]:
    newParts = []
    for part in parts:
        newParts.append(part.replace(".", ""))
    return newParts

def getSlugForFeatureCategory(category: sqlite3) -> str:
    parts = []
    shortName: str = category['shortName']
    parts.append("N{0}".format(category['id']))
    parts.extend(shortName.split(" "))
    parts = removePeriods(parts)
    return ("-".join(parts)).lower()

def getMarkdownForFeatureCategory(category: sqlite3.Row, connection: sqlite3.Connection) -> str:
    markdown = []
    slug = getSlugForFeatureCategory(category)
    markdown.append("## [{0}](needs/#{1})\n".format(category['shortName'], slug))
    features = getFeaturesForCategory(category, connection)
    for feature in features:
        markdown.append(getMarkdownForFeature(feature))
    return '\n'.join(markdown)

def getMarkdownForFeaturesFile(connection: sqlite3.Connection) -> str:
    markdown = []
    markdown.append("# Features\n")
    featureCategories = getFeatureCategories(connection)
    for featureCategory in featureCategories:
        markdown.append(getMarkdownForFeatureCategory(featureCategory, connection))
    return '\n'.join(markdown)

def writeFeaturesFile(featuresFileName: str, connection: sqlite3.Connection):
    featuresFile = open(featuresFileName, "w")
    logging.info("Writing Features file at %s", featuresFileName)
    featuresFile.write(getMarkdownForFeaturesFile(connection))
    featuresFile.close


connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
logging.basicConfig(level=logging.INFO)
writeNeedsFile(NEEDS_FILE, connection)
writeFeaturesFile(FEATURES_FILE, connection)